from voltron.pages.shared.contents.inplay_desktop import InPlayDesktop, InPlayDesktopTabContent
from voltron.pages.ladbrokes.contents.inplay_watchlive_desktop import InPlayWatchLiveDesktopTabContent


class LadbrokesInPlayDesktop(InPlayDesktop):

    @property
    def tab_content(self):
        watch_live = self._find_element_by_selector(selector=self._watch_live, context=self._we, timeout=1)
        if watch_live:
            return InPlayWatchLiveDesktopTabContent(selector=self._tab_content, context=self._we)
        else:
            return InPlayDesktopTabContent(selector=self._tab_content, context=self._we)
