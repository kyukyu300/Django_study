from urllib.parse import urlencode, parse_qs
from django.utils.crypto import get_random_string
import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.core import signing
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import RedirectView
from member.forms import NicknameForm

User = get_user_model()

NAVER_CALLBACK_URL = '/oauth/naver/callback'
NAVER_STATE = 'naver_login'
NAVER_LOGIN_URL = 'https://nid.naver.com/oauth2.0/authorize'
NAVER_TOKEN_URL = 'https://nid.naver.com/oauth2.0/token'
NAVER_PROFILE_URL = 'https://openapi.naver.com/v1/nid/me'

GITHUB_CALLBACK_URL = '/oauth/github/callback'
GITHUB_STATE = 'github_login'
GITHUB_LOGIN_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_PROFILE_URL = 'https://api.github.com/user'


class NaverLoginRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        domain = self.request.scheme + '://' + self.request.META.get('HTTP_HOST', '')
        callback_url = domain + NAVER_CALLBACK_URL
        state = signing.dumps(NAVER_STATE)

        params = {
            'response_type': 'code',
            'client_id': settings.NAVER_CLIENT_ID,
            'redirect_uri': callback_url,
            'state': state
        }

        return f'{NAVER_LOGIN_URL}?{urlencode(params)}'


def naver_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    if not code or not state:
        return HttpResponseBadRequest("code 또는 state 없음")

    if NAVER_STATE != signing.loads(state):
        raise Http404

    access_token = get_naver_access_token(code, state)
    request.session['access_token'] = access_token  # 세션에 저장

    profile = get_naver_profile(access_token)
    email = profile.get('email')

    if not email:
        return HttpResponseBadRequest("네이버 프로필에 이메일이 없습니다")

    user = User.objects.filter(email=email).first()
    if user:
        if not user.is_active:
            user.is_active = True
            user.save()

        login(request, user)
        return redirect('main')

    return redirect(reverse('oauth:nickname') + f'?access_token={access_token}&oauth=naver')  # 이제 access_token은 세션에 있으므로 GET 파라미터 필요 없음


class GithubLoginRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        domain = self.request.scheme + '://' + self.request.META.get('HTTP_HOST', '')

        callback_url = domain + GITHUB_CALLBACK_URL
        state = signing.dumps(GITHUB_STATE)

        params = {
            'response_type': 'code',
            'client_id': settings.GITHUB_CLIENT_ID,
            'redirect_uri': callback_url,
            'state': state
        }

        return f'{GITHUB_LOGIN_URL}?{urlencode(params)}'


def github_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    if GITHUB_STATE != signing.loads(state):
        raise Http404

    access_token = get_github_access_token(code, state)

    print(access_token)
    if not access_token:
        raise Http404

    profile_response = get_github_profile(access_token)

    print('profile request', profile_response)
    email = profile_response.get('email')

    user = User.objects.filter(email=email).first()

    if user:
        if not user.is_active:
            user.is_active = True
            user.save()

        login(request, user)
        return redirect('main')
    return redirect(
        reverse('oauth:nickname') + f'?access_token={access_token}&oauth=github'
    )

def get_github_access_token(code, state):
    params = {
        'grant_type': 'authorization_code',
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_SECRET,
        'code': code,
        'state': state
    }

    response = requests.get(GITHUB_TOKEN_URL, params=params)

    response_str = response.content.decode()
    response_dict = parse_qs(response_str)

    access_token = response_dict.get('access_token', [])[0]

    return access_token


def get_github_profile(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(GITHUB_PROFILE_URL, headers=headers)

    if response.status_code != 200:
        raise Http404

    result = response.json()

    if not result.get('email'):
        result['email'] = f'{result["login"]}@id.github.com'
    return result

def oauth_nickname(request):
    access_token = request.session.get('access_token')
    oauth = request.GET.get('oauth')

    if not access_token or oauth not in ['github', 'naver']:
        return redirect('login')

    profile = get_naver_profile(access_token)
    email = profile.get('email')

    if not email:
        return HttpResponseBadRequest("이메일 없음")

    if User.objects.filter(email=email).exists():
        raise Http404  # 이미 존재하면 에러

    form = NicknameForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)

        if oauth == 'github':
            profile = get_github_profile(access_token)
        else:
            profile = get_naver_profile(access_token)

        user.email = email
        user.is_active = True
        user.set_password(get_random_string(length=12))
        user.save()

        login(request, user)
        return redirect('main')

    return render(request, 'auth/nickname.html', {'form': form})


def get_naver_access_token(code, state):
    params = {
        'grant_type': 'authorization_code',
        'client_id': settings.NAVER_CLIENT_ID,
        'client_secret': settings.NAVER_SECRET,
        'code': code,
        'state': state
    }

    response = requests.get(NAVER_TOKEN_URL, params=params)
    result = response.json()
    print('[DEBUG] token response:', result)
    return result.get('access_token')


def get_naver_profile(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(NAVER_PROFILE_URL, headers=headers)
    if response.status_code != 200:
        raise Http404

    result = response.json()
    print('[DEBUG] profile response:', result)

    return result.get('response')
