from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.football import Football
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.sports_tab_contents.matches_tab_content import MatchesTabContent


class SinglePageAccordionList(AccordionsList):
    _name = 'xpath=.//*[@data-crlat="sportSectionHeader"]'

    def _wait_active(self, timeout=20):
        self._we = self._find_myself()
        self._wait_all_items(poll_interval=3, timeout=timeout)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we, timeout=1)


class AmericanFootball(Football):
    _url_pattern = \
        r'^https?:\/\/.+\/american-football(\/)?(live|matches|coupons|outrights|competitions|specials)?(\/)?(today|tomorrow|future)?$'


class Basketball(Football):
    _url_pattern = r'^https?:\/\/.+\/basketball(\/)?(live|matches|competitions|specials|coupons|outrights)?(\/)?(today|tomorrow|future)?'


class Baseball(Football):
    _url_pattern = r'^https?:\/\/.+\/baseball(\/)?(live|matches|coupons|outrights|competitions|specials)?(\/)?(today|tomorrow|future)?$'
    _tab_content_type = MatchesTabContent
    _section = 'xpath=.//*[@data-crlat="sportSectionHeader"]'

    @property
    def section(self):
        return TextBase(selector=self._section, context=self._we, timeout=5)

    @property
    def tab_content(self):
        return self._tab_content_type(selector=self._tab_content)
