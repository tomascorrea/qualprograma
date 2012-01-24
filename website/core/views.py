from django.template import Context, loader, RequestContext
from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


def home(request):
    template = loader.get_template('core/home.html')
    context = {}
    return HttpResponse(template.render(RequestContext(request,context)))
    
