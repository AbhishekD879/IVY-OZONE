from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.base_contents.sport_base import SportRacingPageBase
from voltron.pages.shared.contents.promotions import PromotionsSection


class DetailDescription(ComponentBase):
    _button = 'xpath=.//a[contains(@class,"btn")]'
    _fanzone_syc_button = 'xpath=.//a[contains(text(), "Show Your Colours")]'
    _link = 'xpath=.//a[contains(text(), "autotest_link")]'
    _in_play_button = 'xpath=.//a[contains(text(), "In-Play")]'
    _home_button = 'xpath=.//a[contains(text(), "Home")]'

    @property
    def button(self):
        return ButtonBase(selector=self._button, context=self._we)

    @property
    def link(self):
        return LinkBase(selector=self._link, context=self._we)

    @property
    def link_url(self):
        return self.link.get_link()

    @property
    def in_play_button(self):
        return ButtonBase(selector=self._in_play_button, context=self._we)

    @property
    def fanzone_syc_button(self):
        return ButtonBase(selector=self._fanzone_syc_button)

    @property
    def home_button(self):
        return ButtonBase(selector=self._home_button, context=self._we)

    @property
    def text(self):
        return self._get_webelement_text(we=self._we)

    @property
    def has_opt_in_button(self):
        return self._find_element_by_selector(selector=self._button, context=self._we, timeout=0.5) is not None


class PromotionDetailsContent(PromotionsSection):
    _promo_detail_description = 'xpath=.//*[@data-crlat="promoDescription"]'
    _image = 'xpath=.//*[@data-crlat="uriMedium"]'

    @property
    def name(self):
        return self.group_header.title_text

    @property
    def detail_description(self):
        return DetailDescription(selector=self._promo_detail_description)

    @property
    def image(self):
        return self._find_element_by_selector(selector=self._image, timeout=2).get_attribute('src')


class TermsAndConditions(EventGroup):
    _terms_details = 'xpath=.//*[@data-crlat="promoDetails"]'

    @property
    def details(self):
        return self._find_element_by_selector(selector=self._terms_details, timeout=2).get_attribute('innerHTML').strip()


class PromotionDetailsTabContent(TabContent):
    _promotion_content = 'xpath=.//*[@data-crlat="promotion.content"]'
    _promotion_content_type = PromotionDetailsContent
    _terms_and_conditions = 'xpath=.//*[@data-crlat="tac"]'
    _terms_and_conditions_type = TermsAndConditions
    _fade_out_overlay = True

    @property
    def promotion(self):
        return self._promotion_content_type(selector=self._promotion_content, context=self._we)

    @property
    def terms_and_conditions(self):
        return self._terms_and_conditions_type(selector=self._terms_and_conditions, context=self._we)

    def _wait_active(self, timeout=15):
        self._we = self._find_myself()
        try:
            self._find_element_by_selector(selector=self._promotion_content, context=self._context,
                                           bypass_exceptions=(NoSuchElementException,))
        except StaleElementReferenceException:
            self._we = self._find_myself()


class PromotionDetails(SportRacingPageBase):
    _url_pattern = r'^http[s]?:\/\/.+\/promotions\/details\/.+'
    _tab_content_type = PromotionDetailsTabContent

    def _wait_active(self, timeout=15):
        self._we = self._find_myself()
        try:
            self._find_element_by_selector(selector=self._tab_content,
                                           bypass_exceptions=(NoSuchElementException, ))
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            self._we = self._find_myself()
