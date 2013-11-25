from django import template
from vcg.company_management.models import ConfigurationLogo
register = template.Library()

@register.filter
def file_name(value):
	return str(value).split('/')[-1]

@register.filter
def active_status(value):
	if value:
		status = "Active"
	else:
		status = "Inactive"
	return status

@register.filter
def company_logo(value):
	company_logo = ConfigurationLogo.objects.filter(company__sub_domain = value)
	if company_logo:
		company_logo_icon = company_logo[0]
		return company_logo_icon.logo
	else: 
		return None

@register.filter
def company_icon(value):
	company_logo = ConfigurationLogo.objects.filter(company__sub_domain = value)
	if company_logo:
		company_logo_icon = company_logo[0]
		return company_logo_icon.favicon
	else: 
		return None
