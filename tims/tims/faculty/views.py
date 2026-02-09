from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
# Create your views here.

from django.views import View
from .models import TrainingSession,StudentAttendance
from django.contrib.auth import get_user_model
User = get_user_model()
from adminapp.models import Batch
from .forms import TrainingSessionForm,StudentAttendanceForm

class TrainingSessionCreateView(View):
    template_name = 'create_session.html'

    def get(self, request):
        form = TrainingSessionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty:training_list')
        return render(request, self.template_name, {'form': form})

class TrainingSessionListView(View):
    template_name = 'Session_list.html'

    def get(self, request):
        sessions = TrainingSession.objects.all()
        return render(request, self.template_name, {'sessions': sessions})

class TrainingSessionUpdateView(View):
    template_name = 'create_session.html'

    def get(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        form = TrainingSessionForm(instance=session)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        form = TrainingSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('faculty:training_list')
        return render(request, self.template_name, {'form': form})
                
class TrainingSessionDeleteView(View):

    def post(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        session.delete()
        return redirect('faculty:training_list')

class StudentAttendanceCreate(View):
    template_name = 'create_attendance.html'

    def get(self, request):
        form = StudentAttendanceForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = StudentAttendanceForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Attendance created successfully.")
            return redirect('faculty:attendance-list')

        return render(request, self.template_name, {'form': form})

class StudentAttendanceList(View):
    template_name = 'attendance_list.html'

    def get(self, request):
        attendances = StudentAttendance.objects.select_related(
            'student', 'faculty', 'batch'
        ).order_by('-attendance_date')

        return render( request, self.template_name, {'attendances': attendances})

class StudentAttendanceUpdate(View):
    template_name = 'create_attendance.html'

    def get(self, request, pk):
        attendance = get_object_or_404(StudentAttendance, pk=pk)
        form = StudentAttendanceForm(instance=attendance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        attendance = get_object_or_404(StudentAttendance, pk=pk)
        form = StudentAttendanceForm(request.POST, instance=attendance)

        if form.is_valid():
            form.save()
            messages.success(request, "Attendance updated successfully.")
            return redirect('faculty:attendance-list')

        return render(request, self.template_name, {'form': form})

class StudentAttendanceDelete(View):

    def get(self, request, pk):
        attendance = get_object_or_404(StudentAttendance, pk=pk)
        attendance.delete()
        messages.success(request, "Attendance deleted successfully.")
        return redirect('faculty:attendance-list')
         
class FacultyAttendanceProgressView(View):
    template_name = "faculty_attendance_progress.html"

    def get(self, request):
        faculty = Faculty.objects.get(user=request.user)

        selected_course = request.GET.get("course")

        # ----------------------------------
        # ONLY courses assigned to faculty
        # ----------------------------------
        faculty_courses = Course.objects.filter(
            studentattendance__faculty=faculty
        ).distinct()

        # ----------------------------------
        # Attendance base query
        # ----------------------------------
        attendance_qs = StudentAttendance.objects.filter(
            faculty=faculty
        )

        if selected_course:
            attendance_qs = attendance_qs.filter(course_id=selected_course)

        attendance_data = []

        students = Student.objects.filter(
            studentattendance__in=attendance_qs
        ).distinct()

        for student in students:
            courses = faculty_courses
            if selected_course:
                courses = courses.filter(id=selected_course)

            for course in courses:
                total_classes = attendance_qs.filter(
                    student=student,
                    course=course
                ).count()

                present_classes = attendance_qs.filter(
                    student=student,
                    course=course,
                    status="Present"
                ).count()

                percentage = (
                    (present_classes / total_classes) * 100
                    if total_classes else 0
                )

                attendance_data.append({
                    "student": student,
                    "course": course,
                    "total": total_classes,
                    "present": present_classes,
                    "percentage": round(percentage, 2),
                })

        context = {
            "courses": faculty_courses,
            "selected_course": selected_course,
            "attendance_data": attendance_data,
        }

        return render(request, self.template_name, context)
        
class FacultyTrainingProgressView(View):
    template_name = "faculty/faculty_training_progress.html"

    def get(self, request):
        faculty = Faculty.objects.get(user=request.user)

        selected_batch = request.GET.get("batch")

        # --------------------------------------
        # ONLY batches assigned to this faculty
        # --------------------------------------
        faculty_batches = Batch.objects.filter(
            trainingsession__faculty=faculty
        ).distinct()

        # --------------------------------------
        # Training sessions base query
        # --------------------------------------
        sessions_qs = TrainingSession.objects.filter(
            faculty=faculty
        )

        if selected_batch:
            sessions_qs = sessions_qs.filter(batch_id=selected_batch)

        # --------------------------------------
        # Batch-wise session count
        # --------------------------------------
        batch_sessions = (
            sessions_qs
            .values("batch__name")
            .annotate(total_sessions=Count("id"))
        )

        context = {
            "batches": faculty_batches,
            "selected_batch": selected_batch,
            "batch_sessions": batch_sessions,
        }

        return render(request, self.template_name, context)