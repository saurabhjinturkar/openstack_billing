from django.contrib import admin
from bills.models import Bill, BillingItem, PaymentMethod, Payment, UsageMetric, Currency, Policy

admin.site.register(Bill)
admin.site.register(BillingItem)
admin.site.register(Payment)
admin.site.register(PaymentMethod)
admin.site.register(UsageMetric)
admin.site.register(Currency)
admin.site.register(Policy)

