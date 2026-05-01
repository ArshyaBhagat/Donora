from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.db.models import QuerySet
from django.conf import settings
import csv
import io
import os
from typing import Iterable, List, Tuple, Optional

from core.models import Donor, Recipient, MatchedTransplantation

# ReportLab for professional PDFs
from reportlab.lib.pagesizes import A4, landscape as rl_landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


@staff_member_required
def admin_spa(request):
    # Single-page app container
    return render(request, 'adminspa/index.html')


# ---------- Helpers ----------

def _parse_date_range(request) -> Tuple[Optional[timezone.datetime], Optional[timezone.datetime]]:
    """Parse ?start=YYYY-MM-DD&end=YYYY-MM-DD and return aware datetimes spanning full days."""
    start_str = request.GET.get('start')
    end_str = request.GET.get('end')
    tz = timezone.get_current_timezone()

    start_dt = None
    end_dt = None

    if start_str:
        d = parse_date(start_str)
        if d:
            start_dt = timezone.make_aware(timezone.datetime(d.year, d.month, d.day, 0, 0, 0), tz)
    if end_str:
        d = parse_date(end_str)
        if d:
            end_dt = timezone.make_aware(timezone.datetime(d.year, d.month, d.day, 23, 59, 59, 999999), tz)

    return start_dt, end_dt


def _apply_range(qs: QuerySet, field: str, start_dt, end_dt) -> QuerySet:
    if start_dt:
        qs = qs.filter(**{f"{field}__gte": start_dt})
    if end_dt:
        qs = qs.filter(**{f"{field}__lte": end_dt})
    return qs


def _fmt_date(dt, fmt: str = '%Y-%m-%d') -> str:
    """Safely format datetimes for CSV. If aware, localize; else format as-is.
    Returns empty string if dt is None or not a datetime.
    """
    if not dt:
        return ''
    try:
        return timezone.localtime(dt).strftime(fmt)
    except Exception:
        try:
            return dt.strftime(fmt)
        except Exception:
            return ''


# ---------- API ENDPOINTS (JSON) ----------
@staff_member_required
def api_donors(request):
    start_dt, end_dt = _parse_date_range(request)
    donors = Donor.objects.select_related('organ').all()
    donors = _apply_range(donors, 'created_at', start_dt, end_dt).order_by('-created_at')
    data = [
        {
            'id': d.id,
            'name': d.name,
            'age': d.age,
            'blood_group': d.blood_group,
            'organ': d.organ.organ_name if d.organ else None,
            'contact': d.contact,
            'matched': d.matched,
            'created_at': timezone.localtime(d.created_at).strftime('%Y-%m-%d '),
            'cancelled': d.cancelled,
        }
        for d in donors
    ]
    return JsonResponse({'results': data})


@staff_member_required
def api_recipients(request):
    start_dt, end_dt = _parse_date_range(request)
    recipients = Recipient.objects.select_related('organ').all()
    recipients = _apply_range(recipients, 'created_at', start_dt, end_dt).order_by('-created_at')
    data = [
        {
            'id': r.id,
            'name': r.name,
            'age': r.age,
            'blood_group': r.blood_group,
            'organ': r.organ.organ_name if r.organ else None,
            'contact': r.contact,
            'matched': r.matched,
            'created_at': timezone.localtime(r.created_at).strftime('%Y-%m-%d'),
            'cancelled': r.cancelled,
        }
        for r in recipients
    ]
    return JsonResponse({'results': data})


@staff_member_required
def api_matches(request):
    start_dt, end_dt = _parse_date_range(request)
    matches = MatchedTransplantation.objects.select_related('organ').all()
    matches = _apply_range(matches, 'matched_on', start_dt, end_dt).order_by('-matched_on')
    data = [
        {
            'transplantation_id': m.transplantation_id,
            'donor_name': m.donor_name,
            'recipient_name': m.recipient_name,
            'organ': m.organ.organ_name if m.organ else None,
            'donor_blood_group': m.donor_blood_group,
            'recipient_blood_group': m.recipient_blood_group,
            'matched_on': timezone.localtime(m.matched_on).strftime('%Y-%m-%d'),
        }
        for m in matches
    ]
    return JsonResponse({'results': data})


