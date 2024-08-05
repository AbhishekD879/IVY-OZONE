from voltron.pages.shared.contents.inplay import InPlay, InPlayTabContent
from voltron.pages.ladbrokes.contents.inplay_watchlive import InPlayWatchLiveTabContentLadbrokes


class LadbrokesInPlay(InPlay):

    @property
    def tab_content(self):
        watch_live = self._find_element_by_selector(selector=self._watch_live, context=self._we, timeout=1)
        if watch_live:
            return InPlayWatchLiveTabContentLadbrokes(selector=self._tab_content, context=self._we)
        else:
            return InPlayTabContent(selector=self._tab_content, context=self._we)
