from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.odds_cards.enhanced_multiples_template import EnhancedMultiplesTemplate
from voltron.pages.shared.components.odds_cards.jackpot_template import JackpotTemplate
from voltron.pages.shared.components.odds_cards.outright_template import OutrightTemplate
from voltron.pages.shared.components.odds_cards.specials_template import SpecialsTemplate
from voltron.pages.shared.components.odds_cards.sport_template import SportTemplate, AggregateSportTemplate
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class SportEventListItem(ComponentBase):
    _odds_card = 'xpath=.//*[starts-with(@data-crlat, "oddsCard") and contains(@data-crlat, "Template")][./div or ./a]' # find if child div exists (tag 'a' - for outright cases)
    _chevron_arrow = 'xpath=.//*[contains(@data-crlat, "chevronArrow") or contains(@class, "chevron")]'
    _see_all_label = 'xpath=.//*[@class="see-all-link"]'

    _templates = {
        'oddsCard.sportTemplate': SportTemplate,
        'oddsCard.sportTemplate-Aggregate': AggregateSportTemplate,
        'oddsCard.enhancedMultiplesTemplate': EnhancedMultiplesTemplate,
        'oddsCard.outrightsTemplate': OutrightTemplate,
        'oddsCard.specialsTemplate': SpecialsTemplate,
        'oddsCard.jackpotTemplate': JackpotTemplate
    }

    _show_stats = 'xpath=.//*[@class="show-stats"]'
    _coupon_stat_widget = 'xpath=.//coupon-stat-widget'
    _hide_stats = 'xpath=.//*[@class="hide-stats"]'

    @property
    def show_stats_link(self):
        return self._find_element_by_selector(selector=self._show_stats, timeout=1)

    @property
    def hide_stats_link(self):
        return self._find_element_by_selector(selector=self._hide_stats, timeout=1)

    @property
    def has_show_stats_link(self):
        return self._find_element_by_selector(selector=self._show_stats, timeout=1) is not None

    @property
    def has_hide_stats_link(self):
        return self._find_element_by_selector(selector=self._hide_stats, timeout=1) is not None

    @property
    def has_coupon_stat_widget(self):
        return self._find_element_by_selector(selector=self._coupon_stat_widget, timeout=1) is not None


    @property
    def aggregated_template(self):
        template_div_we = self._find_element_by_selector(selector=self._odds_card, context=self._we, timeout=0.5)
        if not template_div_we:
            raise VoltronException('Can\'t recognize template type')
        crlat_attr = template_div_we.get_attribute('data-crlat')
        crlat_attr += '-Aggregate'
        template = self._templates[crlat_attr](
            web_element=template_div_we) if crlat_attr is not None and crlat_attr in self._templates else None
        if not template:
            raise VoltronException(f'Event template not identified by data-crlat attribute value: "{crlat_attr}"')
        return template

    @property
    def template(self):
        template_div_we = self._find_element_by_selector(selector=self._odds_card, context=self._we, timeout=0.5)
        if not template_div_we:
            raise VoltronException('Can\'t recognize template type')
        crlat_attr = template_div_we.get_attribute('data-crlat')
        template = self._templates[crlat_attr](web_element=template_div_we) if crlat_attr is not None and crlat_attr in self._templates else None
        if not template:
            raise VoltronException(f'Event template not identified by data-crlat attribute value: "{crlat_attr}"')
        return template

    def has_see_all_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._see_all_label,
                                                                      context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Button shown status to be {expected_result}')
    @property
    def see_all(self):
        return LinkBase(selector=self._see_all_label, timeout=3)

    def click(self):
        self.template.click()

    @property
    def chevron_arrow(self):
        return ComponentBase(selector=self._chevron_arrow, context=self._we, timeout=1)

    def has_chevron_arrow(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._chevron_arrow, timeout=0) is not None,
            name=f'Chevron arrow status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def __getattr__(self, item):
        template = self.template
        self._logger.debug(f'*** Template name: "{template.__class__.__name__}"')
        return getattr(template, item)
