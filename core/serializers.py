from rest_framework import serializers
from .models import *

class AlternativeSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlternativeSchema
        fields = ('content', 'correct')
        
class QuestionSchemaSerializer(serializers.ModelSerializer):
    alternatives = AlternativeSchemaSerializer(many=True)

    class Meta:
        model = QuestionSchema
        fields = ('statement', 'explanation', 'alternatives', 'score', 'tag_type')

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSchemaSerializer(many=True)

    class Meta:
        model = Test
        fields = ('id', 'name', 'questions')

class TestAssignSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(many=True, queryset=Student.objects.all(), write_only=True)

    class Meta:
        model = Test
        fields = ['id', 'students']

class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'rut', 'name')