# ---------- CSV REPORTS ----------

def _csv_response(filename: str):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@staff_member_required
def report_donors_csv(request):
    start_dt, end_dt = _parse_date_range(request)
    qs = _apply_range(Donor.objects.select_related('organ').all(), 'created_at', start_dt, end_dt).order_by('-created_at')
    response = _csv_response('donors.csv')
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Age', 'Blood Group', 'Organ', 'Contact', 'Matched', 'Created At', 'Cancelled'])
    for d in qs:
        writer.writerow([
            d.id,
            d.name,
            d.age,
            d.blood_group,
            d.organ.organ_name if d.organ else '',
            d.contact,
            'Yes' if d.matched else 'No',
            _fmt_date(d.created_at),
            'Yes' if d.cancelled else 'No',
        ])
    return response


@staff_member_required
def report_recipients_csv(request):
    start_dt, end_dt = _parse_date_range(request)
    qs = _apply_range(Recipient.objects.select_related('organ').all(), 'created_at', start_dt, end_dt).order_by('-created_at')
    response = _csv_response('recipients.csv')
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Age', 'Blood Group', 'Organ', 'Contact', 'Matched', 'Created At', 'Cancelled'])
    for r in qs:
        writer.writerow([
            r.id,
            r.name,
            r.age,
            r.blood_group,
            r.organ.organ_name if r.organ else '',
            r.contact,
            'Yes' if r.matched else 'No',
            _fmt_date(r.created_at),
            'Yes' if r.cancelled else 'No',
        ])
    return response


@staff_member_required
def report_matches_csv(request):
    start_dt, end_dt = _parse_date_range(request)
    qs = _apply_range(MatchedTransplantation.objects.select_related('organ').all(), 'matched_on', start_dt, end_dt).order_by('-matched_on')
    response = _csv_response('matches.csv')
    writer = csv.writer(response)
    writer.writerow(['Transplant ID', 'Donor', 'Recipient', 'Organ', 'Donor BG', 'Recipient BG', 'Matched On'])
    for m in qs:
        writer.writerow([
            m.transplantation_id,
            m.donor_name,
            m.recipient_name,
            m.organ.organ_name if m.organ else '',
            m.donor_blood_group,
            m.recipient_blood_group,
            _fmt_date(m.matched_on),
        ])
    return response


# ---------- ReportLab PDF REPORTS ----------

def _pdf_response(filename: str):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def _date_range_text(start_dt, end_dt) -> str:
    if not start_dt and not end_dt:
        return 'All time'
    s = start_dt.strftime('%Y-%m-%d') if start_dt else '...'
    e = end_dt.strftime('%Y-%m-%d') if end_dt else '...'
    return f'{s} to {e}'


def _table_from_rows(headers: List[str], rows: Iterable[List[str]], styles):
    data = [headers]
    for r in rows:
        data.append([Paragraph(str(c) if c is not None else '', styles['BodyText']) for c in r])
    return data


