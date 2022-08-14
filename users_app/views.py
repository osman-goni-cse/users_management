from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


from .forms import RegisterForm, LoginForm, UpdateProfileForm, UpdateUserForm


@login_required
def profile(request):
  user_form = UpdateUserForm()
  profile_form = UpdateProfileForm()
  if request.method == 'POST':
    user_form = UpdateUserForm(request.POST, instance=request.user)
    profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request, 'Your profile is updated successfully')
      return redirect(to='users-profile')
    else:
      user_form = UpdateUserForm(instance=request.user)
      profile_form = UpdateProfileForm(instance=request.user.profile)

  return render(request, 'users_app/profile.html', {'user_form': user_form, 'profile_form': profile_form})

def RegisterView(request):
  if request.user.is_authenticated:
    return redirect('/')
  form = RegisterForm()

  if request.method == 'POST':
    form = RegisterForm(request.POST or None)

    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      
      messages.success(request, f'Account created for {username}')
      return redirect('/')

  data = {
    'form': form,
  }

  return render(request, 'users_app/register.html', data)

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
def home(request):
  return render(request, 'users_app/home.html')