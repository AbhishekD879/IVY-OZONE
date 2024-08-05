from collections import OrderedDict

from voltron.pages.shared.components.markets.your_call_specials_market import SportsYourCallEventGroup
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.components.your_call_static_block import YourCallStaticBlock
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.base_contents.sport_base import SportPageBase


class YourCallEventSlide(EventGroup):
    _home_team = 'xpath=.//*[@data-crlat="homeTeamTitle"]'
    _away_team = 'xpath=.//*[@data-crlat="visitingTeamTitle"]'
    _go_to_event_link = 'xpath=.//*[@data-crlat="goToEvent"]'
    _start_time = 'xpath=.//*[@data-crlat="eventDate"]'

    @property
    def go_to_event_link(self):
        return LinkBase(selector=self._go_to_event_link, context=self._we)

    @property
    def event_name(self):
        return self.name

    @property
    def start_time(self):
        return TextBase(selector=self._start_time, context=self._we, timeout=1)

    @property
    def home_team(self):
        return TextBase(selector=self._home_team, context=self._we, timeout=1)

    @property
    def away_team(self):
        return TextBase(selector=self._away_team, context=self._we, timeout=1)

    @property
    def name(self):
        return '%s %s %s' % (self.home_team.get_attribute('innerHTML'),
                             self.away_team.get_attribute('innerHTML'),
                             self.start_time.get_attribute('innerHTML'))

    def scroll_to_we(self, web_element=None):
        # overridden with empty body because of breaks slider functionality
        # after scrolling it content with javascript
        pass


class YourCallEventsSlideGroup(EventGroup):
    _item = 'xpath=.//*[@data-crlat="eventEntity"]'
    _list_item_type = YourCallEventSlide

    def scroll_to_we(self, web_element=None):
        # overridden with empty body because of breaks slider functionality
        # after scrolling it content with java script
        pass


class YourCallAccordionsList(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="accordion" and not(contains(@class, "page-inner-container"))]'
    _static_block = 'xpath=.//*[@data-crlat="yourcallStaticBlock"]'
    _static_block_type = YourCallStaticBlock
    _section_type_tag = 'xpath=.//*[contains(@data-crlat, "yourcall.")]'
    _section_types = {'yourcall.carousel': YourCallEventsSlideGroup,
                      'yourcall.specials': SportsYourCallEventGroup}

    def _get_yc_section(self, section):
        # have to do this initialization to handle correct expanding
        yc_section = EventGroup(web_element=section)
        yc_section.expand()

        section_type_name = self._find_element_by_selector(selector=self._section_type_tag,
                                                           context=section, timeout=1).get_attribute("data-crlat")
        section_type = self._section_types.get(section_type_name, YourCallEventsSlideGroup)
        self._logger.debug(f'*** Recognized {section_type.__name__} section type ')
        return section_type(web_element=section)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items = OrderedDict()
        for item_we in items_we:
            item_type = self._get_yc_section(section=item_we)
            items.update({item_type.name: item_type})
        return items

    @property
    def static_block(self):
        return YourCallStaticBlock(selector=self._static_block)


class YourCallTabContent(TabContent):
    _accordions_list_type = YourCallAccordionsList


class YourCall(SportPageBase):
    _url_pattern = r'^http[s]?:\/\/.+\/yourcall'
    _tab_content_type = YourCallTabContent

    @property
    def tab_content(self):
        return self._tab_content_type(web_element=self._we, selector=self._selector)
