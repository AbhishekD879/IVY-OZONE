from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.components.primitives.checkboxes import CheckBoxBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase


class ManageMyCards(ComponentBase):
    _url_pattern = r'^http[s]?:\/\/.+\/en/cashier/manage-cards'
    _url_matcher_timeout = 20
    _header = 'xpath=.//*[@id="cashierHeader"]'
    _content = 'xpath=.//*[contains(@class,"cashier-main")]'
    _delete_popup = 'xpath=.//mat-dialog-container'

    @property
    def header(self):
        return ManageMyCardHeader(selector=self._header, timeout=2)

    @property
    def content(self):
        return ManageMyCardContent(selector=self._content, timeout=2)

    @property
    def delete_popup(self):
        return ManageMyCardDeletePopup(selector=self._delete_popup, timeout=2)


class ManageMyCardHeader(ComponentBase):
    _brand_logo = 'xpath=.//button[contains(@class, "Brand")]'
    _header_title = 'xpath=.//*[contains(@class, "cashier-page-heading")]'
    _balance = 'xpath=.//*[contains(@class, "total-balance")]'
    _close_button = 'xpath=.//*[contains(@class, "ui-close")]'

    @property
    def brand_logo(self):
        return ButtonBase(selector=self._brand_logo, timeout=2)

    @property
    def header_title(self):
        return TextBase(selector=self._header_title, timeout=2)

    @property
    def balance(self):
        return TextBase(selector=self._balance, timeout=2).text.upper().replace("GBP", "")

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, timeout=2)


class SelectAll(ComponentBase):
    _text = 'xpath=.//*[contains(@class,"mat-checkbox-label")]'
    _checkbox = 'xpath=.//*[contains(@class,"mat-checkbox-inner-container")]'

    @property
    def name(self):
        return TextBase(selector=self._text, context=self._we, timeout=2)

    @property
    def checkbox(self):
        return CheckBoxBase(selector=self._checkbox, context=self._we, timeout=2)


class PaymentCard(ComponentBase):
    _single_checkbox = 'xpath=.//*[@class="select-single-payment"]/mat-checkbox'
    _manage_card_payment_logo = 'xpath=.//*[@class="manage-cards-payment-logo"]'
    _card_type = 'xpath=.//*[@class="manage-cards-payment-method-details"]/strong'
    _card_number = 'xpath=.//*[@class="manage-cards-payment-method-details"]/p[@class="card-number"]'
    _expiry_date = 'xpath=.//*[@class="manage-cards-payment-method-details"]/p[@class="card-expiry-date"]'
    _edit_details = 'xpath=.//*[@class="manage-cards-payment-method-details"]/p[@class="edit-details"]/a'

    @property
    def name(self):
        return f"{self.card_type.name}+{self.card_number.name}"

    @property
    def checkbox(self):
        return CheckBoxBase(selector=self._single_checkbox, context=self._we, timeout=2)

    @property
    def card_logo(self):
        return ComponentBase(selector=self._manage_card_payment_logo, context=self._we, timeout=2)

    @property
    def card_type(self):
        return TextBase(selector=self._card_type, context=self._we, timeout=2)

    @property
    def card_number(self):
        return TextBase(selector=self._card_number, context=self._we, timeout=2)

    @property
    def expiry_date(self):
        return TextBase(selector=self._expiry_date, context=self._we, timeout=2)

    @property
    def edit_details(self):
        return LinkBase(selector=self._edit_details, context=self._we, timeout=2)


class CardSection(ComponentBase):
    _card_section_title = 'xpath=.//*[contains(@class,"cardHeader")]//*[contains(@class,"manage-cards-text")]'
    _select_all = 'xpath=.//mat-checkbox[@formcontrolname="selectAllPayments"]'
    _selected_card_count_text = 'xpath=.//*[@class="manage-cards-info"]'
    _delete_button = 'xpath=.//button[contains(@class,"delete-btn")]'
    _item = 'xpath=.//*[@class="manage-cards-payment-method"]'
    _list_item_type = PaymentCard

    @property
    def select_all(self):
        return SelectAll(selector=self._select_all, context=self._we, timeout=2)

    @property
    def card_section_title(self):
        return TextBase(selector=self._card_section_title, context=self._we, timeout=2)

    @property
    def cards(self):
        return self.items_as_ordered_dict

    @property
    def selected_card_count(self):
        return TextBase(selector=self._selected_card_count_text, context=self._we, timeout=2)

    @property
    def delete_card_btn(self):
        return ButtonBase(selector=self._delete_button, context=self._we, timeout=2)


class ManageMyCardContent(ComponentBase):
    _card_section = 'xpath=.//manage-cards-list'

    @property
    def card_section(self):
        return CardSection(selector=self._card_section, context=self._we, timeout=2)


class ManageMyCardDeletePopup(ComponentBase):
    _confirm_delete = 'xpath=.//button[contains(@class,"btn-primary-delete")]'

    @property
    def confirm_delete(self):
        return ButtonBase(selector=self._confirm_delete, context=self._we, timeout=2)
