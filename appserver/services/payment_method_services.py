"""Payments Service"""
import bson
from appserver.models.payment_method import PaymentMethodSchema
from appserver.services.exceptions import DataExistsError, NotFoundError
from appserver.data.payment_method_mapper import PaymentMethodMapper


class PaymentsService:
    """Payments Service class"""

    schema = PaymentMethodSchema()

    @classmethod
    def add_payment_method(cls, payment_method_dict):
        """Adds a payment method"""
        payment_method = cls.schema.load(payment_method_dict)
        if PaymentMethodMapper.exists({'name': payment_method.name}):
            raise DataExistsError("Payment method already exists.")
        return PaymentMethodMapper.insert(cls.schema.dump(payment_method))

    @classmethod
    def modify_payment_method(cls, payment_method_id, payment_method_dict):
        """Modifies a payment method"""
        payment_method = cls.schema.load(payment_method_dict)
        if PaymentMethodMapper.exists(
                {'_id': {'$ne': bson.ObjectId(payment_method_id)},
                 'name': payment_method.name}):
            raise DataExistsError("Payment method already exists.")
        ret = PaymentMethodMapper.modify({"_id": bson.ObjectId(payment_method_id)}, payment_method)
        if ret is None:
            raise NotFoundError("Payment method does not exist.")
        return ret

    @classmethod
    def get_payment_methods(cls):
        """Returns available payment methods"""
        categories = PaymentMethodMapper.get_many()
        ret = []
        for payment_method in categories:
            ret.append(cls.schema.dump(payment_method))
        return ret

    @classmethod
    def get_payment_method(cls, payment_method_id):
        """Get payment method by id"""
        payment_method = PaymentMethodMapper.get_by_id(payment_method_id)
        if payment_method is None:
            raise NotFoundError("Payment method not found.")
        return cls.schema.dump(payment_method)

    @classmethod
    def delete_payment_method(cls, payment_method_id):
        """Deletes a payment method"""
        if not PaymentMethodMapper.delete_one_by_id(payment_method_id):
            raise NotFoundError("Payment method not found.")
