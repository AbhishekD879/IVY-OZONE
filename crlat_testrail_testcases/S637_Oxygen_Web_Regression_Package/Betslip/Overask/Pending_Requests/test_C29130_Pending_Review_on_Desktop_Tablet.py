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
class Test_C29130_Pending_Review_on_Desktop_Tablet(Common):
    """
    TR_ID: C29130
    NAME: Pending Review on Desktop/Tablet
    DESCRIPTION: 
    PRECONDITIONS: 1. User is logged in to apllication on tablet/desktop
    PRECONDITIONS: 2. Overask functionality is enabled for the user
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        """
        pass

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection
        EXPECTED: 
        """
        pass

    def test_003_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: *   Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute.' message is displayed on yellow background anchored to the footer
        EXPECTED: *   Loading spinner is shown on the green button, replacing 'Bet Now' label
        EXPECTED: *   'Clear Betslip' and 'Bet Now' buttons become disabled
        EXPECTED: *   'Stake' field becomes disabled
        EXPECTED: **From OX 99**
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        pass

    def test_004_while_review_is_pending_tap_disabled_clear_betslip_button(self):
        """
        DESCRIPTION: While review is pending tap disabled 'Clear Betslip' button
        EXPECTED: Nothing happens, it is impossible to clear betslip
        """
        pass

    def test_005_while_review_is_pending_tap_disabled_bet_now_button(self):
        """
        DESCRIPTION: While review is pending tap disabled 'Bet Now' button
        EXPECTED: Nothing happens, it is impossible to place a Bet
        """
        pass

    def test_006_while_review_is_pending_tap_disabled_stake_field(self):
        """
        DESCRIPTION: While review is pending tap disabled 'Stake' field
        EXPECTED: Nothing happens, it is impossible to modify entered Stake
        """
        pass

    def test_007_while_review_is_pending_go_to_another_pages_and_try_to_add_more_selections_to_the_betslip(self):
        """
        DESCRIPTION: While review is pending go to another pages and try to add more selections to the Betslip
        EXPECTED: *   Selection is not added to the Betslip
        EXPECTED: *   Notification pop-up is shown to the User
        """
        pass

    def test_008_verify_notification_pop_up_elements(self):
        """
        DESCRIPTION: Verify notification pop-up elements
        EXPECTED: It consists of:
        EXPECTED: *   Title: Betslip is busy
        EXPECTED: *   Body: Please wait until the betslip is finished processing your bets before adding more selections. Thanks
        EXPECTED: *   'Close' button
        """
        pass

    def test_009_try_to_cancel_review_process(self):
        """
        DESCRIPTION: Try to cancel review process
        EXPECTED: User cannot cancel review process himself
        """
        pass
