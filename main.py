from instagrapi import Client as InstaClient
from auth import insta_user, insta_pass, test_account_name

class InstaAccount():
    def __init__(self):
        self.cl = InstaClient()
        self.login()

    def login(self):
        valid_2fa = False
        while not valid_2fa:
            code_2fa = input(f"Please enter your 2FA to your Instagram {insta_user} account: ")
            if code_2fa.isnumeric():
                valid_2fa = True
            else:
                print("2FA code must be a number!")
        self.cl.login(insta_user, insta_pass, verification_code=code_2fa)

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
        """Returns a dict of following accounts
        'id_name: id_numbers' of 'account_name',
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
print(my_account.find_followers(test_account_name))
print(f"Accounts following {test_account_name}: ")
print(my_account.find_following(test_account_name))
my_account.logout()
