from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent


class LadbrokesComponentBase(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="emAccordion"]'


class LadbrokesEnhancedMultiplesTabContent(TabContent):
    _accordions_list = 'xpath=..//*[@data-crlat="tab.showEnhancedMultiplesModule"]'
    _accordions_list_type = LadbrokesComponentBase
