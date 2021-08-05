class Gender:
    NEUTRAL = 1
    FEMALE = 2
    MALE = 3

    GENDER_STRINGS = {NEUTRAL: "neutral",
                      FEMALE: "female",
                      MALE: "male"
                      }

    def __init__(self, gender: int = 1):
        self.gender: int = gender

    def __str__(self):
        return self.GENDER_STRINGS[_(self.gender)]

    def __eq__(self, other):
        if isinstance(other, Gender):
            return self.gender == other.gender
        elif isinstance(other, int):
            return self.gender == other
        else:
            return False
