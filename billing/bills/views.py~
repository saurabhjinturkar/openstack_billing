import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.core import serializers
from django.views.decorators.http import require_http_methods
from django.http import QueryDict
from bills.models import Bill
from bills.models import PaymentMethod
from bills.models import Payment, Policy

# You can create bills with this URL : http://localhost:2222/billing/bill
# This method should not be accessed by user. Since internally system will generate bills.
@require_http_methods(['POST'])
def create_bill(request):
    try:
        json_data = json.load(request.POST.item("request"))
        bill = Bill()
        bill.to_object(json_data)
        bill.save()
        response = json.dump(bill.to_json(), sort_keys=True)
        return HttpResponse(response, mimetype='application/json')
    except KeyError as e:
        return HttpResponseBadRequest(e.value, content_type = "text/html")
       
# You can access this method with : http://localhost:2222/billing/bill/{bill_id}
# bill_id is integer. It is primary key of the bills table. Try 1, 2 or 3 for testing
def get_bill_for_id(request, bill_id):
    print "bill"
    print bill_id
    print request.GET.items()
    bills = Bill.objects.filter(pk=int(bill_id))
    print bills
    bills_dictionary = []
    for bill in bills:
        print bill.to_json()
        bills_dictionary.append(bill.to_json())    
    response = json.dumps(bills_dictionary, sort_keys=True)
    return HttpResponse(response, content_type='application/json')

# You can access this method with : http://localhost:2222/billing/bill/{tenant_id}
# tenant_id is 32 character hexadecimal string
def get_bill_for_tenant(request, tenant):
    print "tenant"
    print tenant
    bills = Bill.objects.filter(tenant_id__exact=tenant)
    bills_dictionary = []
    for bill in bills:
        print bill.to_json()
        bills_dictionary.append(bill.to_json())    
    response = json.dumps(bills_dictionary, sort_keys=True)
    return HttpResponse(response, content_type='application/json')

# You can access this method with : http://localhost:2222/billing/bill/{tenant_id}/{mm}/{yyyy}
# mm = month in number. Two digits are necessary. yyyy = year. Four digits are necessary 
def get_bill_for_tenant_month_year(request, tenant_id, month, year):
    print "month year"
    print tenant_id
    print month
    print year 
    bills = Bill.objects.filter(tenant_id__exact=tenant_id, bill_creation_time__month=month, bill_creation_time__year=year)
    print bills
    bills_dictionary = []
    for bill in bills:
        print bill.to_json()
        bills_dictionary.append(bill.to_json())    
    response = json.dumps(bills_dictionary, sort_keys=True)
    return HttpResponse(response, content_type='application/json')

# You can access this method with : http://localhost:2222/billing/payment_method
@require_http_methods(['POST'])
def create_payment_method(request):
    try:
        print request.POST.items()
        payment_method_json = request.POST.get('request')
        payment_dictionary = json.loads(payment_method_json)
        print payment_dictionary
        payment_method = PaymentMethod()
        payment_method.to_object(payment_dictionary)
        payment_method.save();
        return HttpResponse(payment_method.id)
    except Exception as e:
        return HttpResponseBadRequest(e.value, content_type = "text/html")
    

def get_payment_method_for_tenant(request, tenant_id):
    payment_methods = PaymentMethod.objects.filter(tenant_id__exact=tenant_id)
    payment_method_list = []
    for payment_method in payment_methods:
        print payment_method.to_json()
        payment_method_list.append(payment_method.to_json())    
    response = json.dumps(payment_method_list, sort_keys=True)
    return HttpResponse(response, content_type='application/json')

@require_http_methods(['PUT', 'DELETE'])
def update_payment_method(request, tenant_id, payment_method_id):
    if (request.method == 'PUT'):
      #  try:
            print "here"
            put = QueryDict(request.body)
            payment_method_json = put.get('request')
            payment_dictionary = json.loads(payment_method_json)
            print payment_dictionary
            payment_method = PaymentMethod.objects.filter(tenant_id__exact=tenant_id, pk=int(payment_method_id))[0]
            payment_method.to_object(payment_dictionary)
            payment_method.save();
            payment_methods = PaymentMethod.objects.filter(tenant_id__exact=tenant_id, pk=int(payment_method_id)) 
            payment_method_list = []
            for payment_method in payment_methods:
                print payment_method.to_json()
                payment_method_list.append(payment_method.to_json())    
            response = json.dumps(payment_method_list, sort_keys=True)
            return HttpResponse(response, content_type='application/json')
      #  except Exception as e:
      #      return HttpResponseBadRequest(e.value, content_type = "text/html")

    elif (request.method == 'DELETE'):
       payment_methods = PaymentMethod.objects.filter(tenant_id__exact=tenant_id, pk=int(payment_method_id))
       print payment_methods
       payment_methods[0].delete()
       return HttpResponse("DELETE")

def make_payment_against_bill(self, bill_id):
    try:
        print request.POST.items()
        payment_json = request.POST.get('request')
        payment_dictionary = json.loads(payment_json)
        print payment_dictionary
        payment = PaymentMethod()
        payment.to_object(payment_dictionary)
        payment.save();
        payment.bill.bill_status = "Paid"
        return HttpResponse(payment.id)
    except Exception as e:
        return HttpResponseBadRequest(e.value, content_type = "text/html")
    
def get_payment_for_tenant(self, tenant_id):
    payments = Payment.objects.filter(tenant_id__exact=tenant_id)
    payment_list = []
    for payment in payments:
        payment_list.append(payment.to_json())    
    response = json.dumps(payment_list, sort_keys=True)
    return HttpResponse(response, content_type='application/json')

def get_payment_for_tenant_month_year(self, tenant_id, month, year):
    payments = Payment.objects.filter(tenant_id__exact=tenant_id, creation_time__month=month, creation_time__year=year)
    payments_list = []
    for payment in payments:
        payments_list.append(payment.to_json())    
    response = json.dumps(payments_list, sort_keys=True)
    return HttpResponse(response, content_type='application/json')

def get_payment_for_id(self, tenant_id, payment_id):
    payments = Payment.objects.filter(tenant_id__exact=tenant_id, pk=payment_id)
    payments_list = []
    for payment in payments:
        payments_list.append(payment.to_json())    
    response = json.dumps(payments_list, sort_keys=True)
    return HttpResponse(response, content_type='application/json')

def create_policy(self):
    pass

def get_policy(self):
    policies = Policy.objects.all()
    policy_list = []
    for policy in policies:
        policy_list.append(policy.to_json())    
    response = json.dumps(policy_list, sort_keys=True)
    return HttpResponse(response, content_type='application/json')

def update_policy_by_id(self, policy_id):
    pass 

def handler405(request): 
    response = HttpResponse()
    response.content = "This method is not supported by API for this resource"
    response.status_code = 404
    return response
