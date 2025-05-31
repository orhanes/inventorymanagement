from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Unit, TaxRates, Company, AddressType, Currency, OfferStatus, SubCategory, Department, Position, BankType, Bank, PaymentType, PaymentMethod, DeliveryType, DeliveryCompany, VehicleType, VehicleBrand, VehicleModel
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

@login_required
def company_settings(request):
    # Eğer firma bilgisi yoksa yeni oluştur, varsa mevcut bilgileri getir
    company, created = Company.objects.get_or_create(is_active=True)
    
    if request.method == 'POST':
        company.name = request.POST.get('name')
        company.address = request.POST.get('address')
        company.phone = request.POST.get('phone')
        company.web = request.POST.get('web')
        company.email = request.POST.get('email')
        company.tax_administration = request.POST.get('tax_administration')
        company.tax_id = request.POST.get('tax_id')
        company.kep_address = request.POST.get('kep_address')
        company.bank_name = request.POST.get('bank_name')
        company.iban_no = request.POST.get('iban_no')
        company.branch_code = request.POST.get('branch_code')
        company.account_number = request.POST.get('account_number')
        
        # Logo yükleme işlemi
        if 'logo' in request.FILES:
            company.logo = request.FILES['logo']
        
        company.save()
        messages.success(request, 'Firma bilgileri başarıyla güncellendi!')
        return redirect('company_settings')
    
    return render(request, 'common/company_settings.html', {
        'title': 'Firma Bilgileri',
        'company': company
    })

