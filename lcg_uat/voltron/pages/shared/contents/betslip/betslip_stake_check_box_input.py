
from voltron.pages.shared.contents.betslip.betslip_each_way import CheckBoxInput
from voltron.utils.waiters import wait_for_result


class StakeCheckboxInput(CheckBoxInput):

    def is_selected(self, expected_result=True, timeout=1, poll_interval=0.5, name=None):
        return wait_for_result(lambda: self._we.is_selected(),
                               timeout=timeout,
                               poll_interval=poll_interval,
                               name=f'{self.__class__.__name__} selected status to be {expected_result}',
                               expected_result=expected_result)
