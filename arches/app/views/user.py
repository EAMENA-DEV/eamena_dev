'''
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
import django.contrib.auth.password_validation as validation
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.generic import View
from arches.app.models import models
from arches.app.models.system_settings import settings
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from arches.app.views.base import BaseManagerView
from arches.app.utils.forms import ArchesUserProfileForm
from arches.app.utils.JSONResponse import JSONResponse

class UserManagerView(BaseManagerView):

    def get(self, request):

        context = self.get_context_data(
            main_script='views/user-profile-manager',
        )

        context['nav']['icon'] = "fa fa-user"
        context['nav']['title'] = _("Profile Manager")
        context['nav']['login'] = True
        context['nav']['help'] = (_('Profile Editing'),'help/profile-manager-help.htm')
        context['validation_help'] = validation.password_validators_help_texts()
        return render(request, 'views/user-profile-manager.htm', context)

    def post(self, request):

        context = self.get_context_data(
            main_script='views/user-profile-manager',
        )
        context['errors'] = []
        context['nav']['icon'] = 'fa fa-user'
        context['nav']['title'] = _('Profile Manager')
        context['nav']['login'] = True
        context['nav']['help'] = (_('Profile Editing'),'help/profile-manager-help.htm')
        context['validation_help'] = validation.password_validators_help_texts()


        user_info = request.POST.copy()
        user_info['id'] = request.user.id
        user_info['username'] = request.user.username

        form = ArchesUserProfileForm(user_info)
        if form.is_valid():
            user = form.save()
            try:
                admin_info = settings.ADMINS[0][1] if settings.ADMINS else ''
                message = _('Your arches profile was just changed.  If this was unexpected, please contact your Arches administrator at %s.' % (admin_info))
                user.email_user(_('You\'re Arches Profile Has Changed'), message)
            except:
                pass
            request.user = user
        context['form'] = form

        return render(request, 'views/user-profile-manager.htm', context)

class GroupUsers(View):

    def post(self, request):
        res = {}
        users = []
        identity_type = request.POST.get('type')
        identity_id = request.POST.get('id')
        if identity_type == 'group':
            group = Group.objects.get(id=identity_id)
            users = group.user_set.all()
        else:
            users = User.objects.filter(id=identity_id)

        if len(users) > 0:
            res = [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'last_login': user.last_login, 'username': user.username, 'groups': [group.id for group in user.groups.all()] } for user in users]
        return JSONResponse(res)
