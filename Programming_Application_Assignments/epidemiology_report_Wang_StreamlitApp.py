import streamlit as st

st.title("Epidemiology Report Generator")

# 1. Collect user input
city = st.text_input("Enter the city name:").strip()
city = " ".join(city.split())
city = city.title()
disease = st.text_input("Enter the disease name:").strip()
disease = " ".join(disease.split())
disease = disease.title()
population_str = st.text_input("Enter the total population:").strip()
cases_str = st.text_input("Enter the number of reported cases:").strip()
deaths_str = st.text_input("Enter the number of deaths:").strip()
tp_str = st.text_input("Enter the number of true positive cases:").strip()
fn_str = st.text_input("Enter the number of false negative cases:").strip()
tn_str = st.text_input("Enter the number of true negative cases:").strip()
fp_str = st.text_input("Enter the number of false positive cases:").strip()

if st.button("Generate Epidemiology Report"):
    valid_flag = True

    # 2. Validate user input
    city_validation = "".join(city.split())
    if not city_validation.isalpha():
        st.error("Please enter a valid city name with letters only.")
        valid_flag = False

    disease_validation = "".join(disease.split())
    if not disease_validation.isalpha():
        st.error("Please enter a valid disease name with letters only.")
        valid_flag = False

    # 2.1 Validate population
    if not population_str.isdigit():
        st.error("Total population must be an integer with no commas.")
        valid_flag = False

    # 2.2 Validate reported cases
    if not cases_str.isdigit():
        st.error("Reported cases must be an integer with no commas.")
        valid_flag = False

    # 2.3 Validate deaths
    if not deaths_str.isdigit():
        st.error("Deaths must be an integer with no commas.")
        valid_flag = False

    # 2.4 Validate TP, FN, FP, TN
    if not tp_str.isdigit():
        st.error("True positives must be an integer with no commas.")
        valid_flag = False
    if not fn_str.isdigit():
        st.error("False negatives must be an integer with no commas.")
        valid_flag = False
    if not tn_str.isdigit():
        st.error("True negatives must be an integer with no commas.")
        valid_flag = False
    if not fp_str.isdigit():
        st.error("False positives must be an integer with no commas.")
        valid_flag = False

    if valid_flag:
        population = int(population_str)
        total_cases = int(cases_str)
        deaths = int(deaths_str)
        true_positives = int(tp_str)
        false_negatives = int(fn_str)
        true_negatives = int(tn_str)
        false_positives = int(fp_str)

        # 2.5 Validate value ranges
        if population <= 0:
            st.error("Total population must be greater than 0.")
            valid_flag = False
        if total_cases <= 0:
            st.error("Reported cases must be greater than 0.")
            valid_flag = False
        if deaths < 0:
            st.error("Deaths must be greater than or equal to 0.")
            valid_flag = False

        # 2.6 Validate Denominators
        denom_sensitivity = true_positives + false_negatives
        denom_specificity = true_negatives + false_positives
        denom_ppv = true_positives + false_positives
        denom_npv = true_negatives + false_negatives

        if denom_sensitivity == 0:
            st.error("True positives + false negatives cannot be 0.")
            valid_flag = False
        if denom_specificity == 0:
            st.error("True negatives + false positives cannot be 0.")
            valid_flag = False
        if denom_ppv == 0:
            st.error("True positives + false positives cannot be 0.")
            valid_flag = False
        if denom_npv == 0:
            st.error("True negatives + false negatives cannot be 0.")
            valid_flag = False

    # 3. Calculations
    if valid_flag:
        prevalence = (total_cases / population) * 100
        case_fatality_rate = (deaths / total_cases) * 100
        mortality_rate = (deaths / population) * 100
        sensitivity = (true_positives / denom_sensitivity) * 100
        specificity = (true_negatives / denom_specificity) * 100
        ppv = (true_positives / denom_ppv) * 100
        npv = (true_negatives / denom_npv) * 100

    # 4. Generate report
        report = (
            "------------------------------------------------------------\n"
            "Epidemiology Report:\n"
            "------------------------------------------------------------\n"
            f"City: {city}\n"
            f"Disease: {disease}\n"
            f"Population: {population:,}\n"
            f"Cases: {total_cases:,}\n"
            f"Deaths: {deaths:,}\n\n"
            f"Prevalence: {prevalence:0.3f}%\n"
            f"Case Fatality Rate: {case_fatality_rate:0.3f}%\n"
            f"Mortality Rate: {mortality_rate:0.3f}%\n\n"
            "Diagnostic Test Performance:\n"
            f"\tSensitivity: {sensitivity:0.3f}%\n"
            f"\tSpecificity: {specificity:0.3f}%\n"
            f"\tPositive Predictive Value: {ppv:0.3f}%\n"
            f"\tNegative Predictive Value: {npv:0.3f}%\n\n"
            "Summary:\n"
            f"The prevalence of {disease} in {city} is {prevalence:0.3f}%,\n"
            f"with a case fatality rate of {case_fatality_rate:0.3f}%.\n"
            f"Testing sensitivity is {sensitivity:0.3f}%.\n"
            "------------------------------------------------------------"
        )
        st.code(report)