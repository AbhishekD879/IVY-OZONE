import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C10786275_Sports_Tabs_displaying_based_on_data_availability(Common):
    """
    TR_ID: C10786275
    NAME: Sports Tabs displaying based on data availability
    DESCRIPTION: This test case verifies Sports Tabs displaying based on data availability
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - Info about tabs displaying depends on Platforms or Tier Type could be found here: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-TabsdisplayingfordifferentPlatformsandTierTypes
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use the following <sport-config> response:
    PRECONDITIONS: https://<particular env e.g. sports-red-tst2.ladbrokes.com>/cms/api/<Brand>/sport-config/<Category ID>
    PRECONDITIONS: ![](index.php?/attachments/get/100196757)
    PRECONDITIONS: Verify that the available tab should have the parameter **'hidden'** with the value **"false"**
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page
    """
    keep_browser_open = True

    def test_001_verify_sports_tabs_displaying_according_to_received_data_from_cms(self):
        """
        DESCRIPTION: Verify Sports Tabs displaying according to received data from CMS
        EXPECTED: * The Sports Tabs are displayed on the Sports Landing page
        EXPECTED: * Set of Sports Tabs corresponds to data received in <category> response from CMS
        """
        pass

    def test_002_choose_the_tab_that_has_active_check_events_and_enabled_status_could_be_checked_in_cms__sport_pages__sport_categories__sport__tab_and_data_for_this_tab_is_available_on_ss(self):
        """
        DESCRIPTION: Choose the tab that has active 'Check Events' and 'Enabled' status (could be checked in CMS > Sport Pages > Sport Categories > Sport > Tab) and data for this tab is available on SS
        EXPECTED: * The Sports Tab is displayed on the Sports Landing page
        EXPECTED: * Sports Tab is received in <category> response from CMS with **'hidden':"false"** parameter
        """
        pass

    def test_003_choose_the_tab_that_has_active_check_events_and_enabled_status_could_be_checked_in_cms__sport_pages__sport_categories__sport__tab_and_data_for_this_tab_is_not_available_on_ss(self):
        """
        DESCRIPTION: Choose the tab that has active 'Check Events' and 'Enabled' status (could be checked in CMS > Sport Pages > Sport Categories > Sport > Tab) and data for this tab is NOT available on SS
        EXPECTED: * The Sports Tab is NOT displayed on the Sports Landing page
        EXPECTED: * Sports Tab is received in <category> response from CMS but with **'hidden':"true"** parameter
        """
        pass

    def test_004_choose_the_tab_that_has_inactive_check_events_but_active_enabled_status_could_be_checked_in_cms__sport_pages__sport_categories__sport__tab_and_data_for_this_tab_is_available_on_ss(self):
        """
        DESCRIPTION: Choose the tab that has inactive 'Check Events' but active 'Enabled' status (could be checked in CMS > Sport Pages > Sport Categories > Sport > Tab) and data for this tab is available on SS
        EXPECTED: * The Sports Tabs are displayed on the Sports Landing page
        EXPECTED: * Set of Sports Tabs corresponds to data received in <category> response from CMS
        """
        pass

    def test_005_choose_the_tab_that_has_inactive_check_events_but_active_enabled_status_could_be_checked_in_cms__sport_pages__sport_categories__sport__tab_and_data_for_this_tab_is_not_available_on_ss(self):
        """
        DESCRIPTION: Choose the tab that has inactive 'Check Events' but active 'Enabled' status (could be checked in CMS > Sport Pages > Sport Categories > Sport > Tab) and data for this tab is NOT available on SS
        EXPECTED: * The Sports Tab is displayed on the Sports Landing page
        EXPECTED: * Sports Tabs is received in <category> response from CMS
        EXPECTED: * 'No events found' message is displayed on the page
        """
        pass

    def test_006_choose_the_tab_that_has_inactive_enabled_status_could_be_checked_in_cms__sport_pages__sport_categories__sport__tab(self):
        """
        DESCRIPTION: Choose the tab that has inactive 'Enabled' status (could be checked in CMS > Sport Pages > Sport Categories > Sport > Tab)
        EXPECTED: * The Sports Tab is NOT displayed on the Sports Landing page
        EXPECTED: * Sports Tabs is received in <category> response from CMS but with **'hidden':"true"** parameter
        EXPECTED: **Note:**
        EXPECTED: Doesn't matter if 'Check Events' is active or not the tab will be displayed based on 'Enabled' status
        """
        pass

    def test_007__navigate_to_cms__sport_pages__sport_categories__sport__tab_rename_any_sports_tab_save_the_changes(self):
        """
        DESCRIPTION: * Navigate to CMS > Sport Pages > Sport Categories > Sport > Tab.
        DESCRIPTION: * Rename any Sports Tab.
        DESCRIPTION: * Save the changes.
        EXPECTED: The changes are saved successfully
        """
        pass

    def test_008__back_to_the_app_refresh_the_page(self):
        """
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Refresh the page.
        EXPECTED: * Updated name of Sports Tab is displayed on the Sports Landing page
        EXPECTED: * Sports Tab name corresponds to 'displayName' parameter received from CMS in <category> response
        """
        pass

    def test_009__navigate_to_cms__sport_pages__sport_categories__sport_change_the_ordering_of_sports_tabs_by_drag_and_drop(self):
        """
        DESCRIPTION: * Navigate to CMS > Sport Pages > Sport Categories > Sport.
        DESCRIPTION: * Change the ordering of Sports Tabs by drag and drop.
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_010__back_to_the_app_refresh_the_page(self):
        """
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Refresh the page.
        EXPECTED: * The Sports Tabs ordering is changed
        EXPECTED: * The Sports Tabs ordering corresponds to setting in CMS
        EXPECTED: * Ordering of Sports Tabs received in <category> response corresponds to setting in CMS
        """
        pass
