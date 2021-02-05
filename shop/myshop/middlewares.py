from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class PracticeMiddleware(MiddlewareMixin):
	def process_request(self, request):
		if 'click' in request.session:
			if request.session['click'] > 2:
				logout(request)
				return redirect('/login/')
			
