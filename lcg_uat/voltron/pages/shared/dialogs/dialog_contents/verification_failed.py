from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.dialogs.dialog_base import Dialog


class VerificationFailed(Dialog):
    _desktop_title = 'xpath=.//*[@data-crlat="dTitle"]'
    _verify_my_address_button = 'xpath=.//*[@data-crlat="verifyMyAddress"]'
    _welcome_text = 'xpath=.//*[@data-crlat="kycWelcome"]'
    _first_name = 'xpath=.//*[@data-crlat="firstName"]'
    _logout_link = 'xpath=.//*[@data-crlat="logoutLink"]'
    _kyc_upload_required_documents = 'xpath=.//*[@data-crlat="uploadRequiredDoc"]'
    _kyc_address_verification_documents = 'xpath=.//*[@data-crlat="addressVerificationDoc"]'
    _review_my_details = 'xpath=.//*[@data-crlat="reviewMyDetails"]'
    _kyc_direct_chat_panel = 'xpath=.//*[@data-crlat="directChatPanel"]'
    _live_chat_button = 'xpath=.//*[@data-crlat="liveChat"]'

    @property
    def desktop_title(self):
        return self._get_webelement_text(selector=self._desktop_title, context=self._we)

    @property
    def verify_my_address_button(self):
        return ButtonBase(selector=self._verify_my_address_button, context=self._we)

    @property
    def welcome_text(self):
        return self._get_webelement_text(selector=self._welcome_text)

    @property
    def first_name(self):
        return self._get_webelement_text(selector=self._first_name)

    @property
    def logout_link(self):
        return LinkBase(selector=self._logout_link, context=self._we)

    @property
    def kyc_upload_required_documents_block(self):
        return self._get_webelement_text(selector=self._kyc_upload_required_documents, context=self._we)

    @property
    def kyc_address_verification_documents(self):
        return self._get_webelement_text(selector=self._kyc_address_verification_documents, context=self._we)

    @property
    def review_my_details(self):
        return self._get_webelement_text(selector=self._review_my_details, context=self._we)

    @property
    def kyc_direct_chat_panel(self):
        return self._get_webelement_text(selector=self._kyc_direct_chat_panel, context=self._we)

    @property
    def live_chat_button(self):
        return ButtonBase(selector=self._live_chat_button, context=self._we)
