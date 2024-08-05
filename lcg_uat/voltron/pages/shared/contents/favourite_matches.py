from voltron.pages.shared.components.odds_cards.sport_template import SportTemplate
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.components.banner_section import BannerSection
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.utils.waiters import wait_for_result


class FavEventGroup(EventGroup, SportTemplate):
    _item = 'xpath=.//*[@data-crlat="favourites.groupItem"]'
    _odd_name_first = 'xpath=.//*[@data-crlat="EventFirstName"]'
    _odd_name_second = 'xpath=.//*[@data-crlat="EventSecondName"]'

    @property
    def name(self):
        return '%s v %s' % (self._get_webelement_text(selector=self._odd_name_first),
                            self._get_webelement_text(selector=self._odd_name_second))


class FavouritesAccordionList(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="favourites.group"]'
    _list_item_type = FavEventGroup


class FavouritesTabContent(TabContent):
    _accordions_list_type = FavouritesAccordionList


class Favourites(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/favourites'
    _go_to_in_play = 'xpath=.//*[@data-crlat="goToInPlayMatchesButton"]'
    _go_to_matches = 'xpath=.//*[@data-crlat="goToMatchesButton"]'
    _clear_all_favourites = 'xpath=.//*[@data-crlat="clearFavouritesButton"]'
    _info_label = 'xpath=.//*[@data-crlat="widgetLoggedText"]'
    _please_login = 'xpath=.//*[@data-crlat="textMsg"]'
    _login_button = 'xpath=.//*[@data-crlat="signInButton"]'
    _banner_section = 'xpath=.//banners-section'
    _banner_section_type = BannerSection
    _tab_content_type = FavouritesTabContent
    _fade_out_overlay = True
    _verify_spinner = True

    @property
    def banner_section(self):
        return self._banner_section_type(selector=self._banner_section, context=self._we, timeout=3)

    @property
    def please_login_text(self):
        return self._wait_for_not_empty_web_element_text(selector=self._please_login, timeout=0.5)

    @property
    def has_info_label(self):
        result = wait_for_result(lambda: self._get_webelement_text(selector=self._info_label, timeout=0) != '',
                                 name='Waiting for error message',
                                 timeout=3,
                                 poll_interval=0.3)
        return result

    @property
    def info_label(self):
        label = self._get_webelement_text(selector=self._info_label, timeout=2)
        return ' '.join(label.split())

    @property
    def login_button(self):
        return ButtonBase(selector=self._login_button, context=self._we)

    @property
    def go_to_matches_button(self):
        return ButtonBase(selector=self._go_to_matches, context=self._we)

    @property
    def go_to_in_play_matches(self):
        return ButtonBase(selector=self._go_to_in_play, context=self._we)

    @property
    def clear_all_favourites(self):
        return ButtonBase(selector=self._clear_all_favourites, context=self._we)
