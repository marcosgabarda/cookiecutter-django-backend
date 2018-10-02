from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.views import View


class PreviewEmailView(LoginRequiredMixin, View):
    """Preview only for staff users."""

    @staticmethod
    def get(request):
        if not request.user.is_staff:
            raise Http404

        # 1. Create an instance from a TemplateEmailMessage child
        # context = {"user": request.user}
        # email = TemplateEmailMessage(to="name@example.com", context=context)

        # 2. Call method .preview() an make it the argument for HttpResponse
        # return HttpResponse(email.preview())
