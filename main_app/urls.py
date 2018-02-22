from django.conf.urls import url
from .views import index, post_relief_effort, show, post_item_request, relief_efforts_index
from .views import login_view, signup, about, show_donor_profile, show_org_admin_profile
from .views import logout_view, post_donate, remove_item_request, update_item_request, update_relief_effort, make_donation
from .orgadminviews import OrgAdminSignUpView
from .donorviews import DonorSignUpView

urlpatterns = [
    url(r'^$', index),
    url(r'^post_url/$', post_relief_effort, name='post_relief_effort'),
    url(r'^relief_efforts/$', relief_efforts_index, name = 'relief_efforts_index'),
    url(r'^signup_login/$', login_view, name="login"),
    url(r'^logout/$', logout_view, name="logout"),
    url(r'^org_admin_signup/$', OrgAdminSignUpView.as_view(), name='org_admin_signup'),
    url(r'^donor_signup/$', DonorSignUpView.as_view(), name='donor_signup'),
    url(r'^([0-9]+)/update_item_request/$', update_item_request, name='update_item_request'),
    url(r'^([0-9]+)/make_donation/$', make_donation, name='make_donation'),
    url(r'^([0-9]+)/update_relief_effort/$', update_relief_effort, name='update_relief_effort'),
    url(r'^signup/$', signup, name="signup"),
    url(r'^about/$', about, name="about"),
    url(r'^post_donate/$', post_donate, name="post_donate"),
    url(r'^remove_item_request/$', remove_item_request, name="remove_item_request"),
    url(r'^([0-9]+)/$', show, name = 'show'),
    url(r'^([0-9]+)/post_item_request/$', post_item_request, name = 'post_item_request'),
    url(r'^([0-9]+)/donor-profile/$', show_donor_profile, name = 'show_donor_profile'),
    url(r'^([0-9]+)/org-admin-profile/$', show_org_admin_profile, name = 'show_org_admin_profile')
]
