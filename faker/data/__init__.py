from enum import Enum

NAMES = [
    "Liam",
    "Emma",
    "Noah",
    "Olivia",
    "Ava",
    "Elijah",
    "Sophia",
    "Mason",
    "Isabella",
    "Logan",
    "Mia",
    "James",
    "Charlotte",
    "Benjamin",
    "Amelia",
    "Lucas",
    "Harper",
    "Henry",
    "Evelyn",
    "Alexander"
]

RELIGION = [
    "Christianity", 
    "Islam",
    "Buddism",
    "Hinduism"

]

class Sex(str, Enum):
    M = "Male"
    F = "Female"

    @classmethod
    def __iter__(cls):
        return iter(cls.__members__.values())
    
class Perf(str, Enum):
    E = "Exceptional"
    NI = "Needs Improvement"
    S = "Successful"


    @classmethod
    def __iter__(cls):
        return iter(cls.__members__.values())

 
class Race(str, Enum):
    Human = "Human"
    Elf = "Elf"
    Dwarf = "Dwarf"
    Orc = "Orc"
    Gnome = "Gnome"
    Halfling = "Halfling"
    Dragonborn = "Dragonborn"
    Tiefling = "Tiefling"
    HalfElf = "Half-Elf"
    HalfOrc = "Half-Orc"
    Goblin = "Goblin"
    Troll = "Troll"
    Giant = "Giant"
    Vampire = "Vampire"
    Werewolf = "Werewolf"
    Mermaid_Merman = "Mermaid/Merman"
    Fairy = "Fairy"
    Centaur = "Centaur"
    Minotaur = "Minotaur"
    Satyr = "Satyr"

    @classmethod
    def __iter__(cls):
        return iter(cls.__members__.values())

# O_LEVEL_DEPARTMENT = [
#     "Commercial", 
#     "science", 
#     "art"
# ]
O_LEVEL_PERFORMANCE = [
    "Needs improvement (NI)",
    "Successful (S)",
    "Exceptional (E)"
]

O_LEVEL_DEPARTMENT =[
    "Science",
    "Commercial",
    "Art"

]

CATEGORIZED_EXTRACURRICULAR_ACTIVITIES = {
    "Sports Teams": [
        "Soccer", "Basketball", "Baseball/Softball", "Football", "Volleyball",
        "Track and Field", "Tennis", "Swimming", "Gymnastics", "Wrestling"
    ],
    "Clubs and Societies": [
        "Debate Club", "Chess Club", "Science Club", "Math Club", "Computer Club",
        "Robotics Club", "Language Clubs", "Environmental Club", "Drama Club", "Music Club"
    ],
    "Arts and Culture": [
        "School Band", "Choir", "Dance Team", "Art Club", "Theater/Drama",
        "Photography Club", "Film Club", "Writing/Poetry Club"
    ],
    "Academic and Professional Development": [
        "Student Government", "Model United Nations", "Business Club", "Future Farmers of America (FFA)",
        "Health Occupations Students of America (HOSA)", "DECA", "Academic Decathlon"
    ],
    "Community Service and Leadership": [
        "Key Club", "National Honor Society", "Peer Tutoring", "Volunteer Clubs",
        "Leadership Training Programs"
    ],
    "Special Interest Groups": [
        "Book Club", "Culinary Club", "Anime/Manga Club", "LGBTQ+ Alliance", "Gaming Club",
        "Hiking/Outdoor Adventure Club", "Astronomy Club"
    ],
    "STEM Activities": [
        "Science Fair", "Math Olympiad", "Coding Competitions", "Engineering Projects",
        "Biology/Chemistry Experiments"
    ],
    "Cultural and Diversity Groups": [
        "International Students Association", "Cultural Heritage Clubs", "Religious Affiliation Groups"
    ],
    "Health and Wellness": [
        "Yoga Club", "Meditation Group", "Mental Health Awareness Club", "Nutrition Club"
    ],
    "Media and Publications": [
        "School Newspaper", "Yearbook Committee", "Literary Magazine", "Radio Club", "TV/Media Production Club"
    ]
}
