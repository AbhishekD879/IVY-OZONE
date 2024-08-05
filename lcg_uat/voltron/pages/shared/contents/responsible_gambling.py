from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_content import BaseContent


class ResponsibleGambling(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/safer-gambling'
    _responsible_gambling = 'xpath=.//*[contains(@data-crlat, "responsibleGambling")]'
    _want_to_close_account_link = 'xpath=.//a[@href="gambling-controls/account-closure/step-one"]'
    _read_more_about_self_exclusion = 'xpath=.//a[contains(@href, "self-exclusion")] | .//a[contains(@data-routerlink, "self-exclusion")]'
    _take_a_short_break_link = 'xpath=.//a[@href="time-out"]'

    @property
    def responsible_gambling(self):
        return self._find_element_by_selector(selector=self._responsible_gambling, context=self._we)

    @property
    def want_to_close_account_link(self):
        return ButtonBase(selector=self._want_to_close_account_link, context=self._we)

    @property
    def more_about_self_exclusion_link(self):
        return ButtonBase(selector=self._read_more_about_self_exclusion, context=self._we)

    @property
    def take_a_short_break_link(self):
        return ButtonBase(selector=self._take_a_short_break_link, context=self._we)
