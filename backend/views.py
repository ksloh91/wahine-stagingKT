from django.shortcuts import render,redirect
from backend.forms import *
import uuid
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.forms import formset_factory
from django.contrib.auth.forms import AuthenticationForm #add this
# Create your views here.
## TODO
## IF data exist, show existing data/edit mode
## If fields can have multiple entry (eg policy), show no of policies

def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request,'backend/index.html')

def who_we_are(request):
    return render(request,'backend/who-we-are.html')    

def wvault(request):
    return render(request,'backend/wvault.html')

def contact_us(request):
    return render(request,'backend/contact-us.html')

def terms_of_service(request):
    return render(request,'backend/terms-of-service.html')

def return_refund_policy(request):
    return render(request,'backend/return-refund-policy.html')

def privacy_policy(request):
    return render(request,'backend/privacy-policy.html')


def signup(request):
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("bank_account_form")
            messages.info(request, f"You can login now.")
            return redirect('login')
        else:
            print(form.errors)
            print(form.cleaned_data)
            return render(request,'backend/signup.html', {'form': form})
    form = SignUpForm()
    return render(request,'backend/signup.html', {'form': form})

def login_view(request):
    if request.POST:
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("bank_account_form")
            return redirect('bank_account_form')
        else:
            print(form)
            print(form.errors)
            return render(request,'backend/login.html', {'form': form})
    form = AuthenticationForm()
    print(form)
    return render(request,'backend/login.html', {'form': form})

def selectplan(request):
    if request.POST:
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            plan = form.cleaned_data['plan']
            item = Subscription.objects.create(
                user=request.user,
                plan = plan)
            redirect('profile')
        else:
            return render(request,'backend/select-a-plan.html', {'form': form})
    form = SignUpForm()
    return render(request,'backend/select-a-plan.html', {'form': form})

def dashboard(request):
    return render(request,'backend/dashboard.html')

def dashboard_assets(request):
    return render(request,'backend/dashboard-assets.html')

def profile(request):
    return render(request,'backend/profile.html')

def bank_account_form(request):
    form = BankAccountForm()
    # formset = formset_factory(form)
    if request.POST:
        form = BankAccountForm(request.POST)
        # formset = formset_factory(form)
        if form.is_valid():
            account_type = form.cleaned_data['account_type']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            account_value = form.cleaned_data['account_value']
            item = Item.objects.create(
                user=request.user,
                data={'account_type':account_type,
                    'bank_name':bank_name,
                    'account_no':account_no,
                    'account_value':account_value},
                item_type='Bank Account',
                created_by=request.user
                )
            messages.add_message(request, messages.INFO, 'Bank data successfully updated.')
            return redirect('epf_socso_form')
        else:
            context = {'form':form}
            return render(request,'backend/assets-1-bank.html',context)
    context = {'form':form}
    return render(request,'backend/assets-1-bank.html',context)

def epf_socso_form(request):
    form = EpfSocsoForm()
    if request.POST:
        form = EpfSocsoForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'Success.')
                return redirect('insurance_form')
            is_epf_member = form.cleaned_data['is_epf_member']
            epf_member_no = form.cleaned_data['epf_member_no']
            epf_nominee_name = form.cleaned_data['epf_nominee_name']
            is_socso_member = form.cleaned_data['is_socso_member']
            socso_nominee_name = form.cleaned_data['socso_nominee_name']
            socso_member_no = form.cleaned_data['socso_member_no']
            epf_account_value = form.cleaned_data['epf_account_value']
            socso_account_value = form.cleaned_data['socso_account_value']
            item = Item.objects.create(
                user=request.user,
                data={'is_epf_member':is_epf_member,
                    'is_socso_member':is_socso_member,
                    'epf_member_no':epf_member_no,
                    'socso_member_no':socso_member_no,
                    'epf_nominee_name':epf_nominee_name,
                    'socso_nominee_name':socso_nominee_name,
                    'epf_account_value':epf_account_value,
                    'socso_account_value':socso_account_value,
                }  ,
                item_type='EPF Socso',
                created_by=request.user
                )
            messages.add_message(request, messages.INFO, 'EPF/Socso successfully updated.')
            return redirect('insurance_form')
        else:
            print(form.errors)
            context = {'form':form}
            return render(request,'backend/assets-2-epf.html',context)
    context = {'form':form}
    return render(request,'backend/assets-2-epf.html',context)

