from voltron.pages.shared import get_device_properties
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.helpers import normalize_name


class PageTitleBase(ComponentBase):
    _title_text = 'xpath=.//*[@data-crlat="titleText"] | .//*[@data-crlat="topBarTitle"]'

    def title_displayed(self):
        return self._find_element_by_selector(selector=self._title_text, timeout=1).is_displayed()

    @property
    def title(self):
        if not self._find_element_by_selector(selector='xpath=./*', timeout=2):
            text = normalize_name(self._get_webelement_text(we=self._we))
        else:
            text = normalize_name(self._get_webelement_text(selector=self._title_text, timeout=1))
        device_type = get_device_properties()['type']
        if device_type == 'desktop':
            text = text.replace(' v ', ' V ')
        return text


class PageTitle(PageTitleBase):
    _sport_icon = 'xpath=.//*[@data-crlat="sportIcon"]'
    _sport_title = 'xpath=.//*[@data-crlat="titleText"]'

    def icon_displayed(self):
        return self._find_element_by_selector(selector=self._sport_icon, timeout=1).is_displayed()

    @property
    def sport_title(self):
        return self.title

    @property
    def text(self):
        return self._we.text


class HeaderLine(ComponentBase):
    _back_button = 'xpath=.//*[@data-crlat="btnBack"]'
    _page_title = 'xpath=.//*[@data-crlat="topBarTitle"] | .//*[@data-crlat="bsTab" and contains(text(),"My Bets")]'
    _page_title_type = PageTitle
    _go_to_favourites_page = 'xpath=.//*[@data-crlat="navigateToFavourites" or @data-crlat="favouriteIcon"]'
    _favourite_counter = 'xpath=.//*[@data-crlat="favouriteCounter"]'
    _sport_icon = 'xpath=.//*[local-name()="svg"][@data-crlat="sportIcon"]'

    @property
    def go_to_favourites_page(self):
        return ButtonBase(selector=self._go_to_favourites_page)

    @property
    def has_favourites_icon(self):
        return self._find_element_by_selector(selector=self._go_to_favourites_page, timeout=2) is not None

    @property
    def favourites_counter(self):
        favourites_counter = self._wait_for_not_empty_web_element_text(self._favourite_counter, timeout=2)
        return favourites_counter if favourites_counter else '0'

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we, timeout=3)

    @property
    def page_title(self):
        return self._page_title_type(selector=self._page_title)

    @property
    def page_title_exists(self):
        return self._find_element_by_selector(selector=self._page_title, timeout=0) is not None

    @property
    def has_back_button(self):
        return self._find_element_by_selector(selector=self._back_button, timeout=2) is not None

    def press_back(self):
        self.scroll_to_we()
        self.back_button.click()

    @property
    def has_sport_icon(self):
        return self._find_element_by_selector(selector=self._sport_icon, timeout=0) is not None


class HeaderLineBase(ComponentBase):
    _back_button = 'xpath=.//*[@data-crlat="btnBack"]'
    _page_title = 'xpath=.//*[@data-crlat="titleText"]'
    _page_title_type = PageTitle

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button)

    @property
    def page_title(self):
        return self._page_title_type(selector=self._page_title)

    @property
    def back_button_exists(self):
        return self._find_element_by_selector(selector=self._back_button, timeout=0) is not None

    def press_back(self):
        self.scroll_to_we()
        self.back_button.click()
