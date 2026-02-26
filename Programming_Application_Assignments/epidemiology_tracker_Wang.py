#------------------------------------------------
# Application 1: Epidemiology Metric Report Generator
# Name: Rita Wang
# Date: 2/25/2026
#------------------------------------------------

# 1.Collect and clean all user input 
print("Enter the information with no commas.\n")

city = input("Enter the city name: ")
city = city.strip()
city = " ".join(city.split())
city = city.title()

disease = input("Enter the disease name: ")
disease = disease.strip()
disease = " ".join(disease.split())
disease = disease.title()

population_str = input("Enter the total population: ").strip()
cases_str = input("Enter the number of reported cases: ").strip()
deaths_str = input("Enter the number of deaths: ").strip()
tp_str = input("Enter the number of true positive cases: ").strip()
fn_str = input("Enter the number of false negative cases: ").strip()
fp_str = input("Enter the number of false positive cases: ").strip()
tn_str = input("Enter the number of true negative cases: ").strip()

# 2. Validate input 

# 2.1 Validate city 
city_validation = "".join(city.split())
while not city_validation.isalpha() or len(city_validation) == 0:
    print("Error: Please enter a valid city name with letters only and no numbers.")
    city = input("Enter the city name: ")
    city = city.strip()
    city = " ".join(city.split())
    city = city.title()
    city_validation = "".join(city.split())

# 2.2 Validate disease
disease_validation = "".join(disease.split())
while not disease_validation.isalpha() or len(disease_validation) == 0:
    print("Error: Please enter a valid disease name with letters only and no numbers.")
    disease = input("Enter the disease name: ")
    disease = disease.strip()
    disease = " ".join(disease.split())
    disease = disease.title()
    disease_validation = "".join(disease.split())

# 2.3 Validate population
valid_flag = False
while not valid_flag:
    if not population_str.isdigit():
        print("Error: Please enter an integer with no commas.")
        population_str = input("Enter the total population: ").strip()
    else:
        population = int(population_str)
        if not (population > 0):
            print("Error: Please enter a population greater than 0.")
            population_str = input("Enter the total population: ").strip()
        else:
            valid_flag = True

# 2.4 Validate reported cases
valid_flag = False
while not valid_flag:
    if not cases_str.isdigit():
        print("Error: Please enter the number of reported cases with no commas.")
        cases_str = input("Enter the number of reported cases: ").strip()
    else:
        total_cases = int(cases_str)
        if not (total_cases > 0):
            print("Error: Please enter the number of reported cases greater than 0.")
            cases_str = input("Enter the number of reported cases: ").strip()
        else:
            valid_flag = True

# 2.5 Validate deaths 
valid_flag = False
while not valid_flag:
    if not deaths_str.isdigit():
        print("Error: Please enter an integer with no commas.")
        deaths_str = input("Enter the number of deaths: ").strip()
    else:
        deaths = int(deaths_str)
        if not (deaths >= 0):
            print("Error: Please enter a number of deaths greater than or equal to 0.")
            deaths_str = input("Enter the number of deaths: ").strip()
        else:
            valid_flag = True

# 2.6 Validate TP, FN, FP, TN
valid_flag = False
while not valid_flag:
    while not tp_str.isdigit():
        print("Error: True positive cases must be an integer with no commas.")
        tp_str = input("Enter the number of true positive cases: ").strip()
    while not fn_str.isdigit():
        print("Error: False negative cases must be an integer with no commas.")
        fn_str = input("Enter the number of false negative cases: ").strip()
    while not fp_str.isdigit():
        print("Error: False positive cases must be an integer with no commas.")
        fp_str = input("Enter the number of false positive cases: ").strip()
    while not tn_str.isdigit():
        print("Error: True negative cases must be an integer with no commas.")
        tn_str = input("Enter the number of true negative cases: ").strip()

    true_positives = int(tp_str)
    false_negatives = int(fn_str)
    false_positives = int(fp_str)
    true_negatives = int(tn_str)
    denom_sensitivity = true_positives + false_negatives
    denom_specificity = true_negatives + false_positives
    denom_ppv = true_positives + false_positives
    denom_npv = true_negatives + false_negatives

# 2.7 Validate Denominators
    denom_error = False
    if denom_sensitivity == 0:
        print("Error: True positives + false negatives cannot be 0 for sensitivity.")
        tp_str = input("Re-enter the number of true positive cases: ").strip()
        denom_error = True

    if denom_specificity == 0:
        print("Error: True negatives + false positives cannot be 0 for specificity.")
        tn_str = input("Re-enter the number of true negative cases: ").strip()
        denom_error = True

    if denom_ppv == 0:
        print("Error: True positives + false positives cannot be 0 for PPV.")
        fp_str = input("Re-enter the number of false positive cases: ").strip()
        denom_error = True

    if denom_npv == 0:
        print("Error: True negatives + false negatives cannot be 0 for NPV.")
        fn_str = input("Re-enter the number of false negative cases: ").strip()
        denom_error = True

    if not denom_error:
        valid_flag = True

# 3. Epidemiological calculations
prevalence = (total_cases / population) * 100
case_fatality_rate = (deaths / total_cases) * 100
mortality_rate = (deaths / population) * 100
sensitivity = (true_positives / denom_sensitivity) * 100
specificity = (true_negatives / denom_specificity) * 100
ppv = (true_positives / denom_ppv) * 100
npv = (true_negatives / denom_npv) * 100

# 4. Print report
print("\nEpidemiology Report:")
print("------------------------------------------------------------")
print(f"City: {city}")
print(f"Disease: {disease}")
print(f"Population: {population:,}")
print(f"Cases: {total_cases:,}")
print(f"Deaths: {deaths:,}\n")
print(f"Prevalence: {prevalence:0.3f}%")
print(f"Case Fatality Rate: {case_fatality_rate:0.3f}%")
print(f"Mortality Rate: {mortality_rate:0.3f}%\n")
print("Diagnostic Test Performance:")
print(f"\tSensitivity: {sensitivity:0.3f}%")
print(f"\tSpecificity: {specificity:0.3f}%")
print(f"\tPositive Predictive Value: {ppv:0.3f}%")
print(f"\tNegative Predictive Value: {npv:0.3f}%\n")
print("Summary:")
print(f"The prevalence of {disease} in {city} is {prevalence:0.3f}%,")
print(f"with a case fatality rate of {case_fatality_rate:0.3f}%.")
print(f"Testing sensitivity is {sensitivity:0.3f}%.")
print("------------------------------------------------------------")
