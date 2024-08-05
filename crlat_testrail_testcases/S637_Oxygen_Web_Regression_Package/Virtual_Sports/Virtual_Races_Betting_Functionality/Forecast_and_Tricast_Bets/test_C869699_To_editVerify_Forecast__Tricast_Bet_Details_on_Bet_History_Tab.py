import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869699_To_editVerify_Forecast__Tricast_Bet_Details_on_Bet_History_Tab(Common):
    """
    TR_ID: C869699
    NAME: [To edit]Verify Forecast / Tricast Bet Details on 'Bet History' Tab
    DESCRIPTION: This test case verifies the displaying of 'Forecast / Tricast' bet on the 'Bet History' and 'My Bets' pages.
    DESCRIPTION: for
    DESCRIPTION: *   Virtual Motorsports (Class ID 288)
    DESCRIPTION: *   Virtual Cycling (Class ID 290)
    DESCRIPTION: *   Virtul Horse Racing (Class ID 285)
    DESCRIPTION: *   Virtual Greyhound Racing (Class ID 286)
    DESCRIPTION: *   Virtual Grand National (Class ID 26604)
    DESCRIPTION: **JIRA Ticket** :
    DESCRIPTION: BMA-9397 'Extend Forecast and Tricast betting to Virtual Sports'
    DESCRIPTION: BMA-15524: Removing Bet History Download Links from Bet History Pages
    PRECONDITIONS: 1. User should be logged in to view their bet history.
    PRECONDITIONS: 2. User should have few pending/win/lose/cancelled/cashed out Single and Multiples bets
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_on_right_menu_icon(self):
        """
        DESCRIPTION: Tap on Right menu icon
        EXPECTED: Right menu is opened
        """
        pass

    def test_003_tap_on_my_account_menu_item(self):
        """
        DESCRIPTION: Tap on 'My Account' menu item
        EXPECTED: 'My Account' page is opened
        """
        pass

    def test_004_select_bet_history_frommy_account_sub_menu(self):
        """
        DESCRIPTION: Select 'Bet History' from 'My Account' sub menu
        EXPECTED: 1. 'Bet History' page is opened with 'Bet History' header and Back button
        EXPECTED: 2. Two sort filters are present :
        EXPECTED: *   Regular (selected by default)
        EXPECTED: *   Lotto
        EXPECTED: *   Pools
        EXPECTED: 3. Sorting section with two options is present:
        EXPECTED: *   Last 2 days (selected by default)
        EXPECTED: *   Show All
        EXPECTED: 3. Pending/win/lose/cancelled/cashed out bet sections are present (all collapsed by default)
        """
        pass

    def test_005_expand_bet_section_verify_bet_details_and_check_if_bet_details_are_same_as_in_ims_system(self):
        """
        DESCRIPTION: Expand bet section, verify bet details and check if bet details are same as in IMS system
        EXPECTED: Bet is expanded, bet details are shown:
        EXPECTED: 1. Bet Receipt No
        EXPECTED: 2. Status field (Status: Cashed out) is shown for Cashed out bets only
        EXPECTED: 3. Selection details:
        EXPECTED: The main body of the bet:
        EXPECTED: *   **Result - **i.e. Won, Cancelled, Lost, Pending ('Result' field is not shown for Cashed out bets only)
        EXPECTED: *   The **Class name **that customer has bet on - i.e. Greyhounds
        EXPECTED: *   **Event name **and associated event type - i.e. Belle Vue 3:17
        EXPECTED: *   **Date and time of event** in DD.MM HH:MM fashion using 12-hour clock (AM/PM)
        EXPECTED: *   **Market name** user has bet on - i.e. Win or Each Way
        EXPECTED: *   **Outcome name **user has bet on i.e. Lovely Horse
        EXPECTED: *   **Odds **of selections made by user (N/A for 'SP' price type). Format: Outcome name **@** Odds
        EXPECTED: NOTE: For Forecast / Tricast selection details are shown for every selection which form the forecast / tricast bets
        EXPECTED: 4. Stake Returns and Details:
        EXPECTED: *   Date and time bet was placed at - DD.MM HH:MM fashion using 12-hour clock (AM/PM)
        EXPECTED: *   **Bet Type** placed by user - i.e. Forecast (k), Tricast(k) etc.
        EXPECTED: *   **Number of Lines**
        EXPECTED: 5. Number of win Lines
        EXPECTED: 6. Total Stake of bet placed in format: <currency symbol>XX.XX
        EXPECTED: 7. Total Returns in the case Winning, Losing, Cancelled bets in format: <currency symbol>XX.XX
        EXPECTED: 8. Total Estimated returns in case of Pending bets (N/A for forecast, tricast bets)
        EXPECTED: 9. Cashed out returns in case of Cashed out bets in format: <currency symbol>XX.XX
        """
        pass

    def test_006_place_a_bet_and_verify_bet_with_status_pending_in_bet_history(self):
        """
        DESCRIPTION: Place a bet and verify bet with status 'Pending' in Bet History
        EXPECTED: Bet with status 'Pending' should be present in Bet History, bet details are correct
        """
        pass

    def test_007_trigger_the_situation_of_winning_a_bet_and_verify_bet_with_status_win_in_bet_history(self):
        """
        DESCRIPTION: Trigger the situation of Winning a bet and verify bet with status 'Win' in Bet History
        EXPECTED: Bet with status 'Win' should be present in Bet History, bet details are correct
        """
        pass

    def test_008_trigger_the_situation_of_losing_a_bet_and_verify_bet_with_lost_in_bet_history(self):
        """
        DESCRIPTION: Trigger the situation of  Losing a bet and verify bet with  'Lost' in Bet History
        EXPECTED: Bet with status 'Lost' should be present in Bet History, bet details are correct
        """
        pass

    def test_009_trigger_the_situation_of_cancelling_a_bet_and_verify_bet_with_cancelled_in_bet_history(self):
        """
        DESCRIPTION: Trigger the situation of  Cancelling a bet and verify bet with  'Cancelled' in Bet History
        EXPECTED: Bet with status 'Cancelled' should be present in Bet History, bet details are correct
        """
        pass

    def test_010_place_a_bet___cashed_out_and_verify_bet_with_status_cashed_out_in_bet_history(self):
        """
        DESCRIPTION: Place a bet -> Cashed out and verify bet with status 'Cashed out' in Bet History
        EXPECTED: Bet with status 'Cashed out' should be present in Bet History, bet details are correct
        """
        pass

    def test_011_repeat_steps_2_11_for_multiple_bets(self):
        """
        DESCRIPTION: Repeat steps 2-11 for Multiple bets
        EXPECTED: 
        """
        pass

    def test_012_trigger_the_situation_for_multiple_bet_of_winningloosingcancelling_one_of_selection_in_multiple_bet(self):
        """
        DESCRIPTION: Trigger the situation for Multiple bet of winning/loosing/cancelling one of selection in Multiple bet
        EXPECTED: *   Correct bet result should be present in section header (e.g. Won/Lost/Cancelled/Pending - depends on type of Multiple bet)
        EXPECTED: *   In bet details for Multiple bet correct result should be shown for each selection
        """
        pass
