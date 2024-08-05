from voltron.pages.shared.contents.base_content import BaseContent


class GamingHistory(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/gaming-history'
    _no_gaming_history = 'xpath=.//*[@data-crlat="cashout.noGameData"]'

    @property
    def has_no_history_label(self):
        return self._find_element_by_selector(selector=self._no_gaming_history, timeout=0) is not None
