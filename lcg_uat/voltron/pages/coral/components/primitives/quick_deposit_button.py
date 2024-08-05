from selenium.common.exceptions import WebDriverException

from voltron.pages.shared.components.primitives.buttons import ButtonNoScrollBase
from voltron.pages.shared.components.quick_deposit_button import QuickDepositButton
from voltron.utils.exceptions.voltron_exception import VoltronException


class CoralQuickDepositButton(ButtonNoScrollBase, QuickDepositButton):

    def click(self, scroll_to=True):
        if scroll_to:
            self.scroll_to_we()
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')


class CoralDepositAndPlaceButton(CoralQuickDepositButton):
    pass
