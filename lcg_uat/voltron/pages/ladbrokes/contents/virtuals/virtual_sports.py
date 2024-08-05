from voltron.pages.shared.components.breadcrumbs import Breadcrumbs
from voltron.pages.shared.contents.virtuals.sports_carousel import VirtualSportsCarouselItem
from voltron.pages.shared.contents.virtuals.virtual_sports import VirtualSports
from voltron.pages.shared.contents.virtuals.virtual_sports import VirtualSportsCarousel


class LadbrokesVirtualSportsCarouselItem(VirtualSportsCarouselItem):
    _item_name = 'xpath=.//*[@data-crlat="name"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._item_name, context=self._we)


class LadbrokesVirtualSportsCarousel(VirtualSportsCarousel):
    _list_item_type = LadbrokesVirtualSportsCarouselItem
    _active_tab = 'xpath=.//*[@data-crlat="item" and contains(@class, "active")]/*[@data-crlat="name"]'

    @property
    def current(self):
        return self._get_webelement_text(selector=self._active_tab, context=self._we)


class LadbrokesVirtualSports(VirtualSports):
    _sport_carousel_type = LadbrokesVirtualSportsCarousel


class LadbrokesVirtualSportsDesktop(LadbrokesVirtualSports):
    _breadcrumbs_type = Breadcrumbs
    _breadcrumbs = 'xpath=.//*[@data-crlat="breadcrumbsContainer"]'

    @property
    def breadcrumbs(self):
        return self._breadcrumbs_type(selector=self._breadcrumbs, context=self._we)
