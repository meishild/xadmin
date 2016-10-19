import sys
from django.template.context import RequestContext


def get_context_dict(context):
    """
     Contexts in django version 1.9+ must be dictionaries. As xadmin has a legacy with older versions of django,
    the function helps the transition by converting the [RequestContext] object to the dictionary when necessary.
    :param context: RequestContext
    :return: dict
    """
    if isinstance(context, RequestContext):
        ctx = {}
        if sys.version < '3':
            map(ctx.update, context.dicts)
        else:
            list(map(ctx.update, context.dicts))
    else:
        ctx = context
    return ctx
