# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse

import views
import utils

class YadisMiddleware:
  def process_request(self, request):
      if 'application/xrds+xml' in request.META.get('HTTP_ACCEPT', ''):
          return views.yadis(request)
  
  def process_response(self, request, response):
      if response.status_code >= 200 and response.status_code < 300:
          response['X-XRDS-Location'] = utils.absolute_url(reverse(views.yadis))
      return response