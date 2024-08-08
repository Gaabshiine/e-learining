# middleware.py

from django.shortcuts import redirect
from django.urls import reverse
import re

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Paths that do not require login
        user_public_paths = [
            reverse('account_app:login'),
            reverse('account_app:admin_login'),
            reverse('account_app:add_admin'),
            reverse('account_app:admin_register'),
            reverse('account_app:admin_register'),
            reverse('account_app:add_student_by_user'),
            reverse('account_app:add_student_from_slider'),
            

            # Add other paths that should be accessible without login
        ]


        # dynamic_skip_patterns = [
        #     re.compile(r'^/account/password_reset_form/[^/]+/[^/]+/$'),
        # ]

        # Check if request path is in skip_paths or matches dynamic patterns
        if request.path in user_public_paths:
            return self.get_response(request)

        # Check if request path requires login
        if request.path.startswith('/account/') or request.path.startswith('/student_dashboard/'):
            if not request.session.get('student_id') and not request.session.get('admin_id'):
                return redirect(reverse('account_app:login'))

        return self.get_response(request)
