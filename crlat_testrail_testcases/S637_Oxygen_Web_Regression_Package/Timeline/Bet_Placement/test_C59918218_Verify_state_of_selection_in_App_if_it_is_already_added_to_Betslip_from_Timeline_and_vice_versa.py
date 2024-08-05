import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.timeline
@vtest
class Test_C59918218_Verify_state_of_selection_in_App_if_it_is_already_added_to_Betslip_from_Timeline_and_vice_versa(Common):
    """
    TR_ID: C59918218
    NAME: Verify state of selection in App  if it is already added to Betslip from Timeline and vice versa
    DESCRIPTION: This test case verifies the state of selection in App if it is already added to Betslip from Timeline and vice versa
    PRECONDITIONS: "Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the toal number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: 2.Timeline should be enabled in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Enabled' checkbox ) and also, Timeline should be turned ON in the general System configuration ( CMS -> 'System configuration' -> 'Structure' -> 'FeatureToggle' section -> 'Timeline' )
    PRECONDITIONS: 3.Timeline is available for the configured pages in CMS ( CMS -> 'Timeline' section -> 'Timeline System Config' item -> 'Page Urls' field )
    PRECONDITIONS: 4.Timeline posts with prices are created and published
    PRECONDITIONS: Zeplin Design -
    PRECONDITIONS: -Load the app
    PRECONDITIONS: -User is logged in
    PRECONDITIONS: -Selection from app is already added to Betslip. The same selection is configured in Timeline
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse"
    """
    keep_browser_open = True

    def test_001_navigate_to_the_page_with_configured_timeline_eghomefeatured(self):
        """
        DESCRIPTION: Navigate to the page with configured 'Timeline' (e.g./home/featured)
        EXPECTED: Timeline is displayed at the bottom of the page, above Footer menu
        """
        pass

    def test_002_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - **Green 'selected' state is shown in timeline for that selection that already added to Betslip from app**
        """
        pass

    def test_003___uncheck_this_selection__navigate_to_page_in_app_where_it_was_selected_beforeeg_edp_page(self):
        """
        DESCRIPTION: - Uncheck this selection
        DESCRIPTION: - Navigate to page in app where it was selected before,e.g. EDP page
        EXPECTED: - 'Selected' state isn't green anymore, it is displayed as an unchecked selection
        EXPECTED: - This selection is removed from Betslip
        """
        pass

    def test_004___navigate_to_timeline_again_and__tap_on_the_price_button_and_add_to_betslip(self):
        """
        DESCRIPTION: - Navigate to Timeline again and
        DESCRIPTION: - Tap on the price button and add to Betslip
        EXPECTED: - Green 'selected' state is applied in timeline for that selection
        EXPECTED: - Selection is added to Betslip
        EXPECTED: - Betslip counter is increased by one
        """
        pass

    def test_005___minimize_timeline__navigate_to_app_where_this_selection_is_shown(self):
        """
        DESCRIPTION: - Minimize Timeline
        DESCRIPTION: - Navigate to app where this selection is shown
        EXPECTED: - **Green 'selected' state is shown in elsewhere in the app (e.g EDP)**
        """
        pass

    def test_006_navigate_to_the_betslip_and_remove_this_selection(self):
        """
        DESCRIPTION: Navigate to the Betslip and Remove this selection
        EXPECTED: 'Selected' state isn't green anymore, it is displayed as an unchecked selection for Timeline as well as for elsewhere in the app
        """
        pass
