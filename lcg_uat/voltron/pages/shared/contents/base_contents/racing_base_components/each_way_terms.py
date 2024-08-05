import re

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase


class EachWayTerms(ComponentBase):
    _value = 'xpath=.//*[@data-crlat="eachWayContainer"]'

    @property
    def value(self):
        return self._get_webelement_text(selector=self._value, timeout=1)


class ExtraPlace(ComponentBase):

    @property
    def value(self):
        return self._get_webelement_text(we=self._we)

    def is_selected(self, expected_result=None, timeout=0, poll_interval=0.5, name=None):
        font_weight = self.css_property_value(value='font-weight')
        return font_weight == '700'


class EachWayTermsEnhanced(EachWayTerms):
    _odds = 'xpath=.//*[@data-crlat="raceCard.odds"]'
    _item = 'xpath=.//*[@data-crlat="raceCard.place"]'
    _extra_place = 'xpath=.//*[@data-crlat="raceCard.place.selected"]'

    @property
    def odds(self):
        odds = TextBase(selector=self._odds, timeout=2, context=self._we)
        odds.scroll_to()
        return odds.text

    @property
    def label(self):
        text = self._get_webelement_text(we=self._we, timeout=1)
        search = re.search(r'([a-zA-Z]+\s[a-zA-Z]+)', text)
        return search.group(1) if search else ''

    @property
    def places(self):
        return ''.join([self._get_webelement_text(we=item, timeout=1) for item in self._find_elements_by_selector(selector=self._item)])

    @property
    def extra_place(self):
        return ExtraPlace(selector=self._extra_place, context=self._we)

    @property
    def value(self):
        return '%s %s %s%s' % (self.odds, self.label, self.places, self.extra_place.value)


class EachWayRacingResults(EachWayTerms):
    _label = 'xpath=.//td[1]'
    _item = 'xpath=.//td[2]'

    @property
    def label(self):
        return self._get_webelement_text(selector=self._label)

    @property
    def _odds_and_places(self):
        return '-'.join([self._get_webelement_text(we=item) for item in self._find_elements_by_selector(selector=self._item)])

    @property
    def odds(self):
        search = re.search(r'^(\d+\/\d+ odds)', self._odds_and_places)
        return search.group(1) if search else ''

    @property
    def places(self):
        search = re.search(r'[P|p]laces\s([,\d]*)', self._odds_and_places)
        return search.group(0) if search else ''

    @property
    def value(self):
        return '%s%s' % (self.label, self._odds_and_places)
