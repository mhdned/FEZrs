class OException(Exception):
    """Custom Exception for FEZrs"""
    def __init__(self, message="An error occurred in FEZrs"):
        self.message = message
        super().__init__(self.message)
