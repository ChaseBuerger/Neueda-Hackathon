class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.profile = {}  # Additional user details

    def update_profile(self, profile_data):
        self.profile.update(profile_data)

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "profile": self.profile
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["username"], data["password"])
        user.profile = data.get("profile", {})
        return user
