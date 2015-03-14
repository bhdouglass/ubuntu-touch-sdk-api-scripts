from django.shortcuts import render_to_response
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.template import RequestContext
from django import forms
import woc

APP_OPTIONS = (
    ('--store-session-cookies', 'Store cookies'),
    ('--enable-addressbar', 'Show header'),
    ('--enable-back-forward', 'Show back and forward buttons'),
    ('--fullscreen', 'Run fullscreen'),
)


class WebappForm(forms.Form):
    displayname = forms.CharField(
        max_length=200, required=True, label='App name',
        help_text='ex. Duck Duck Go')
    url = forms.URLField(
        max_length=200, required=True, label='Webapp URL',
        help_text='ex. https://duckduckgo.com')
    icon = forms.FileField(
        required=True, label='App icon',
        help_text='Recommended 256x256 px, png format')
    options = forms.MultipleChoiceField(
        choices=APP_OPTIONS,
        label="App options", help_text='Use CTRL to select multiple options',
        required=False)
    nickname = forms.RegexField(
        regex='^[\w-]+$', max_length=200, required=True,
        label='Developer namespace',
        help_text='The namespace you picked for your \
            <a href="https://myapps.developer.ubuntu.com \
            /dev/account/">MyApps account</a>')
    fullname = forms.CharField(
        max_length=200, required=True, label='Maintainer full name',
        help_text='ex. Miao Tian')
    email = forms.EmailField(
        max_length=200, required=True, label='Maintainer email',
        help_text='ex. miaotian@ubuntu.com')


def webapp(request):
    if request.method == 'POST':
        webapp_form = WebappForm(request.POST, request.FILES)
        if webapp_form.is_valid():
            tmp, click_name, click_path = woc.create(webapp_form.cleaned_data)
            click_file = FileWrapper(open(click_path))
            response = HttpResponse(click_file,
                                    content_type="application/x-click")
            response['Content-Disposition'] = 'attachment; filename=%s' % (
                click_name,)
            return response
    else:
        webapp_form = WebappForm()
    return render_to_response(
        'webapp.html',
        {'webapp_form': webapp_form},
        context_instance=RequestContext(request))
