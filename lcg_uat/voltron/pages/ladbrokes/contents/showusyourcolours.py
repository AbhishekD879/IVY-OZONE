from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result


class SYCTeams(ComponentBase):
    _name = 'xpath=.//*[contains(@class,"crest-image__card-text")]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=5)

    def is_highlighted(self, expected_result=True, timeout=2, poll_interval=0.5, name=None):
        result = wait_for_result(lambda: 'highlight' in self._we.get_attribute('class'),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name)
        return result


class ShowUsYourColours(ComponentBase):
    _select_your_team_message = 'xpath=.//*[@class="select-your-team__message select-your-team__text"]'
    _i_dont_support_any_teams = 'xpath=.//*[contains(text(),"I don\'t support any of these teams")]'
    _item = 'xpath=.//*[contains(@class,"card select-your-team__card")]'
    _list_item_type = SYCTeams
    _back_button = 'xpath=.//*[@data-crlat="btnBack"]'

    @property
    def select_your_team_message(self):
        return self._find_element_by_selector(selector=self._select_your_team_message, timeout=5)

    @property
    def i_dont_support_any_teams(self):
        return self._find_element_by_selector(selector=self._i_dont_support_any_teams, timeout=5)

    @property
    def back_button(self):
        return self._find_element_by_selector(selector=self._back_button, context=self._we)
