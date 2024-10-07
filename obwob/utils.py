from django.shortcuts import render


# encapsulated views.py functionality with exception rendering custom error page
def get_object_or_error(request, model, object_id, template_path, extra_context=None, event_name=None):
    try:
        object = model.objects.get(pk=object_id)
        context_key = model.__name__.lower()
        context = {context_key: object}

        # merge extra_context, if provided, into context
        if extra_context:
            context.update(extra_context)

        return render(request, f"obwob/{template_path}", context)
    
    except model.DoesNotExist:
        requested_object = model.__name__.lower()
        return render(request, "obwob/404.html", {
            'error_message': f'Sorry, that {requested_object} does not exist.'
        })