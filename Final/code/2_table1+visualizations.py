#-----------------------------------------------------------------------------------------------------------------------
# Name: Rita Wang
# Date: 4/15/26
# BIOS 584 Final Project: Table 1 and Visualizations Script
#-----------------------------------------------------------------------------------------------------------------------
"""
1) creates Table 1
2) creates visualizations for Aim 1 and Aim 2
3) saves table 1 and visualizations to outputs directory
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import textwrap
sns.set_theme(style="whitegrid")

# Load cleaned data
df = pd.read_csv("Final/data/student-mat-clean.csv")

NUMERIC_FOR_TABLE = ["age", "absences", "Dalc", "Walc", "total_alcohol", "G1", "G2", "G3"]
CATEGORICAL_FOR_TABLE = ["sex", "school", "address", "Pstatus", "internet", "any_parent_teacher", "studytime", "goout", "Medu", "Fedu"]

VARIABLE_LABELS = {
    "age": "Age (years)",
    "studytime": "Weekly study time",
    "absences": "Number of School Absences",
    "goout": "Going out with friends",
    "Medu": "Mother's education",
    "Fedu": "Father's education",
    "Dalc": "Weekday alcohol consumption (Dalc)",
    "Walc": "Weekend alcohol consumption (Walc)",
    "total_alcohol": "Total alcohol consumption (Dalc + Walc)",
    "G1": "First period grade (G1)",
    "G2": "Second period grade (G2)",
    "G3": "Final grade (G3)",
    "sex": "Sex",
    "school": "School",
    "address": "Home address type",
    "Pstatus": "Parental cohabitation status",
    "internet": "Internet access at home",
    "any_parent_teacher": "Any parent has teacher job",}

LEVEL_LABELS = {
    "sex": {"F": "Female", "M": "Male"},
    "school": {"GP": "Gabriel Pereira (GP)", "MS": "Mousinho da Silveira (MS)"},
    "address": {"U": "Urban", "R": "Rural"},
    "Pstatus": {"T": "Living together", "A": "Apart"},
    "internet": {"yes": "Yes", "no": "No"},
    "any_parent_teacher": {1: "Yes", 0: "No"},}

ORDINAL_LEVEL_LABELS = {
    "studytime": {
        1: "1 - <2 hours",
        2: "2 - 2 to 5 hours",
        3: "3 - 5 to 10 hours",
        4: "4 - >10 hours",},
    "Medu": {
        0: "0 - none",
        1: "1 - primary education (4th grade)",
        2: "2 - 5th to 9th grade",
        3: "3 - secondary education",
        4: "4 - higher education",},
    "Fedu": {
        0: "0 - none",
        1: "1 - primary education (4th grade)",
        2: "2 - 5th to 9th grade",
        3: "3 - secondary education",
        4: "4 - higher education",},
    "goout": {
        1: "1 - very low",
        2: "2 - low",
        3: "3 - medium",
        4: "4 - high",
        5: "5 - very high",},}

# Create Table 1
table_rows = []
table_rows.append({"Characteristic": "Sample size", "Summary Mean (SD) or N (%)": f"n = {len(df)}",})

for col in NUMERIC_FOR_TABLE:
    table_rows.append({
        "Characteristic": VARIABLE_LABELS[col],
        "Summary Mean (SD) or N (%)": f"{df[col].mean():.2f} ({df[col].std():.2f})",})

for col in CATEGORICAL_FOR_TABLE:
    table_rows.append({"Characteristic": VARIABLE_LABELS[col], "Summary Mean (SD) or N (%)": "",})
    n_total = len(df)
    if col in ORDINAL_LEVEL_LABELS:
        ordered_levels = list(ORDINAL_LEVEL_LABELS[col].keys())
        for level in ordered_levels:
            count = int((df[col] == level).sum())
            pct = 100 * count / n_total
            level_name = ORDINAL_LEVEL_LABELS[col].get(level, str(level))
            table_rows.append({"Characteristic": f"  - {level_name}", "Summary Mean (SD) or N (%)": f"n = {count} ({pct:.1f}%)",})
    else:
        value_counts = df[col].value_counts()
        for level, count in value_counts.items():
            pct = 100 * count / n_total
            level_name = LEVEL_LABELS.get(col, {}).get(level, str(level))
            table_rows.append({"Characteristic": f"  - {level_name}", "Summary Mean (SD) or N (%)": f"n = {count} ({pct:.1f}%)",})

table1 = pd.DataFrame(table_rows)
table1.to_csv("Final/outputs/table1.csv", index=False)

# Aim 1 plots
plt.figure(figsize=(7, 5))
sns.boxplot(data=df, x="sex", y="total_alcohol")
plt.title("Total Alcohol Consumption by Sex")
plt.xlabel("Sex")
plt.ylabel("Total Alcohol (Dalc + Walc)")
sex_levels = list(df["sex"].value_counts().index)
sex_labels = [LEVEL_LABELS["sex"].get(level, str(level)) for level in sex_levels]
plt.xticks(ticks=range(len(sex_levels)), labels=sex_labels)
plt.tight_layout()
plt.savefig(f"Final/outputs/aim1_total_alcohol_by_sex.png", dpi=300)
plt.close()

plt.figure(figsize=(7, 5))
sns.boxplot(data=df, x="school", y="total_alcohol")
plt.title("Total Alcohol Consumption by School")
plt.xlabel("School")
plt.ylabel("Total Alcohol (Dalc + Walc)")
school_levels = list(df["school"].value_counts().index)
school_labels = [LEVEL_LABELS["school"].get(level, str(level)) for level in school_levels]
plt.xticks(ticks=range(len(school_levels)), labels=school_labels)
plt.tight_layout()
plt.savefig(f"Final/outputs/aim1_total_alcohol_by_school.png", dpi=300)
plt.close()

# Aim 2 exploratory plots
plt.figure(figsize=(7, 5))
sns.histplot(df["G3"], bins=10, kde=True)
plt.title("Distribution of Final Grade")
plt.xlabel("Final Grade")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(f"Final/outputs/aim2_g3_histogram.png", dpi=300)
plt.close()

# Continuous predictors: regplot
continuous_predictors = ["age", "absences"]
for col in continuous_predictors:
    plt.figure(figsize=(7, 5))
    sns.regplot(data=df, x=col, y="G3", scatter_kws={"alpha": 0.6})
    predictor_label = VARIABLE_LABELS.get(col, col)
    plt.title(f"Final Grade vs {predictor_label}")
    plt.xlabel(predictor_label)
    plt.ylabel("Final Grade")
    plt.tight_layout()
    plt.savefig(f"Final/outputs/aim2_g3_vs_{col}.png", dpi=300)
    plt.close()

# Ordinal predictors: boxplots by level
ordinal_predictors = ["studytime", "goout", "Medu", "Fedu"]
for col in ordinal_predictors:
    level_order = sorted(df[col].dropna().unique())
    label_lookup = ORDINAL_LEVEL_LABELS.get(col, {})
    plot_df = df.copy()
    plot_df[f"{col}_label"] = plot_df[col].map(label_lookup).fillna(plot_df[col].astype(str))
    label_order = [label_lookup.get(level, str(level)) for level in level_order]
    if col in ["Medu", "Fedu"]:
        label_order = [textwrap.fill(label, width=22) for label in label_order]
        plot_df[f"{col}_label"] = plot_df[f"{col}_label"].apply(lambda x: textwrap.fill(str(x), width=22))
        plt.figure(figsize=(10, 5))
    else:
        plt.figure(figsize=(7, 5))
    sns.boxplot(data=plot_df, x=f"{col}_label", y="G3", order=label_order)
    predictor_label = VARIABLE_LABELS.get(col, col)
    plt.title(f"Final Grade by {predictor_label}")
    plt.xlabel(predictor_label, labelpad=20)
    plt.ylabel("Final Grade")
    if col in ["Medu", "Fedu"]: plt.xticks(fontsize=9)
    plt.tight_layout()
    plt.savefig(f"Final/outputs/aim2_g3_by_{col}.png", dpi=300)
    plt.close()

categorical_predictors = ["sex", "school", "any_parent_teacher"]
for col in categorical_predictors:
    level_order = list(df[col].value_counts().index)
    label_lookup = LEVEL_LABELS.get(col, {})
    plot_df = df.copy()
    plot_df[f"{col}_label"] = plot_df[col].map(label_lookup).fillna(plot_df[col].astype(str))
    label_order = [label_lookup.get(level, str(level)) for level in level_order]
    plt.figure(figsize=(7, 5))
    sns.boxplot(data=plot_df, x=f"{col}_label", y="G3", order=label_order)
    predictor_label = VARIABLE_LABELS.get(col, col)
    plt.title(f"Final Grade by {predictor_label}")
    plt.xlabel(predictor_label)
    plt.ylabel("Final Grade")
    plt.tight_layout()
    plt.savefig(f"Final/outputs/aim2_g3_by_{col}.png", dpi=300)
    plt.close()
