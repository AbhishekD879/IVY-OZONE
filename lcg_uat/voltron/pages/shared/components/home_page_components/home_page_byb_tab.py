from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase, FavouritesIcon
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.utils.waiters import wait_for_result


class EventDetailsContainer(ComponentBase):
    _item = 'xpath=.//*[contains(@data-crlat, "team")]'
    _list_item_type = TextBase
    _home_team = 'xpath=.//*[@data-crlat="teamHome"]'
    _away_team = 'xpath=.//*[@data-crlat="teamAway"]'
    _date = 'xpath=.//*[@data-crlat="eventDate"]'

    @property
    def home_team(self):
        return self._get_webelement_text(selector=self._home_team, timeout=0.5)

    @property
    def away_team(self):
        return self._get_webelement_text(selector=self._away_team, timeout=0.5)

    @property
    def event_name(self):
        return f'{self.home_team} vs {self.away_team}'

    @property
    def event_date(self):
        return self._get_webelement_text(selector=self._date, timeout=1)


class BYBEvent(ComponentBase):
    _event_details_container = 'xpath=.//*[@data-crlat="eventDetails"]'
    _event_details_container_type = EventDetailsContainer
    _go_to_event_link = 'xpath=.//*[@data-crlat="goToEventLink"]'
    _favorite_icon = 'xpath=.//*[@data-crlat="favouriteIcon"]'

    @property
    def team_names_container(self):
        return self._event_details_container_type(selector=self._event_details_container, context=self._we)

    @property
    def event_name(self):
        return self.team_names_container.event_name

    @property
    def event_date(self):
        return self.team_names_container.event_date

    @property
    def go_to_event_link(self):
        return ButtonBase(selector=self._go_to_event_link, context=self._we)

    @property
    def favourite_icon(self):
        return FavouritesIcon(selector=self._favorite_icon, context=self._we)

    def has_favourite_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._favorite_icon,
                                                   timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_go_to_event_link(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._go_to_event_link,
                                                   timeout=0) is not None,
            name=f'Link status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class BYBEventGroup(EventGroup):
    _item = 'xpath=.//*[@data-crlat="eventEntity"]'
    _list_item_type = BYBEvent
    # workaround, spinner is always in DOM, it is actually a section itself
    _local_spinner = 'xpath=.//*[not(contains(@class, "container-inner-content")) and contains(@data-crlat, "spinner.loader") or contains(@class, "spinner-loader")]'


class BYBAccordionsList(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="ycAccordion"]/section[@data-crlat="accordion"]'
    _list_item_type = BYBEventGroup
    # workaround, spinner is always in DOM, it is actually a section itself
    _local_spinner = 'xpath=.//*[not(contains(@class, "container-inner-content")) and contains(@data-crlat, "spinner.loader") or contains(@class, "spinner-loader")]'


class BYBTabContent(TabContent):
    _accordions_list_type = BYBAccordionsList
