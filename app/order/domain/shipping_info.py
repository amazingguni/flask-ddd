


class Receiver(object):
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
    
    def __composite_values__(self):
        return self.name, self.phone

    def __repr__(self):
        return f'Receiver(name={self.name}, phone={self.phone})'
    
    def __eq__(self, other):
        return isinstance(other, Receiver) and \
            other.name == self.name and \
            other.phone == self.phone
    
    def __ne__(self, other):
        return not self.__eq__(other)

class Address(object):
    def __init__(self, zip_code, address1, address2):
        self.zip_code = zip_code
        self.address1 = address1
        self.address2 = address2
    
    def __composite_values__(self):
        return self.zip_code, self.address1, self.address2

    def __repr__(self):
        return f'Address(zip_code={self.zip_code}, address1={self.address1}, address2={self.address2})'
    
    def __eq__(self, other):
        return isinstance(other, Address) and \
            other.zip_code == self.zip_code and \
            other.address1 == self.address1 and \
            other.address2 == self.address2
    
    def __ne__(self, other):
        return not self.__eq__(other)
    



class ShippingInfo(object):
    def __init__(self, receiver, address, message):
        self.receiver = receiver
        self.address = address
        self.message = message
    
    def __repr__(self):
        return f'ShippingInfo(message={self.message}, receiver={self.receiver})'
    
    def __eq__(self, other):
        return isinstance(other, ShippingInfo) and \
            other.receiver == self.receiver and \
            other.address == self.address and \
            other.message == self.message 
    
    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def _generate(cls, receiver_name, receiver_phone, \
            zip_code, address1, address2, message):
        return ShippingInfo(
            Receiver(receiver_name, receiver_phone),
            Address(zip_code, address1, address2),
            message
        )

    def __composite_values__(self):
        return \
            self.address.__composite_values__() + self.receiver.__composite_values__(), \
            self.message

