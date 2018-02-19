from django.conf.urls import url
from .views import index, post_relief_effort, show, post_item_request, relief_efforts_index
from .views import login_view, org_admin_signup, post_org_admin_user

urlpatterns = [
    url(r'^$', index),
    url(r'^org_admin_signup/$', org_admin_signup, name='org_admin_signup'),
    url(r'^post_url/$', post_relief_effort, name='post_relief_effort'),
    url(r'^org_admin_signup_post/$', post_org_admin_user, name='post_org_admin_user'),
    url(r'^relief_efforts/$', relief_efforts_index, name = 'relief_efforts_index'),
    url(r'^signup_login/$', login_view, name="login"),
    url(r'^([0-9]+)/$', show, name = 'show'),
    url(r'^([0-9]+)/post_item_request/$', post_item_request, name = 'post_item_request')
]
