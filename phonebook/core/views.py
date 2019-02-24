from django.shortcuts import redirect, render
from django.views import View
from .models import Organization, Department, OrgDepAssociation, Position, Employee, Contact, ContactType


def get_contacts(employee):
    contacts = Contact.objects.filter(employee__id=employee.id)
    contacts_dictionary = {i.contact_type.name: [] for i in contacts}
    for contact in contacts:
        contacts_dictionary[contact.contact_type.__str__()].append(contact.data)
    return contacts_dictionary


def get_phonebook(organization):
    contact_types = [value.__str__()
                     for value in ContactType.objects.filter(phonebook_display=True).order_by('phonebook_order')]
    department_key = Department._meta.verbose_name.title()
    employee_key = Employee._meta.verbose_name.title()
    header = [department_key, employee_key] + contact_types
    phonebook_content = []
    employees = Employee.objects.filter(org_dep_association__organization__id=organization.id)
    for employee in employees:
        contacts_dictionary = get_contacts(employee)
        employee_dictionary = {}
        employee_org_dep = OrgDepAssociation.objects.filter(id=employee.org_dep_association.id)
        department = None
        if employee_org_dep:
            department = Department.objects.filter(id=employee_org_dep[0].department.id)
        if department:
            employee_dictionary.update({department_key: department[0].name})
        employee_dictionary.update({employee_key: employee.__str__()})
        for key in header:
            if key in contacts_dictionary.keys():
                employee_dictionary.update({key: contacts_dictionary[key]})
        phonebook_content.append(employee_dictionary)
    return {'phonebook_header': header, 'phonebook_content': phonebook_content}


class PhonebookView(View):
    def get(self, request, *args, **kwargs):
        organizations = Organization.objects.all()
        context = {'organizations': organizations}
        if 'slug' in kwargs:
            organization = Organization.objects.filter(slug=kwargs['slug'])
        if organization:
            phonebook = get_phonebook(organization[0])
            context.update({'phonebook': phonebook})
        return render(request, 'phonebook.html', context)
