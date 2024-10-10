import json
from django.core.management.base import BaseCommand
from core.models import *

class Command(BaseCommand):
    help = 'Carga datos de seed desde un archivo JSON'

    def handle(self, *args, **kwargs):
        AlternativeSchema.objects.all().delete()
        QuestionSchema.objects.all().delete()
        Test.objects.all().delete()
        Student.objects.all().delete()

        with open('seed_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            for student_data in data['students']:
                Student.objects.update_or_create(
                    rut=student_data['rut'],
                    name=student_data['name']
                )

            for test_data in data['tests']:
                test, _= Test.objects.update_or_create(
                    name=test_data['name']
                )
                
                for question_data in test_data['questions']:
                    question, _ = QuestionSchema.objects.update_or_create(
                        statement=question_data['statement'],
                        explanation=question_data['explanation'],
                        score=question_data['score'],
                        tag_type=question_data['axisType']
                    )
                    test.questions.add(question)

                    for alt_data in question_data['alternatives']:
                        alternative, _ = AlternativeSchema.objects.update_or_create(
                            content=alt_data['content'],
                            correct=alt_data['correct']
                        )
                        question.alternatives.add(alternative)

        self.stdout.write(self.style.SUCCESS('Datos de seed cargados con éxito'))