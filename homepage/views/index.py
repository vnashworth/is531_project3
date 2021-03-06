from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login

############### LOGIN USER ###############
@view_function
def process_request(request):
    '''Logs in a user using a form'''

    #if user is already logged in, send to asset page
    if request.user.is_authenticated():
        return HttpResponseRedirect('/assets')

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #login user
            login(request, form.user)
            return HttpResponseRedirect('/assets')

    context = {
        'form' : form,
    }

    return request.dmp_render('index.html', context)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', required=True, max_length=100, widget=forms.TextInput(attrs={ 'class': 'form-control' }))
    password = forms.CharField(label='Password', required=True, max_length=100, widget=forms.PasswordInput(attrs={ 'class': 'form-control' }))

    def clean(self):
        user = authenticate(username = self.cleaned_data.get('username'), password = self.cleaned_data.get('password'))
        if user == None:
            raise forms.ValidationError('The username and password was not found.')
        self.user = user
        return self.cleaned_data
