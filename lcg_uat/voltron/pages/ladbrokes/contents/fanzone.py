from voltron.pages.shared.components.grouping_buttons import GroupingSelectionButtons
from voltron.pages.shared.components.odds_cards.sport_template import SportTemplate
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.sports_tab_contents.popular_bets_tab_content import PopularBetCard
from voltron.pages.shared.contents.trending_bets.trending_bets import TrendingBetCard
from voltron.utils.waiters import wait_for_result
from collections import OrderedDict


class FanZoneEvents(ComponentBase):
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'
    _name = 'xpath=.//*[@data-crlat="oddsNames"]'

    @property
    def bet_button(self):
        return ButtonBase(selector=self._bet_button, context=self._we)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)


class FanZoneEventGroup(Accordion):
    _name = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _item = 'xpath=.//*[@data-crlat="oddsCard"]'
    _list_item_type = FanZoneEvents

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)


class OutrightAccordionsList(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="accordion"]'
    _list_item_type = FanZoneEventGroup


class FanZoneItems(TabContent):
    _name = 'xpath=.//*[@class="event-title-bar__container"]/*[@data-crlat="defBar"]'
    _accordions_list = 'xpath=.//*[@data-crlat="accordionsList"]'
    _accordions_list_type = OutrightAccordionsList

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)


class FanZoneAccordionList(ComponentBase):
    _item = 'xpath=.//*[@class="fz-outrights-header"]/following-sibling::div[*]'
    _list_item_type = FanZoneItems


class FanZoneHighlightCarousel(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"] | .//*[@data-crlat="highlightsCarousel.title"]'
    _item = 'xpath=.//*[@data-crlat="oddsCard.sportTemplate"]'
    _list_item_type = SportTemplate

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)


class FanzonePromotion(ComponentBase):
    _name = 'xpath=.//*[@class="club-title"]'
    _banner = 'xpath=.//*[@class="club-banner"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)

    @property
    def banner(self):
        return self._find_element_by_selector(selector=self._banner, timeout=5)

class FanzoneYourBetCard(TrendingBetCard):
    _name = 'xpath=.//*[@data-crlat="fzBetCard.outcome"]'
    _market_name = 'xpath=.//*[@data-crlat="fzBetCard.market"]'
    _event_name = 'xpath=.//*[@data-crlat="fzBetCard.event"]'
    _backed = 'xpath=.//*[@data-crlat="fzBetCard.backedTxt"]'
    _odd = 'xpath=.//*[@data-crlat="fzBetCard.priceOddsBtn"]'
    @property
    def name(self):
        return f'{self._get_webelement_text(selector=self._name, timeout=5)} {self._get_webelement_text(selector=self._market_name, timeout=5)}'

    @property
    def bet_button(self):
        return BetButton(selector=self._odd, context=self._we)

class PopularbetsYourTeam(Accordion):
    _name = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _item = 'xpath=.//*[@data-crlat="fanzoneBetsCarouselSlide"]'
    _list_item_type = FanzoneYourBetCard

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)


class FanzoneOtherFanBetCard(PopularBetCard):
    _name = 'xpath=.//*[@data-crlat="fzOtherBetsbasedCard.outcome"]'
    _market_name = 'xpath=.//*[@data-crlat="fzOtherBetsbasedCard.eventMarket"]'
    _backed_text = 'xpath=.//*[@data-crlat="fzOtherBetsbasedCard.backedTxt"]'
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'


class PopularbetsOtherFanBets(Accordion):
    _name = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _item = 'xpath=.//*[@class="card"]'
    _show_more = 'xpath=.//*[@data-crlat="toggleIcon"]'
    _show_less = 'xpath=.//*[@data-crlat="toggleIcon"]'
    _list_item_type = FanzoneOtherFanBetCard

    @property
    def show_more(self):
        return ButtonBase(selector=self._show_more, context=self._we)

    @property
    def show_less(self):
        return ButtonBase(selector=self._show_more, context=self._we)


    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)


