def identity_verified(user):
    return True
    from django.contrib import messages
    if not user.profile.identity_verified or not user.profile.id_back_scanned or not user.profile.id_front_scanned:
        from feed.middleware import get_current_request
        messages.warning(get_current_request(), 'You need to verify your identity before you may see this page.')
        return False
    return True

def identity_really_verified(user):
    from django.utils import timezone
    import datetime
    from django.conf import settings
    v = user.verifications.filter(submitted__gte=timezone.now() - datetime.timedelta(hours=settings.SIG_VALID_HOURS), verified=True).order_by('-submitted').first()
    if not (user.profile.identity_verified or (v and v.verified)):
        from django.contrib import messages
        from feed.middleware import get_current_request
        messages.warning(get_current_request(), 'You need to verify your identity before you may see this page.')
        return False
    return True
