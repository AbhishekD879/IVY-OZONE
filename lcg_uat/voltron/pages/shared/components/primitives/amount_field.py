import re
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.voltron_exception import VoltronException


class AmountField(ComponentBase):

    @property
    def _text(self):
        wait_for_result(lambda: self._get_webelement_text(we=self._we),
                        name='Amount field text to display',
                        timeout=3)
        text = self._get_webelement_text(we=self._we)
        if not text:
            raise VoltronException(f'Cannot get text for {self.__class__.__name__}. Current result: {text}')
        return text

    def __str__(self):
        return str(self._text)

    @property
    def _parsed_string(self):
        text = self._text
        matched = re.match(r'^(£|\$|€|Kr)([0-9\.,]+)$', text, re.U)
        if matched is not None and matched.group(2) is not None:
            currency_symbol = matched.group(1)
            amount = matched.group(2)
            return currency_symbol, amount
        else:
            self._logger.error('*** Failed parsing string: "%s"' % text)
            return '', text

    @property
    def currency(self):
        return self._parsed_string[0]

    @property
    def value(self):
        return self._parsed_string[1]
