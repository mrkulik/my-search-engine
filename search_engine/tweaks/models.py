from django.shortcuts import _get_queryset


def get_object_or_None(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except klass.DoesNotExist:
        return None
