
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from mycinema.models import MyUser, CinemaHall, Session, Ticket


def change_status(modeladmin, request, queryset):
    for obj in queryset:
        obj.is_staff = not obj.is_staff
    MyUser.objects.bulk_update(queryset, ['is_staff'])


class MyUserAdmin(UserAdmin):
    actions = [change_status]
    fieldsets = (
        (_('Profile'), {'fields': ('username', 'password', 'total_price')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'total_price'),
        }),
    )


class CinemaHallAdmin(admin.ModelAdmin):
    fields = ('name', 'size')
    search_fields = ('name',)
    list_display = ('name', 'size')


class SessionAdmin(admin.ModelAdmin):
    exclude = ('show_date',)
    search_fields = ('price',)
    list_display = ('hall', 'show_date', 'price', 'status')
    list_filter = ('status',)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('customer', 'session', 'quantity')


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(CinemaHall, CinemaHallAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Ticket, TicketAdmin)