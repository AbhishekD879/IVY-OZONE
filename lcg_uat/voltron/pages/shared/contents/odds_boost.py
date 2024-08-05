from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.components.base import ComponentBase
from collections import OrderedDict
from multidict import MultiDict


class OddsBoostsSection(ComponentBase):
    _header = 'xpath=.//*[@data-crlat="sectionHeader"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._header, timeout=1)


class OddsBoostItem(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="oddsBoostTitle"]'
    _details = 'xpath=.//*[@data-crlat="oddsBoostDetails"]'
    _expiration_date = 'xpath=.//*[@data-crlat="useByDate"]'
    _arrow_link = 'xpath=.//*[@data-crlat="oddsBoostIcon"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._title, timeout=1)

    @property
    def details(self):
        return self._get_webelement_text(selector=self._details, timeout=1)

    @property
    def arrow_link(self):
        return self.ButtonBase(selector=self._arrow_link, context=self._we)


class OddsBoostSectionItem(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="multiSport" or @data-crlat="categoryName" or @class="category-name" or @class="multiSport" ]'
    _list_item_type = OddsBoostItem
    _item = 'xpath=.//*[@data-crlat="oddsBoostCard"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._title, timeout=1)


class TodayOddsBoosts(OddsBoostsSection):
    _login_button = 'xpath=.//*[@data-crlat="logIn"]'
    _available_now_amount = 'xpath=.//*[@data-crlat="availableNowAmount"]'
    _upcoming_amount = 'xpath=.//*[@data-crlat="upcomingAmount"]'
    _odds_boost_description = 'xpath=.//*[@data-crlat="oddsBoostsDescription"]'

    @property
    def description(self):
        return self._get_webelement_text(selector=self._odds_boost_description)

    @property
    def login_button(self):
        return ButtonBase(selector=self._login_button, context=self._we)

    @property
    def available_now(self):
        return TextBase(selector=self._available_now_amount, context=self._we)

    @property
    def upcoming_boosts(self):
        return TextBase(selector=self._upcoming_amount, context=self._we)


class SportPillsItem(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="filter"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._title, timeout=1)


class SportPills(ComponentBase):
    _list_item_type = SportPillsItem
    _item = 'xpath=.//*[@data-crlat="filterWrapper"]'


class BoostsAvailableNow(OddsBoostsSection):
    _list_item_type = OddsBoostItem
    _item = 'xpath=.//*[@data-crlat="oddsBoostCard"]'
    _section_item = 'xpath=.//li'
    _section_item_type = OddsBoostSectionItem

    @property
    def name(self):
        return self._we.get_attribute('data-crlat')

    @property
    def items_as_ordered_dict(self) -> MultiDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(
            '*** Found %s %s items' % (len(items_we), self.__class__.__name__ + ' - ' + self._list_item_type.__name__))
        items_ordered_dict = []
        for item_we in items_we:
            list_item_type = self._list_item_type(web_element=item_we)
            items_ordered_dict.append((list_item_type.name, list_item_type))
        return MultiDict(items_ordered_dict)

    @property
    def section_items_as_ordered_dict(self) -> MultiDict:
        items_we = self._find_elements_by_selector(selector=self._section_item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._section_item_type(web_element=item_we)
            list_item.scroll_to()
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict


class UpcomingBoosts(BoostsAvailableNow):
    _upcoming_boosts = 'xpath=.//*[@data-crlat="upcomingBoostsList"]'


class TermsAndConditions(OddsBoostsSection):
    _header = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _terms_and_conditions = 'xpath=.//*[@data-crlat="termsAndConditionsContent"]'

    @property
    def description(self):
        return self._get_webelement_text(selector=self._terms_and_conditions)


class OddsBoost(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+/(oddsboost|superbooster)$'
    _odds_boost_page = 'tag=odds-boost-page'

    @property
    def sections(self):
        return OddsBoostSections(selector=self._odds_boost_page, context=self._we)


class OddsBoostSections(ComponentBase):
    _item = 'xpath=.//*[contains(@data-crlat, "oddsBoostSection")]'
    _sport_pills = 'xpath=.//*[@data-crlat="sportPills"]'

    _odds_boost_section_types = {
        'oddsBoostSection.Upcoming': UpcomingBoosts,
        'oddsBoostSection.Todays': TodayOddsBoosts,
        'oddsBoostSection.Available': BoostsAvailableNow,
        'oddsBoostSection.TermsAndConditions': TermsAndConditions}

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            odds_boost_type = self._odds_boost_section_types[item_we.get_attribute('data-crlat')]
            list_item_type = odds_boost_type(web_element=item_we)
            name = list_item_type.name
            items_ordered_dict.update({name: list_item_type})
        return items_ordered_dict

    @property
    def sports_pills(self):
        return SportPills(selector=self._sport_pills, timeout=2)
