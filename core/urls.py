from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('home/', views.home_page, name="home_page"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name="login"),

    path('aboutus/', views.aboutus_view, name="aboutus"),
    path('FAQs/', views.FAQs_view, name="FAQs"),
    path('privacy-policy/', views.privacy_policy_view, name="privacy_policy"),
    path('terms-of-use/', views.terms_of_use_view, name="terms_of_use"),
    path('security/', views.security_view, name="security"),
    path('other-policies/', views.other_policies_view, name="other_policies"),

    path('organ/', views.organ_view, name="organ"),
    path('lung/', views.lung_view, name="lung"),
    path('liver/', views.liver_view, name="liver"),
    path('kidney/', views.kidney_view, name="kidney"),
    path('skin/', views.skin_view, name="skin"),

    # Contact Us (saves to DB via ContactSubmission)
    path('contactus/', views.contactus_view, name="contactus"),

    # Notifications and account actions
    path('notifications/', views.notifications_view, name="notifications"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Organ-specific Donor and Recipient form URLs
    path('organ/<int:organ_id>/become-donor/', views.become_donor, name='become_donor'),
    path('organ/<int:organ_id>/become-recipient/', views.become_recipient, name='become_recipient'),

    # Cancel and Reapply Notification
    path('notifications/cancel-donor/<int:donor_id>/', views.cancel_donor, name='cancel_donor'),
    path('notifications/cancel-recipient/<int:recipient_id>/', views.cancel_recipient, name='cancel_recipient'),
    path('notifications/reapply-donor/<int:donor_id>/', views.reapply_donor, name='reapply_donor'),
    path('notifications/reapply-recipient/<int:recipient_id>/', views.reapply_recipient, name='reapply_recipient'),

    # Custom Forgot Password (no email – updates directly via form)
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),

    # Django Built-in Password Change (for logged-in users)
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='change_password.html'
    ), name='password_change'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='change_password_done.html'
    ), name='password_change_done'),

    # Acknowledgment receipt page for matched transplantations
    path('acknowledgment/<int:transplantation_id>/', views.acknowledgment_view, name='acknowledgment'),
]
