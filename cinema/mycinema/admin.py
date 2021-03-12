from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from mycinema.models import MyUser, CinemaHall, Session, Ticket

admin.site.register(MyUser, UserAdmin)
admin.site.register(CinemaHall)
admin.site.register(Session)
admin.site.register(Ticket)
