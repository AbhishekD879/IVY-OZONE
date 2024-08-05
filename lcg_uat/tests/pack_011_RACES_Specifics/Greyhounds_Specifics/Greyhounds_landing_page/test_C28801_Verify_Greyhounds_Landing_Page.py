import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C28801_Verify_Greyhounds_Landing_Page(Common):
    """
    TR_ID: C28801
    NAME: Verify Greyhounds Landing Page
    DESCRIPTION: This test case verifies Greyhounds landing page
    PRECONDITIONS: Make sure that events for all tabs are available on the Site Server for <Race> sports
    """
    keep_browser_open = True
    expected_tabs = ['TODAY', 'TOMORROW', 'FUTURE']

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        """
        self.site.wait_content_state('homepage')

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap Greyhounds icon from the Sports Menu Ribbon
        EXPECTED: 1.  Greyhounds landing page is opened
        EXPECTED: 2.  'Today' tab is opened by default
        EXPECTED: 3.  Banner carousel if it is configured on the CMS is displayed above the all tabs
        """
        sport_name = vec.sb.GREYHOUND if tests.settings.brand == 'ladbrokes' else vec.sb.GREYHOUND.upper()
        self.site.open_sport(name=sport_name, timeout=15)
        if self.brand == 'ladbrokes':
            today = vec.sb.TABS_NAME_TODAY
        else:
            today = vec.sb.SPORT_DAY_TABS.today
        self.site.greyhound.tabs_menu.click_button(today)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(today).is_selected(),
                        msg='"Today tab" is not present')

    def test_003_check_4_tabs_displaying(self):
        """
        DESCRIPTION: Check 4 tabs displaying
        EXPECTED: 'Today', 'Tomorrow', 'Future' and 'Results' tabs are displayed in one row
        EXPECTED: Results tab was removed in OX98
        """
        ui_tabs = list(self.site.greyhound.tabs_menu.items_as_ordered_dict.keys())
        for tab in self.expected_tabs:
            self.assertIn(tab, ui_tabs, msg=f'Actual tab "{tab}" is not in'
                                            f'Expected tab "{ui_tabs}"')
