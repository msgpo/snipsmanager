# -*-: coding utf-8 -*-
""" Downloader for Snips assistants. """

from http_helpers import post_request_json
import os
import json
import re

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen, Request, URLError

USER_AUTH_ROUTE = "https://private-gateway.snips.ai/v1/user/auth"


class AuthException(Exception):
    pass


class AuthExceptionInvalidCredentials(AuthException):
    pass


class AuthExceptionInvalidAssistantId(AuthException):
    pass


class DownloaderException(Exception):
    """ Exceptions related to downloads of Snips assistants. """
    pass


def email_is_valid(email):
    return True if re.match(r"[^@]+@[^@]+\.[^@]+", email) else False


# pylint: disable=too-few-public-methods
class Downloader(object):
    """ Downloader for Snips assistants. """

    @staticmethod
    def download(url, output_dir, filename):
        """ Download a file, and save it to a file.

        :param url: the URL of the file.
        :param output_dir: the directory where the file should be
                           saved.
        """
        try:
            response = urlopen(url)
        except Exception:
            raise DownloaderException()

        Downloader.save(response.read(),
                        output_dir,
                        filename)

    @staticmethod
    def save(content, output_dir, filename):
        """ Save content of a file.

        :param content: the content of the file to save.
        :param output_dir: the directory where the assistant should be
                           saved.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_filename = "{}/{}".format(output_dir, filename)
        with open(output_filename, "wb") as output_file:
            output_file.write(content)


class AuthDownloader(Downloader):
    def __init__(self, email, password, assistantId):
        self.auth_url = USER_AUTH_ROUTE
        self.email = email
        self.password = password
        self.assistantId = assistantId
        self.validate_input()
        self._DOWNLOAD_URL = "https://private-gateway.snips.ai/v1/assistant/{}/download".format(assistantId)

    def validate_input(self):
        if not email_is_valid(self.email):
            raise AuthExceptionInvalidCredentials("Error, Email is not valid")

        if len(self.password) < 1:
            raise AuthExceptionInvalidCredentials("Error, password is too short")

        if len(self.assistantId) < 14:
            raise AuthExceptionInvalidAssistantId("Error, assistantId is too short")

    def retrieve_auth_token(self):
        data = {'email': self.email, 'password': self.password}

        try:
            response, response_headers = post_request_json(self.auth_url, data)
            token = response_headers.getheader('Authorization')
            return token
        except URLError:
            raise DownloaderException

    def download(self, output_dir, filename):
        try:
            token = self.retrieve_auth_token()
            request = Request(self._DOWNLOAD_URL, headers={'Authorization': token, 'Accept': 'application/json'})
            response = urlopen(request)
        except Exception:
            raise DownloaderException()

        Downloader.save(response.read(),
                        output_dir,
                        filename)
