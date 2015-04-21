from django.conf.urls import patterns, url

from bills import views

urlpatterns = patterns('',
    url(r'^bill/$', views.create_bill),
    url(r'^bill/([0-9]+)$', views.get_bill_for_id),
    url(r'^bill/([0-9a-f]{32})$', views.get_bill_for_tenant),
    url(r'^bill/([0-9a-f]{32})/([0-9]{2})/([0-9]{4})$', views.get_bill_for_tenant_month_year),
    url(r'^payment_method/$', views.create_payment_method),
    url(r'^payment_method/([0-9a-f]{32})$', views.get_payment_method_for_tenant),
    url(r'^payment_method/([0-9a-f]{32})/([0-9]+)$', views.update_payment_method),
    url(r'^payment/([0-9]+)/$', views.make_payment_against_bill),
    url(r'^payment/([0-9a-f]{32})$', views.get_payment_for_tenant),
    url(r'^payment/([0-9a-f]{32})/([0-9]{2})/([0-9]{4})$', views.get_payment_for_tenant_month_year),
    url(r'^payment/([0-9a-f]{32})/([0-9]+)$', views.get_payment_for_id),
    url(r'^policy/$', views.create_policy),
    url(r'^policy$', views.get_policy),
    url(r'^policy/([0-9]+)$', views.update_policy_by_id),
)

