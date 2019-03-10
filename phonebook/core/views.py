from django.shortcuts import redirect, render
from django.views import View
from .models import Organization, Department, OrgDepAssociation, Position, Employee, Contact, ContactType
from collections import defaultdict


def get_contacts(employee):
    contacts = Contact.objects.filter(employee__id=employee.id)
    contacts_dictionary = {i.contact_type.name: [] for i in contacts}
    for contact in contacts:
        contacts_dictionary[contact.contact_type.__str__()].append(contact.data)
    return contacts_dictionary


class Phonebook:
    def __init__(self):
        self.department_key = Department._meta.verbose_name.title()
        self.position_key = Position._meta.verbose_name.title()
        self.employee_key = Employee._meta.verbose_name.title()
        self.employees_key = Employee._meta.verbose_name_plural.title()
        self.header = self.__update_header()
        self.content = []

    def __update_header(self):
        contact_types = [value.__str__()
                         for value in ContactType.objects.filter(phonebook_display=True).order_by('phonebook_order')]
        return [self.position_key, self.employee_key] + contact_types

    def get_phonebook(self, organization):
        org_deps = OrgDepAssociation.objects.filter(organization=organization).order_by('phonebook_order')
        for org_dep in org_deps:
            department = Department.objects.get(id=org_dep.department.id)
            employees = Employee.objects.filter(org_dep_association=org_dep).order_by('phonebook_order')
            data = defaultdict(list)
            data[self.department_key] = department.name
            for employee in employees:
                contacts = get_contacts(employee)
                employee_dict = defaultdict(dict)
                employee_dict.update({self.position_key: employee.position})
                employee_dict.update({self.employee_key: employee})
                for key in self.header:
                    if key in contacts.keys():
                        employee_dict.update({key: contacts[key]})
                    elif key not in employee_dict.keys():
                        employee_dict.update({key: ''})
                data[self.employees_key].append(dict(employee_dict))
            self.content.append(dict(data))
        return {'phonebook_header': self.header, 'phonebook_content': self.content,
                'department_key': self.department_key, 'employee_key': self.employee_key,
                'position_key': self.position_key}


class PhonebookView(View):
    def get(self, request, *args, **kwargs):
        organizations = Organization.objects.all()
        context = {'organizations': organizations}
        if 'slug' in kwargs:
            organization = Organization.objects.filter(slug=kwargs['slug'])
            if organization:
                organization = organization[0]
        else:
            organization = Organization.objects.all()[0]
        if organization:
            phonebook = Phonebook().get_phonebook(organization)
            context.update(phonebook)
        return render(request, 'phonebook.html', context)
