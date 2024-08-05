from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.sport_list_item import SportEventListItem
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.utils.exceptions.voltron_exception import VoltronException


class OutrightsSportEventListItem(SportEventListItem):

    @property
    def template(self):
        template_div_we = self._we
        if not template_div_we:
            raise VoltronException('Can\'t recognize template type')
        crlat_attr = template_div_we.get_attribute('data-crlat')
        template = self._templates[crlat_attr](
            web_element=template_div_we) if crlat_attr is not None and crlat_attr in self._templates else None
        if not template:
            raise VoltronException(f'Event template not identified by data-crlat attribute value: "{crlat_attr}"')
        return template

    def __getattr__(self, item):
        template = self.template
        self._logger.debug(f'*** Template name: "{template.__class__.__name__}"')
        return getattr(template, item)


class OutrightsEventGroup(EventGroup):
    _item = 'xpath=.//*[contains(@data-crlat, "oddsCard") and contains(@data-crlat, "Template")]' \
            '[./div or ./a]'  # find if child div exists (tag 'a' - for outright cases)
    _list_item_type = OutrightsSportEventListItem


class OutrightsAccordionsList(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="accordion"]'
    _list_item_type = OutrightsEventGroup


class OutrightsTabContent(TabContent):
    _accordions_list_type = OutrightsAccordionsList
