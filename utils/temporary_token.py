"""
    Created by: @pdonaire1 October 06, 2016
    Ing. Pablo Alejandro González Donaire
    depends of python-dateutil
"""
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import hashlib
import base64
import datetime
import dateutil.parser

class TemporaryToken:
    """
        Class for create limited or unlimited token from an user.
        created by: @pdonaire1 05-10-2016
    """
    def __init__(self, user):
        self.user = user
        
    def hash_user_encode(self, hours_limit=None, extra_token=''):
        """
            This method allow create a temporary or unlimited token 
            for users.
            hours_limit => int(24) for 1 day
            extra_token => a string value for more security
                This extra token not support the next caracter: "|"
        """
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        date = datetime.datetime.now()
        date_str = date.isoformat()
        until = date + datetime.timedelta(hours=hours_limit) if hours_limit else 'unlimited'
        token_hash = '%s|%s|%s|%s|%s' % (
            uidb64, token, date_str, until, extra_token)
        
        return base64.urlsafe_b64encode(bytes(token_hash, "ascii"))
        
    def hash_user_valid(self, token, extra_token=''):
        """
            This method allow to check if token is valid either 
            temporary or unlimited.
        """
        token_split = token.split("=")
        # if the token is altered
        if (token_split[-1:][0] != "" or len(token_split) > 3
            or token_split[1] != ""): 
            return False
        try:
            token_hash = base64.urlsafe_b64decode(bytes(token))
        except: return False
        uidb64, token_decoded, date, limit, token_added = \
            token_hash.split('|')
        valid_uid = int(urlsafe_base64_decode(uidb64)) == \
            self.user.pk
        valid_token = token_decoded == \
            default_token_generator.make_token(self.user)
        present = datetime.datetime.now()
        if not self.hash_has_limit(token):
            limit = present + datetime.timedelta(minutes=1)
        else:
            limit = dateutil.parser.parse(limit)

        valid_extra_token = token_added == extra_token
        if (valid_uid and valid_token and (present < limit)
            and valid_extra_token):
            return True
        return False
    
    def hash_get_uid(self, token):
        """
            Method that return the user id
        """
        try:
            token_hash = base64.urlsafe_b64decode(bytes(token))
        except: return False
        uidb64 = token_hash.split('|')[0]
        return int(urlsafe_base64_decode(uidb64))

    def hash_get_extra_token(self, token):
        """
            Method that return the user id
        """
        try:
            token_hash = base64.urlsafe_b64decode(bytes(token))
        except: return False
        extra_token = token_hash.split('|')[4]
        return extra_token
    
    def hash_has_limit(self, token):
        """
            Method which allow know if token si limited
        """
        try: 
            token_hash = base64.urlsafe_b64decode(bytes(token))
        except: return False
        limit = token_hash.split('|')[3]
        if limit == 'unlimited':
            return False
        else:
            return True

    def hash_get_limit(self, token):
        """
            This function allow to check if token is valid either 
            temporary or unlimited.
            created by: @pdonaire1 05-10-2016
            limit => format '%b %d %Y %I:%M%p'
        """
        try:
            token_hash = base64.urlsafe_b64decode(bytes(token))
        except: return False
        limit = token_hash.split('|')[3]
        if limit == 'unlimited':
            return False
        if not self.hash_has_limit(token_hash):
            present = datetime.datetime.now()
            limit = present + datetime.timedelta(minutes=1)
        else:
            limit = dateutil.parser.parse(limit)
        return limit