class Person:
    """Baseline for users"""
    #Constructor
    def __init__(self, name: str, email: str):
        self._name = name
        self._email = email
    #Getter properties
    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email