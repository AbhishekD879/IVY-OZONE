from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.primitives.buttons import IconBase


class InfoPanel(ComponentBase):
    _text = 'xpath=./span'
    # some parts of html templates are located in js-files and custom tags are removed while compiling
    # so we have to check /limits hyperlink presence
    _hyperlink = 'xpath=.//*[@data-crlat="limits" or contains(@href, "limits")]'
    _click_here_link = 'xpath=.//*[@data-crlat="depositExternalLink" or contains(@href, "/deposit/addcard")]'
    _info_icon = 'xpath=.//*[@class="alert-icon"]'

    @property
    def info_icon(self):
        return IconBase(selector=self._info_icon, context=self._we, timeout=2)

    def has_link_to_limits_page(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._hyperlink,
                                                   timeout=0) is not None,
            name=f'Time panel status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def has_click_here_link(self):
        return self._find_element_by_selector(selector=self._click_here_link, timeout=0.5) is not None

    @property
    def click_here_link(self):
        return ButtonBase(selector=self._click_here_link, context=self._we)

    @property
    def link_to_limits_page(self):
        return ButtonBase(selector=self._hyperlink, context=self._we)

    @property
    def text(self):
        self.scroll_to_we()
        return self._get_webelement_text(we=self._we)

    @property
    def texts(self):
        if not self.text:
            return ''
        return self.text.split('\n')

    def click(self):
        self._wait_active()
        self.scroll_to_we()
        self._we.click()

    def wait_to_change(self):
        text = self.text
        wait_for_result(lambda: text != self.text,
                        name='Info Panel text to change',
                        timeout=5)

    def _wait_active(self, timeout=0):
        self._we = self._find_myself()
        return wait_for_result(lambda: self._we.is_displayed() and self._get_webelement_text(we=self._we),
                               name='Info panel shown',
                               timeout=3,
                               poll_interval=0.2)
