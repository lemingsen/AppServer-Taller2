"""Order model"""
from marshmallow import Schema, fields, post_load, validates, ValidationError, validate
from appserver.utils.mongo import ObjectId
from appserver.models.base import BaseModel
from appserver.models.location import LocationSchema
# pylint: disable=R0903,R0201,C0103


class OrderUserInfo:
    def __init__(self, username, email):
        self.username = username
        self.email = email


class OrderUserInfoSchema(Schema):
        username = fields.Str(required=True)
        email = fields.Email(required=True)


class TrackingInfo:
    """TrackingInfo"""
    def __init__(self, tracking_id, status, update_at):
        self.id = tracking_id
        self.status = status
        self.updateat = update_at


class TrackingInfoSchema(Schema):
    """TackingInfo Schema"""
    id = fields.Int(required=True)
    status = fields.Str(required=True)
    updateat = fields.DateTime(required=True)

    @post_load
    def make_product_tracking_code(self, data):
        """Creates a TrackingInfo from data dictionary"""
        return TrackingInfo(data['id'], data['status'], data['updateat'])


class PaymentInfo:
    """Represents the order payment information"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class PaymentInfoSchema(Schema):
    """PaymentInfo schema"""
    payment_method = fields.Str(required=True, validate=validate.Length(
        min=1, error="Product name cannot be empty"))
    cardholder_name = fields.Str(validate=validate.Length(
        min=1, error="Cardholder name field cannot be empty"))
    card_number = fields.Str(validate=validate.Length(
        min=1, error="Card number field cannot be empty"))
    expiration_date = fields.Str(validate=validate.Length(
        min=1, error="Expiration date field cannot be empty"))
    security_code = fields.Str(validate=validate.Length(
        min=1, error="Security code field cannot be empty"))

    @post_load
    def make_payment_info(self, data):
        """creates a order object from data dictionary"""
        return PaymentInfo(**data)


class Order(BaseModel):
    """Order"""
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)


class OrderSchema(Schema):
    """marshmallow order schema"""
    _id = ObjectId()
    product_id = ObjectId(required=True)
    product_name = fields.Str(validate=validate.Length(
        min=1, error="Product name cannot be empty"))
    units = fields.Int(required=True)
    unit_price = fields.Float()
    payment_info = fields.Nested(PaymentInfoSchema, required=True)
    datetime = fields.Str()
    buyer_info = fields.Nested(OrderUserInfoSchema)
    seller_info = fields.Nested(OrderUserInfoSchema)
    buyer_location = fields.Nested(LocationSchema)
    product_location = fields.Nested(LocationSchema)
    total = fields.Float()
    tracking_number = fields.Int()
    status = fields.Str()
    last_status_update = fields.DateTime()
    rate = fields.Str()

    @validates('units')
    def validate_units(self, value):
        """Validates that order units are greater than zero"""
        if value <= 0:
            raise ValidationError("Order units must be greater than 0.")

    @validates('unit_price')
    def validate_unit_price(self, value):
        """Validates that order unit price is greater than zero"""
        if value <= 0:
            raise ValidationError("Order unit_price must be greater than 0.")

    @validates('total')
    def validate_total(self, value):
        """Validates that order total is greater than zero"""
        if value <= 0:
            raise ValidationError("Order total must be greater than 0.")

    @post_load
    def make_order(self, data):
        """creates a order object from data dictionary"""
        return Order(**data)