@login_required
def category_list(request):
    categories = Category.objects.filter(is_deleted=False).order_by('-created_at')
    paginator = Paginator(categories, 10)  # Her sayfada 10 kayıt göster
    
    page = request.GET.get('page')
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)
        
    return render(request, 'common/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if Category.objects.filter(name=name, is_deleted=False).exists():
            messages.error(request, 'Bu kategori zaten mevcut!')
            return redirect('category_list')
        
        Category.objects.create(name=name)
        messages.success(request, 'Kategori başarıyla oluşturuldu!')
        return redirect('category_list')
    
    return render(request, 'common/category_form.html', {'title': 'Yeni Kategori'})

@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if Category.objects.filter(name=name, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu kategori zaten mevcut!')
            return redirect('category_list')
        
        category.name = name
        category.save()
        messages.success(request, 'Kategori başarıyla güncellendi!')
        return redirect('category_list')
    
    return render(request, 'common/category_form.html', {'title': 'Kategori Düzenle', 'category': category})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.is_deleted = True
    category.save()
    messages.success(request, 'Kategori başarıyla silindi!')
    return redirect('category_list')

@login_required
def subcategory_list(request):
    subcategories = SubCategory.objects.filter(is_deleted=False).select_related('category').order_by('category__name', 'name')
    paginator = Paginator(subcategories, 15)  # Her sayfada 15 kayıt göster
    
    page = request.GET.get('page')
    try:
        subcategories = paginator.page(page)
    except PageNotAnInteger:
        subcategories = paginator.page(1)
    except EmptyPage:
        subcategories = paginator.page(paginator.num_pages)
        
    return render(request, 'common/subcategory_list.html', {'subcategories': subcategories})

@login_required
def subcategory_create(request):
    categories = Category.objects.filter(is_deleted=False)
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        if SubCategory.objects.filter(name=name, category_id=category_id, is_deleted=False).exists():
            messages.error(request, 'Bu alt kategori zaten mevcut!')
            return redirect('subcategory_list')
        SubCategory.objects.create(name=name, category_id=category_id)
        messages.success(request, 'Alt kategori başarıyla oluşturuldu!')
        return redirect('subcategory_list')
    return render(request, 'common/subcategory_form.html', {'title': 'Yeni Alt Kategori', 'categories': categories})

@login_required
def subcategory_edit(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    categories = Category.objects.filter(is_deleted=False)
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        if SubCategory.objects.filter(name=name, category_id=category_id, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu alt kategori zaten mevcut!')
            return redirect('subcategory_list')
        subcategory.name = name
        subcategory.category_id = category_id
        subcategory.save()
        messages.success(request, 'Alt kategori başarıyla güncellendi!')
        return redirect('subcategory_list')
    return render(request, 'common/subcategory_form.html', {'title': 'Alt Kategori Düzenle', 'subcategory': subcategory, 'categories': categories})

@login_required
def subcategory_delete(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    subcategory.is_deleted = True
    subcategory.save()
    messages.success(request, 'Alt kategori başarıyla silindi!')
    return redirect('subcategory_list')

@login_required
def unit_list(request):
    units = Unit.objects.filter(is_deleted=False).order_by('name')
    paginator = Paginator(units, 15)  # Her sayfada 15 kayıt göster
    
    page = request.GET.get('page')
    try:
        units = paginator.page(page)
    except PageNotAnInteger:
        units = paginator.page(1)
    except EmptyPage:
        units = paginator.page(paginator.num_pages)
        
    return render(request, 'common/unit_list.html', {'units': units})

@login_required
def unit_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if Unit.objects.filter(name=name, is_deleted=False).exists():
            messages.error(request, 'Bu birim zaten mevcut!')
            return redirect('unit_list')
        
        Unit.objects.create(name=name)
        messages.success(request, 'Birim başarıyla oluşturuldu!')
        return redirect('unit_list')
    
    return render(request, 'common/unit_form.html', {'title': 'Yeni Birim'})

@login_required
def unit_edit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if Unit.objects.filter(name=name, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu birim zaten mevcut!')
            return redirect('unit_list')
        
        unit.name = name
        unit.save()
        messages.success(request, 'Birim başarıyla güncellendi!')
        return redirect('unit_list')
    
    return render(request, 'common/unit_form.html', {'title': 'Birim Düzenle', 'unit': unit})

@login_required
def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    unit.is_deleted = True
    unit.save()
    messages.success(request, 'Birim başarıyla silindi!')
    return redirect('unit_list')

@login_required
def tax_rate_list(request):
    tax_rates = TaxRates.objects.filter(is_deleted=False).order_by('name')
    paginator = Paginator(tax_rates, 10)  # Her sayfada 10 kayıt göster
    
    page = request.GET.get('page')
    try:
        tax_rates = paginator.page(page)
    except PageNotAnInteger:
        tax_rates = paginator.page(1)
    except EmptyPage:
        tax_rates = paginator.page(paginator.num_pages)
        
    return render(request, 'common/tax_rate_list.html', {'tax_rates': tax_rates})

@login_required
def tax_rate_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        rate = request.POST.get('rate')
        is_active = request.POST.get('is_active') == 'on'
        
        if TaxRates.objects.filter(name=name, is_deleted=False).exists():
            messages.error(request, 'Bu vergi oranı zaten mevcut!')
            return redirect('tax_rate_list')
        
        TaxRates.objects.create(name=name, rate=rate, is_active=is_active)
        messages.success(request, 'Vergi oranı başarıyla oluşturuldu!')
        return redirect('tax_rate_list')
    
    return render(request, 'common/tax_rate_form.html', {'title': 'Yeni Vergi Oranı'})

@login_required
def tax_rate_edit(request, pk):
    tax_rate = get_object_or_404(TaxRates, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        rate = request.POST.get('rate')
        is_active = request.POST.get('is_active') == 'on'
        
        if TaxRates.objects.filter(name=name, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu vergi oranı zaten mevcut!')
            return redirect('tax_rate_list')
        
        tax_rate.name = name
        tax_rate.rate = rate
        tax_rate.is_active = is_active
        tax_rate.save()
        messages.success(request, 'Vergi oranı başarıyla güncellendi!')
        return redirect('tax_rate_list')
    
    return render(request, 'common/tax_rate_form.html', {'title': 'Vergi Oranı Düzenle', 'tax_rate': tax_rate})

@login_required
def tax_rate_delete(request, pk):
    tax_rate = get_object_or_404(TaxRates, pk=pk)
    tax_rate.is_deleted = True
    tax_rate.save()
    messages.success(request, 'Vergi oranı başarıyla silindi!')
    return redirect('tax_rate_list')

@login_required
def address_type_list(request):
    address_types = AddressType.objects.filter(is_deleted=False).order_by('name')
    paginator = Paginator(address_types, 15)  # Her sayfada 15 kayıt göster
    
    page = request.GET.get('page')
    try:
        address_types = paginator.page(page)
    except PageNotAnInteger:
        address_types = paginator.page(1)
    except EmptyPage:
        address_types = paginator.page(paginator.num_pages)
        
    return render(request, 'common/address_type_list.html', {'address_types': address_types})

@login_required
def address_type_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if AddressType.objects.filter(name=name, is_deleted=False).exists():
            messages.error(request, 'Bu adres tipi zaten mevcut!')
            return redirect('address_type_list')
        
        AddressType.objects.create(name=name)
        messages.success(request, 'Adres tipi başarıyla oluşturuldu!')
        return redirect('address_type_list')
    
    return render(request, 'common/address_type_form.html', {'title': 'Yeni Adres Tipi'})

@login_required
def address_type_edit(request, pk):
    address_type = get_object_or_404(AddressType, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if AddressType.objects.filter(name=name, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu adres tipi zaten mevcut!')
            return redirect('address_type_list')
        
        address_type.name = name
        address_type.description = description
        address_type.is_active = is_active
        address_type.save()
        
        messages.success(request, 'Adres tipi başarıyla güncellendi!')
        return redirect('address_type_list')
    
    return render(request, 'common/address_type_form.html', {'title': 'Adres Tipi Düzenle', 'address_type': address_type})

@login_required
def address_type_delete(request, pk):
    address_type = get_object_or_404(AddressType, pk=pk)
    address_type.is_deleted = True
    address_type.save()
    messages.success(request, 'Adres tipi başarıyla silindi!')
    return redirect('address_type_list')

@login_required
def department_list(request):
    departments = Department.objects.filter(is_deleted=False)
    paginator = Paginator(departments, 20)
    page = request.GET.get('page')
    try:
        departments = paginator.page(page)
    except PageNotAnInteger:
        departments = paginator.page(1)
    except EmptyPage:
        departments = paginator.page(paginator.num_pages)
    return render(request, 'common/department_list.html', {'departments': departments})

@login_required
def department_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if Department.objects.filter(name=name, is_deleted=False).exists():
            messages.error(request, 'Bu departman zaten mevcut!')
            return redirect('department_list')
        
        Department.objects.create(name=name)
        messages.success(request, 'Departman başarıyla oluşturuldu!')
        return redirect('department_list')
    
    return render(request, 'common/department_form.html', {'title': 'Yeni Departman'})

@login_required
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if Department.objects.filter(name=name, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu departman zaten mevcut!')
            return redirect('department_list')
        
        department.name = name
        department.save()
        messages.success(request, 'Departman başarıyla güncellendi!')
        return redirect('department_list')
    
    return render(request, 'common/department_form.html', {'title': 'Departman Düzenle', 'department': department})

@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.is_deleted = True
    department.save()
    messages.success(request, 'Departman başarıyla silindi!')
    return redirect('department_list')

@login_required
def position_list(request):
    positions = Position.objects.filter(is_deleted=False).select_related('department')
    paginator = Paginator(positions, 20)
    page = request.GET.get('page')
    try:
        positions = paginator.page(page)
    except PageNotAnInteger:
        positions = paginator.page(1)
    except EmptyPage:
        positions = paginator.page(paginator.num_pages)
    return render(request, 'common/position_list.html', {'positions': positions})

@login_required
def position_create(request):
    departments = Department.objects.filter(is_deleted=False)
    if request.method == 'POST':
        name = request.POST.get('name')
        department_id = request.POST.get('department')
        if Position.objects.filter(name=name, department_id=department_id, is_deleted=False).exists():
            messages.error(request, 'Bu pozisyon zaten mevcut!')
            return redirect('position_list')
        Position.objects.create(name=name, department_id=department_id)
        messages.success(request, 'Pozisyon başarıyla oluşturuldu!')
        return redirect('position_list')
    return render(request, 'common/position_form.html', {'title': 'Yeni Pozisyon', 'departments': departments})

@login_required
def position_edit(request, pk):
    position = get_object_or_404(Position, pk=pk)
    departments = Department.objects.filter(is_deleted=False)
    if request.method == 'POST':
        name = request.POST.get('name')
        department_id = request.POST.get('department')
        if Position.objects.filter(name=name, department_id=department_id, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu pozisyon zaten mevcut!')
            return redirect('position_list')
        position.name = name
        position.department_id = department_id
        position.save()
        messages.success(request, 'Pozisyon başarıyla güncellendi!')
        return redirect('position_list')
    return render(request, 'common/position_form.html', {'title': 'Pozisyon Düzenle', 'position': position, 'departments': departments})

@login_required
def position_delete(request, pk):
    position = get_object_or_404(Position, pk=pk)
    position.is_deleted = True
    position.save()
    messages.success(request, 'Pozisyon başarıyla silindi!')
    return redirect('position_list')

@login_required
def bank_type_list(request):
    bank_types = BankType.objects.filter(is_deleted=False).order_by('-created_at')
    paginator = Paginator(bank_types, 10)  # Her sayfada 10 kayıt göster
    
    page = request.GET.get('page')
    try:
        bank_types = paginator.page(page)
    except PageNotAnInteger:
        bank_types = paginator.page(1)
    except EmptyPage:
        bank_types = paginator.page(paginator.num_pages)
        
    return render(request, 'common/bank_type_list.html', {'bank_types': bank_types})

@login_required
def bank_type_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if BankType.objects.filter(name=name, is_deleted=False).exists():
            messages.error(request, 'Bu banka türü zaten mevcut!')
            return redirect('bank_type_list')
        
        BankType.objects.create(name=name)
        messages.success(request, 'Banka türü başarıyla oluşturuldu!')
        return redirect('bank_type_list')
    
    return render(request, 'common/bank_type_form.html', {'title': 'Yeni Banka Türü'})

@login_required
def bank_type_edit(request, pk):
    bank_type = get_object_or_404(BankType, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if BankType.objects.filter(name=name, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu banka türü zaten mevcut!')
            return redirect('bank_type_list')
        
        bank_type.name = name
        bank_type.save()
        messages.success(request, 'Banka türü başarıyla güncellendi!')
        return redirect('bank_type_list')
    
    return render(request, 'common/bank_type_form.html', {'title': 'Banka Türü Düzenle', 'bank_type': bank_type})

@login_required
def bank_type_delete(request, pk):
    bank_type = get_object_or_404(BankType, pk=pk)
    bank_type.is_deleted = True
    bank_type.save()
    messages.success(request, 'Banka türü başarıyla silindi!')
    return redirect('bank_type_list')

@login_required
def bank_list(request):
    banks = Bank.objects.filter(is_deleted=False).select_related('bank_type').order_by('name')
    paginator = Paginator(banks, 15)  # Her sayfada 10 kayıt göster
    
    page = request.GET.get('page')
    try:
        banks = paginator.page(page)
    except PageNotAnInteger:
        banks = paginator.page(1)
    except EmptyPage:
        banks = paginator.page(paginator.num_pages)
        
    return render(request, 'common/bank_list.html', {'banks': banks})

@login_required
def bank_create(request):
    bank_types = BankType.objects.filter(is_deleted=False)
    if request.method == 'POST':
        name = request.POST.get('name')
        bank_type_id = request.POST.get('bank_type')
        eft_code = request.POST.get('eft_code')
        phone = request.POST.get('phone')
        fax = request.POST.get('fax')
        customer_service = request.POST.get('customer_service')
        email = request.POST.get('email')
        address = request.POST.get('address')
        website = request.POST.get('website')
        
        if Bank.objects.filter(name=name, is_deleted=False).exists():
            messages.error(request, 'Bu banka zaten mevcut!')
            return redirect('bank_list')
        
        bank = Bank.objects.create(
            name=name,
            bank_type_id=bank_type_id,
            eft_code=eft_code,
            phone=phone,
            fax=fax,
            customer_service=customer_service,
            email=email,
            address=address,
            website=website
        )
        
        if 'logo' in request.FILES:
            bank.logo = request.FILES['logo']
            bank.save()
        
        messages.success(request, 'Banka başarıyla oluşturuldu!')
        return redirect('bank_list')
    
    return render(request, 'common/bank_form.html', {
        'title': 'Yeni Banka',
        'bank_types': bank_types
    })

@login_required
def bank_edit(request, pk):
    bank = get_object_or_404(Bank, pk=pk)
    bank_types = BankType.objects.filter(is_deleted=False)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        bank_type_id = request.POST.get('bank_type')
        eft_code = request.POST.get('eft_code')
        phone = request.POST.get('phone')
        fax = request.POST.get('fax')
        customer_service = request.POST.get('customer_service')
        email = request.POST.get('email')
        address = request.POST.get('address')
        website = request.POST.get('website')
        
        if Bank.objects.filter(name=name, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu banka zaten mevcut!')
            return redirect('bank_list')
        
        bank.name = name
        bank.bank_type_id = bank_type_id
        bank.eft_code = eft_code
        bank.phone = phone
        bank.fax = fax
        bank.customer_service = customer_service
        bank.email = email
        bank.address = address
        bank.website = website
        
        if 'logo' in request.FILES:
            bank.logo = request.FILES['logo']
        
        bank.save()
        messages.success(request, 'Banka başarıyla güncellendi!')
        return redirect('bank_list')
    
    return render(request, 'common/bank_form.html', {
        'title': 'Banka Düzenle',
        'bank': bank,
        'bank_types': bank_types
    })

@login_required
def bank_delete(request, pk):
    bank = get_object_or_404(Bank, pk=pk)
    bank.is_deleted = True
    bank.save()
    messages.success(request, 'Banka başarıyla silindi!')
    return redirect('bank_list')

@login_required
def currency_list(request):
    currencies = Currency.objects.all().order_by('name')
    paginator = Paginator(currencies, 20)  # Her sayfada 20 kayıt
    page = request.GET.get('page')
    try:
        currencies = paginator.page(page)
    except PageNotAnInteger:
        currencies = paginator.page(1)
    except EmptyPage:
        currencies = paginator.page(paginator.num_pages)
    return render(request, 'common/currency_list.html', {'currencies': currencies})

@login_required
def currency_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        symbol = request.POST.get('symbol')
        
        if Currency.objects.filter(name=name).exists():
            messages.error(request, 'Bu para birimi adı zaten mevcut!')
            return redirect('currency_list')
        
        if Currency.objects.filter(code=code).exists():
            messages.error(request, 'Bu para birimi kodu zaten mevcut!')
            return redirect('currency_list')
        
        Currency.objects.create(name=name, code=code, symbol=symbol)
        messages.success(request, 'Para birimi başarıyla oluşturuldu!')
        return redirect('currency_list')
    
    return render(request, 'common/currency_form.html', {'title': 'Yeni Para Birimi'})

@login_required
def currency_edit(request, pk):
    currency = get_object_or_404(Currency, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        symbol = request.POST.get('symbol')
        
        if Currency.objects.filter(name=name).exclude(pk=pk).exists():
            messages.error(request, 'Bu para birimi adı zaten mevcut!')
            return redirect('currency_list')
        
        if Currency.objects.filter(code=code).exclude(pk=pk).exists():
            messages.error(request, 'Bu para birimi kodu zaten mevcut!')
            return redirect('currency_list')
        
        currency.name = name
        currency.code = code
        currency.symbol = symbol
        currency.save()
        messages.success(request, 'Para birimi başarıyla güncellendi!')
        return redirect('currency_list')
    
    return render(request, 'common/currency_form.html', {'title': 'Para Birimi Düzenle', 'currency': currency})

@login_required
def currency_delete(request, pk):
    currency = get_object_or_404(Currency, pk=pk)
    currency.delete()
    messages.success(request, 'Para birimi başarıyla silindi!')
    return redirect('currency_list')

@login_required
def payment_type_list(request):
    payment_types = PaymentType.objects.filter(is_deleted=False).order_by('name')
    paginator = Paginator(payment_types, 20)  # Her sayfada 20 kayıt
    page = request.GET.get('page')
    try:
        payment_types = paginator.page(page)
    except PageNotAnInteger:
        payment_types = paginator.page(1)
    except EmptyPage:
        payment_types = paginator.page(paginator.num_pages)
    return render(request, 'common/payment_type_list.html', {'payment_types': payment_types})

@login_required
def payment_type_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if PaymentType.objects.filter(name=name, is_deleted=False).exists():
            messages.error(request, 'Bu ödeme türü zaten mevcut!')
            return redirect('payment_type_list')
        
        PaymentType.objects.create(name=name)
        messages.success(request, 'Ödeme türü başarıyla oluşturuldu!')
        return redirect('payment_type_list')
    
    return render(request, 'common/payment_type_form.html', {'title': 'Yeni Ödeme Türü'})

@login_required
def payment_type_edit(request, pk):
    payment_type = get_object_or_404(PaymentType, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if PaymentType.objects.filter(name=name, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu ödeme türü zaten mevcut!')
            return redirect('payment_type_list')
        
        payment_type.name = name
        payment_type.save()
        messages.success(request, 'Ödeme türü başarıyla güncellendi!')
        return redirect('payment_type_list')
    
    return render(request, 'common/payment_type_form.html', {'title': 'Ödeme Türü Düzenle', 'payment_type': payment_type})

@login_required
def payment_type_delete(request, pk):
    payment_type = get_object_or_404(PaymentType, pk=pk)
    payment_type.is_deleted = True
    payment_type.save()
    messages.success(request, 'Ödeme türü başarıyla silindi!')
    return redirect('payment_type_list')

@login_required
def payment_method_list(request):
    payment_methods = PaymentMethod.objects.filter(is_deleted=False).order_by('name')
    paginator = Paginator(payment_methods, 20)  # Her sayfada 20 kayıt
    page = request.GET.get('page')
    try:
        payment_methods = paginator.page(page)
    except PageNotAnInteger:
        payment_methods = paginator.page(1)
    except EmptyPage:
        payment_methods = paginator.page(paginator.num_pages)
    return render(request, 'common/payment_method_list.html', {'payment_methods': payment_methods})

@login_required
def payment_method_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if PaymentMethod.objects.filter(name=name, is_deleted=False).exists():
            messages.error(request, 'Bu ödeme yöntemi zaten mevcut!')
            return redirect('payment_method_list')
        
        PaymentMethod.objects.create(name=name)
        messages.success(request, 'Ödeme yöntemi başarıyla oluşturuldu!')
        return redirect('payment_method_list')
    
    return render(request, 'common/payment_method_form.html', {'title': 'Yeni Ödeme Yöntemi'})

@login_required
def payment_method_edit(request, pk):
    payment_method = get_object_or_404(PaymentMethod, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if PaymentMethod.objects.filter(name=name, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu ödeme yöntemi zaten mevcut!')
            return redirect('payment_method_list')
        
        payment_method.name = name
        payment_method.save()
        messages.success(request, 'Ödeme yöntemi başarıyla güncellendi!')
        return redirect('payment_method_list')
    
    return render(request, 'common/payment_method_form.html', {'title': 'Ödeme Yöntemi Düzenle', 'payment_method': payment_method})

@login_required
def payment_method_delete(request, pk):
    payment_method = get_object_or_404(PaymentMethod, pk=pk)
    payment_method.is_deleted = True
    payment_method.save()
    messages.success(request, 'Ödeme yöntemi başarıyla silindi!')
    return redirect('payment_method_list')

@login_required
def delivery_type_list(request):
    delivery_types = DeliveryType.objects.filter(is_deleted=False).order_by('name')
    paginator = Paginator(delivery_types, 20)  # Her sayfada 20 kayıt
    page = request.GET.get('page')
    try:
        delivery_types = paginator.page(page)
    except PageNotAnInteger:
        delivery_types = paginator.page(1)
    except EmptyPage:
        delivery_types = paginator.page(paginator.num_pages)
    return render(request, 'common/delivery_type_list.html', {'delivery_types': delivery_types})

@login_required
def delivery_type_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if DeliveryType.objects.filter(name=name, is_deleted=False).exists():
            messages.error(request, 'Bu nakliye türü zaten mevcut!')
            return redirect('delivery_type_list')
        
        DeliveryType.objects.create(
            name=name,
            description=description,
            is_active=is_active
        )
        messages.success(request, 'Nakliye türü başarıyla oluşturuldu!')
        return redirect('delivery_type_list')
    
    return render(request, 'common/delivery_type_form.html', {'title': 'Yeni Nakliye Türü'})

@login_required
def delivery_type_edit(request, pk):
    delivery_type = get_object_or_404(DeliveryType, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if DeliveryType.objects.filter(name=name, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu nakliye türü zaten mevcut!')
            return redirect('delivery_type_list')
        
        delivery_type.name = name
        delivery_type.description = description
        delivery_type.is_active = is_active
        delivery_type.save()
        messages.success(request, 'Nakliye türü başarıyla güncellendi!')
        return redirect('delivery_type_list')
    
    return render(request, 'common/delivery_type_form.html', {
        'title': 'Nakliye Türü Düzenle',
        'delivery_type': delivery_type
    })

@login_required
def delivery_type_delete(request, pk):
    delivery_type = get_object_or_404(DeliveryType, pk=pk)
    delivery_type.is_deleted = True
    delivery_type.save()
    messages.success(request, 'Nakliye türü başarıyla silindi!')
    return redirect('delivery_type_list')

@login_required
def delivery_company_list(request):
    delivery_companies = DeliveryCompany.objects.filter(is_deleted=False).order_by('name')
    paginator = Paginator(delivery_companies, 20)  # Her sayfada 20 kayıt
    page = request.GET.get('page')
    try:
        delivery_companies = paginator.page(page)
    except PageNotAnInteger:
        delivery_companies = paginator.page(1)
    except EmptyPage:
        delivery_companies = paginator.page(paginator.num_pages)
    return render(request, 'common/delivery_company_list.html', {'delivery_companies': delivery_companies})

@login_required
def delivery_company_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone', '')
        fax = request.POST.get('fax', '')
        customer_service = request.POST.get('customer_service', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        website = request.POST.get('website', '')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if DeliveryCompany.objects.filter(name=name, is_deleted=False).exists():
            messages.error(request, 'Bu nakliye firması zaten mevcut!')
            return redirect('delivery_company_list')
        
        delivery_company = DeliveryCompany.objects.create(
            name=name,
            phone=phone,
            fax=fax,
            customer_service=customer_service,
            email=email,
            address=address,
            website=website,
            description=description,
            is_active=is_active
        )
        
        if 'logo' in request.FILES:
            delivery_company.logo = request.FILES['logo']
            delivery_company.save()
        
        messages.success(request, 'Nakliye firması başarıyla oluşturuldu!')
        return redirect('delivery_company_list')
    
    return render(request, 'common/delivery_company_form.html', {'title': 'Yeni Nakliye Firması'})

@login_required
def delivery_company_edit(request, pk):
    delivery_company = get_object_or_404(DeliveryCompany, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone', '')
        fax = request.POST.get('fax', '')
        customer_service = request.POST.get('customer_service', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        website = request.POST.get('website', '')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if DeliveryCompany.objects.filter(name=name, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu nakliye firması zaten mevcut!')
            return redirect('delivery_company_list')
        
        delivery_company.name = name
        delivery_company.phone = phone
        delivery_company.fax = fax
        delivery_company.customer_service = customer_service
        delivery_company.email = email
        delivery_company.address = address
        delivery_company.website = website
        delivery_company.description = description
        delivery_company.is_active = is_active
        
        if 'logo' in request.FILES:
            delivery_company.logo = request.FILES['logo']
        
        delivery_company.save()
        messages.success(request, 'Nakliye firması başarıyla güncellendi!')
        return redirect('delivery_company_list')
    
    return render(request, 'common/delivery_company_form.html', {
        'title': 'Nakliye Firması Düzenle',
        'delivery_company': delivery_company
    })

@login_required
def delivery_company_delete(request, pk):
    delivery_company = get_object_or_404(DeliveryCompany, pk=pk)
    delivery_company.is_deleted = True
    delivery_company.save()
    messages.success(request, 'Nakliye firması başarıyla silindi!')
    return redirect('delivery_company_list')

@login_required
def vehicle_type_list(request):
    vehicle_types = VehicleType.objects.filter(is_deleted=False).order_by('name')
    paginator = Paginator(vehicle_types, 15)  # Her sayfada 15 kayıt göster
    
    page = request.GET.get('page')
    try:
        vehicle_types = paginator.page(page)
    except PageNotAnInteger:
        vehicle_types = paginator.page(1)
    except EmptyPage:
        vehicle_types = paginator.page(paginator.num_pages)
        
    return render(request, 'common/vehicle_type_list.html', {'vehicle_types': vehicle_types})

@login_required
def vehicle_type_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if VehicleType.objects.filter(name=name, is_deleted=False).exists():
            messages.error(request, 'Bu araç tipi zaten mevcut!')
            return redirect('vehicle_type_list')
        
        VehicleType.objects.create(
            name=name,
            description=description,
            is_active=is_active
        )
        messages.success(request, 'Araç tipi başarıyla oluşturuldu!')
        return redirect('vehicle_type_list')
    
    return render(request, 'common/vehicle_type_form.html', {'title': 'Yeni Araç Tipi'})

@login_required
def vehicle_type_edit(request, pk):
    vehicle_type = get_object_or_404(VehicleType, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if VehicleType.objects.filter(name=name, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu araç tipi zaten mevcut!')
            return redirect('vehicle_type_list')
        
        vehicle_type.name = name
        vehicle_type.description = description
        vehicle_type.is_active = is_active
        vehicle_type.save()
        messages.success(request, 'Araç tipi başarıyla güncellendi!')
        return redirect('vehicle_type_list')
    
    return render(request, 'common/vehicle_type_form.html', {
        'title': 'Araç Tipi Düzenle',
        'vehicle_type': vehicle_type
    })

@login_required
def vehicle_type_delete(request, pk):
    vehicle_type = get_object_or_404(VehicleType, pk=pk)
    vehicle_type.is_deleted = True
    vehicle_type.save()
    messages.success(request, 'Araç tipi başarıyla silindi!')
    return redirect('vehicle_type_list')

@login_required
def vehicle_brand_list(request):
    vehicle_brands = VehicleBrand.objects.filter(is_deleted=False).select_related('vehicle_type').order_by('vehicle_type__name', 'name')
    paginator = Paginator(vehicle_brands, 15)  # Her sayfada 15 kayıt göster
    
    page = request.GET.get('page')
    try:
        vehicle_brands = paginator.page(page)
    except PageNotAnInteger:
        vehicle_brands = paginator.page(1)
    except EmptyPage:
        vehicle_brands = paginator.page(paginator.num_pages)
        
    return render(request, 'common/vehicle_brand_list.html', {'vehicle_brands': vehicle_brands})

@login_required
def vehicle_brand_create(request):
    vehicle_types = VehicleType.objects.filter(is_deleted=False, is_active=True)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        vehicle_type_id = request.POST.get('vehicle_type')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if VehicleBrand.objects.filter(name=name, vehicle_type_id=vehicle_type_id, is_deleted=False).exists():
            messages.error(request, 'Bu araç markası zaten mevcut!')
            return redirect('vehicle_brand_list')
        
        VehicleBrand.objects.create(
            name=name,
            vehicle_type_id=vehicle_type_id,
            description=description,
            is_active=is_active
        )
        messages.success(request, 'Araç markası başarıyla oluşturuldu!')
        return redirect('vehicle_brand_list')
    
    return render(request, 'common/vehicle_brand_form.html', {
        'title': 'Yeni Araç Markası',
        'vehicle_types': vehicle_types
    })

@login_required
def vehicle_brand_edit(request, pk):
    vehicle_brand = get_object_or_404(VehicleBrand, pk=pk)
    vehicle_types = VehicleType.objects.filter(is_deleted=False, is_active=True)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        vehicle_type_id = request.POST.get('vehicle_type')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if VehicleBrand.objects.filter(name=name, vehicle_type_id=vehicle_type_id, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu araç markası zaten mevcut!')
            return redirect('vehicle_brand_list')
        
        vehicle_brand.name = name
        vehicle_brand.vehicle_type_id = vehicle_type_id
        vehicle_brand.description = description
        vehicle_brand.is_active = is_active
        vehicle_brand.save()
        messages.success(request, 'Araç markası başarıyla güncellendi!')
        return redirect('vehicle_brand_list')
    
    return render(request, 'common/vehicle_brand_form.html', {
        'title': 'Araç Markası Düzenle',
        'vehicle_brand': vehicle_brand,
        'vehicle_types': vehicle_types
    })

@login_required
def vehicle_brand_delete(request, pk):
    vehicle_brand = get_object_or_404(VehicleBrand, pk=pk)
    vehicle_brand.is_deleted = True
    vehicle_brand.save()
    messages.success(request, 'Araç markası başarıyla silindi!')
    return redirect('vehicle_brand_list')

@login_required
def vehicle_model_list(request):
    vehicle_models = VehicleModel.objects.filter(is_deleted=False).select_related('brand', 'brand__vehicle_type').order_by('brand__vehicle_type__name', 'brand__name', 'name')
    paginator = Paginator(vehicle_models, 15)  # Her sayfada 15 kayıt göster
    
    page = request.GET.get('page')
    try:
        vehicle_models = paginator.page(page)
    except PageNotAnInteger:
        vehicle_models = paginator.page(1)
    except EmptyPage:
        vehicle_models = paginator.page(paginator.num_pages)
        
    return render(request, 'common/vehicle_model_list.html', {'vehicle_models': vehicle_models})

@login_required
def vehicle_model_create(request):
    vehicle_brands = VehicleBrand.objects.filter(is_deleted=False, is_active=True).select_related('vehicle_type')
    
    if request.method == 'POST':
        brand_id = request.POST.get('brand')
        name = request.POST.get('name')
        year_start = request.POST.get('year_start') or None
        year_end = request.POST.get('year_end') or None
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if VehicleModel.objects.filter(brand_id=brand_id, name=name, is_deleted=False).exists():
            messages.error(request, 'Bu araç modeli zaten mevcut!')
            return redirect('vehicle_model_list')
        
        VehicleModel.objects.create(
            brand_id=brand_id,
            name=name,
            year_start=year_start,
            year_end=year_end,
            description=description,
            is_active=is_active
        )
        messages.success(request, 'Araç modeli başarıyla oluşturuldu!')
        return redirect('vehicle_model_list')
    
    return render(request, 'common/vehicle_model_form.html', {
        'title': 'Yeni Araç Modeli',
        'vehicle_brands': vehicle_brands
    })

@login_required
def vehicle_model_edit(request, pk):
    vehicle_model = get_object_or_404(VehicleModel, pk=pk)
    vehicle_brands = VehicleBrand.objects.filter(is_deleted=False, is_active=True).select_related('vehicle_type')
    
    if request.method == 'POST':
        brand_id = request.POST.get('brand')
        name = request.POST.get('name')
        year_start = request.POST.get('year_start') or None
        year_end = request.POST.get('year_end') or None
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if VehicleModel.objects.filter(brand_id=brand_id, name=name, is_deleted=False).exclude(pk=pk).exists():
            messages.error(request, 'Bu araç modeli zaten mevcut!')
            return redirect('vehicle_model_list')
        
        vehicle_model.brand_id = brand_id
        vehicle_model.name = name
        vehicle_model.year_start = year_start
        vehicle_model.year_end = year_end
        vehicle_model.description = description
        vehicle_model.is_active = is_active
        vehicle_model.save()
        messages.success(request, 'Araç modeli başarıyla güncellendi!')
        return redirect('vehicle_model_list')
    
    return render(request, 'common/vehicle_model_form.html', {
        'title': 'Araç Modeli Düzenle',
        'vehicle_model': vehicle_model,
        'vehicle_brands': vehicle_brands
    })

@login_required
def vehicle_model_delete(request, pk):
    vehicle_model = get_object_or_404(VehicleModel, pk=pk)
    vehicle_model.is_deleted = True
    vehicle_model.save()
    messages.success(request, 'Araç modeli başarıyla silindi!')
    return redirect('vehicle_model_list')

