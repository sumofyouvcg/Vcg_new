from datetime import date

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from vcg.admin_management.models import Company
from vcg.utilities import Email
from vcg.config import mail
        
class Command(BaseCommand):
    args = '<vendor_id vendor_id ...>'
    def handle(self, *args, **options):
        currentdate = date.today()
        companys = Company.objects.all()
        for company in companys:
            if company.expiry_date  < currentdate or company.from_date  > currentdate:
                Company.objects.filter(company_number = company.company_number).update(active = False)
                User.objects.filter(username = company.company_number).update(is_staff = False, is_active = False)
                Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_DEACTIVATION_MSG %(company.company_name), [company.email], "html")
            elif (company.from_date  == currentdate) and company.expiry_date  > currentdate:
                Company.objects.filter(company_number = company.company_number).update(active = True)
                User.objects.filter(username = company.company_number).update(is_staff = True, is_active = True)
                Email().send_email(mail.USER_CREATION_SUBJECT, mail.USER_ACTIVATION_MSG %(company.company_name), [company.email], "html")