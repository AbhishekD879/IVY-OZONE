from voltron.pages.shared.components.base import ComponentBase


class Messages(ComponentBase):
    _title = 'xpath=.//lh-header-bar//div[contains(@class,"header-ctrl-txt")]'
    _close_button = None
    _message_details = 'xpath=.//div[contains(@class,"player-inbox-message-container")]'
    _message_counter = None
    _no_messages_text = 'xpath=.//div[@class="inbox-message-viewer"]'

    @property
    def title(self):
        return self._find_element_by_selector(selector=self._title, context=self._context, timeout=5)

    @property
    def close_button(self):
        return self._find_element_by_selector(selector=self._close_button, context=self._context, timeout=5)

    @property
    def message_details(self):
        return self._find_element_by_selector(selector=self._message_details, context=self._context, timeout=5)

    @property
    def counter(self):
        return self._find_element_by_selector(selector=self._message_counter, context=self._context, timeout=5)

    @property
    def no_messages_text(self):
        return self._find_element_by_selector(selector=self._no_messages_text, context=self._context, timeout=5)


class MessagesDesktop(Messages):
    _close_button = 'xpath=.//div[@class="header-ctrl-r"]'
    _message_counter = 'xpath=.//a/span[contains(@class,"badge badge-circle")]'


class MessagesMobile(Messages):
    _back_button = 'xpath=.//*[contains(@class, "ui-back")]'
    _message_expand = 'xpath=.//*[contains(text(), "Congratulations, you are verified!")]'
    _message_counter = 'xpath=.//i[contains(@class,"ui-icon ui-icon-size-xl theme-inbox")]/span'

    @property
    def back_button(self):
        return self._find_element_by_selector(selector=self._back_button, context=self._context, timeout=3)

    @property
    def message_expand(self):
        return self._find_element_by_selector(selector=self._message_expand, context=self._context, timeout=5)
