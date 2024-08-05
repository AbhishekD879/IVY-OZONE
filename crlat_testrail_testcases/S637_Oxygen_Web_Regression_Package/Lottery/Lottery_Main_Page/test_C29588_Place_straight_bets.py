import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.lotto
@vtest
class Test_C29588_Place_straight_bets(Common):
    """
    TR_ID: C29588
    NAME: Place straight bets
    DESCRIPTION: This Test Case verifies placing straight bets on Lotteries.
    DESCRIPTION: AUTOTEST: [C11892867]
    DESCRIPTION: AUTOTEST: [C14735715]
    DESCRIPTION: **Jira Ticket: **
    DESCRIPTION: BMA-5831 Lottery - Place straight bets
    DESCRIPTION: BMA-7590 - Lotto Bet Receipt
    PRECONDITIONS: 1. Launch Invictus application
    PRECONDITIONS: To get a list of lotteries and draws use following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Lottery/X.XX/LotteryToDraw/
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: **To verify data on Bet Receipt page: **
    """
    keep_browser_open = True

    def test_001_navigate_to_lotto_page(self):
        """
        DESCRIPTION: Navigate to 'Lotto' page
        EXPECTED: *   'Lotto' page is opened.
        EXPECTED: *   Stake entry box is disabled until at least one ball will be selected.
        """
        pass

    def test_002_select_any_numbers_using_select_numbers_pop_up_and_tap_done_button(self):
        """
        DESCRIPTION: Select any numbers using Select Numbers pop-up and tap 'Done' button
        EXPECTED: *   Selected numbers are displayed in number line in increasing order
        EXPECTED: *   Odds Section is displayed in one row with Straight Bet. By default if no numbers selected, the Odds value is equal to 'priceNum'/'priceDen' attribute values according to the attribute 'numberPicks=5' from SiteServer.
        EXPECTED: *   Value about Single Straight Bet is displayed before Stake entry box as '1x'.
        EXPECTED: *   Stake entry box is available to enter the bet amount. Default value within Stake entry box is "0.00" and has right alignment within field. Currency sign has left alignment.
        """
        pass

    def test_003_tap_on_stake_entry_box(self):
        """
        DESCRIPTION: Tap on Stake entry box
        EXPECTED: Keypad is opened.
        """
        pass

    def test_004_enter_different_data_into_stake_entry_box_eg_numbers_special_characters_letters(self):
        """
        DESCRIPTION: Enter different data into Stake entry box (e.g. numbers, special characters, letters)
        EXPECTED: *   Only entered numbers are displayed within the Stake field.
        EXPECTED: *   It is impossible to enter letters (nothing happen while entering them).
        EXPECTED: *   It is impossible to enter special characters (nothing happen while entering them).
        EXPECTED: *   XXX,XXX,XXX,XXX.XX is the max value limitations for Stake field.
        EXPECTED: *   It is impossible to enter more than 12 digits and 2 decimals in Stake field.
        """
        pass

    def test_005_verify_place_bet_for_button(self):
        """
        DESCRIPTION: Verify 'Place Bet for' button
        EXPECTED: *   'Place Bet for' button should be automaticaly update with the Total Stake of the bet entered into Stake entry box.
        EXPECTED: *   Appropriate currency symbol sould be displayed within 'Place Bet for' button.
        """
        pass

    def test_006_tap_on_place_bet_for_button(self):
        """
        DESCRIPTION: Tap on 'Place Bet for' button
        EXPECTED: *   'Place Bet for' button label is changed to 'Confirm Bet?'.
        EXPECTED: *   'Place Bet for' button's color is changed to amber.
        """
        pass

    def test_007_tap_on_anywhere_within_the_page_except_confirm_button(self):
        """
        DESCRIPTION: Tap on anywhere within the page except 'Confirm?' button
        EXPECTED: *   'Confirm Bet?' button label is changed back to 'Place Bet for'.
        EXPECTED: *   'Confirm Bet?' button's color is changed back to green.
        """
        pass

    def test_008_repeat_step_6(self):
        """
        DESCRIPTION: Repeat step #6
        EXPECTED: 
        """
        pass

    def test_009_tap_on_confirm_bet_button(self):
        """
        DESCRIPTION: Tap on 'Confirm Bet?' button
        EXPECTED: 1.  Stake is placed successfully.
        EXPECTED: 2.  Bet Receipt is displayed with following items:
        EXPECTED: *   the Lottery product - e.g. 49's 6 Ball (note this is the Lotto product and the variation depending on selecting woth or without the bonus ball - 6 Ball or 7 Ball)
        EXPECTED: *    List of selected draws with Draw date and time (in one line for each draw). Time = 'drawAtTime' from SSResponse
        EXPECTED: *   Bet Type: e.g. "Match (3)" or "All Trebles"
        EXPECTED: *   Bet Selections: e.g. 1,2,3
        EXPECTED: *   Bet Odds: e.g. 600/1 or 601.0 (make sure you handle decimal and fractional)
        EXPECTED: *   Stake: e.g. £1.00 x 1
        EXPECTED: *   Separator
        EXPECTED: *   Total Stake
        EXPECTED: *   Potential return
        EXPECTED: *   Bet Placed: time and date of bet placement
        """
        pass

    def test_010_verify_bet_selections_order(self):
        """
        DESCRIPTION: Verify bet selections order
        EXPECTED: Selected numbers are displayed in ascending
        """
        pass

    def test_011_select_any_other_lottery_and_repeat_steps_2_9(self):
        """
        DESCRIPTION: Select any other Lottery and repeat steps #2-9
        EXPECTED: 
        """
        pass
