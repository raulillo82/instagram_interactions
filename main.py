from instagrapi import Client as InstaClient
from instagrapi.exceptions import LoginRequired
from auth import (insta_user, insta_pass, test_account_name,
                  session_file)
from os import path, chmod
import pprint

class InstaAccount():
    def __init__(self):
        self.cl = InstaClient()
        self.cl.delay_range = [1, 3]
        self.login()

    def login(self):
        if path.isfile(session_file):
            print("Session file found, trying to authenticate with it...")
            self.login_session()
        else:
            print("Session file not found, authenticating with user/pass...")
            self.login_2fa()

    def login_session(self):
        session = self.cl.load_settings(session_file)
        self.cl.set_settings(session)
        session_id = session["uuids"]["client_session_id"]
        #Does not seem to work as of https://github.com/subzeroid/instagrapi/issues/1641
        #self.cl.login_by_sessionid(session_id)
        self.cl.login("", "")
        try:
            self.cl.get_timeline_feed()
        except LoginRequired:
            print("Session not valid, authenticating with user/pass...")
            old_session = self.cl.get_settings()
            # use the same device uuids across logins
            self.cl.set_settings({})
            self.cl.set_uuids(old_session["uuids"])
            self.login_2fa()

    def login_2fa(self):
        valid_2fa = False
        while not valid_2fa:
            code_2fa = input(f"Please enter your 2FA to your Instagram {insta_user} account: ")
            if code_2fa.isnumeric():
                valid_2fa = True
            else:
                print("2FA code must be a number!")
        #Try to log in and save session for next time
        if self.cl.login(insta_user, insta_pass, verification_code=code_2fa):
            print("Storing session locally for next login...")
            self.cl.dump_settings(session_file)
            chmod(session_file, 0o400)

    def logout(self):
        self.cl.logout()

    def find_following(self, account_name):
        """Returns a dict of follower accounts
        'id_name: id_numbers' to 'account_name',
        every entry in the dict looks like this:
            'username': 'useridnumber' """
        account_id = self.cl.user_info_by_username(account_name).dict()["pk"]
        following = self.cl.user_following(account_id)
        following_ids = {following[key].dict()["username"]: key
                         for key in following.keys()}
        return following_ids

    def find_followers(self, account_name):
        """Returns a dict of followed accounts
        'id_name: id_numbers' by 'account_name',
        every entry in the dict looks like this:
            'username': 'useridnumber' """
        account_id = self.cl.user_info_by_username(account_name).dict()["pk"]
        followers = self.cl.user_followers(account_id)
        followers_ids = {followers[key].dict()["username"]: key
                         for key in followers.keys()}
        return followers_ids

    def follow(self, account_name):
        account_id = self.cl.user_info_by_username(account_name).dict()["pk"]
        return self.cl.user_follow(account_id)

my_account = InstaAccount()
print(f"Followers of {test_account_name}: ")
pp = pprint.PrettyPrinter(depth=4)
pp.pprint(my_account.find_followers(test_account_name))
print(f"Accounts followed by {test_account_name}: ")
pp.pprint(my_account.find_following(test_account_name))
#Do not log out unless explicitly needed
#my_account.logout()
