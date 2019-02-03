from django.contrib import admin
from .models import Organization, Department, OrgDepAssociation, Position, Employee, Contact, ContactType


class ContactAdmin(admin.ModelAdmin):
	list_display = ('employee', 'contact_type', 'data')


class ContactInline(admin.TabularInline):
    model = Contact


class EmployeeAdmin(admin.ModelAdmin):
    inlines = [
        ContactInline,
    ]


class ContactTypeAdmin(admin.ModelAdmin):
    inlines = [
        ContactInline,
    ]

admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(OrgDepAssociation)
admin.site.register(Position)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(ContactType, ContactTypeAdmin)
admin.site.register(Contact, ContactAdmin)
