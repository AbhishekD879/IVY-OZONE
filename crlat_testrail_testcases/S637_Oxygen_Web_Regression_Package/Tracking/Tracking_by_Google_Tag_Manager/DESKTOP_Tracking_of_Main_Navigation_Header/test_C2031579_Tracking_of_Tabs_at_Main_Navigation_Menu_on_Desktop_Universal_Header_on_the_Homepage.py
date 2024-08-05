import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2031579_Tracking_of_Tabs_at_Main_Navigation_Menu_on_Desktop_Universal_Header_on_the_Homepage(Common):
    """
    TR_ID: C2031579
    NAME: Tracking of Tabs at Main Navigation Menu on Desktop Universal Header on the Homepage
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on tabs Main Navigation Menu on Desktop Universal Header on the Homepage.
    DESCRIPTION: Need to run the test case on Desktop.
    PRECONDITIONS: Browser console should be opened.
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Take a look at the following test case https://ladbrokescoral.testrail.com/index.php?/cases/view/28124 for creation tabs in Universal Header by CMS.
    PRECONDITIONS: Links to CMS for different endpoints:
    PRECONDITIONS: DEV - https://coral-cms-dev0.symphony-solutions.eu/
    PRECONDITIONS: TST2 - https://coral-cms-tst2.symphony-solutions.eu/
    PRECONDITIONS: STG2 - https://coral-cms-stg2.symphony-solutions.eu/
    PRECONDITIONS: HL - https://coral-cms-hl.symphony-solutions.eu/
    PRECONDITIONS: PROD - https://coral-cms.symphony-solutions.eu/
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: * Homepage is loaded
        EXPECTED: * Main Navigation Menu is displayed at Desktop Universal Header with list of tabs set via CMS
        """
        pass

    def test_002_click_on_some_tab_in_main_navigation_menu_on_the_homepage_for_example_lottery(self):
        """
        DESCRIPTION: Click on some tab in Main Navigation Menu on the Homepage (for example Lottery)
        EXPECTED: User is navigated to the appropriate page (Target Uri is set in CMS)
        """
        pass

    def test_003_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'navigation',
        EXPECTED: 'eventAction' : 'header',
        EXPECTED: 'eventLabel' : '<< NAV ITEM >>'
        EXPECTED: })
        """
        pass

    def test_004_repeat_steps_2_3_for_other_tabs_from_main_navigation_menu(self):
        """
        DESCRIPTION: Repeat steps 2-3 for other tabs from Main Navigation Menu
        EXPECTED: 
        """
        pass
