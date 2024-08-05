from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.inplay import InPlayEventGroupHeader, InPlayEventGroup


class InPlaySportGroup(AccordionsList, EventGroup):
    _list_item_type = InPlayEventGroup
    _header_type = InPlayEventGroupHeader
