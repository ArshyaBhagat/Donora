from django.urls import path
from . import views

urlpatterns = [
    # SPA entry point
    path('', views.admin_spa, name='admin_spa'),

    # Data API endpoints (staff-only) with optional date filters
    path('api/donors/', views.api_donors, name='api_donors'),
    path('api/recipients/', views.api_recipients, name='api_recipients'),
    path('api/matches/', views.api_matches, name='api_matches'),

    # CSV download endpoints (accept ?start=YYYY-MM-DD&end=YYYY-MM-DD)
    path('reports/donors.csv', views.report_donors_csv, name='report_donors_csv'),
    path('reports/recipients.csv', views.report_recipients_csv, name='report_recipients_csv'),
    path('reports/matches.csv', views.report_matches_csv, name='report_matches_csv'),

    # PDF download endpoints (accept ?start=YYYY-MM-DD&end=YYYY-MM-DD)
    path('reports/donors.pdf', views.report_donors_pdf, name='report_donors_pdf'),
    path('reports/recipients.pdf', views.report_recipients_pdf, name='report_recipients_pdf'),
    path('reports/matches.pdf', views.report_matches_pdf, name='report_matches_pdf'),
]