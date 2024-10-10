from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import *
from ..serializers import *

class TestController(APIView):
    def post(self, request):
        serializer = TestSerializer(data=request.data)

        if serializer.is_valid():
            test_data = serializer.validated_data
            test = Test.objects.create(name=test_data["name"])

            for question_data in test_data["questions"]:
                alternatives_data = question_data.pop("alternatives")
                question = QuestionSchema.objects.create(
                    statement = question_data["statement"],
                    explanation = question_data["explanation"],
                    score = question_data["score"],
                    tag_type = question_data["tag_type"],
                )
                question.alternatives.set([
                    AlternativeSchema.objects.create(**alt_data) for alt_data in alternatives_data
                ])
                test.questions.add(question)
            return Response({"status": "Ok", "id": test.id, "message": ""}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "Error", "message": "[!] Error con la pregunta Número 1"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def assign_test(request, test_id):
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return Response({"status": "Error", "message": "La prueba no existe"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TestAssignSerializer(data=request.data)
    if serializer.is_valid():
        student_ids = request.data.get('students', [])
        success_ids = []
        error_ids = []

        for student_id in student_ids:
            try:
                student = Student.objects.get(id=student_id)
                test.students.add(student)
                success_ids.append(student_id)
            except Student.DoesNotExist:
                error_ids.append(student_id)

        if error_ids:
            return Response({
                "status": "Error",
                "message": "[!] Estudiante no existe",
                "success": success_ids,
                "error": error_ids,
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "Ok",
                "success": success_ids,
                "error": error_ids,
            }, status=status.HTTP_200_OK)

    return Response({
        "status": "Error",
        "message": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

class TestAnswersView(APIView):
    def get(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({"status": "Error", "message": "La prueba no existe"}, status=status.HTTP_404_NOT_FOUND)

        students_data = []
        students = Student.objects.filter(answer__question__test=test).distinct()

        for student in students:
            answers = Answer.objects.filter(student=student, question__test=test)
            correct = wrong = skip = score = 0

            for answer in answers:
                question = answer.question

                try:
                    correct_alternative = question.alternatives.get(correct=True)
                except AlternativeSchema.DoesNotExist:
                    continue 
                
                if answer.answer == correct_alternative.content:
                    correct += 1
                    score += question.score

                elif answer.answer == "":
                    skip += 1
                    
                else:
                    wrong += 1

            students_data.append({
                "id": student.id,
                "name": student.name,
                "score": score,
                "stats": {
                    "correct": correct,
                    "wrong": wrong,
                    "skip": skip
                }
            })

        result = {
            "id": test.id,
            "name": test.name,
            "students": students_data
        }
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({"status": "Error", "message": "La prueba no existe"}, status=status.HTTP_404_NOT_FOUND)

        student_data = request.data.get('students', [])
        success_ids = []
        error_ids = []

        for student_info in student_data:
            student_id = student_info.get('id')
            try:
                student = Student.objects.get(id=student_id)
                success_ids.append(student_id)

                for question_data in student_info.get('questions', []):
                    question_id = question_data.get('id')
                    answer_value = question_data.get('answer')

                    try:
                        question = QuestionSchema.objects.get(id=question_id)
                        Answer.objects.create(
                            student=student,
                            question=question,
                            answer=answer_value
                        )
                    except QuestionSchema.DoesNotExist:
                        pass

            except Student.DoesNotExist:
                error_ids.append(student_id)

        if error_ids:
            return Response({
                "status": "Error",
                "message": "[!] Estudiante no existe",
                "success": success_ids,
                "error": error_ids
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "Ok",
                "success": success_ids,
                "error": error_ids
            }, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_student(request):
    serializer = CreateStudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "Ok", "student": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"status": "Error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)