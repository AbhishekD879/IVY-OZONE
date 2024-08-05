from voltron.pages.shared.components.home_page_components.home_page_byb_tab import BYBTabContent
from voltron.pages.shared.components.home_page_components.home_page_byb_tab import BYBAccordionsList


class LadbrokesBYBAccordionsList(BYBAccordionsList):
    _item = 'xpath=.//*[@data-crlat="ycAccordion"]'


class LadbrokesBYBTabContent(BYBTabContent):
    _accordions_list_type = LadbrokesBYBAccordionsList
