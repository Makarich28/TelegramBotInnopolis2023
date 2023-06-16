class Student:
    COUNT = 0

    def __init__(self, name: str, age: int) -> None:
        self._name = name
        self._age = age

        self.count_student()
    # def description(self):
    #     return f'{self.name}, {self.age}'

    @classmethod
    def count_student(cls):
        cls.COUNT += 1

    def student_bio(self):
         print(f'{self._name}, {self._age}, count = {Student.COUNT}')
