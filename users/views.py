from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view


from .forms import SignUpForm
from .models import User

@api_view(['POST'])
def signUpView(request):
    print("signUpView st----:",request.data)
    p_email = request.data.get('email', '')
    p_password = request.data.get('password', '')
    p_team_id=request.data.get('team_id', '')
    print(p_email, p_password)
    data={
        'email':p_email,
        'password1':p_password,
        'password2':p_password,
    }
    form = SignUpForm(data)

    if form.is_valid():
        print("signUpView form valid----")
        
        #username = form.cleaned_data.get('username')
        form_data=form.cleaned_data
        email = form_data.get('email')
        username=email.split('@')[0]
        if len(username)<2: return
        #project=form_data.get('project')
        #raw_password = form_data.get('password')
        raw_password = p_password

        # u = User(
        #     email = email,
        #     username = username,
        #     project = project,
        #     password = raw_password
        # )
        # u.save()
        
        new_user = form.save(commit=False)
        new_user.email = email
        new_user.username=username
        new_user.team_id = p_team_id
        #new_user.project=project
        new_user.password=raw_password

        new_user.save() 

        return Response({"signup": 'done'})

    return Response({"signup": 'error'})
            #form.save()
            #print('username:',username)
            #print('pj:',form.cleaned_data)
            #user = authenticate(username=username, password=raw_password)
    #             login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
    #             return redirect('/')
    # else:
    #     form = SignUpForm()
    # return render(request, 'signup.html', {'form': form})