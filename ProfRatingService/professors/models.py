from django.db import models
from django.contrib.auth.models import User

# professor model that holds all basic info of a professor
class Professor(models.Model):
    professor_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)


# module model that holds all the information of a module
class Module(models.Model):
    DEPARTMENT_CODES = [
        ("COMP", "Computer Science"),
        ("MATH", "Mathematics"),
        ("BIOL", "Biology"),
        ("PSYC", "Psychology"),
        ("ENGR", "Engineering"),
        ("HIST", "History"),
        ("ECON", "Economics"),
        ("MEDS", "Medicine"),
        ("PHYS", "Physics"),
        ("LITR", "Literature")
        ]
    module_id = models.CharField(max_length=3, primary_key=True)
    department = models.CharField(max_length=4, choices=DEPARTMENT_CODES)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    year_group = models.IntegerField(default=1)
    semester = models.IntegerField()

# iteration model that holds all the information of an iteration of a module by a professor
class Iteration(models.Model):
    iteration_id = models.IntegerField(primary_key=True)
    professor_id = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module_id = models.ForeignKey(Module, on_delete=models.CASCADE)


# rating model that holds the rating of a module by a professor assigned by a student
class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        ]
    rating_id = models.IntegerField(primary_key=True)
    iteration_id = models.ForeignKey(Iteration, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
