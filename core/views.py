from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import (
    UserProfile,
    Donor,
    Recipient,
    Organ,
    MatchedTransplantation,
    Notification,
    ContactSubmission,  # for Contact Us saving
)
from .forms import DonorForm, RecipientForm, ContactForm  # includes ContactForm


# Blood group compatibility map
compatibility = {
    'O+': ['O+', 'A+', 'B+', 'AB+'],
    'O-': ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'],
    'A+': ['A+', 'AB+'],
    'A-': ['A+', 'A-', 'AB+', 'AB-'],
    'B+': ['B+', 'AB+'],
    'B-': ['B+', 'B-', 'AB+', 'AB-'],
    'AB+': ['AB+'],
    'AB-': ['AB+', 'AB-'],
}


def home_page(request):
    return render(request, 'homepage.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        location = request.POST.get('location', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        context = {
            'form': {
                'username': username,
                'phone': phone,
                'email': email,
                'location': location,
            }
        }

        if not all([username, phone, email, location, password, confirm_password]):
            messages.error(request, "All fields are required!")
            return render(request, 'signup.html', context)

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'signup.html', context)

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'signup.html', context)

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use!")
            return render(request, 'signup.html', context)

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, phone=phone, location=location)
        messages.success(request, "Signup successful! Please log in.")
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        messages.error(request, "Invalid username or password!")
        return render(request, 'login.html', {'username': username})
    return render(request, 'login.html')


def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not new_password or not confirm_password:
            messages.error(request, "All fields are required!")
            return render(request, 'forgot_password.html')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'forgot_password.html')

        if len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters long!")
            return render(request, 'forgot_password.html')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password updated successfully. Please login.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Username not found!")
            return render(request, 'forgot_password.html')

    return render(request, 'forgot_password.html')


def aboutus_view(request): return render(request, 'aboutus.html')
def FAQs_view(request): return render(request, 'FAQs.html')
def privacy_policy_view(request): return render(request, 'privacy_policy.html')
def terms_of_use_view(request): return render(request, 'terms_of_use.html')
def security_view(request): return render(request, 'security.html')
def other_policies_view(request): return render(request, 'other_policies.html')
def organ_view(request): return render(request, 'organ.html')
def lung_view(request): return render(request, 'lung.html')
def liver_view(request): return render(request, 'liver.html')
def kidney_view(request): return render(request, 'kidney.html')
def skin_view(request): return render(request, 'skin.html')


def contactus_view(request):
    # GET shows form; POST saves a ContactSubmission row.
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactSubmission.objects.create(**form.cleaned_data)
            messages.success(request, "Thanks! Your message has been recorded.")
            return redirect('contactus')  # PRG pattern
        messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    return render(request, 'contactus.html', {"form": form})


