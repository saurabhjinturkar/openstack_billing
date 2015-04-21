from django.db import models
import InvalidFormatError
import json

class UsageMetric(models.Model):
    usage_metric = models.CharField(max_length = 255)
    metric_description = models.CharField(max_length = 255)
    openstack_service = models.CharField(max_length = 255)
    entity_name = models.CharField(max_length = 255)

    def __unicode__(self): 
        return str(self.usage_metric) + str(self.openstack_service)
 
    def to_object(self, json_dict):
        try: 
            self.usage_metric = json_dict["usage_metric"]
            self.metric_description = json_dict["metric_description"]
            self.openstack_service = json_dict["openstack_service"]
        except KeyError as e:
            raise InvalidFormatError("Incorrect format for " + str(json))
   
    def to_json(self):
        dict = {}
        dict["usage_metric"] = self.usage_metric
        dict["metric_description"] = self.metric_description
        dict["openstack_service"] = self.openstack_service
        return dict

class Currency(models.Model):
    currency = models.CharField(max_length = 32)
    currency_shortform = models.CharField(max_length = 3)
    symbol = models.CharField(max_length = 2)
    conversion_rate = models.FloatField()

    def __unicode__(self): 
        return str(self.currency_shortform) + "(" + str(self.symbol) + ")"

    def to_object(self, json_dict):
        try:
           self.currency = json_dict['currency']
           self.currency_shortform = json_dict['currency_shortform'] 
           self.symbol = json_dict['symbol']
           self.conversion_rate = json_dict['conversion_rate']
        except KeyError as e:
            raise InvalidFormatError("Incorrect format for " + str(json))

    def to_json(self): 
        dict = {}
        dict['currency'] = self.currency
        dict['currency_shortform'] = self.currency_shortform 
        dict['symbol'] = self.symbol
        dict['conversion_rate'] = self.conversion_rate
        return dict

class Policy(models.Model):
    usage_metric = models.ForeignKey(UsageMetric)
    default_currency = models.ForeignKey(Currency)
    unit_usage_currency_ratio = models.FloatField()
    creation_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self): 
        return str(self.usage_metric) + str(self.default_currency) + str(self.unit_usage_currency_ratio)

    def to_object(self, json_dict):
        try:
           self.usage_metric = UsageMetric.objects.get(pk=json_dict['usage_metric_id'])
           self.default_currency = Currency.objects.get(pk=json_dict['default_currency_id']) 
           self.unit_usage_currency_ratio = json_dict['unit_usage_currency_ratio']
        except KeyError as e:
            raise InvalidFormatError("Incorrect format for " + str(json))

    def to_json(self): 
        dict = {}
        dict['policy_id'] = self.pk
        dict['usage_metric'] = self.usage_metric.to_json()
        dict['default_currency'] = self.default_currency.to_json()  
        dict['unit_usage_currency_ratio'] = self.unit_usage_currency_ratio
        return dict

class Bill(models.Model):
    tenant_id =  models.CharField(max_length=255)
    billing_period_start_time = models.DateTimeField()
    billing_period_end_time = models.DateTimeField()
    bill_status = models.CharField(max_length=50)
    bill_settle_time = models.DateTimeField(null=True, blank=True)
    bill_creation_time = models.DateTimeField(auto_now_add=True)
    bill_version_id = models.IntegerField()
    total_charge =  models.FloatField()
    
    def __unicode__(self):
        return self.tenant_id + ',' +  str(self.bill_creation_time) + ',' + str(self.total_charge)
     
    def to_object(self, json_dict):
        try:
            self.tenant_id = json_dict["tenant_id"]
            self.billing_period_start_time = datetime.strptime( json_dict["billing_period_start_time"][:-1], "%Y-%m-%dT%H:%M:%S" )
            self.billing_period_end_time = datetime.strptime( json_dict["billing_period_end_time"][:-1], "%Y-%m-%dT%H:%M:%S" )
            self.bill_status = json_dict["bill_status"]
            self.bill_version_id = json_dict["bill_version_id"]
            self.total_charge = json_dict["total_charge"]
        except KeyError as e:
            raise InvalidFormatError("Incorrect format for " + str(json))

    def to_json(self): 
        dict = {}
        dict["bill_id"] = self.pk
        dict["tenant_id"] = self.tenant_id 
        dict["billing_period_start_time"] = self.billing_period_start_time.ctime()
        dict["billing_period_end_time"] = self.billing_period_end_time.ctime()
        dict["bill_status"] = self.bill_status
        dict["bill_settle_time"] = "" if self.bill_settle_time is None else self.bill_settle_time.ctime()
        dict["bill_creation_time"] = self.bill_creation_time.ctime()
        dict["bill_version_id"] = self.bill_version_id
        dict["total_charge"] = self.total_charge
        billing_items = list(BillingItem.objects.filter(bill__pk=self.pk))
        print billing_items
        billing_item_list = []
        for billing_item in billing_items:
            billing_item_list.append(billing_item.to_json())
        dict["billing_item"] = billing_item_list
        return dict
    
