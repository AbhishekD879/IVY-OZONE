from voltron.pages.shared.contents.inplay import InPlayAccordionList, InPlayTabContent, InPlay


class InPlayDesktopTabContent(InPlayTabContent):
    _item = 'xpath=.//*[@data-crlat="accordionList"]'
    _accordions_list_type = InPlayAccordionList


class InPlayDesktop(InPlay):
    _tab_content_type = InPlayDesktopTabContent

    @property
    def tab_content(self):
        watch_live = self._find_element_by_selector(selector=self._watch_live, context=self._we, timeout=1)
        if watch_live:
            from voltron.pages.shared.contents.inplay_watchlive_desktop import InPlayWatchLiveDesktopTabContent
            return InPlayWatchLiveDesktopTabContent(selector=self._tab_content, context=self._we)
        else:
            return InPlayDesktopTabContent(selector=self._tab_content, context=self._we)
