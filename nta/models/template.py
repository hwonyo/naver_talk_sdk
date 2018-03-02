from .base import Base
from .buttons import Buttons


class BaseTemplate(Base):
    def __init__(self, quick_reply=None, **kwargs):
        """__init__method.

        Args:
            - quick_reply: list of Template.Buttons or Template.QuickReply
        """
        super(BaseTemplate, self).__init__(**kwargs)

        if quick_reply:
            if isinstance(quick_reply, list):
                self.quick_reply = QuickReply(quick_reply)
            elif isinstance(quick_reply, QuickReply):
                self.quick_reply = quick_reply


class TextContent(BaseTemplate):
    def __init__(self, text, code=None, input_type=None, **kwargs):
        super(TextContent, self).__init__(**kwargs)

        self.text = text
        self.code = code
        self.input_type = input_type


class ImageContent(BaseTemplate):
    def __init__(self, image_url=None, image_id=None, **kwargs):
        super(ImageContent, self).__init__(**kwargs)

        if image_url is not None:
            self.image_url = image_url
        elif image_id is not None:
            self.image_id = image_id
        else:
            raise TypeError("'required 1 positional argument: 'image_url' or 'image_id'")


class CompositeContent(BaseTemplate):
    def __init__(self, composite_list, **kwargs):
        """__init__ method.

        Args:
            - composite_list: list of Composites
        """
        super(CompositeContent, self).__init__(**kwargs)

        self.composite_list = composite_list


class Composite(BaseTemplate):
    """
    Composite
    content element for CompositeContent

    """
    def __init__(self, title, description=None, image=None, element_list=None, button_list=None, **kwargs):
        """__init__method.

        Args:
            - title: str
            - description: str
            - image: image url
            - element_list: list of Template.Elements
            - button_list: list of Template.buttons or dict buttons
        """
        super(Composite, self).__init__(**kwargs)

        self.title = title
        self.description = description
        if image is not None:
            self.image = ImageContent(image)
        self.element_list = element_list
        self.button_list = Buttons.convert_shortcut_buttons(button_list)


class ElementList(BaseTemplate):
    def __init__(self, data, **kwargs):
        super(ElementList, self).__init__(**kwargs)

        self.type = "LIST"
        self.data = data


class ElementData(Base):
    def __init__(self, title, description=None, sub_description=None, image=None, button=None, **kwargs):
        """__init__ method."""
        super(ElementData, self).__init__(**kwargs)

        self.title = title
        self.description = description
        self.sub_description = sub_description
        if image is not None:
            self.image = ImageContent(image)
        self.button = button


class QuickReply(Base):
    def __init__(self, button_list, **kwargs):
        super(QuickReply, self).__init__(**kwargs)

        self.button_list = Buttons.convert_shortcut_buttons(button_list)


class PaymentInfo(Base):
    def __init__(
            self,
            merchant_pay_key,
            total_pay_amount,
            product_items,
            merchant_user_key=None,
            product_name=None,
            product_count=None,
            delivery_fee=None,
            tax_scope_amount=None,
            tax_ex_scope_amount=None,
            purchaser_name=None,
            purchaser_birthday=None,
            **kwargs
    ):
        super(PaymentInfo, self).__init__(**kwargs)

        self.merchant_pay_key = merchant_pay_key
        self.total_pay_amount = total_pay_amount
        self.product_items = product_items
        self.merchant_user_key = merchant_user_key
        self.product_name = product_name
        self.product_count = product_count
        self.delivery_fee = delivery_fee
        self.tax_scope_amount = tax_scope_amount
        self.tax_ex_scope_amount = tax_ex_scope_amount
        self.purchaser_name = purchaser_name
        self.purchaser_birthday = purchaser_birthday


class ProductItem(Base):
    def __init__(
            self,
            category_type,
            category_id,
            uid,
            name,
            start_date=None,
            end_date=None,
            seller_id=None,
            count=None,
            **kwargs
    ):
        super(ProductItem, self).__init__(**kwargs)

        self.category_type = category_type
        self.category_id = category_id
        self.uid = uid
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.seller_id = seller_id
        self.count = count


class Menus(Base):
    def __init__(self, menus, **kwargs):
        super(Menus, self).__init__(**kwargs)

        self.menus = menus