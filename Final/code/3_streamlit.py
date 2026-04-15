#-----------------------------------------------------------------------------------------------------------------------
# Name: Rita Wang
# Date: 4/15/26
# BIOS 584 Final Project: Streamlit App
#-----------------------------------------------------------------------------------------------------------------------
"""
Deployment app:
1) loads completed Table 1 output
2) displays saved figures from Script 2
3) provides CSV download for Table 1
"""

from pathlib import Path

import pandas as pd
import streamlit as st

# Resolves to .../Final/outputs whether you run locally or on Streamlit Cloud.
_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
TABLE_CSV = _OUTPUT_DIR / "table1.csv"


def _paths_that_exist(paths: list[Path]) -> list[Path]:
    return [p for p in paths if p.is_file()]

AIM1_FIGURES = [
    _OUTPUT_DIR / "aim1_total_alcohol_by_sex.png",
    _OUTPUT_DIR / "aim1_total_alcohol_by_school.png",]

AIM2_FIGURES = [
    _OUTPUT_DIR / "aim2_FinalGrade_histogram.png",
    _OUTPUT_DIR / "aim2_FinalGrade_vs_age.png",
    _OUTPUT_DIR / "aim2_FinalGrade_vs_absences.png",
    _OUTPUT_DIR / "aim2_FinalGrade_by_studytime.png",
    _OUTPUT_DIR / "aim2_FinalGrade_by_goout.png",
    _OUTPUT_DIR / "aim2_FinalGrade_by_Medu.png",
    _OUTPUT_DIR / "aim2_FinalGrade_by_Fedu.png",
    _OUTPUT_DIR / "aim2_FinalGrade_by_sex.png",
    _OUTPUT_DIR / "aim2_FinalGrade_by_school.png",
    _OUTPUT_DIR / "aim2_FinalGrade_by_any_parent_teacher.png",]

st.set_page_config(page_title="Student Alcohol Project", layout="wide")

st.title("Student Alcohol Consumption: Table 1 and Visualizations")
st.write("Web app view of final outputs from data cleaning and table 1 and visualizations.")
st.markdown(
"""
### About this project
This project uses the **Mathematics course** dataset (`student-mat.csv`) from the [Student Alcohol Consumption data](https://www.kaggle.com/datasets/uciml/student-alcohol-consumption/data)

Current outputs include:
- **Table 1:** Descriptive characteristics of the sample
- **Aim 1 figures:** Total alcohol consumption by sex and by school
- **Aim 2 figures:** Exploratory plots of final grade (G3) against student, family, and school-related factors. These should help identify which variables may be associated with final grade so we can choose covariates and adjust for plausible confounders in Aim 3 (multivariable modeling).

""")

st.subheader("Table 1")
if not TABLE_CSV.is_file():
    st.error(
        "Table 1 file is missing in this deployment. Streamlit Cloud only sees files that are **committed and pushed** to GitHub."
    )
    st.markdown(
        f"Expected path in the repo: `{TABLE_CSV.relative_to(Path(__file__).resolve().parent.parent.parent)}` "
        f"(full: `{TABLE_CSV}`)."
    )
    st.info(
        "On your computer: run `2_table1+visualizations.py`, then `git add Final/outputs/table1.csv` "
        "and the figure PNGs, commit, and push. Redeploy the app."
    )
    st.stop()

table1_df = pd.read_csv(TABLE_CSV)
st.dataframe(table1_df.fillna(""), use_container_width=True, height=520, hide_index=True,)

st.download_button(
    label="Download Table 1 CSV",
    data=TABLE_CSV.read_bytes(),
    file_name="table1.csv",
    mime="text/csv",
)

st.subheader("Figures")


def label_from_filename(figure_path: Path) -> str:
    return figure_path.stem.replace("_", " ").replace("aim1 ", "").replace("aim2 ", "").title()


aim1_existing = _paths_that_exist(AIM1_FIGURES)
aim2_existing = _paths_that_exist(AIM2_FIGURES)
missing_figs = [p.name for p in AIM1_FIGURES + AIM2_FIGURES if not p.is_file()]
if missing_figs:
    st.warning(
        f"{len(missing_figs)} figure file(s) not found in `Final/outputs/` on the server (often not pushed to Git): "
        f"{', '.join(missing_figs[:5])}"
        + (" …" if len(missing_figs) > 5 else "")
    )

col_aim1, col_aim2 = st.columns(2)
with col_aim1:
    st.markdown("### Aim 1")
    if aim1_existing:
        aim1_options = {label_from_filename(path): path for path in aim1_existing}
        selected_aim1 = st.selectbox(
            "Select Aim 1 plot",
            options=list(aim1_options.keys()),
            key="aim1_plot_select",
        )
        st.image(str(aim1_options[selected_aim1]), caption=selected_aim1, use_container_width=True)
    else:
        st.caption("No Aim 1 PNGs in `Final/outputs/`. Add and push them to GitHub.")

with col_aim2:
    st.markdown("### Aim 2")
    if aim2_existing:
        aim2_options = {label_from_filename(path): path for path in aim2_existing}
        selected_aim2 = st.selectbox(
            "Select Aim 2 plot",
            options=list(aim2_options.keys()),
            key="aim2_plot_select",
        )
        st.image(str(aim2_options[selected_aim2]), caption=selected_aim2, use_container_width=True)
    else:
        st.caption("No Aim 2 PNGs in `Final/outputs/`. Add and push them to GitHub.")