class FanzonePopularBets(AccordionsList):
    _item = 'xpath=.//accordion'
    _accordions_list_type = {
        "fz-your-acc": PopularbetsYourTeam,
        "fzotherFansBasedAcc": PopularbetsOtherFanBets
    }


    def _get_accordion_type(self, section):
        self.scroll_to_we(section)
        accordion_type = self._accordions_list_type[section.get_attribute('data-crlat')]
        return accordion_type

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_as_ordered_dict = OrderedDict()
        for item_we in items_we:
            accordion_template_type = self._get_accordion_type(section=item_we)
            accordion_template = accordion_template_type(web_element=item_we)
            items_as_ordered_dict.update({accordion_template.name: accordion_template})
        return items_as_ordered_dict


class FanZoneTabContent(TabContent):
    _highlight_carousel = 'xpath=.//*[@data-crlat="highlight-carousel-container"]|.//*[contains(@class,"highlight_carousel")]'
    _highlight_carousel_type = FanZoneHighlightCarousel
    _fanzone_popular_bets = 'xpath=.//fz-popular-bets'
    _fanzone_popular_bets_type = FanzonePopularBets
    _accordions_list = 'xpath=.//fanzone-outrights'
    _accordions_list_type = FanZoneAccordionList
    _club_container = 'xpath=.//*[contains(@class,"club-promo-description")]'
    _club_container_type = FanzonePromotion

    @property
    def popular_bets(self):
        return self._fanzone_popular_bets_type(selector=self._fanzone_popular_bets, context=self._we)

    @property
    def highlight_carousels(self):
        items_we = self._find_elements_by_selector(selector=self._highlight_carousel, context=self._we)
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            highlight_carousel = self._highlight_carousel_type(web_element=item_we)
            items_ordered_dict[highlight_carousel.name] = highlight_carousel
        return items_ordered_dict

    def has_highlight_carousels(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._highlight_carousel, timeout=0) is not None,
            expected_result=expected_result,
            timeout=timeout,
            name=f'Highlight carousel status to be "{expected_result}"')

    @property
    def club_container(self):
        items_we = self._find_elements_by_selector(selector=self._club_container, context=self._we)
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            club_container = self._club_container_type(web_element=item_we)
            items_ordered_dict[club_container.name] = club_container
        return items_ordered_dict


class PremierLeague(BaseContent):
    _league_table_opened = 'xpath=.//*[@class="league-table-opened"]'
    _close_button = 'xpath=.//*[@class="btn-close"]'

    def is_league_table_opened(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._league_table_opened, timeout=0) is not None,
            name=f'league table opened status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def close_button(self):
        return self._find_element_by_selector(selector=self._close_button, context=self._we)


class FanZone(BaseContent):
    _tabs_menu = 'xpath=.//*[@data-crlat="switchers"]'
    _tabs_menu_type = GroupingSelectionButtons
    _tab_content = 'xpath=.//fanzone-home'
    _tab_content_type = FanZoneTabContent
    _setting_link = 'xpath=.//*[@class = "fanzone-preference"]'
    _premier_leauge_table = 'xpath=.//*[@data-crlat="premierLeagueTableTitle"]'
    _premier_league = 'xpath=.//*[@class="modal-content"]'
    _fanzone_heading = 'xpath=.//*[@class="fanzone-heading"]'
    _fanzone_banner_header = 'xpath=.//*[@class="fanzone-banner"]/header'
    _team_icon = 'xpath=.//*[contains(@class, "fanzone-icon")]'

    @property
    def tabs_menu(self):
        return self._tabs_menu_type(selector=self._tabs_menu, context=self._we, timeout=5)

    @property
    def premier_leauge_link(self):
        return self._find_element_by_selector(selector=self._premier_leauge_table, timeout=5)

    @property
    def setting_link(self):
        return ButtonBase(selector=self._setting_link, context=self._we)

    @property
    def fanzone_heading(self):
        return self._get_webelement_text(selector=self._fanzone_heading, context=self._we)

    @property
    def team_icon(self):
        return self._find_element_by_selector(selector=self._team_icon, context=self._we)

    @property
    def tab_content(self) -> TabContent:
        return self._tab_content_type(selector=self._tab_content, context=self._we)

    @property
    def premier_leauge(self):
        return PremierLeague(selector=self._premier_league, timeout=5)

    @property
    def fanzone_banner_header(self):
        return self._find_element_by_selector(selector=self._fanzone_banner_header, timeout=5)
