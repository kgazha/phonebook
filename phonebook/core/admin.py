from django.contrib import admin
from .models import Organization, Department, OrgDepAssociation, Position, Employee, Contact, ContactType


class ContactAdmin(admin.ModelAdmin):
	list_display = ('employee', 'contact_type', 'data')


class ContactInline(admin.TabularInline):
    model = Contact


class EmployeeAdmin(admin.ModelAdmin):
    # def organization_name(self, obj):
        # return obj.org_dep_association.organization

    # autocomplete_fields  = ['org_dep_association']
    # list_display = ('surname', 'name', 'patronymic', 'position', 'organization_name')
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
