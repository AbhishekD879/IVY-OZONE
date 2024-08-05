from voltron.pages.ladbrokes.dialogs.dialog_contents.team_Confirmation import TeamConfirmation
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class ChangeTeam(TeamConfirmation):
    _exit_button = 'xpath=.//button[contains(@class,"SYC-Popup__ctaButton")]'

    def has_exit_button(self, expected_result=True, timeout=3):
        self.scroll_to_we()
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._exit_button, timeout=0) is not None,
                               name=f'{self.__class__.__name__} Exit button displayed status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def exit_button(self):
        return ButtonBase(selector=self._exit_button, timeout=5)