def insurance_form(request):
    form = InsuranceForm()
    if request.POST:
        form = InsuranceForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'Success.')
                return redirect('investment_form')
            insurance_type = form.cleaned_data['insurance_type']
            policy_no = form.cleaned_data['policy_no']
            nominee_name = form.cleaned_data['nominee_name']
            sum_insured = form.cleaned_data['sum_insured']
            item = Item.objects.create(user=request.user,data={'insurance_type':insurance_type,'policy_no':policy_no,'nominee_name':nominee_name,'sum_insured':sum_insured},item_type='Insurance',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Insurance data successfully updated.')
            return redirect('investment_form')
    context = {'form':form}
    return render(request,'backend/assets-3-insurance.html',context)

def investment_form(request):
    form = InvestmentForm()
    if request.POST:
        form = InvestmentForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'Success.')
                return redirect('property_form')
            investment_type = form.cleaned_data['investment_type']
            account_no = form.cleaned_data['account_no']
            fund_name = form.cleaned_data['fund_name']
            account_value = form.cleaned_data['account_value']
            item = Item.objects.create(user=request.user,data={'investment_type':investment_type,'account_no':account_no,'fund_name':fund_name,'account_value':account_value},item_type='Investment',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Investment data successfully updated.')
            return redirect('property_form')
    context = {'form':form}
    return render(request,'backend/assets-4-investment.html',context)

def property_form(request):
    form = PropertyForm()
    if request.POST:
        form = PropertyForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'Success.')
                return redirect('vehicles_form')
            property_type = form.cleaned_data['property_type']
            residential_type = form.cleaned_data['residential_type']
            address = form.cleaned_data['address']
            spa_price = form.cleaned_data['spa_price']
            item = Item.objects.create(user=request.user,data={'property_type':property_type,'residential_type':residential_type,'address':address,'spa_price':spa_price},item_type='Property',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Property data successfully updated.')
            return redirect('vehicles_form')
    context = {'form':form}
    return render(request,'backend/assets-5-property.html',context)

def vehicles_form(request):
    form = VehicleForm()
    if request.POST:
        form = VehicleForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'Success.')
                return redirect('asset_others_form')
            vehicle_type = form.cleaned_data['vehicle_type']
            make_model = form.cleaned_data['make_model']
            registration_no = form.cleaned_data['registration_no']
            item = Item.objects.create(user=request.user,data={'vehicle_type':vehicle_type,'make_model':make_model,'registration_no':registration_no},item_type='Vehicle',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Vehicle data successfully updated.')
            return redirect('asset_others_form')
    context = {'form':form}
    return render(request,'backend/assets-6-vehicles.html',context)

def asset_others_form(request):
    form = AssetOthersForm()
    if request.POST:
        form = AssetOthersForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'Success.')
                return redirect('assets_overview')
            asset_name = form.cleaned_data['asset_name']
            asset_value = form.cleaned_data['asset_value']
            item = Item.objects.create(user=request.user,data={'asset_name':asset_name,'asset_value':asset_value},item_type='Other Assets',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Assets successfully updated.')
            return redirect('assets_overview')
    context = {'form':form}
    return render(request,'backend/assets-7-others.html',context)

def liability_credit_card_form(request):
    form = CreditCardForm()
    if request.POST:
        form = CreditCardForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'Success.')
                return redirect('personal_loan_form')
            bnpl_service = form.cleaned_data['bnpl_service']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            amount_outstanding = form.cleaned_data['amount_outstanding']
            item = Item.objects.create(user=request.user,data={'bnpl_service':bnpl_service,'bank_name':bank_name,'account_no':account_no,'amount_outstanding':amount_outstanding},item_type='Credit Card',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Done.')
            return redirect('personal_loan_form')
    context = {'form':form}
    return render(request,'backend/liabilities-1-credit-card.html',context)

def personal_loan_form(request):
    form = PersonalLoanForm()
    if request.POST:
        form = PersonalLoanForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'Success.')
                return redirect('vehicles_loan_form')
            loan_tenure = form.cleaned_data['loan_tenure']
            loan_interest = form.cleaned_data['loan_interest']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            loan_amount = form.cleaned_data['loan_amount']
            item = Item.objects.create(user=request.user,data={'bank_name':bank_name,'account_no':account_no,'loan_amount':loan_amount,'loan_tenure':loan_tenure,'loan_interest':loan_interest},item_type='Personal Loan',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Done.')
            return redirect('vehicles_loan_form')
    context = {'form':form}
    return render(request,'backend/liabilities-2-personal-loan.html',context)

def vehicles_loan_form(request):
    form = VehicleLoanForm()
    if request.POST:
        form = VehicleLoanForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'Success.')
                return redirect('property_loan_form')
            loan_tenure = form.cleaned_data['loan_tenure']
            loan_interest = form.cleaned_data['loan_interest']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            loan_amount = form.cleaned_data['loan_amount']
            item = Item.objects.create(user=request.user,data={'bank_name':bank_name,'account_no':account_no,'loan_amount':loan_amount,'loan_tenure':loan_tenure,'loan_interest':loan_interest},item_type='Vehicle Loan',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Done.')
            return redirect('property_loan_form')
    context = {'form':form}
    return render(request,'backend/liabilities-3-vehicle-loan.html',context)


def property_loan_form(request):
    form = PropertyLoanForm()
    if request.POST:
        form = PropertyLoanForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'Success.')
                return redirect('liabilities_others_form')
            loan_tenure = form.cleaned_data['loan_tenure']
            loan_interest = form.cleaned_data['loan_interest']
            bank_name = form.cleaned_data['bank_name']
            account_no = form.cleaned_data['account_no']
            loan_amount = form.cleaned_data['loan_amount']
            item = Item.objects.create(user=request.user,data={'bank_name':bank_name,'account_no':account_no,'loan_amount':loan_amount,'loan_tenure':loan_tenure,'loan_interest':loan_interest},item_type='Property Loan',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Done.')
            return redirect('liabilities_others_form')
    context = {'form':form}
    return render(request,'backend/liabilities-4-property.html',context)

def liabilities_others_form(request):
    form = LiabilitiesOthersForm()
    if request.POST:
        form = LiabilitiesOthersForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['yesno'] == 'no':
                messages.add_message(request, messages.INFO, 'Success.')
                return redirect('liabilities_others_form')
            liability_name = form.cleaned_data['liability_name']
            liability_value = form.cleaned_data['liability_value']
            item = Item.objects.create(user=request.user,data={'liability_value':liability_value,'liability_name':liability_name},item_type='Other Liabilities',created_by=request.user)
            messages.add_message(request, messages.INFO, 'Done.')
            return redirect('liabilities_overview')
    context = {'form':form}
    return render(request,'backend/liabilities-5-others.html',context)

def assets_overview(request):
    user = request.user
    items = Item.objects.filter(user=user)
    banks = items.filter(item_type='Bank Account')
    epf_socso = items.filter(item_type='EPF Socso')
    insurances = items.filter(item_type='Insurance')
    investments = items.filter(item_type='Investment')
    properties = items.filter(item_type='Property')
    vehicles = items.filter(item_type='Vehicles')
    others = items.filter(item_type='Other Assets')
    print(banks)
    print(epf_socso)
    print(insurances)
    print(investments)
    print(properties)
    print(vehicles)
    print(others)
    context = {'items':items}
    return render(request,'backend/assets-overview.html',context)

def liabilities_overview(request):
    context = {}
    return render(request,'backend/liabilities-overview.html',context)

def dashboard(request):
    context = {}
    return render(request,'backend/dashboard.html',context)
