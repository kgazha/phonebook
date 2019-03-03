from django.shortcuts import redirect, render
from django.views import View
from .models import Organization, Department, OrgDepAssociation, Position, Employee, Contact, ContactType


def get_contacts(employee):
    contacts = Contact.objects.filter(employee__id=employee.id)
    contacts_dictionary = {i.contact_type.name: [] for i in contacts}
    for contact in contacts:
        contacts_dictionary[contact.contact_type.__str__()].append(contact.data)
    return contacts_dictionary


class Phonebook:
    def __init__(self):
        self.department_key = Department._meta.verbose_name.title()
        self.employee_key = Employee._meta.verbose_name.title()
        self.header = self.__update_header()
        self.content = []

    def __update_header(self):
        contact_types = [value.__str__()
                         for value in ContactType.objects.filter(phonebook_display=True).order_by('phonebook_order')]
        return [self.department_key, self.employee_key] + contact_types

    def get_phonebook(self, organization):
        org_deps = OrgDepAssociation.objects.filter(organization=organization)
        for org_dep in org_deps:
            department = Department.objects.get(id=org_dep.department.id)
            employees = Employee.objects.filter(org_dep_association=org_dep)
            for employee in employees:
                contacts = get_contacts(employee)
                data = {self.department_key: department.name,
                        self.employee_key: employee}
                for key in self.header:
                    if key in contacts.keys():
                        data.update({key: contacts[key]})
                    elif key not in data.keys():
                        data.update({key: None})
                self.content.append(data)
        return {'phonebook_header': self.header, 'phonebook_content': self.content}


class PhonebookView(View):
    def get(self, request, *args, **kwargs):
        organizations = Organization.objects.all()
        context = {'organizations': organizations}
        if 'slug' in kwargs:
            organization = Organization.objects.filter(slug=kwargs['slug'])
        if organization:
            phonebook = Phonebook().get_phonebook(organization[0])
            context.update({'phonebook': phonebook})
        return render(request, 'phonebook.html', context)
