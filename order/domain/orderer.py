class Orderer(object):
    def __init__(self, member_id, name):
        self.member_id = name
        self.name = name

    def __composite_values__(self):
        return self.member_id, self.name

    def __repr__(self):
        return f'Orderer(member_id={self.member_id}, name={self.name})'

    def __eq__(self, other):
        return isinstance(other, Orderer) and \
            other.member_id == self.member_id and \
            other.name == self.name

    def __ne__(self, other):
        return not self.__eq__(other)