from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase


class BoostButton(ButtonBase):
    _boost_indicator = 'xpath=.//*[@data-crlat="boostIndicator"]'

    @property
    def boost_indicator(self):
        return ComponentBase(selector=self._boost_indicator, context=self._we).get_attribute('class')

    @property
    def has_boost_indicator(self):
        return self._find_element_by_selector(selector=self._boost_indicator, timeout=0) is not None


class OddsBoostHeader(ComponentBase):
    _odds_boost_label = 'xpath=.//*[@data-crlat="oddsBoostText"]'
    _tap_to_boost_your_betslip_label = 'xpath=.//*[@data-crlat="tapToBoostText"]'
    _info_icon = 'xpath=.//*[@data-crlat="infoButton"]'
    _odds_boost_button = 'xpath=.//*[@data-crlat="oddsBoostButton"]'

    @property
    def odds_boost_label(self):
        return TextBase(selector=self._odds_boost_label, context=self._we)

    @property
    def tap_to_boost_your_betslip_label(self):
        return TextBase(selector=self._tap_to_boost_your_betslip_label, context=self._we)

    @property
    def info_button(self):
        return ButtonBase(selector=self._info_icon, context=self._we)

    @property
    def boost_button(self):
        return BoostButton(selector=self._odds_boost_button, context=self._we)
