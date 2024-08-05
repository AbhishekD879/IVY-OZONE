from selenium.common.exceptions import WebDriverException

from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.helpers import find_element


class PreferencesOverlay(ComponentBase):
    # TODO https://jira.egalacoral.com/browse/VOL-1746
    _save_preferences_button = 'xpath=.//button[contains(text(), "Save my preferences")]'

    def click_save_preferences_button(self):
        button = find_element(selector=self._save_preferences_button, timeout=5)
        if button:
            try:
                get_driver().execute_script("arguments[0].click();", button)
            except WebDriverException:
                pass
