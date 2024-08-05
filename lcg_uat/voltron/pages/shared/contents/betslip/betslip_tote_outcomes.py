from voltron.pages.shared.components.base import ComponentBase


class SingleToteOutcome(ComponentBase):
    _number = 'xpath=.//*[@data-crlat="outcome.number"]'
    _outcome_name = 'xpath=.//*[@data-crlat="outcome.name"]'

    @property
    def number(self):
        return self._get_webelement_text(selector=self._number)

    @property
    def outcome_name(self):
        return self._get_webelement_text(selector=self._outcome_name)

    @property
    def name(self):
        return '%s %s' % (self.number, self.outcome_name)


class SingleToteOutcomes(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="stake.outcome"]'
    _list_item_type = SingleToteOutcome


class MultipleToteOutcome(ComponentBase):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we, timeout=1).replace('\n', ' - ')


class MultipleToteOutcomes(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="toteBetSlip.leg"]'
    _list_item_type = MultipleToteOutcome
