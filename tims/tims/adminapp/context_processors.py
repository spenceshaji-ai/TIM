from tims.adminapp.models import LeaveApplication





def admin_leave_notifications(request):
    if request.user.is_authenticated and request.user.is_staff:
        pending_count = LeaveApplication.objects.filter(
            status="Pending"
        ).count()
    else:
        pending_count = 0

    return {
        "admin_pending_leave_count": pending_count
    }


def faculty_leave_notification(request):
    if request.user.is_authenticated and not request.user.is_staff:
        faculty_leave_update = LeaveApplication.objects.filter(
            user=request.user,
            status__in=["Approved", "Rejected"]
        ).exists()
    else:
        faculty_leave_update = False

    return {
        "faculty_leave_update": faculty_leave_update
    }
