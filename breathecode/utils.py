import logging
from rest_framework.views import exception_handler
from breathecode.authenticate.models import ProfileAcademy
from django.contrib.auth.models import AnonymousUser
logger = logging.getLogger(__name__)

def localize_query(query, request, matcher=None):

    # not a part of the staff, cannot access all info
    if isinstance(request.user, AnonymousUser):
        return query
    
    if request.user.is_staff == True:
        return query

    academy_ids = ProfileAcademy.objects.filter(user=request.user).values_list('academy__id', flat=True)
    kwargs = {}
    if matcher is None:
        kwargs["academy__id__in"] = academy_ids
    else:
        kwargs[matcher] = academy_ids

    logger.debug(f"Localizing academies: [{','.join([ str(i) for i in academy_ids])}]")
    # only cohorts from that academy
    query = query.filter(**kwargs)

    return query

def breathecode_exception_handler(exc, context):
    # This is to be used with the Django REST Framework (DRF) as its
    # global exception handler.  It replaces the POST data of the Django
    # request with the parsed data from the DRF.  This is necessary
    # because we cannot read the request data/stream more than once.
    # This will allow us to see the parsed POST params in the rollbar
    # exception log.

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    context['request']._request.POST = context['request'].data
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.

    if response is not None:
        if isinstance(response.data, list):
            if response.data[0].code != 'invalid':
                response.data = { 'status_code': response.data[0].code, 'details': str(response.data[0]) }
            else:
                response.data = { 'status_code': 500, 'details': str(response.data[0]) }
        else:
            response.data['status_code'] = response.status_code

    return response

