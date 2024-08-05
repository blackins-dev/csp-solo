"""
The goal of this package is to generate fake user information
from repositories of avaiable data.

This information includes, name, age, sex, race, email, matriculation number.


Matriculation number is a unique identifier for students in a university.
Format: 210591019 | xxxxxxyyy

Where x is the year of admission based on the department namespace
Where y is the unique identifier for the student

Assigning extra-curricular activities to students where each student can participate
in  a maximum of 3 activities.
"""

import secrets
from typing import Dict, Optional, List, TypeVar, TypedDict, Union
from enum import Enum
from dataclasses import dataclass
import json  

from data import NAMES, Sex, Race, CATEGORIZED_EXTRACURRICULAR_ACTIVITIES ,  RELIGION , O_LEVEL_DEPARTMENT , Perf


S = TypeVar('S', bound=Enum)


def random_from_enum(
    choices: List[S],
    weight: Optional[Dict[S, int]] = None
) -> S:

    if weight is None:
        return secrets.choice(choices)

    for item in weight:
        choices.extend([item] * weight[item])

    return secrets.choice(choices)


T = TypeVar('T')


def random_from_list(
    data:  List[T],
    weight: Optional[Dict[T, int]] = None
) -> T:

    if weight is None:
        return secrets.choice(data)

    choices = data

    for item in weight:
        choices.extend([item] * weight[item])

    return secrets.choice(choices)


class PersonConfiguration(TypedDict):
    name_source: List[str]
    name_weight: Optional[Dict[str, int]]

    age_range_min: int
    age_range_max: int

    age_range_weight: Optional[Dict[int, int]]

    sex_source: List[Sex]
    sex_weight: Optional[Dict[Sex, int]]

    perf_source: List[Perf]
    perf_weight: Optional[Dict[Sex, int]]

    race_source: List[Race]
    race_weight: Optional[Dict[Race, int]]

    extracurricular_categories: Dict[str, List[str]]
    extracurricular_category_weight: Optional[Dict[str, int]]

    religion_source: List[str]
    o_level_dept_source: List[str]


@dataclass
class Person:
    name: str
    age: int
    sex: Sex
    race: Race
    religion: str
    email: str
    matriculation_number: str
    o_level_dept: str
    perf: Perf
    extracurricular_activities: List[Dict[str, str]] 

    # config: PersonConfiguration

    def __init__(
        self,
        config: PersonConfiguration,
        matriculation_number: str
    ) -> None:
        self.config = config
        self.matriculation_number = matriculation_number

        self.populate_person()

    def __str__(self) -> str:
        activities = ", ".join(
        [f"{item['category']}: {item['activity']}" for item in self.extracurricular_activities]
         )
        return f"""
        _______________________________________

        Profile
        Name: {self.name}
        Email: {self.email}
        Matriculation Number: {self.matriculation_number}

        Stats
        Age: {self.age}
        Sex: {self.sex.value}
        Race: {self.race.value}
        Religion: {self.religion}

        o_level_departent: {self.o_level_dept}
        o_level_perfomance: {self.perf.value}
        Extracurricular Activities: {activities}
        """.replace("        ", "")
    
    
    def populate_person(self) -> None:

        first_name: str = self.get_name()
        last_name: str = self.get_name()

        self.name = f"{first_name} {last_name}"
        self.email = f"{first_name}.{last_name}@example.com".lower()

        self.age = self.get_age()
        self.sex = self.get_sex()
        self.race = self.get_race()
        self.religion =  self.get_religion()
        self.o_level_dept = self.get_o_level_dept()
        self.perf = self.get_o_level_perf()

        self.extracurricular_activities = self.get_extracurricular_activities()

    def get_sex(self) -> Sex:
        return random_from_enum(
            self.config["sex_source"],
            self.config["sex_weight"])

    def get_race(self) -> Race:
        return random_from_enum(
            self.config["race_source"],
            self.config["race_weight"]
        )

    def get_name(self) -> str:
        return random_from_list(
            self.config["name_source"],
            self.config["name_weight"]
        )
    def get_religion(self) -> str:
        return random_from_list(
            self.config["religion_source"],
            # self.config["name_weight"]
        )

    def get_age(self) -> int:
        age_range = range(
            self.config["age_range_min"],
            self.config["age_range_max"]
        )

        valid_ages = [age for age in age_range]

        return random_from_list(
            valid_ages,
            self.config["age_range_weight"]
        )
    def get_o_level_dept(self) -> str:
        return random_from_list(
            self.config["o_level_dept_source"],
            # self.config["name_weight"]
        )
    def get_o_level_perf(self)-> Perf:
        return random_from_enum(
            self.config["perf_source"],
            self.config["perf_weight"]
        )
    
    def get_extracurricular_activities(self) -> List[Dict[str, str]]:
        activities = []
        chosen_activities = [] # To avoid duplicate activities
        categories = list(self.config["extracurricular_categories"].keys())

        # randomising the amount of activities that can be performed by a single person 
        activity_weights = {1:100} #weights or ratio for 1, 2 or 3 activities 
        random_activities_performed = random_from_list(
            list(activity_weights.keys()), 
            weight = activity_weights
        )
        for _ in range(random_activities_performed):
            category = random_from_list(categories, self.config["extracurricular_category_weight"])
            possible_activities = [
                act for act in self.config["extracurricular_categories"][category]
                if act not in chosen_activities
            ]
            if possible_activities:
                activity = random_from_list(possible_activities)
                chosen_activities.append(activity)
                activities.append({"category": category, "activity": activity})
        return activities
    
   

