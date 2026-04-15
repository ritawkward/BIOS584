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

_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
TABLE_CSV = _OUTPUT_DIR / "table1.csv"

AIM1_FIGURES = [
    _OUTPUT_DIR / "aim1_total_alcohol_by_sex.png",
    _OUTPUT_DIR / "aim1_total_alcohol_by_school.png",
]

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
    _OUTPUT_DIR / "aim2_FinalGrade_by_any_parent_teacher.png",
]

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

"""
)

st.subheader("Table 1")
table1_df = pd.read_csv(TABLE_CSV)
st.dataframe(table1_df.fillna(""), use_container_width=True, height=520, hide_index=True)

st.download_button(
    label="Download Table 1 CSV",
    data=TABLE_CSV.read_bytes(),
    file_name="table1.csv",
    mime="text/csv",
)

st.subheader("Figures")


def label_from_filename(figure_path: Path) -> str:
    return figure_path.stem.replace("_", " ").replace("aim1 ", "").replace("aim2 ", "").title()


aim1_options = {label_from_filename(path): path for path in AIM1_FIGURES}
aim2_options = {label_from_filename(path): path for path in AIM2_FIGURES}

col_aim1, col_aim2 = st.columns(2)
with col_aim1:
    st.markdown("### Aim 1")
    selected_aim1 = st.selectbox(
        "Select Aim 1 plot",
        options=list(aim1_options.keys()),
        key="aim1_plot_select",
    )
    st.image(str(aim1_options[selected_aim1]), caption=selected_aim1, use_container_width=True)

with col_aim2:
    st.markdown("### Aim 2")
    selected_aim2 = st.selectbox(
        "Select Aim 2 plot",
        options=list(aim2_options.keys()),
        key="aim2_plot_select",
    )
    st.image(str(aim2_options[selected_aim2]), caption=selected_aim2, use_container_width=True)
