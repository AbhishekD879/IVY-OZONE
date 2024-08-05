from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result
from voltron.utils.js_functions import mouse_event_click as safari_click


class CheckBoxInput(ComponentBase):

    def click(self):
        if self.is_safari:
            safari_click(self._we)
        else:
            get_driver().execute_script("arguments[0].click();", self._we)


class EachWay(ComponentBase):
    _input = 'xpath=.//input'
    _each_way_label = 'xpath=.//*[@data-crlat="label.eachWay"]'

    def is_selected(self, expected_result=True, timeout=1.5, poll_interval=0.5, name=None):
        we = self._find_element_by_selector(selector=self._input)
        return wait_for_result(lambda: we.is_selected(),
                               name=f'Each Way checkbox selected status to be "{expected_result}"',
                               timeout=timeout,
                               poll_interval=poll_interval,
                               expected_result=expected_result)

    @property
    def each_way_label(self):
        return self._get_webelement_text(selector=self._each_way_label).strip()

    @property
    def input(self):
        return CheckBoxInput(selector=self._input, context=self._we, timeout=4)


class EachWayQuickBet(EachWay):
    _label = 'xpath=.//label'
    _input = 'xpath=.//input'

    def click(self):
        ComponentBase(selector=self._label, context=self._we).click()
