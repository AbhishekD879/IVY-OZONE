from voltron.pages.shared.components.base import ComponentBase
from collections import OrderedDict
from voltron.pages.coral.menus.right_menu import CoralRightMenuHeader
from voltron.utils.helpers import find_element
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class ConfirmationBox(ComponentBase):
    _text = 'xpath=.//div[@class="confirmation-window-body pc-txt"]/p'
    _cancel_button = 'xpath=.//button[text()="Cancel"]'
    _close_chat = 'xpath=.//button[text()="Close Chat"]'

    @property
    def confirmation_text(self):
        return self._get_webelement_text(selector=self._text)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, timeout=2)

    @property
    def close_chat_button(self):
        return ButtonBase(selector=self._close_chat, timeout=2)

    def has_cancel_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._cancel_button,
                                                   timeout=0) is not None,
            name=f'Cancel button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_close_chat_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._close_chat,
                                                   timeout=0) is not None,
            name=f'Close chat button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class ChatHeader(ConfirmationBox):
    _title = 'xpath=.//span[@class="chat-title"]'
    _close_button = 'xpath=.//a[@id="closeBtn"]'
    _toggle_button = 'xpath=.//a[@id="toggleBtn"]'

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, timeout=5)

    @property
    def toggle_button(self):
        return ButtonBase(selector=self._toggle_button, context=self._we)

    def has_close_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._close_button,
                                                   timeout=0) is not None,
            name=f'Close button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_toggle_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._toggle_button,
                                                   timeout=0) is not None,
            name=f'toggle button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class LiveChat(ComponentBase):
    _chat_header = 'xpath=.//div[@class="chat-container"]'
    _chat_header_type = ChatHeader
    _text_verification = 'xpath=.//*[@class="queue-head"]/div'
    _welcome_text = 'xpath=.//li[@class="external"]//span[@class="text"]'
    _agent_name = 'xpath=.//li[@class="notice"]//div[@class="message"]'

    @property
    def header(self):
        return self._chat_header_type(selector=self._chat_header, timeout=5)

    @property
    def agent_name_verification(self):
        return find_element(selector=self._agent_name, timeout=3)

    @property
    def welcome_text_verification(self):
        return find_element(selector=self._welcome_text, timeout=3)

    @property
    def live_chat_text_verification(self):
        return find_element(selector=self._text_verification, timeout=3)


class TopicListItems(ComponentBase):
    _name = 'xpath=.//*[@class="custom-control-label"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)


class TopicsList(ComponentBase):

    _item = 'xpath=.//*[contains(@class, "form-element")]'
    _list_item_type = TopicListItems


class HelpContactUs(LiveChat, CoralRightMenuHeader):
    _topic = 'xpath=.//*[@class="helpcontact-categorysection"] | .//*[text() = " All categories"]/following-sibling::div[1] | .//*[text() = " Popular categories"]/following-sibling::div[1]'
    _subcategory = 'xpath=.//*[@class="helpcontact-subcategory"]'
    _yes_button = 'xpath=.//button[@id="helpcontact-yesbtn"]'
    _no_button = 'xpath=.//button[@id="helpcontact-nobtn"]'
    _chat_options = 'xpath=.//*[contains(@class, "card-body cursorPointer")]'
    _verify_details = 'xpath=.//*[@id="newdocUploadTxt"]'
    _header = 'xpath=.//vn-header-bar/div'

    @property
    def topics(self):
        return TopicsList(selector=self._topic, context=self._we, timeout=60)

    @property
    def subcategory(self):
        return TopicsList(selector=self._subcategory, context=self._we)

    @property
    def yes_button(self):
        return ComponentBase(selector=self._yes_button)

    @property
    def no_button(self):
        return ComponentBase(selector=self._no_button)

    @property
    def chat_options(self):
        elements = self._find_elements_by_selector(selector=self._chat_options, context=self._we)
        item_dict = OrderedDict()
        for element in elements:
            item_we = element.text
            item_dict.update({item_we: element})
        return item_dict

    @property
    def verify_details(self):
        return TextBase(selector=self._verify_details)
