from voltron.pages.shared.components.accordions_container import Accordion


class RightColumnItem(Accordion):
    _header = 'xpath=.//*[@data-crlat="containerHeader"]'
    _content = 'xpath=./*[@data-crlat="containerContent"]'
