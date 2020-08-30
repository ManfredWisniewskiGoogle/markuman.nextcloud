import os
import requests
from ansible.errors import AnsibleError

class NextcloudHandler:
    def __init__(self, kwargs):
        self.HOST = kwargs.get('host') or os.environ.get('NEXTCLOUD_HOST')
        if self.HOST is None:
            raise AnsibleError('Unable to continue. No Nextcloud Host is given.')

        self.USER = kwargs.get('user') or os.environ.get('NEXTCLOUD_USER')
        if self.USER is None:
            raise AnsibleError('Unable to continue. No Nextcloud User is given.')

        self.TOKEN = kwargs.get('api_token') or os.environ.get('NEXTCLOUD_TOKEN')
        if self.TOKEN is None:
            raise AnsibleError('Unable to continue. No Nextcloud Token is given.')

    def get(self, path):
        r = requests.get(
            'https://{HOST}/{PATH}'.format(HOST=self.HOST, PATH=path),
            auth=(self.USER, self.TOKEN)
        )

        if r.status_code == 200:
            return r
        elif r.status_code == 404:
            raise AnsibleError('File {FILE} does not exist'.format(FILE=path))
        else:
            self.status_code_error(r.status_code)


    def put(self, path, src):
        r = requests.put(
            'https://{HOST}/{PATH}'.format(HOST=self.HOST, PATH=path), 
            data=open(src, 'rb'), auth=(self.USER, self.TOKEN)
        )
        
        if r.status_code in [201, 204]:
            return r, True
        else:
            self.status_code_error(r.status_code)



    def delete(self, path):
        r = requests.delete(
            'https://{HOST}/{PATH}'.format(HOST=self.HOST, PATH=path),
            auth=(self.USER, self.TOKEN)
        )

        if r.status_code == 204:
            return r, True
        elif r.status_code == 404:
            return r, False
        else:
            self.status_code_error(r.status_code)

    def user(self):
        return self.USER

    def status_code_error(status):
        raise AnsibleError('Nextcloud retured with status code {SC}'.format(SC = status))
