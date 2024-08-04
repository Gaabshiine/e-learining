# admin_page_app/models.py

from django.db import models
from account_app.models import Student, Instructor

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'courses'

class Assignment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    max_score = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'assignments'

class AssignmentSubmission(models.Model):
    submission_file = models.CharField(max_length=255)
    submission_date = models.DateTimeField()
    score = models.IntegerField()
    feedback = models.TextField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.student.email_address} for {self.assignment.name}"

    class Meta:
        db_table = 'assignment_submissions'

class Quiz(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    max_score = models.IntegerField()
    duration = models.IntegerField()  # Duration in minutes
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'quizzes'

class QuizQuestion(models.Model):
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=(('multiple_choice', 'Multiple Choice'), ('true_false', 'True/False')))
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

    class Meta:
        db_table = 'quiz_questions'

class QuizAnswer(models.Model):
    answer_text = models.TextField()
    is_correct = models.BooleanField()
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer_text

    class Meta:
        db_table = 'quiz_answers'

class StudentQuizSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    total_score = models.IntegerField()
    selected_answer = models.ForeignKey(QuizAnswer, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.student.email_address} for {self.quiz.name}"

    class Meta:
        db_table = 'student_quiz_submissions'

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    event_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'events'

class Zoom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    zoom_event_date = models.DateField()
    zoom_link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'zooms'

class Enrollment(models.Model):
    enrollment_date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.email_address} enrolled in {self.course.name}"

    class Meta:
        db_table = 'enrollments'

class Certificate(models.Model):
    issue_date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.student.email_address} in {self.course.name}"

    class Meta:
        db_table = 'certificates'

class Review(models.Model):
    review_text = models.TextField()
    rating = models.IntegerField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.student.email_address} for {self.course.name}"

    class Meta:
        db_table = 'reviews'

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'lessons'


class ActivationRequest(models.Model):
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')), default='pending')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        db_table = 'activation_requests'