def main() -> None:
    student_configuration: PersonConfiguration = {
        "name_source": NAMES,
        "name_weight": None,
        "age_range_min": 16,
        "age_range_max": 50,
        "age_range_weight": None,
        "sex_source": [item for item in Sex],
        "sex_weight": {
            Sex.F: 5,
            Sex.M: 5
        },
        "religion_source": RELIGION,
        # "religion_weight": None,
        "race_source": [item for item in Race],
        "race_weight": {
            Race.Human: 2,
        },
        "perf_source": [item for item in Perf],
        "perf_weight": {
            Perf.NI:6,
            Perf.E: 2,
            Perf.S: 5,
        },
        "extracurricular_categories": CATEGORIZED_EXTRACURRICULAR_ACTIVITIES,
        "extracurricular_category_weight": {
            "Sports Teams": 5,
            "Clubs and Societies": 3,
            "Arts and Culture": 2,
            "Academic and Professional Development": 1,
            "Community Service and Leadership": 1,
            "Special Interest Groups": 2,
            "STEM Activities": 1,
            "Cultural and Diversity Groups": 1,
            "Health and Wellness": 1,
            "Media and Publications": 1
        }, 
        "o_level_dept_source": O_LEVEL_DEPARTMENT
        
    }
    

    # Lets make 30 students

    department_code: str = "ID-210591"
    profile_arr = []
    for i in range(10000):
        student_id: str = str(i).rjust(3, "0")

        matriculation_number = f"{department_code}{student_id}"

        student = Person(student_configuration, matriculation_number)
        
        profile = {
            "name": student.name,
            "email":student.email,
            "matriculation": student.matriculation_number,
            "age":student.age,
            "sex": student.sex,
            "race":student.race.value,
            "religion": student.religion,
            "o_level_department": student.o_level_dept,
            "o_level_performance": student.perf.value,
            "extracurricular-activities": student.extracurricular_activities

        }     
    
        profile_arr.append(profile)
    
    
    filename = 'profile.json'

    # Write the dictionary to a JSON file
    with open(filename, 'w') as file:
        json.dump(profile_arr, file, indent=4)
    print(profile_arr)

    
if __name__ == '__main__':
    main()
