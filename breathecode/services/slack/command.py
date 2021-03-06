import re, sys, logging, inspect
from breathecode.services.slack import commands
from breathecode.authenticate.models import ProfileAcademy

logger = logging.getLogger(__name__)

def command(only=None):        
    def decorator(function):
        def wrapper(*args, **kwargs):
            print(kwargs)
            if "context" not in kwargs or kwargs["context"] is None:
                raise Exception("Missing scope information on slack command")
            context = kwargs["context"]

            profiles = None
            if only == "staff":
                profiles = ProfileAcademy.objects.filter(user__slackuser__slack_id=context['user_id'], academy__slackteam__slack_id=context['team_id']).values_list('academy__id', flat=True)
                if len(profiles) == 0:
                    raise Exception(f"Your user {context['user_id']} don't have permissions to query this student, are you a staff on this academy?")

            kwargs["academies"] = profiles
            kwargs["user_id"] = context['user_id']
            kwargs["team_id"] = context['team_id']
            kwargs["channel_id"] = context['channel_id']
            kwargs["text"] = context['text']

            result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator