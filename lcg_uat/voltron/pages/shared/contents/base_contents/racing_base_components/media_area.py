from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class WatchFreeArea(ComponentBase):
    _video = 'id=QL_goingDown'

    @property
    def video(self):
        return self._find_element_by_selector(selector=self._video)

    @property
    def video_size(self):
        return self.video.get_attribute('style')


class WatchFreeLink(ButtonBase):
    _span = 'xpath=.//*[@data-crlat="labelWatchFreeInfo"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._span, timeout=2)


class VideoStreamArea(WatchFreeArea):
    pass
