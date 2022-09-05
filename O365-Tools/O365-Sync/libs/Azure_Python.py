
import logging
from libs.UserObj import UserObj
from enum import Enum
import threading


class AzureType(Enum):
    NONE = 0
    GETALLUSERS = 1


class Azure():
    """
    Manage Azure AD
    see https://pypi.org/project/O365/#directory-and-users
    see https://docs.microsoft.com/en-us/graph/api/user-list?view=graph-rest-1.0&tabs=http#optional-query-parameters
    """
    accounts = []
    type = AzureType.NONE

    def __init__(self, config):
        self.logger = logging.getLogger('Azure')
        self.config = config
        self.client_id = self.config['azure']['client_id']
        self.client_secret = self.config['azure']['client_secret']
        self.tenant_id = self.config['azure']['tenant_id']

        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True

    def getThread(self):
      return self.thread

    def start(self):
      self.thread.start()

    def setType(self, type_):
        """ which type of Thread to execute, see AzureType """
        self.type = type_

    def run(self):
      if self.type == AzureType.NONE:
          pass
      if self.type == AzureType.GETALLUSERS:
          self.getAccounts()

    def getAccounts(self):
        # Anwendungs-ID (Client)
        # Client Secret (Wert) from SecretKeys
        credentials = (self.client_id, self.client_secret)

        account = Account(credentials, auth_flow_type='credentials', tenant_id=self.tenant_id)
        if account.authenticate():
            self.logger.info('Authenticated with Azure AD!')
            directory = account.directory()
            # get_users(self, limit=100, *, query=None, order_by=None, batch=None)
            # get User in Part à 100 Users
            self.accounts = []
            for user in directory.get_users(limit=10000, batch=100):
                obj = UserObj

                obj.display_name = user.display_name
                obj.assigned_licenses = user.assigned_licenses
                obj.assigned_plans = user.assigned_plans
                obj.full_name = user.full_name
                obj.given_name = user.given_name
                obj.mail = user.mail
                obj.surname = user.surname
 
                self.accounts.append(obj)

# Test
#a = Azure()
#a.getAccounts()
