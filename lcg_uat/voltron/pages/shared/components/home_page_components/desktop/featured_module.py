from voltron.pages.shared.components.home_page_components.desktop.base_desktop_module import BaseDesktopModule
from voltron.pages.shared.components.home_page_components.home_page_featured_tab import DesktopHomePageFeaturedTabContent


class FeaturedModule(BaseDesktopModule):
    _content_type = DesktopHomePageFeaturedTabContent

    @property
    def tab_content(self) -> DesktopHomePageFeaturedTabContent:
        return self._content_type(web_element=self._we, selector=self._selector)
