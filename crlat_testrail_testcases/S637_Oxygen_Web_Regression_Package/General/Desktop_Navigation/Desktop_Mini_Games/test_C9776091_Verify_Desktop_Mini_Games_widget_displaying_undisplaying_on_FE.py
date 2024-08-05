import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9776091_Verify_Desktop_Mini_Games_widget_displaying_undisplaying_on_FE(Common):
    """
    TR_ID: C9776091
    NAME: Verify Desktop Mini Games widget displaying/undisplaying on FE
    DESCRIPTION: This test case verifies Desktop Mini Games widget displaying/undisplaying on FE
    PRECONDITIONS: 1. Desktop Mini games widget is created and configured in CMS > Widgets
    PRECONDITIONS: 2. Desktop Mini games widget is active in CMS.
    """
    keep_browser_open = True

    def test_001_load_desktop_app_verify_desktop_mini_games_widget(self):
        """
        DESCRIPTION: Load Desktop App verify Desktop Mini Games widget
        EXPECTED: Desktop Mini Games widget is displayed in Right Column right under Betslip widget
        """
        pass

    def test_002_in_cms_disable_mini_games_widget_and_verify_changes_on_fe(self):
        """
        DESCRIPTION: In CMS disable Mini Games widget and Verify changes on FE
        EXPECTED: Desktop Mini Games widget is not displayed on FE.
        """
        pass
