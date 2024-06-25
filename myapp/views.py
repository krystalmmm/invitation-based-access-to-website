from django.shortcuts import render, redirect
from .models import InvitationCode
from .forms import InvitationCodeForm
from django.utils.timezone import now
from django.contrib import messages

# Create your views here.
# Get client's IP address
def get_client_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = request.META.get('REMOTE_ADDR')
  return ip


# Input invitation code, check the code, if right, redirect to the corresponding page
def index(request):
  session_key = "user_ip_{}".format(get_client_ip(request))
  # if user IP address is in session, and = TRUE, display hidden content
  if session_key in request.session and request.session[session_key]:
    return render(request, "myapp/index.html")
  else:
    form = InvitationCodeForm()
    return render(request, "myapp/index.html", {"form": form,})


# Verify user invitation code. Right invite code then set up session key as user IP, value=TRUE, conversation lasts for 60 seconds
def code_verify(request):
  session_key = "user_ip_{}".format(get_client_ip(request))
  if request.method == "POST":
    code = request.POST.get("code", "")
    code_obj = InvitationCode.objects.filter(code=code, expire__gt=now()).first()
    if code_obj:
      request.session[session_key] = True
      request.session.set_expiry(60) # Conversation valid for 60 seconds. Re-submit invite code after 60 seconds
      messages.success(request, 'You have a valid invitation code. This conversation will be valid for 60 seconds.')
    else:
      messages.warning(request, 'Your invite code is wrong or expired. Please try again.')
      if session_key in request.session:
        del request.session[session_key]

  return redirect("/")
