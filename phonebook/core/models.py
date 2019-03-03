from django.db import models
from django.utils.text import slugify


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Наименование")
    organization_fk = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Вышестоящая организация")
    slug = models.SlugField(blank=True, unique=True, allow_unicode=True)
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.__str__(), allow_unicode=True)
            organizations = Organization.objects.filter(slug=self.name.lower()).values_list('id', flat=True)
            if len(organizations) > 0 and self.id not in organizations:
                slug = '%s-%s' % (slug, len(organizations))
            self.slug = slug
        super(Organization, self).save(*args, **kwargs)


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")
    department_fk = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Вышестоящий отдел")
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name


class OrgDepAssociation(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Организация")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Отдел")
    department_order = models.IntegerField(default=0, verbose_name="Порядковый номер")
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Связь отдела с организацией'
        verbose_name_plural = 'Связи отделов с организациями'

    def __str__(self):
        return '%s %s' % (self.organization.name, self.department.name)


class Position(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.name


class Employee(models.Model):
    surname = models.CharField(max_length=255, verbose_name="Фамилия")
    name = models.CharField(max_length=255, verbose_name="Имя")
    patronymic = models.CharField(max_length=255, verbose_name="Отчество")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Должность")
    org_dep_association = models.ForeignKey(OrgDepAssociation, on_delete=models.CASCADE, verbose_name="Отдел")
    slug = models.SlugField(blank=True, unique=True, allow_unicode=True)
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return "%s %s %s" % (self.surname, self.name, self.patronymic)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.__str__(), allow_unicode=True)
            employees = Employee.objects.filter(surname=self.surname,
                                                name=self.name,
                                                patronymic=self.patronymic).values_list('id', flat=True)
            if len(employees) > 0 and self.id not in employees:
                slug = '%s-%s' % (slug, len(employees))
            self.slug = slug
        super(Employee, self).save(*args, **kwargs)


class ContactType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")
    phonebook_display = models.BooleanField(default=True, verbose_name="Отображать в справочнике")
    phonebook_order = models.IntegerField(default=0, verbose_name="Порядковый номер")
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Тип контактных данных'
        verbose_name_plural = 'Типы контактных данных'

    def __str__(self):
        return self.name


class Contact(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Сотрудник")
    contact_type = models.ForeignKey(ContactType, on_delete=models.CASCADE, verbose_name="Тип контактных данных")
    data = models.CharField(max_length=255, verbose_name="Контактные данные")
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контактные данные'

    def __str__(self):
        return "%s %s" % (self.employee, self.contact_type.name)
