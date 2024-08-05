import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


# @pytest.mark.tst2 - NA for tst env
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9776091_Verify_Desktop_Mini_Games_widget_displaying_undisplaying_on_FE(BaseUserAccountTest):
    """
    TR_ID: C9776091
    NAME: Verify Desktop Mini Games widget displaying/undisplaying on FE
    DESCRIPTION: This test case verifies Desktop Mini Games widget displaying/undisplaying on FE
    PRECONDITIONS: 1. Desktop Mini games widget is created and configured in CMS > Widgets
    PRECONDITIONS: 2. Desktop Mini games widget is active in CMS.
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_001_load_desktop_app_verify_desktop_mini_games_widget(self):
        """
        DESCRIPTION: Load Desktop App verify Desktop Mini Games widget
        EXPECTED: Desktop Mini Games widget is displayed in Right Column right under Betslip widget
        """
        name = self.get_filtered_widget_name(self.cms_config.constants.MINI_GAMES_TYPE_NAME)
        self.site.wait_content_state(state_name='Homepage')
        mini_games = self.site.right_column.items_as_ordered_dict.get(name)
        self.assertTrue(mini_games, msg='Mini Games widget is not displayed')

    def test_002_in_cms_disable_mini_games_widget_and_verify_changes_on_fe(self):
        """
        DESCRIPTION: In CMS disable Mini Games widget and Verify changes on FE
        EXPECTED: Desktop Mini Games widget is not displayed on FE.
        """
        # This step is NA for Prod
