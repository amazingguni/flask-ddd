from werkzeug.exceptions import InternalServerError


class NoOrderProductError(InternalServerError):
    description = 'Given product id is invalid'

    def __init__(self, response=None, original_exception=None):
        super(NoOrderProductError, self).__init__(
            description=self.description, response=response
        )
