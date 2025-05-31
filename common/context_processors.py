from .models import Company

def company_info(request):
    try:
        company = Company.objects.get(is_active=True)
    except Company.DoesNotExist:
        company = None
    return {'common': {'company': company}} 