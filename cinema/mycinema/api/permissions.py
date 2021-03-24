from rest_framework import permissions


class CustomCinemaHallUpdatePermisson(permissions.BasePermission):
    message = 'You cannot change which hall is occupied'

    def has_permission(self, request, view):
        if request.method in ['PATCH', 'PUT']:
            sessions = view.get_object().sessions.filter(status=True)
            if sessions:
                for session in sessions:
                    if session.session_tickets.first():
                        return False
        return True


class CustomSessionUpdatePermisson(permissions.BasePermission):
    message = 'You cannot change the session for which the ticket was purchased'

    def has_permission(self, request, view):
        if request.method in ['PATCH', 'PUT']:
            if view.get_object().session_tickets.first():
                return False
        return True