class BillingItem(models.Model):
    bill = models.ForeignKey(Bill)
    description = models.CharField(max_length=255)
    entity_name = models.CharField(max_length=255)
    billing_period_start_time = models.DateTimeField()
    billing_period_end_time = models.DateTimeField()
    usage_amount = models.FloatField()
    charge_amount = models.FloatField()
    policy = models.ForeignKey(Policy)

    def __unicode__(self): 
        return self.entity_name + ',' + str(self.usage_amount) + ',' + str(self.charge_amount)

    def to_object(self, json_dict):
        try:
            dict = {}
        except KeyError as e:
            raise InvalidFormatError("Incorrect format for " + str(json))

    def to_json(self): 
        dict = {}
        dict["bill_id"] = self.bill.pk 
        dict["bill_item_id"] = self.pk
        dict["description"] = self.description
        dict["entity_name"] = self.entity_name
        dict["billing_period_start_time"] = str(self.billing_period_start_time.ctime())
        dict["billing_period_end_time"] = str(self.billing_period_end_time.ctime())
        dict["usage_amount"] = self.usage_amount
        dict["charge_amount"] = self.charge_amount
        dict["policy"] = self.policy.to_json()
        return dict

class PaymentMethod(models.Model):
    tenant_id = models.CharField(max_length = 32)
    type = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255) 
    identity = models.CharField(max_length = 20)
    vendor = models.CharField(max_length = 50)
    cvv = models.CharField(max_length = 3)
    valid_through =  models.CharField(max_length = 8)
    preferred_method = models.BooleanField()
    zip = models.IntegerField()
    
    def __unicode__(self): 
        return self.type + ',' + self.identity

    def to_object(self, json_dict):
        try:
           self.tenant_id = json_dict['tenant_id']
           self.name = json_dict['name'] 
           self.type = json_dict['type'] 
           self.identity = json_dict['identity']
           self.vendor = json_dict['vendor']
           self.cvv = json_dict['cvv']
           self.valid_through = json_dict['valid_through']
           self.preferred_method = json_dict['preferred_method']
           self.zip = int(json_dict['zip'])
        except KeyError as e:
            raise InvalidFormatError("Incorrect format for " + str(json))

    def to_json(self): 
        dict = {}
        dict["payment_method_id"] = self.pk
        dict['tenant_id'] = self.tenant_id
        dict['type'] = self.type
        dict['name'] = self.name  
        dict['identity'] = self.identity
        dict['vendor'] = self.vendor
        dict['cvv'] = self.cvv
        dict['valid_through'] = self.valid_through
        dict['preferred_method'] = self.preferred_method
        dict['zip'] = self.zip
        return dict

class Payment(models.Model):
    type = models.CharField(max_length = 255)
    payment_method = models.ForeignKey(PaymentMethod)
    bill = models.ForeignKey(Bill)
    tenant_id = models.CharField(max_length = 255)
    amount = models.FloatField()
    creation_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self): 
        return str(self.payment_method) + str(self.bill) + str(self.amount)

    def to_object(self, json_dict):
        try:
           self.type = json_dict['type']
           self.payment_method = PaymentMethod.objects.get(pk == json_dict['payment_method_id']) 
           self.bill = Bill.objects.get(pk = json_dict['bill_id'])
           self.tenant_id = json_dict['tenant_id']
           self.amount = json_dict['amount']
        except KeyError as e:
            raise InvalidFormatError("Incorrect format for " + str(json))

    def to_json(self): 
        dict = {}
        dict['payment_id'] = self.pk
        dict['type'] = self.type
        dict['payment_method'] = self.payment_method.to_json()  
        dict['bill'] = self.bill.to_json()
        dict['tenant_id'] = self.tenant_id
        dict['amount'] = self.amount
        return dict


