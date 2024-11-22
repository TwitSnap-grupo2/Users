class ExistentUserError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class UserNotFound(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)


class NotAllowed(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BlockedUser(Exception):
    def __init__(self, message="This user is currently blocked"):
        self.message = message
        super().__init__(self.message)
