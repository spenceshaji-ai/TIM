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