import pandas as pd

file = pd.read_csv("cleaned_animal_disease_prediction.csv")

print(set(file.Disease_Prediction.to_list()))
print(len(set(file.Disease_Prediction.to_list())))

