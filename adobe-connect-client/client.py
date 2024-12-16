import requests
from xml.etree import ElementTree

# Adobe Connect API Client Package
class AdobeConnectClient:
    BASE_URL = "https://your-adobe-connect-domain.com/api/xml"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session_cookie = None

    def login(self):
        login_payload = {
            'action': 'login',
            'login': self.username,
            'password': self.password
        }
        response = requests.post(self.BASE_URL, data=login_payload)

        if response.status_code == 200:
            xml_response = ElementTree.fromstring(response.text)
            status = xml_response.find('status').get('code')
            if status == "ok":
                print("Login successful")
                self.session_cookie = response.cookies['BREEZESESSION']
            else:
                raise Exception("Login failed: " + status)
        else:
            raise Exception(f"HTTP Error: {response.status_code}")

    def create_meeting(self, meeting_name, folder_id="", start_date="", end_date=""):
        if not self.session_cookie:
            raise Exception("Not logged in. Please log in first.")

        create_payload = {
            'action': 'sco-update',
            'type': 'meeting',
            'name': meeting_name,
            'folder-id': folder_id,
            'date-begin': start_date,
            'date-end': end_date,
            'permission-id': 'view',
        }

        response = requests.post(self.BASE_URL, data=create_payload, cookies={'BREEZESESSION': self.session_cookie})

        if response.status_code == 200:
            xml_response = ElementTree.fromstring(response.text)
            status = xml_response.find('status').get('code')
            if status == "ok":
                sco_id = xml_response.find('sco').get('sco-id')
                print(f"Meeting room created successfully with SCO-ID: {sco_id}")
                return sco_id
            else:
                raise Exception("Error creating meeting room: " + status)
        else:
            raise Exception(f"HTTP Error: {response.status_code}")

    def set_permission(self, sco_id, principal_id, permission_id):
        if not self.session_cookie:
            raise Exception("Not logged in. Please log in first.")

        permission_payload = {
            'action': 'permissions-update',
            'acl-id': sco_id,
            'principal-id': principal_id,
            'permission-id': permission_id
        }

        response = requests.post(self.BASE_URL, data=permission_payload, cookies={'BREEZESESSION': self.session_cookie})

        if response.status_code == 200:
            xml_response = ElementTree.fromstring(response.text)
            status = xml_response.find('status').get('code')
            if status == "ok":
                print(f"Permission updated successfully for SCO-ID: {sco_id}")
            else:
                raise Exception("Error setting permission: " + status)
        else:
            raise Exception(f"HTTP Error: {response.status_code}")

    def get_meeting_id_by_name(self, meeting_name):
        if not self.session_cookie:
            raise Exception("Not logged in. Please log in first.")

        search_payload = {
            'action': 'sco-search',
            'query': meeting_name
        }

        response = requests.post(self.BASE_URL, data=search_payload, cookies={'BREEZESESSION': self.session_cookie})

        if response.status_code == 200:
            xml_response = ElementTree.fromstring(response.text)
            status = xml_response.find('status').get('code')
            if status == "ok":
                sco = xml_response.find('sco')
                if sco is not None:
                    sco_id = sco.get('sco-id')
                    print(f"Meeting found with SCO-ID: {sco_id}")
                    return sco_id
                else:
                    print("No meeting found with the given name.")
                    return None
            else:
                raise Exception("Error searching for meeting: " + status)
        else:
            raise Exception(f"HTTP Error: {response.status_code}")

# Package setup for reuse
# Create a directory structure as follows:
# adobe_connect/
#   __init__.py
#   client.py

# __init__.py
# from .client import AdobeConnectClient

# To install as a package:
# Create setup.py with the following content:
#
# from setuptools import setup, find_packages
#
# setup(
#     name="adobe_connect",
#     version="0.1.0",
#     packages=find_packages(),
#     install_requires=["requests"],
#     description="A package for interacting with Adobe Connect API",
#     author="Your Name",
#     author_email="your.email@example.com",
#     url="https://github.com/your-repo/adobe-connect-client",
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires=">=3.6",
# )

# Then install locally:
# > pip install .
