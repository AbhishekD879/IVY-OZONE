import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.timeline
@vtest
class Test_C59927154_Verify_price_updates_from_SP_to_LP_and_vice_versa_for_the_selection_in_the_Timeline(Common):
    """
    TR_ID: C59927154
    NAME: Verify price updates from SP to LP and vice versa for the selection in the Timeline
    DESCRIPTION: This test case verifies price updates from SP to LP and vice versa for the selection in the Timeline
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: Confluence instruction - How to create Timeline Template, Campaign, Posts - https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Timeline should be enabled in CMS
    PRECONDITIONS: 2.Live Campaign is created
    PRECONDITIONS: 3.Timeline Post with LP (e.g. 1/2) HORSE selection is available/created and published
    PRECONDITIONS: 4.Load the app
    PRECONDITIONS: 5.User is logged in
    PRECONDITIONS: Navigate to the page with configured 'Timeline' (e.g./home/featured)
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes Lounge
    PRECONDITIONS: Coral- Coral Pulse
    """
    keep_browser_open = True

    def test_001_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - 'POST' response is present with all fields form CMS in WS
        EXPECTED: - Post with **LP** selection is available and displayed
        """
        pass

    def test_002_navigate_to_the_ti_backoffice_and_untick_lp_available_and_tick_sp_available_on_the_market_level_for_the_selection_for_the_timeline_post(self):
        """
        DESCRIPTION: Navigate to the TI (backoffice) and **untick LP Available** and **tick SP Available** on the market level for the selection for the Timeline Post
        EXPECTED: - Changes are saved successfully in TI (backoffice)
        """
        pass

    def test_003_return_to_the_timeline_and_verify_sp_selection_for_the_post(self):
        """
        DESCRIPTION: Return to the 'Timeline' and verify **SP** selection for the Post
        EXPECTED: - 'Price/Odds' button immediately displays the new price **"SP"**
        EXPECTED: - The following attributes are received in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type "POST_CHANGED":
        EXPECTED: - priceDeс: "SP"
        EXPECTED: - priceType: "SP"
        """
        pass

    def test_004_navigate_to_the_ti_backoffice_again_and_untick_sp_available_and_tick_lp_available_on_the_market_level_for_the_selection_for_the_timeline_post_and_add_price_eg_12_for_the_selection(self):
        """
        DESCRIPTION: Navigate to the TI (backoffice) again and **untick SP Available** and **tick LP Available** on the market level for the selection for the Timeline Post and add price (e.g. 1/2) for the selection
        EXPECTED: - Changes are saved successfully in TI (backoffice)
        """
        pass

    def test_005_return_to_the_timeline_and_verify_lp_eg_12_selection_for_the_post(self):
        """
        DESCRIPTION: Return to the 'Timeline' and verify **LP (e.g. 1/2)** selection for the Post
        EXPECTED: - 'Price/Odds' button immediately displays the new price **LP (e.g. 1/2)**
        EXPECTED: - The following attributes are received in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type  "POST_CHANGED":
        EXPECTED: - priceDen: "X" (e.g. '1')
        EXPECTED: - priceNum: "Y" (e.g. '2')
        EXPECTED: - priceType: "LP"
        """
        pass

    def test_006_collapse_the_timeline_and_trigger_price_change_from_lp_to_sp_selection_in_ti_backoffice(self):
        """
        DESCRIPTION: Collapse the 'Timeline' and trigger price change **from LP to SP selection** in TI (backoffice)
        EXPECTED: - Changes are saved successfully in TI (backoffice)
        EXPECTED: - The following attributes are received on UI in Network WS -> ?EIO=3&transport=websocket wss://timeline-api-response with type  "POST_CHANGED":
        EXPECTED: - priceDeс: "SP"
        EXPECTED: - priceType: "SP"
        """
        pass

    def test_007_expand_timeline_and_verify_price_change_for_the_selection_on_ui(self):
        """
        DESCRIPTION: Expand 'Timeline' and verify price change for the selection on UI
        EXPECTED: - Price/Odds' button immediately displays the new price **"SP"**
        """
        pass

    def test_008_repeat_steps_6_7_trigger_price_change_from_sp_to_lp_selection_in_ti_backoffice(self):
        """
        DESCRIPTION: Repeat steps 6-7 trigger price change **from SP to LP selection** in TI (backoffice)
        EXPECTED: 
        """
        pass
