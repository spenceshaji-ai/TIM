from django.shortcuts import render,redirect, get_object_or_404

# Create your views here.

from django.views import View
from .models import TrainingSession,StudentAttendance
from .forms import TrainingSessionForm,StudentAttendanceForm

class TrainingSessionCreate(View):
    template_name = 'create_session.html'

    def get(self, request):
        return render(request, self.template_name, {
            'form': TrainingSessionForm(),
            'title': 'Create Training Session'
        })

    def post(self, request):
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty:training_list')
        return render(request, self.template_name, {
            'form': form,
            'title': 'Create Training Session'
        })
class TrainingSessionList(View):
    template_name = 'Session_list.html'

    def get(self, request):
        sessions = (
            TrainingSession.objects
            #.select_related('batch', 'faculty')
            .order_by('-session_date')
        )
        return render(request, self.template_name, {
            'sessions': sessions
        })
class TrainingSessionUpdate(View):
    template_name = 'update_session.html'

    def get(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        return render(request, self.template_name, {
            'form': TrainingSessionForm(instance=session),
            'title': 'Update Training Session'
        })

    def post(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        form = TrainingSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('faculty:training_list')
        return render(request, self.template_name, {
            'form': form,
            'title': 'Update Training Session'
        })
                
class TrainingSessionDelete(View):

    def post(self, request, pk):
        session = get_object_or_404(TrainingSession, pk=pk)
        session.delete()
        return redirect('faculty:training_list')


training_session_delete_view = TrainingSessionDelete.as_view()

class AttendanceCreate(View):
    template_name = 'create_attendance.html'

    def get(self, request):
        return render(request, self.template_name, {
            'form': StudentAttendanceForm(),
            'title': 'Add Attendance'
        })

    def post(self, request):
        form = StudentAttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty:attendance_list')
        return render(request, self.template_name, {
            'form': form,
            'title': 'Add Attendance'
        })
     

class AttendanceList(View):
    template_name = 'attendance_list.html'

    def get(self, request):
        attendance_list = (
            StudentAttendance.objects
            # .select_related('student', 'faculty', 'batch')
            .order_by('-attendance_date')
        )

        return render(request, self.template_name, {
            'attendance_list': attendance_list,
            'title': 'Attendance List'
        })


class AttendanceUpdate(View):
    template_name = 'update_attendance.html'

    def get(self, request, pk):
        attendance = get_object_or_404(StudentAttendance, pk=pk)
        return render(request, self.template_name, {
            'form': StudentAttendanceForm(instance=attendance),
            'title': 'Update Attendance'
        })

    def post(self, request, pk):
        attendance = get_object_or_404(StudentAttendance, pk=pk)
        form = StudentAttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
        return render(request, self.template_name, {
            'form': form,
            'title': 'Update Attendance'
        })


class AttendanceDelete(View):

    def post(self, request, pk):
        attendance = get_object_or_404(StudentAttendance, pk=pk)
        attendance.delete()
        return redirect('faculty:attendance_list')

         
class FacultyAttendanceProgressView(View):
    template_name = "faculty/faculty_attendance_progress.html"

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