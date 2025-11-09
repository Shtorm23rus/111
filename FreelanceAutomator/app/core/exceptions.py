class FreelanceAssistantException(Exception):
    pass

class PlatformConnectionError(FreelanceAssistantException):
    pass

class AIGenerationError(FreelanceAssistantException):
    pass

class JobParsingError(FreelanceAssistantException):
    pass

class DatabaseError(FreelanceAssistantException):
    pass

class ConfigurationError(FreelanceAssistantException):
    pass