# ----- NOTIFICATIONS SYSTEM -----
@login_required
def notifications_view(request):
    now = timezone.now()

    # Recent 4 matches for history
    all_matches = []
    donor_objs = Donor.objects.filter(user=request.user)
    donor_matches = MatchedTransplantation.objects.filter(donor__in=donor_objs).order_by('-transplantation_id')[:4]
    for match in donor_matches:
        all_matches.append({"match": match, "role": "donor"})
    recipient_objs = Recipient.objects.filter(user=request.user)
    recipient_matches = MatchedTransplantation.objects.filter(recipient__in=recipient_objs).order_by('-transplantation_id')[:4]
    for match in recipient_matches:
        all_matches.append({"match": match, "role": "recipient"})
    all_matches = sorted(all_matches, key=lambda m: m["match"].transplantation_id, reverse=True)
    seen_ids = set()
    unique_matches = []
    for item in all_matches:
        if item["match"].transplantation_id not in seen_ids:
            unique_matches.append(item)
            seen_ids.add(item["match"].transplantation_id)
    all_matches = unique_matches[:4]

    # Active pending donor/recipient (uncancelled, < 24h old)
    pending_donor = Donor.objects.filter(
        user=request.user, cancelled=False
    ).order_by('-created_at').first()
    hours_left_donor = None
    if pending_donor and (now - pending_donor.created_at) <= timedelta(hours=24):
        delta = timedelta(hours=24) - (now - pending_donor.created_at)
        hours_left_donor = max(int(delta.total_seconds() // 3600), 0)
    else:
        pending_donor = None

    pending_recipient = Recipient.objects.filter(
        user=request.user, cancelled=False
    ).order_by('-created_at').first()
    hours_left_recipient = None
    if pending_recipient and (now - pending_recipient.created_at) <= timedelta(hours=24):
        delta = timedelta(hours=24) - (now - pending_recipient.created_at)
        hours_left_recipient = max(int(delta.total_seconds() // 3600), 0)
    else:
        pending_recipient = None

    # --- Fetch persistent notifications (unread only, mark as read after display) ---
    notif_qs = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    user_notifications = list(notif_qs)
    notif_qs.update(is_read=True)

    # For reapply, figure out type/id
    notif_for_reapply = None
    notif_reapply_type = None
    notif_reapply_id = None
    for notif in user_notifications:
        if notif.notif_type == 'reapply':
            if notif.donor is not None:
                notif_for_reapply = notif
                notif_reapply_type = 'donor'
                notif_reapply_id = notif.donor.id
                break
            elif notif.recipient is not None:
                notif_for_reapply = notif
                notif_reapply_type = 'recipient'
                notif_reapply_id = notif.recipient.id
                break

    context = {
        'matched': all_matches[0]["match"] if all_matches else None,
        'role': all_matches[0]["role"] if all_matches else None,
        'user': request.user,
        'all_matches': all_matches,
        'pending_donor': pending_donor,
        'pending_recipient': pending_recipient,
        'hours_left_donor': hours_left_donor,
        'hours_left_recipient': hours_left_recipient,
        'now': now,
        'user_notifications': user_notifications,
        'notif_for_reapply': notif_for_reapply,
        'notif_reapply_type': notif_reapply_type,
        'notif_reapply_id': notif_reapply_id,
    }
    return render(request, 'notifications.html', context)


@login_required
def cancel_donor(request, donor_id):
    donor = get_object_or_404(Donor, pk=donor_id, user=request.user, cancelled=False)
    now = timezone.now()
    if (now - donor.created_at) > timedelta(minutes=3):
        messages.error(request, "Cancellation window exceeded (after 24 hours).")
        return redirect('notifications')

    donor.cancelled = True
    donor.cancelled_at = now
    donor.save()

    # Create notification for the donor who cancelled
    Notification.objects.create(
        user=request.user,
        notif_type='info',
        message=f"You have successfully cancelled your donor application for {donor.organ.organ_name}.",
        donor=donor
    )

    # Notify matched recipient and cancel their application so both can reapply
    if donor.matched:
        match = MatchedTransplantation.objects.filter(donor=donor).first()
        if match and match.recipient:
            recipient = match.recipient
            Notification.objects.create(
                user=recipient.user,
                notif_type='reapply',
                message=f"Your donor for {donor.organ.organ_name} has cancelled their registration. We are finding a new donor for you. To reapply, click the button below.",
                recipient=recipient
            )
            if not recipient.cancelled:
                recipient.cancelled = True
                recipient.cancelled_at = now
                recipient.save()

    messages.success(request, f"You have cancelled your donor application for {donor.organ.organ_name}.")
    return redirect('notifications')


@login_required
def cancel_recipient(request, recipient_id):
    recip = get_object_or_404(Recipient, pk=recipient_id, user=request.user, cancelled=False)
    now = timezone.now()
    if (now - recip.created_at) > timedelta(minutes=3):
        messages.error(request, "Cancellation window exceeded (after 24 hours).")
        return redirect('notifications')

    recip.cancelled = True
    recip.cancelled_at = now
    recip.save()

    # Create notification for the recipient who cancelled
    Notification.objects.create(
        user=request.user,
        notif_type='info',
        message=f"You have successfully cancelled your recipient application for {recip.organ.organ_name}.",
        recipient=recip
    )

    # Notify matched donor and cancel their application so both can reapply
    if recip.matched:
        match = MatchedTransplantation.objects.filter(recipient=recip).first()
        if match and match.donor:
            donor = match.donor
            Notification.objects.create(
                user=donor.user,
                notif_type='reapply',
                message=f"Your recipient for {recip.organ.organ_name} has cancelled their registration. We are finding a new recipient for you. To reapply, click the button below.",
                donor=donor
            )
            if not donor.cancelled:
                donor.cancelled = True
                donor.cancelled_at = now
                donor.save()

    messages.success(request, f"You have cancelled your recipient application for {recip.organ.organ_name}.")
    return redirect('notifications')


@login_required
def reapply_donor(request, donor_id):
    old = get_object_or_404(Donor, pk=donor_id)
    if not old.cancelled:
        messages.warning(request, "You can only reapply after cancellation.")
        return redirect('notifications')

    # Limit 4 uncancelled attempts
    active_attempts = Donor.objects.filter(user=request.user, cancelled=False).count()
    if active_attempts >= 4:
        messages.error(request, "You have already used all 4 donor attempts. Please cancel one to reapply. If cancellation unavailable,contact us.")
        return redirect('notifications')

    Donor.objects.create(
        user=old.user,
        organ=old.organ,
        name=old.name,
        age=old.age,
        blood_group=old.blood_group,
        # If you want to copy files too, you could assign old.aadhar_image, old.blood_report
        aadhar_image=getattr(old, 'aadhar_image', None),
        blood_report=getattr(old, 'blood_report', None),
        contact=old.contact,
        matched=False,
        cancelled=False
    )
    Notification.objects.filter(user=old.user, notif_type='reapply', donor=old).update(is_read=True)
    messages.success(request, f"You have reapplied as a donor for {old.organ.organ_name}.")
    return redirect('notifications')


@login_required
def reapply_recipient(request, recipient_id):
    old = get_object_or_404(Recipient, pk=recipient_id)
    if not old.cancelled:
        messages.warning(request, "You can only reapply after cancellation.")
        return redirect('notifications')

    # Limit 4 uncancelled attempts
    active_attempts = Recipient.objects.filter(user=request.user, cancelled=False).count()
    if active_attempts >= 4:
        messages.error(request, "You have already used all 4 recipient attempts. Please cancel one to reapply. If cancellation unavailable,contact us.")
        return redirect('notifications')

    Recipient.objects.create(
        user=old.user,
        organ=old.organ,
        name=old.name,
        age=old.age,
        blood_group=old.blood_group,
        aadhar_image=getattr(old, 'aadhar_image', None),
        blood_report=getattr(old, 'blood_report', None),
        contact=old.contact,
        matched=False,
        cancelled=False
    )
    Notification.objects.filter(user=old.user, notif_type='reapply', recipient=old).update(is_read=True)
    messages.success(request, f"You have reapplied as a recipient for {old.organ.organ_name}.")
    return redirect('notifications')


@login_required
def become_donor(request, organ_id):
    organ = get_object_or_404(Organ, pk=organ_id)

    # Limit 4 uncancelled attempts
    active_attempts = Donor.objects.filter(user=request.user, cancelled=False).count()
    if active_attempts >= 4:
        messages.error(request, "You have already used your 4 donor attempts. Please cancel one before reapplying. If cancellation unavailable,contact us at +91 123 456 7890.")
        return redirect('notifications')

    if request.method == 'POST':
        # Include request.FILES for file uploads
        form = DonorForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.organ = organ
            donor.save()

            compatible_recipient_groups = compatibility.get(donor.blood_group, [])
            # Exclude recipients already matched with this user's previous donors
            recipient_user_ids_to_exclude = MatchedTransplantation.objects.filter(
                donor__user=request.user
            ).values_list('recipient__user_id', flat=True)

            unmatched_recipient = Recipient.objects.filter(
                organ=donor.organ,
                blood_group__in=compatible_recipient_groups,
                matched=False,
                cancelled=False
            ).exclude(
                user__in=recipient_user_ids_to_exclude
            ).exclude(
                pk__in=MatchedTransplantation.objects.values_list('recipient_id', flat=True)
            ).order_by('pk').first()

            if unmatched_recipient:
                match = MatchedTransplantation.objects.create(
                    donor_name=donor.name,
                    recipient_name=unmatched_recipient.name,
                    organ=donor.organ,
                    donor_blood_group=donor.blood_group,
                    recipient_blood_group=unmatched_recipient.blood_group,
                    donor=donor,
                    recipient=unmatched_recipient,
                )
                donor.matched = True
                unmatched_recipient.matched = True
                donor.save()
                unmatched_recipient.save()
                
                # Create notification for the donor
                Notification.objects.create(
                    user=donor.user,
                    notif_type='match',
                    message=f"Great news! You have been matched as a donor for {organ.organ_name}. Transplantation ID: {match.transplantation_id}.",
                    donor=donor,
                    is_read=False
                )
                
                # Create notification for the recipient
                Notification.objects.create(
                    user=unmatched_recipient.user,
                    notif_type='match',
                    message=f"Great news! A donor has been found for your {organ.organ_name} request. Transplantation ID: {match.transplantation_id}.",
                    recipient=unmatched_recipient,
                    is_read=False
                )
                
                messages.success(request, f"Thank you {request.user.username}, registered as donor for {organ.organ_name}! Transplantation ID: {match.transplantation_id}")
            else:
                messages.success(request, f"Thank you {request.user.username}, registered as donor for {organ.organ_name}! No current matching recipient yet.")
        else:
            messages.error(request, "Please fix errors below.")
    else:
        form = DonorForm(user=request.user)

    return render(request, 'donor_form.html', {'form': form, 'organ': organ})


@login_required
def become_recipient(request, organ_id):
    organ = get_object_or_404(Organ, pk=organ_id)

    # Limit 4 uncancelled attempts
    active_attempts = Recipient.objects.filter(user=request.user, cancelled=False).count()
    if active_attempts >= 4:
        messages.error(request, "You have already used your 4 recipient attempts. Please cancel one before reapplying. If cancellation unavailable,contact us at +91 123 456 7890.")
        return redirect('notifications')

    if request.method == 'POST':
        # Include request.FILES for file uploads
        form = RecipientForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            recipient = form.save(commit=False)
            recipient.user = request.user
            recipient.organ = organ
            recipient.save()

            compatible_donor_groups = [bg for bg, recips in compatibility.items() if recipient.blood_group in recips]
            # Exclude donors already matched with this user's previous recipients
            donor_user_ids_to_exclude = MatchedTransplantation.objects.filter(
                recipient__user=request.user
            ).values_list('donor__user_id', flat=True)

            unmatched_donor = Donor.objects.filter(
                organ=recipient.organ,
                blood_group__in=compatible_donor_groups,
                matched=False,
                cancelled=False
            ).exclude(
                user__in=donor_user_ids_to_exclude
            ).exclude(
                pk__in=MatchedTransplantation.objects.values_list('donor_id', flat=True)
            ).order_by('pk').first()

            if unmatched_donor:
                match = MatchedTransplantation.objects.create(
                    donor_name=unmatched_donor.name,
                    recipient_name=recipient.name,
                    organ=recipient.organ,
                    donor_blood_group=unmatched_donor.blood_group,
                    recipient_blood_group=recipient.blood_group,
                    donor=unmatched_donor,
                    recipient=recipient,
                )
                unmatched_donor.matched = True
                recipient.matched = True
                unmatched_donor.save()
                recipient.save()
                
                # Create notification for the donor
                Notification.objects.create(
                    user=unmatched_donor.user,
                    notif_type='match',
                    message=f"Great news! You have been matched with a recipient for {organ.organ_name}. Transplantation ID: {match.transplantation_id}.",
                    donor=unmatched_donor,
                    is_read=False
                )
                
                # Create notification for the recipient
                Notification.objects.create(
                    user=recipient.user,
                    notif_type='match',
                    message=f"Great news! A donor has been found for your {organ.organ_name} request. Transplantation ID: {match.transplantation_id}.",
                    recipient=recipient,
                    is_read=False
                )
                
                messages.success(request, f"Thank you {request.user.username}, your request for {organ.organ_name} has been recorded! Transplantation ID: {match.transplantation_id}")
            else:
                messages.success(request, f"Thank you {request.user.username}, your request for {organ.organ_name} has been recorded! No current matching donor yet.")
        else:
            messages.error(request, "Please fix errors below.")
    else:
        form = RecipientForm(user=request.user)

    return render(request, 'recipient_form.html', {'form': form, 'organ': organ})


@login_required
def acknowledgment_view(request, transplantation_id):
    match = get_object_or_404(MatchedTransplantation, transplantation_id=transplantation_id)
    if (
        (match.donor and match.donor.user == request.user) or
        (match.recipient and match.recipient.user == request.user)
    ):
        if match.donor and match.donor.user == request.user:
            role = "donor"
            username = match.donor.user.username
        else:
            role = "recipient"
            username = match.recipient.user.username

        generated_datetime = timezone.now().strftime('%A, %B %d, %Y')
        return render(request, 'acknowledgment.html', {
            "match": match,
            "role": role,
            "username": username,
            "generated_datetime": generated_datetime,
        })
    return redirect('home_page')
