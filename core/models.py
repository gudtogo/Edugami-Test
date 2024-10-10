from django.db import models

# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=250)

class TagEnum(models.TextChoices):
    NUMEROS = 'Numeros', 'Números'
    GEOMATRIA = 'Geometria', 'Geometría'
    ALGEBRA = 'Algebra y Funciones', 'Álgebra y Funciones'
    PROBABILIDAD = 'Probabilidad y Estadística', 'Probabilidad y Estadísticas'

class AlternativeSchema(models.Model):
    content = models.TextField()
    correct = models.BooleanField()

class QuestionSchema(models.Model):
    statement = models.TextField()
    explanation = models.TextField()
    alternatives = models.ManyToManyField(AlternativeSchema)
    score = models.IntegerField()
    tag_type = models.CharField(max_length=250, choices=TagEnum.choices)

class Test(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    questions = models.ManyToManyField(QuestionSchema)
    students = models.ManyToManyField(Student, related_name="tests")

class Answer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionSchema, on_delete=models.CASCADE)
    answer = models.CharField(max_length=250)

