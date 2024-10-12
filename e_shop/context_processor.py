from e_shop.models import *

def default(request):
    vendors = Vendor.objects.all()
    categories = Category.objects.all()
    try:
        address = Address.objects.get(user = request.user)
    except:
        address=None
    
    return {
        "categories": categories,
        "address": address,
        "vendors": vendors
    }
