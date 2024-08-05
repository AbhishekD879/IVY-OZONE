from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.deposit.deposit_base import GVCDepositContent
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class GVCTypeCard(ButtonBase):

    _name = 'xpath=.//*[@class="payment-name"]'

    @property
    def name(self):
        name_we = self._get_webelement_text(selector=self._name, context=self._we)
        if not name_we:
            raise VoltronException('Payment method name web element not found on deposit page')
        return name_we


class GVCSelectTypeCard(GVCDepositContent):
    _item = 'xpath=.//*[contains(@id,"option")]'
    _list_item_type = GVCTypeCard
    _debit_card_button = 'xpath=.//*[contains(@class, "payment-method-card")]'
    _maestro_button = 'xpath=.//*[contains(@class, "maestro")]'
    _visa_button = 'xpath=.//*[contains(@class, "visa")]'
    _master_card_button = 'xpath=.//*[contains(@class, "mastercard")]'
    _successful_message = 'xpath=.//*[contains(@class, "cashier-options")]//descendant::h4'
    _make_deposit_message = 'xpath=.//*[@class="message-text"]/p'

    @property
    def debit_card_button(self):
        return self._find_element_by_selector(selector=self._debit_card_button, context=self._we)

    @property
    def maestro_button(self):
        return GVCTypeCard(selector=self._maestro_button, context=self._we)

    @property
    def visa_button(self):
        return GVCTypeCard(selector=self._visa_button, context=self._we)

    @property
    def master_card_button(self):
        return GVCTypeCard(selector=self._master_card_button, context=self._we)

    @property
    def successful_message(self):
        """
        First part of message on green panel: 'You are registered!'
        :return: message
        """
        wait_for_result(lambda: self._get_webelement_text(selector=self._successful_message, context=self._we) != "",
                        name='Successful message to be displayed',
                        timeout=30)
        return self._get_webelement_text(selector=self._successful_message, context=self._we)

    @property
    def make_deposit_message(self):
        """
        Second part of message on green panel: 'Almost there, make a deposit and get your welcome bonus.'
        :return: message
        """
        return self._get_webelement_text(selector=self._make_deposit_message, context=self._we)
