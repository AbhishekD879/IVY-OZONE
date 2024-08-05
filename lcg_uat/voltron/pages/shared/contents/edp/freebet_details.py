from datetime import datetime

from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class FreeBetDetails(ComponentBase):
    _used_by = 'xpath=.//*[@data-crlat="usedBy"]'
    _expires = 'xpath=.//*[@data-crlat="expires"]'
    _value = 'xpath=.//*[@data-crlat="amount"]'
    _name = 'xpath=.//*[@data-crlat="freebetName"]'
    _link = 'xpath=.//*[@data-crlat="betNowLink"] | .//*[@data-crlat="fbLink"]'
    _no_freebets = 'xpath=.//*[@data-crlat="noFreeBets"]'
    _fb_icon = 'xpath=.//*[@data-crlat="fbIcon"]'

    def has_fb_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._fb_icon,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Expires status to be {expected_result}')

    def has_expires(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._expires,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Expires status to be {expected_result}')

    @property
    def expires(self):
        expire_date = self._find_element_by_selector(selector=self._expires, timeout=2)
        if expire_date:
            return expire_date.text
        return ''

    @property
    def used_by(self):
        date = self._find_element_by_selector(selector=self._used_by, timeout=0)
        if date:
            return datetime.strptime(date.text, '%d/%m/%Y %H:%M:%S')
        return ''

    @property
    def title(self):
        title = self._find_element_by_selector(selector=self._name)
        if title:
            return title.text
        else:
            raise VoltronException('Freebet\'s title is not shown')

    @property
    def value(self):
        value = self._find_element_by_selector(selector=self._value, timeout=0)
        if value:
            return float(self.strip_currency_sign(value.text).replace(' Free Bet', ''))
        else:
            raise VoltronException('Freebet\'s value is not shown')

    @property
    def bet_now(self):
        return ButtonBase(selector=self._link, context=self._we)
