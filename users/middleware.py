from django.utils.translation import activate

class UserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            language = getattr(request.user, 'language', 'ru')
            activate(language)
        else:
            activate('ru')

        return self.get_response(request)
