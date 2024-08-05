from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.deposit.deposit_base import GVCDepositContent, GVCDepositIframeBase


class GVCDepositTransactionDetailsSection(ComponentBase):
    """
    Class contains TRANSACTION DETAILS:
        - Transaction ID
        - Deposit with MasterCard
        - Fee
        - Total Deposit
    """
    # Not sure is it needed at all, just placeholder just for case
    pass


class GVCDepositTransactionSummary(GVCDepositContent):
    _url_pattern = '^http[s]?:\/\/.+\/deposit?'
    _ok_button = 'xpath=.//*[contains(@class, "btn btn-primary")]'
    _make_another_deposit_button = 'xpath=.//*[@id="another-deposit-dep-success"]'
    _details_section = 'xpath=.//*[@class="details-section"]'
    _successful_message = 'xpath=.//*[@class="deposit-success-header"] | .//*[contains(@class,"deposit-success-header")] | //*[contains(@class, "deposit-success-inner-wrapper")]'
    _successful_message_with_email = 'xpath=.//*[@class="message-text"]/p'

    @property
    def ok_button(self):
        return ButtonBase(selector=self._ok_button, context=self._we)

    @property
    def make_another_deposit_button(self):
        return ButtonBase(selector=self._make_another_deposit_button, context=self._we)

    @property
    def details_section(self):
        return GVCDepositTransactionDetailsSection(selector=self._details_section, context=self._we)

    @property
    def successful_message(self):
        """
        Displays first part of message. Example:
            - Your deposit of 22.00 GBP has been successful
        :return: message
        """
        return self._get_webelement_text(selector=self._successful_message, context=self._we, timeout=0).strip().replace('\n',' ')

    @property
    def successful_message_with_email(self):
        """
        Displays second part of message. Example:
            - An email has been sent to your registered email address.
        :return: message
        """
        return self._get_webelement_text(selector=self._successful_message_with_email, context=self._we).strip()


class GVCDepositTransactionDetailsDialog(GVCDepositIframeBase, GVCDepositTransactionSummary):
    _details_section = 'xpath=.//*[@class="details-section"]'
    _successful_message = 'xpath=.//*[@class="success-msg"]/h2'
    _content = 'xpath=.//div[contains(@class,"qd-main")]'

    @property
    def successful_message_with_email(self):
        raise NotImplementedError(f'Second part of successful message is not present on {self.__class__.__name__}')

    @property
    def ok_button(self):
        raise NotImplementedError(f'"OK" button is not present on {self.__class__.__name__}')

    @property
    def make_another_deposit_button(self):
        raise NotImplementedError(f'"Make Another Deposit" button is not present on {self.__class__.__name__}')
