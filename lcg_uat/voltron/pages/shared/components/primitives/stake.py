import re

from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException


class Stake(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="label"]'
    _value = 'xpath=.//*[@data-crlat="value"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we, timeout=2)

    @property
    def value(self):
        return self._get_webelement_text(selector=self._value, context=self._we, timeout=2)

    @property
    def currency(self):
        value = self.value
        currency = re.match(r'^([^0-9]+)', value)
        if currency:
            return currency.group(1)
        else:
            raise VoltronException('Error occurred parsing stake string "%s"' % value)

    @property
    def amount(self):
        value = self.value
        amount = re.match(r'^([^0-9]+)([0-9]+[\,|\.][0-9]{2})', value)
        if amount:
            return amount.group(2)
        else:
            raise VoltronException('Error occurred parsing stake string "%s"' % value)