def _build_pdf(title: str, headers: List[str], rows: Iterable[List[str]], pagesize, date_range_text: str) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=pagesize,
        leftMargin=36,
        rightMargin=36,
        topMargin=70,
        bottomMargin=40,
    )
    styles = getSampleStyleSheet()
    story: List = []

    # Title and range
    story.append(Paragraph(f'<b>{title}</b>', styles['Title']))
    story.append(Paragraph(f'Date range: {date_range_text}', styles['Normal']))
    story.append(Paragraph(f'Generated at: {timezone.localtime().strftime("%Y-%m-%d")}', styles['Normal']))
    story.append(Spacer(1, 12))

    # Build table
    data = _table_from_rows(headers, rows, styles)
    table = Table(data, repeatRows=1)
    # Table styling
    tbl_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#E5E7EB')),
    ]
    # Alternating row background
    for i in range(1, len(data)):
        if i % 2 == 0:
            tbl_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#FAFAFA')))
    table.setStyle(TableStyle(tbl_style))

    story.append(table)

    # Header/Footer
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')

    def on_page(canvas, doc_):
        canvas.saveState()
        width, height = doc_.pagesize
        # Logo
        if os.path.exists(logo_path):
            try:
                canvas.drawImage(logo_path, 36, height - 42, width=80, height=24, preserveAspectRatio=True, mask='auto')
            except Exception:
                pass
        # Title
        canvas.setFont('Helvetica-Bold', 10)
        canvas.drawString(130, height - 30, title)
        # Date range on right
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(width - 36, height - 30, date_range_text)
        # Footer
        canvas.setFont('Helvetica', 8)
        canvas.drawString(36, 20, f"Generated at {timezone.localtime().strftime('%Y-%m-%d')}")
        canvas.drawRightString(width - 36, 20, f"Page {doc_.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    pdf = buf.getvalue()
    buf.close()
    return pdf


@staff_member_required
def report_donors_pdf(request):
    start_dt, end_dt = _parse_date_range(request)
    qs = _apply_range(Donor.objects.select_related('organ').all(), 'created_at', start_dt, end_dt).order_by('-created_at')
    headers = ['ID', 'Name', 'Age', 'Blood Group', 'Organ', 'Contact', 'Matched', 'Created At', 'Cancelled']
    rows = (
        [
            d.id,
            d.name,
            d.age,
            d.blood_group,
            d.organ.organ_name if d.organ else '',
            d.contact,
            'Yes' if d.matched else 'No',
            timezone.localtime(d.created_at).strftime('%Y-%m-%d'),
            'Yes' if d.cancelled else 'No',
        ]
        for d in qs
    )
    date_text = _date_range_text(start_dt, end_dt)
    pdf = _build_pdf('Donora - Donors Report', headers, rows, A4, date_text)
    resp = _pdf_response('donors.pdf')
    resp.write(pdf)
    return resp


@staff_member_required
def report_recipients_pdf(request):
    start_dt, end_dt = _parse_date_range(request)
    qs = _apply_range(Recipient.objects.select_related('organ').all(), 'created_at', start_dt, end_dt).order_by('-created_at')
    headers = ['ID', 'Name', 'Age', 'Blood Group', 'Organ', 'Contact', 'Matched', 'Created At', 'Cancelled']
    rows = (
        [
            r.id,
            r.name,
            r.age,
            r.blood_group,
            r.organ.organ_name if r.organ else '',
            r.contact,
            'Yes' if r.matched else 'No',
            timezone.localtime(r.created_at).strftime('%Y-%m-%d'),
            'Yes' if r.cancelled else 'No',
        ]
        for r in qs
    )
    date_text = _date_range_text(start_dt, end_dt)
    pdf = _build_pdf('Donora - Recipients Report', headers, rows, A4, date_text)
    resp = _pdf_response('recipients.pdf')
    resp.write(pdf)
    return resp


@staff_member_required
def report_matches_pdf(request):
    start_dt, end_dt = _parse_date_range(request)
    qs = _apply_range(MatchedTransplantation.objects.select_related('organ').all(), 'matched_on', start_dt, end_dt).order_by('-matched_on')
    headers = ['Transplant ID', 'Donor', 'Recipient', 'Organ', 'Donor BG', 'Recipient BG', 'Matched On']
    rows = (
        [
            m.transplantation_id,
            m.donor_name,
            m.recipient_name,
            m.organ.organ_name if m.organ else '',
            m.donor_blood_group,
            m.recipient_blood_group,
            timezone.localtime(m.matched_on).strftime('%Y-%m-%d'),
        ]
        for m in qs
    )
    date_text = _date_range_text(start_dt, end_dt)
    pdf = _build_pdf('Donora - Matches Report', headers, rows, rl_landscape(A4), date_text)
    resp = _pdf_response('matches.pdf')
    resp.write(pdf)
    return resp