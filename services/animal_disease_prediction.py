import pandas as pd

class DataSet:
    def __init__(self):
        self.file = pd.read_csv("cleaned_animal_disease_prediction.csv")
        self.animals = {i for i in self.file.species}
        self.file_dict = self.file.to_dict()
        self.data_frame = pd.DataFrame(self.file)

        self.animal_breeds = {
            i: {self.file_dict["Breed"][a] for a in self.file_dict["species"] if
                self.file_dict["species"][a] == i}
            for i in self.animals
        }

        self.animal_categories = {
            "carnivores": {"Dog", "Cat", "Pig"},
            "ruminants": {"Cow", "Goat", "Horse", "Sheep"},
            "dairy": {"Cow", "Goat", "Sheep"},
            "herbivore": {"Cow", "Pig", "Goat", "Horse", "Rabbit", "Sheep"}
        }


class AnimalSymptoms:
    def __init__(self, breed: str, species: str, gender: str, symptoms: list, **kwargs):
        self.r = DataSet()

        self.kwargs = kwargs
        self.breed = breed.title()
        self.species = species.title()
        self.gender = gender.title()
        # self.categories = [i for i in self.r.animal_categories if self.species in self.r.animal_categories[i]]
        # self.categories = [self.r.animal_categories[i] for i in self.categories][0]
        self.symptoms = symptoms
        self.prognosis = []

        self.observable_symptoms = symptoms
        self.follow_up_symptoms = {
            i: False
            for i in self.r.file.columns[10:19]
        }

        self.follow_up_symptoms = dict(zip(self.follow_up_symptoms, kwargs.values()))

        self.physical_test_result = {
            i: 0.0
            for i in self.r.file.columns[19:21]
        }

        self.prioritized_results = {
            "P1": [None, 0],
            "P2": [None, 0],
            "P3": [None, 0],
        }

    def priority_one(self):
        confirm_breed = False

        if self.breed in self.r.animal_breeds[self.species]:
            confirm_breed = True

        if not confirm_breed:
            return confirm_breed

        self.breed_result = self.r.data_frame[
            (self.r.data_frame.species == self.species) & (self.r.data_frame.Breed == self.breed) & (self.r.data_frame.Gender == self.gender)]

        ###################################################################################################################################
        self.breed_symptoms = {
                                  "S1": self.breed_result.Symptom_1.to_list(),
                                  "S2": self.breed_result.Symptom_2.to_list(),
                                  "S3": self.breed_result.Symptom_3.to_list(),
                                  "S4": self.breed_result.Symptom_4.to_list(),
                                  "Disease": self.breed_result.Disease_Prediction.to_list()
                              } | {
                                  i: self.breed_result[i].to_list()
                                  for i in self.follow_up_symptoms.keys()
                              }

        for i in range(len(self.breed_symptoms["S1"])):
            count = 0

            for j in self.symptoms:

                for k in self.breed_symptoms:

                    if j.lower() == self.breed_symptoms[k][i].lower():

                        if self.breed_symptoms["Disease"][i].lower() not in [i[0] for i in self.prognosis]:
                            count += 1
                            self.prognosis.append([self.breed_symptoms["Disease"][i].lower(), (count / 13) * 100])

                        else:
                            count += 1
                            d_index = [i[0] for i in self.prognosis].index(self.breed_symptoms["Disease"][i].lower())
                            if self.prognosis[d_index][1] < (count / 13) * 100:
                                self.prognosis[d_index][1] = (count / 13) * 100

            for j in self.follow_up_symptoms:
                if self.breed_symptoms[j][i] == "Yes" or self.breed_symptoms[j][i] == "No":
                    value = True if self.breed_symptoms[j][i] == "Yes" else False

                    if self.follow_up_symptoms[j] == value and self.breed_symptoms["Disease"][i].lower() in [i[0] for i
                                                                                                             in
                                                                                                             self.prognosis]:
                        count += 1
                        d_index = [i[0] for i in self.prognosis].index(self.breed_symptoms["Disease"][i].lower())
                        if self.prognosis[d_index][1] < (count / 13) * 100:
                            self.prognosis[d_index][1] = (count / 13) * 100

                    elif self.follow_up_symptoms[j] == value and self.breed_symptoms["Disease"][i].lower() not in [i[0]
                                                                                                                   for i
                                                                                                                   in
                                                                                                                   self.prognosis]:
                        count += 1
                        self.prognosis.append([self.breed_symptoms["Disease"][i].lower(), (count / 13) * 100])

        ##############################################################################################################################

        print()
        print(self.prognosis)

        highest_probability = [None, 0]
        for i in self.prognosis:
            if i[1] > highest_probability[1]:
                highest_probability = i

        self.prioritized_results["P1"] = highest_probability

        return self.breed_result

    def priority_two(self):
        confirm_breed = False

        if self.breed in self.r.animal_breeds[self.species]:
            confirm_breed = True

        if not confirm_breed:
            return confirm_breed

        self.breed_result = self.r.data_frame[
            (self.r.data_frame.species == self.species) & (self.r.data_frame.Breed == self.breed)]

        ###################################################################################################################################
        self.breed_symptoms = {
                                  "S1": self.breed_result.Symptom_1.to_list(),
                                  "S2": self.breed_result.Symptom_2.to_list(),
                                  "S3": self.breed_result.Symptom_3.to_list(),
                                  "S4": self.breed_result.Symptom_4.to_list(),
                                  "Disease": self.breed_result.Disease_Prediction.to_list()
                              } | {
                                  i: self.breed_result[i].to_list()
                                  for i in self.follow_up_symptoms.keys()
                              }

        for i in range(len(self.breed_symptoms["S1"])):
            count = 0

            for j in self.symptoms:

                for k in self.breed_symptoms:

                    if j.lower() == self.breed_symptoms[k][i].lower():

                        if self.breed_symptoms["Disease"][i].lower() not in [i[0] for i in self.prognosis]:
                            count += 1
                            self.prognosis.append([self.breed_symptoms["Disease"][i].lower(), (count / 13) * 100])

                        else:
                            count += 1
                            d_index = [i[0] for i in self.prognosis].index(self.breed_symptoms["Disease"][i].lower())
                            if self.prognosis[d_index][1] < (count / 13) * 100:
                                self.prognosis[d_index][1] = (count / 13) * 100

            for j in self.follow_up_symptoms:
                if self.breed_symptoms[j][i] == "Yes" or self.breed_symptoms[j][i] == "No":
                    value = True if self.breed_symptoms[j][i] == "Yes" else False

                    if self.follow_up_symptoms[j] == value and self.breed_symptoms["Disease"][i].lower() in [i[0] for i
                                                                                                             in
                                                                                                             self.prognosis]:
                        count += 1
                        d_index = [i[0] for i in self.prognosis].index(self.breed_symptoms["Disease"][i].lower())
                        if self.prognosis[d_index][1] < (count / 13) * 100:
                            self.prognosis[d_index][1] = (count / 13) * 100

                    elif self.follow_up_symptoms[j] == value and self.breed_symptoms["Disease"][i].lower() not in [i[0]
                                                                                                                   for i
                                                                                                                   in
                                                                                                                   self.prognosis]:
                        count += 1
                        self.prognosis.append([self.breed_symptoms["Disease"][i].lower(), (count / 13) * 100])

        ##############################################################################################################################

        print()
        print(self.prognosis)
        print()

        highest_probability = [None, 0]
        for i in self.prognosis:
            if i[1] > highest_probability[1] and i[0] not in [t[0] for t in self.prioritized_results.values()]:
                highest_probability = i

        self.prioritized_results["P2"] = highest_probability

        return self.breed_result

    def priority_three(self):
        confirm_breed = False

        if self.breed in self.r.animal_breeds[self.species]:
            confirm_breed = True

        if not confirm_breed:
            return confirm_breed

        self.breed_result = self.r.data_frame[(self.r.data_frame.species == self.species)]
        ###################################################################################################################################
        self.breed_symptoms = {
                                  "S1": self.breed_result.Symptom_1.to_list(),
                                  "S2": self.breed_result.Symptom_2.to_list(),
                                  "S3": self.breed_result.Symptom_3.to_list(),
                                  "S4": self.breed_result.Symptom_4.to_list(),
                                  "Disease": self.breed_result.Disease_Prediction.to_list()
                              } | {
                                  i: self.breed_result[i].to_list()
                                  for i in self.follow_up_symptoms.keys()
                              }

        for i in range(len(self.breed_symptoms["S1"])):
            count = 0

            for j in self.symptoms:

                for k in self.breed_symptoms:

                    if j.lower() == self.breed_symptoms[k][i].lower():

                        if self.breed_symptoms["Disease"][i].lower() not in [i[0] for i in self.prognosis]:
                            count += 1
                            self.prognosis.append([self.breed_symptoms["Disease"][i].lower(), (count / 13) * 100])

                        else:
                            count += 1
                            d_index = [i[0] for i in self.prognosis].index(self.breed_symptoms["Disease"][i].lower())
                            if self.prognosis[d_index][1] < (count / 13) * 100:
                                self.prognosis[d_index][1] = (count / 13) * 100

            for j in self.follow_up_symptoms:
                if self.breed_symptoms[j][i] == "Yes" or self.breed_symptoms[j][i] == "No":
                    value = True if self.breed_symptoms[j][i] == "Yes" else False

                    if self.follow_up_symptoms[j] == value and self.breed_symptoms["Disease"][i].lower() in [i[0] for i
                                                                                                             in
                                                                                                             self.prognosis]:
                        count += 1
                        d_index = [i[0] for i in self.prognosis].index(self.breed_symptoms["Disease"][i].lower())
                        if self.prognosis[d_index][1] < (count / 13) * 100:
                            self.prognosis[d_index][1] = (count / 13) * 100

                    elif self.follow_up_symptoms[j] == value and self.breed_symptoms["Disease"][i].lower() not in [i[0]
                                                                                                                   for i
                                                                                                                   in
                                                                                                                   self.prognosis]:
                        count += 1
                        self.prognosis.append([self.breed_symptoms["Disease"][i].lower(), (count / 13) * 100])

        ##############################################################################################################################

        print()
        print(self.prognosis)
        print()

        highest_probability = [None, 0]
        for i in self.prognosis:
            if i[1] > highest_probability[1] and i[0] not in [t[0] for t in self.prioritized_results.values()]:
                highest_probability = i

        self.prioritized_results["P3"] = highest_probability

        return self.breed_result

# a = AnimalSymptoms("Bulldog",
#                    "Dog",
#                    "Male",
#                    ["Nasal discharge","loss of appetite","vomiting"],
#                    **{
#                         "Appetite_Loss": True,
#                         "Vomiting": False,
#                         "Diarrhea": False,
#                         "Coughing": True,
#                         "Labored_Breathing": True,
#                         "Lameness": False,
#                         "Skin_Lesions": False,
#                         "Nasal_Discharge": True,
#                         "Eye_Discharge": False
#                    }
# )
#
# a.priority_one()
# a.priority_two()
# a.priority_three()
#
# print(*a.prioritized_results.values(), sep="\n")