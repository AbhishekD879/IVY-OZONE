import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C10469338_Verify_Matches_tab_behavior_after_content_disappearing(Common):
    """
    TR_ID: C10469338
    NAME: Verify 'Matches'  tab behavior after content disappearing
    DESCRIPTION: This test case verifies 'Matches'  tab behavior after content disappearing
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Please see the next test case https://ladbrokescoral.testrail.com/index.php?/cases/view/9776601 to make the necessary settings in CMS
    PRECONDITIONS: - To verify Sports Configs received from the CMS use the next link:
    PRECONDITIONS: https://cms-dev0.coralsports.dev.cloud.ladbrokescoral.com/cms/api/<Brand>/sport-config/<Category ID>
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead:**
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Choose the tab that has ticked 'Check Events' checkbox in CMS
    PRECONDITIONS: 4. Make sure that live and pre-match events are created and 'In-Play' module (Mobile/Tablet only) is switched on
    """
    keep_browser_open = True

    def test_001__trigger_the_undisplaying_of_pre_match_events_on_the_page_use_ob_system_verify_changes_reflection_on_the_page(self):
        """
        DESCRIPTION: * Trigger the undisplaying of pre-match events on the page (Use OB system).
        DESCRIPTION: * Verify changes reflection on the page.
        EXPECTED: * Pre-match events disappear from the page immediately
        EXPECTED: * 'In-Play' module is still displayed
        EXPECTED: * 'No events found' message appears on the page below 'In-Play' module
        """
        pass

    def test_002__refresh_the_page_verify_that_no_events_found_message_disappears(self):
        """
        DESCRIPTION: * Refresh the page.
        DESCRIPTION: * Verify that 'No events found' message disappears
        EXPECTED: * 'In-Play' module is still displayed
        EXPECTED: * 'No events found' message is NOT displayed on the page below 'In-Play' module
        """
        pass

    def test_003__switch_off_the_in_play_module_in_cms_trigger_the_displaying_of_pre_match_events_on_the_page_use_ob_system_refresh_the_page(self):
        """
        DESCRIPTION: * Switch off the 'In-Play' module in CMS.
        DESCRIPTION: * Trigger the displaying of pre-match events on the page (Use OB system).
        DESCRIPTION: * Refresh the page.
        EXPECTED: * Pre-match events are displayed on the page
        EXPECTED: * 'In-Play' module is NOT displayed
        """
        pass

    def test_004__trigger_the_undisplaying_of_all_data_on_the_page_use_ob_system_verify_changes_reflection_on_the_page(self):
        """
        DESCRIPTION: * Trigger the undisplaying of all data on the page (Use OB system).
        DESCRIPTION: * Verify changes reflection on the page.
        EXPECTED: * Pre-match events disappear from the page immediately
        EXPECTED: * 'No events found' message is displayed on the page
        """
        pass

    def test_005__refresh_the_page_verify_which_tab_is_selected(self):
        """
        DESCRIPTION: * Refresh the page.
        DESCRIPTION: * Verify which tab is selected.
        EXPECTED: * The current chosen tab disappears
        EXPECTED: * The first available tab is selected
        EXPECTED: **Note:**
        EXPECTED: - For Tier 1 Sport 'Matches' tab will be visible all the time without dependence on data availability.
        EXPECTED: - For Tier 2 (Desktop only) Sport 'Matches' tab will be visible all the time without dependence on data availability.
        """
        pass
