from werkzeug.exceptions import InternalServerError


class NoCategoryEx(InternalServerError):
    description = 'No category error'

    def __init__(self, response=None, original_exception=None):
        self.original_exception = original_exception
        super(InternalServerError, self).__init__(
            description=description, response=response
        )
