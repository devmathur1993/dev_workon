from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views import View
from bridge.models import MaintainSession
import jwt
import base64
import sys


class BridgeGateway(View):
    def get(self, request, link):

        response = self.stipulate_connection(request, link)
        if response['responseKey'] == 'User_authenticated':
            try:
                return render(request, 'bridge/index.html', context=response)
               #return HttpResponseRedirect('/' + response['path'] + 'id=' + response['xid'] + '/')
            except:
                return HttpResponse(response['path'])
        else:
            return render(request, 'bridge/index.html', context=response)

    def stipulate_connection(self, request, link):
        try:
            decoded = jwt.decode(link, 'alskDJFHgqpwoeiRUTYVBCNmzx', algorithms=['HS256'])
        except jwt.InvalidTokenError:
            response = {'responseKey': 'Invalid request please try again !'}
            return response

        id = decoded['uid']
        path = decoded['path']
        xid = decoded['param']
        session_var = MaintainSession
        is_link_valid = session_var.objects.filter(pk_session_key=id, link_used=1).values('pk_session_key')

        if is_link_valid.count() is 0:
            response = {'responseKey': 'Your Link has been expired'}
            return response
        else:
            update_session_model = session_var.objects.filter(pk_session_key=id, link_used=1).update(link_used='0')
            response = AuthenticateUser().fetch_user_details(request, id, path, xid)
        return response


class AuthenticateUser():

    def fetch_user_details(self, request, user_id, path, xid):
        session_var = MaintainSession
        get_user = session_var.objects.filter(pk_session_key=user_id).values('pk_session_key', 'username', 'useremail')
        if get_user.count() is 0:
            response = {'responseKey': 'user does not exist'}
            return response
        else:
            for itr in get_user:
                session_key = itr['pk_session_key']
                user_name = str(itr['username'])
                user_email = str(itr['useremail'])

            valid_user = self.do_authentication(request, session_key, user_name, user_email)

            if valid_user is not None:
                if request.user.is_authenticated:
                    request.session['userid'] = session_key
                    request.session['username'] = user_name
                    request.session['email'] = user_email

                    response = {'responseKey': 'User_authenticated','userid':session_key, 'username':user_name,'email':user_email,'path': path, 'xid': xid}
            else:
                response = {'responseKey': 'user is not validated'}

            return response

    def do_authentication(self, request, session_key, user_name, user_email):
        try:
            user = User.objects.get(username=user_name)
        except:
            user = User.objects.create_user(user_name, user_email, session_key)
            user.save()

        valid_user = authenticate(username=user_name, password=session_key)
        login(request, valid_user)
        return valid_user
