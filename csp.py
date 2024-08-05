"""The first task is to work on the various attributes by modifing the faker data to suite our objective in this program below 
encapsulated attributes 
    name 
    age 
    id 
    sex
    religion 

academic attributes(ordinary-level)
    department/class 
        science 
        commercial 
        art 
    performance 
        Needs improvement (NI)
        Successful (S)
        Exceptional (E)
shared attibutes 
    course 
        dependent on department 
    (faculty 
        departments)
    faculty 
        sciences 
            chemistry 
            computer science 
            microbiology
        engineering 
            mechanical 
            electrical 
            aerospace 
        art
            english 
            history 
            linguistica
        management science 
            business administration
            marketing 
            accounting 
        

The next stage is to work on the assignment of students into various faculties, departments
    to achieve this i would need to getthe student data from the json file (done)
    assign students into various department then map it to its faculty
        to achieve this, i will work with the o level department, this will be the major key to consider when the faculty assignment occurs (done)
the next task is to create a relationship between students within and outside a department, formation of relationship, could be based off instrest such as extracurricullar activities, and other key factors, such as race, age factor etc
        this is achieved with the use of kmeans algorithm 
 """

import json
from typing import List , Dict
from dataclasses import dataclass , field
import random
import pandas as pd
from sklearn.preprocessing import OneHotEncoder , StandardScaler
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd





with open("profile.json", 'r') as file:
    data = json.load(file)
    

@dataclass
class ExtracurricularActivity:
    category: str
    activity: str

@dataclass
class Department:
    name: str
    faculty: str

@dataclass
class Faculty:
    name: str
    departments: Dict[str, Department] = field(default_factory=dict)

@dataclass
class Student:
    name: str
    email: str
    matriculation_number: str
    age: int
    sex: str
    race: str
    religion: str
    o_level_department: str
    o_level_performance: str
    extracurricular_activity: List[ExtracurricularActivity]
    chosen_department: str = field(default=None)
    department: Department = field(init=False)
    faculty: Faculty = field(init=False)

    def __post_init__(self):
        if not self.chosen_department:
            self.chosen_department = self.choose_random_department(self.o_level_department)
        self.department = self.get_department(self.chosen_department)
        self.faculty = self.get_faculty(self.department.faculty)

    def choose_random_department(self, o_level_department: str) -> str:
        department_choices = {
            "Science": ["Computer Science", "Microbiology", "Chemistry", "Mechanical Engineering", "Electrical Engineering", "Aerospace Engineering"],
            "Art": ["Literature", "Linguistics", "History"], 
            "Commercial": ["Business Administration", "Accounting", "Marketing"],
        }
        possible_departments = department_choices.get(o_level_department, [])
        if not possible_departments:
            raise ValueError(f"No departments found for O-level department: {o_level_department}")
        return random.choice(possible_departments)
    
    def get_department(self, department_name: str) -> Department:
        department_mapping = {
            "Computer Science": Department(name="Computer Science", faculty="Sciences"),
            "Electrical Engineering": Department(name="Electrical Engineering", faculty="Engineering"),
            "Mechanical Engineering": Department(name="Mechanical Engineering", faculty="Engineering"),
            "Aerospace Engineering": Department(name="Aerospace Engineering", faculty="Engineering"),
            "Microbiology": Department(name="Microbiology", faculty="Sciences"),
            "Chemistry": Department(name="Chemistry", faculty="Sciences"),
            "History": Department(name="History", faculty="Arts"),
            "Linguistics": Department(name="Linguistics", faculty="Arts"),
            "Literature": Department(name="Literature", faculty="Arts"),
            "Marketing": Department(name="Marketing", faculty="Management Sciences"),
            "Business Administration": Department(name="Business Administration", faculty="Management Sciences"),
            "Accounting": Department(name="Accounting", faculty="Management Sciences")
        }
        if department_name in department_mapping:
            return department_mapping[department_name]
        else:
            raise ValueError(f"Department not found: {department_name}")
    
    def get_faculty(self, faculty_name: str) -> Faculty:
        faculty_mapping = {
            "Engineering": Faculty(name="Engineering"),
            "Sciences": Faculty(name="Sciences"),
            "Arts": Faculty(name="Arts"),
            "Management Sciences": Faculty(name="Management Sciences")
        }

        if faculty_name in faculty_mapping:
            return faculty_mapping[faculty_name]
        else:
            raise ValueError(f"Faculty not found: {faculty_name}")

        

# this instantiates the Student class from the json data
def create_student_from_json(response_data):
    extracurricular_activities = [
        ExtracurricularActivity(**activity) for activity in response_data.get("extracurricular-activities", [])
    ]

    return Student(
        name = response_data["name"],
        email = response_data["email"],
        matriculation_number = response_data["matriculation"],
        age = response_data["age"],
        sex = response_data["sex"],
        race = response_data["race"],
        religion = response_data["religion"],
        o_level_department = response_data["o_level_department"], 
        o_level_performance = response_data["o_level_performance"],
        extracurricular_activity= extracurricular_activities
    )



# the instance of the class Student, assigned to the variable students in a list
students = [create_student_from_json(response) for response in data]

# creating of student cluster using kmeans algorithm 
students_df = pd.DataFrame(students)
encoder = OneHotEncoder()
encoded_features = encoder.fit_transform(students_df[['race', 'religion', 'o_level_department']]).toarray()


scaler = StandardScaler()
scaled_features = scaler.fit_transform(students_df[['age']])

def flatten_extracurricular_activities(extracurricular_list):
    return ' '.join([f"{activity['category']} {activity['activity']}" for activity in extracurricular_list])

interests_list = students_df['extracurricular_activity'].apply(flatten_extracurricular_activities).values

encoded_interests = encoder.fit_transform(interests_list.reshape(-1, 1)).toarray()

features = np.hstack((encoded_features, scaled_features, encoded_interests))

# Clustering
k = 2000
kmeans = KMeans(n_clusters=k)
kmeans.fit(features)


students_df['cluster'] = kmeans.labels_


for cluster_id in range(k):
    print(f"Cluster {cluster_id}:")
    cluster_students = students_df[students_df['cluster'] == cluster_id]
    for _, student in cluster_students.iterrows():
        student_dict = student["department"]
        print(f"""  
            Name -  {student["name"]}
            Sex  -  {student["sex"]}
            Age  -  {student["age"]}
            Matriculation Number  -  {student["matriculation_number"]}
            Academic Performance  -  {student["o_level_performance"]}
            Department -  {student['department']}
            Extracurricular Activity - {student['extracurricular_activity']}

""")


