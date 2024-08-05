import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29115_Verify_FreeBet_notification_icon_displaying_on_Event_Details_page(Common):
    """
    TR_ID: C29115
    NAME: Verify 'FreeBet' notification icon displaying on Event Details page
    DESCRIPTION: This test case verifies 'FreeBet' notification icon displaying on Event Details page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has not Free Bets available on their account
    PRECONDITIONS: 3. User has payment method selected
    PRECONDITIONS: **Note:**
    PRECONDITIONS: For creating Free Bets for different levels please use instruction mentioned in the following test case:
    PRECONDITIONS: https://ladbrokescoral.testrail.com/index.php?/cases/view/370606
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: * Homepage is opened
        EXPECTED: * 'Freebet' notification icon is NOT displayed on the header (on the Balance button/icon)
        """
        pass

    def test_002_apply_freebet_offer_on_the_market_level_using_instruction_from_preconditions(self):
        """
        DESCRIPTION: Apply Freebet offer on the market level using instruction from Preconditions
        EXPECTED: Freebet offer is created successfully
        """
        pass

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Page is reloaded
        """
        pass

    def test_004_navigate_to_the_relevent_event_details_page(self):
        """
        DESCRIPTION: Navigate to the relevent Event details page
        EXPECTED: * 'Freebet' notification icon is displayed on the relevant Event details page
        EXPECTED: * 'FreeBets' notification icon is placed at the right side of the Event Bar **For Mobile/Tablet** and at the left side of the Event Header next to 'Favorites' icon **For Desktop**
        """
        pass

    def test_005_clicktap_on_freebet_notification_icon(self):
        """
        DESCRIPTION: Click/Tap on 'Freebet' notification icon
        EXPECTED: 'My Freebets/Bonuses' page is opened
        """
        pass

    def test_006_clicktap_on_back_button(self):
        """
        DESCRIPTION: Click/Tap on 'Back' button
        EXPECTED: User navigate to the previous page (Event details page)
        """
        pass

    def test_007_place_a_bet_using_current_freebet_offer_market_level(self):
        """
        DESCRIPTION: Place a bet using current Freebet offer (market level)
        EXPECTED: * 'Freebet' notification icon disappeared from the Event details page after page refresh
        EXPECTED: * 'Freebet' notification icon disappeared from the Balance icon immediately
        """
        pass

    def test_008_repeat_steps_1_6_for_levels(self):
        """
        DESCRIPTION: Repeat steps 1-6 for levels:
        EXPECTED: -Selection level
        EXPECTED: -Event level
        EXPECTED: -Type level
        EXPECTED: -Class level
        EXPECTED: -All (All bets)
        """
        pass
