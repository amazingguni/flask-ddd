class Orderer(object):
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __composite_values__(self):
        return self.user_id, self.name

    def __repr__(self):
        return f'Orderer(user_id={self.user_id}, name={self.name})'

    def __eq__(self, other):
        return isinstance(other, Orderer) and \
            other.user_id == self.user_id and \
            other.name == self.name

    def __ne__(self, other):
        return not self.__eq__(other)