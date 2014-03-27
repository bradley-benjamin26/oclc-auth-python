# -*- coding: utf-8 -*-

###############################################################################
# Copyright 2014 OCLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

"""Class represents and authentication code object

HMAC Requests, which are strictly server side, use an Authenication Code object to store their parameters
and perform hashing.

"""

from urlparse import urlparse
import urllib

AUTHORIZATION_SERVER = 'https://authn.sd00.worldcat.org/oauth2'


class InvalidParameter(Exception):
    """Custom exception - invalid parameter was passed to class"""

    def __init__(self, message):
        self.message = message


"""Class begins here"""


class AuthCode(object):
    """Class represents an authentication code object.

    Organizes the parameters and produces a request url so that an authentication code can be obtained
    from OCLC's servers.

    Class Variables:
        authorization_server          string   the oclc server that conducts authentication
        client_id                     string   the public portion of the Web Services Key (WSKey)
        authenticating_institution_id string   the institutionID that is authenticated against
        context_institution_id        string   the institutionID that the request is made against
        redirect_uri                  string   the redirect_uri for the request
        scopes                        list     a list of one or more web services
    """
    authorization_server = AUTHORIZATION_SERVER
    client_id = None
    authenticating_institution_id = None
    context_institution_id = None
    redirect_uri = None
    scopes = None

    def __init__(self,
                 client_id=None,
                 authenticating_institution_id=None,
                 context_institution_id=None,
                 redirect_uri=None,
                 scopes=None):
        """Constructor.

        Args:
            client_id: string, the public portion of the Web Services Key (WSKey)
            authenticating_institution_id: string, the institutionID that is authenticated against
            context_institution_id: string, the institutionID that the request is made against
            redirect_uri: string, the redirect_uri for the request
            scopes: list, a list of one or more web services
        """

        self.client_id = client_id
        self.authenticating_institution_id = authenticating_institution_id
        self.context_institution_id = context_institution_id
        self.redirect_uri = redirect_uri
        self.scopes = scopes

        if self.client_id == None:
            raise InvalidParameter('Required option missing: client_id.')
        elif self.client_id == '':
            raise InvalidParameter('Cannot be empty string: client_id.')

        if self.authenticating_institution_id == None:
            raise InvalidParameter('Required option missing: authenticating_institution_id.')
        elif self.authenticating_institution_id == '':
            raise InvalidParameter('Cannot be empty string: authenticating_institution_id.')

        if self.context_institution_id == None:
            raise InvalidParameter('Required option missing: context_institution_id.')
        elif self.context_institution_id == '':
            raise InvalidParameter('Cannot be empty string: context_institution_id.')

        if self.redirect_uri == None:
            raise InvalidParameter('Required option missing: redirect_uri.')
        elif self.redirect_uri == '':
            raise InvalidParameter('Cannot be empty string: redirect_uri.')
        else:
            scheme = urlparse("".join(self.redirect_uri)).scheme
            if scheme != 'http' and scheme != 'https':
                raise InvalidParameter('Invalid redirect_uri. Must begin with http:// or https://')

        if self.scopes == None or self.scopes == '':
            raise InvalidParameter(
                'Required option missing: scopes. Note scopes must be a list of one or more scopes.')
        elif len(self.scopes) == 0 or self.scopes[0] == None or self.scopes[0] == '':
            raise InvalidParameter('You must pass at least one valid scope')


    def get_login_url(self):
        """Returns a login url based on the auth code parameters."""
        return (
            AuthCode.authorization_server + '/authorizeCode' +
            '?' + 'authenticatingInstitutionId=' + self.authenticating_institution_id +
            '&' + 'client_id=' + self.client_id +
            '&' + 'contextInstitutionId=' + self.context_institution_id +
            '&' + urllib.urlencode({'redirect_uri': self.redirect_uri}) +
            '&' + 'response_type=code' +
            '&' + 'scope=' + " ".join(self.scopes)
        )

    def __str__(self):
        ret = ''
        ret += '\tauthorization_server: ' + str(self.authorization_server) + "\n"
        ret += '\tclient_id: ' + str(self.client_id) + "\n"
        ret += '\tauthenticating_institution_id: ' + str(self.authenticating_institution_id) + "\n"
        ret += '\tcontext_institution_id: ' + str(self.context_institution_id) + "\n"
        ret += '\tredirect_uri: ' + str(self.redirect_uri) + "\n"
        ret += '\tscopes: ' + str(self.scopes) + "\n"

        return ret
