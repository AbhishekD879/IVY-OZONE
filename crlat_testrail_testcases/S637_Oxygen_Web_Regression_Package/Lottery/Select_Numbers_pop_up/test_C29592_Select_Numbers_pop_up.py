import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.lotto
@vtest
class Test_C29592_Select_Numbers_pop_up(Common):
    """
    TR_ID: C29592
    NAME: Select Numbers pop-up
    DESCRIPTION: This test case verifies Select Numbers pop-up displaying and launching
    DESCRIPTION: JIRA tickets:
    DESCRIPTION: BMA-7579 Lottery - Select numbers (as popup)
    PRECONDITIONS: Load Invictus app
    PRECONDITIONS: Go to Lotto page
    PRECONDITIONS: To verify Lottery values from SiteServer please use link: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Lottery/2.16/LotteryToDraw/
    """
    keep_browser_open = True

    def test_001_select_lottery_and_tapany_ball_of_a_number_line_on_the_main_page(self):
        """
        DESCRIPTION: Select Lottery and tap any ball of a number line on the main page
        EXPECTED: The number grid pop-up is displayed with next elements:
        EXPECTED: *   'Choose your lucky numbers below' text
        EXPECTED: *   'Save to Favourites' button (not implemented in current version)
        EXPECTED: *   'Reset Numbers' button
        EXPECTED: *   Numbers grid
        EXPECTED: *   'Choose your lucky dip' text
        EXPECTED: *   'Lucky X' buttons
        EXPECTED: *   'Done' button
        EXPECTED: *   'X' button
        """
        pass

    def test_002_verify_balls_quantity_depending_on_selected_lottery(self):
        """
        DESCRIPTION: Verify balls quantity depending on selected lottery
        EXPECTED: Balls quantity is equal to SiteServer 'maxNumber' value for selected Lotttery.
        """
        pass

    def test_003_on_the_main_lottery_page_selectstraight_bets_tap_any_ball_of_a_number_line(self):
        """
        DESCRIPTION: On the main lottery page select straight bets. Tap any ball of a number line.
        EXPECTED: *   The number grid pop-up is displayed
        EXPECTED: *   Up to 5 numbers can be selected for straight bets
        """
        pass

    def test_004_verify_order_of_selected_numbers(self):
        """
        DESCRIPTION: Verify order of selected numbers
        EXPECTED: Selected numbers are displayed in ascending on 'Lotto' page
        """
        pass

    def test_005_on_the_main_lottery_page_select_combo_bet_tap_any_ball_of_a_number_line(self):
        """
        DESCRIPTION: On the main lottery page select combo bet. Tap any ball of a number line
        EXPECTED: *   The number grid pop-up is displayed
        EXPECTED: *   Up to 15 numbers can be selcted for combo bets
        """
        pass

    def test_006_maximum_number_of_balls_for_the_lottery_is_already_selected_5_balls_for_streight_bet_and_15_balls_for_combo_bettap_any_unselected_ball(self):
        """
        DESCRIPTION: Maximum number of balls for the lottery is already selected. (5 balls for streight bet and 15 balls for combo bet).
        DESCRIPTION: Tap any unselected ball.
        EXPECTED: *   New ball cannot be selected.
        EXPECTED: *   All balls are disabled
        """
        pass

    def test_007_on_the_main_lottery_page_number_line_is_empty_tap_any_ball_of_a_number_line(self):
        """
        DESCRIPTION: On the main lottery page number line is empty. Tap any ball of a number line.
        EXPECTED: The number grid pop-up is displayed with no numbers marked as already selected.
        """
        pass

    def test_008_on_the_main_lottery_page_number_line_contains_already_selected_numberstap_any_ball_of_a_number_line(self):
        """
        DESCRIPTION: On the main lottery page number line contains already selected numbers.
        DESCRIPTION: Tap any ball of a number line.
        EXPECTED: The number grid pop-up is displayed with marked and selected numbers from the number line
        """
        pass

    def test_009_do_not_select_any_balltap_done_button(self):
        """
        DESCRIPTION: Do not select any ball.
        DESCRIPTION: Tap 'Done' button
        EXPECTED: *   'Done' button is disabled
        EXPECTED: *   Nothing happens after tapping
        """
        pass

    def test_010_on_the_main_lotto_page_tap_the_ball_on_selected_number_lineselect_balls_on_numbers_pop_uptap_done_button(self):
        """
        DESCRIPTION: On the main lotto page tap the ball on selected number line.
        DESCRIPTION: Select balls on numbers pop-up.
        DESCRIPTION: Tap 'Done' button
        EXPECTED: *   Number pop-up is closed
        EXPECTED: *   Previously selected number line is filled in with selected numbers
        EXPECTED: *   Previously selected number line is focused on the main lottery page
        """
        pass

    def test_011_1_on_the_main_lottery_page_number_line_is_empty2_tap_any_ball_of_a_number_line3_select_balls_on_pop_up4_tap_x_button(self):
        """
        DESCRIPTION: 1. On the main lottery page number line is empty.
        DESCRIPTION: 2. Tap any ball of a number line.
        DESCRIPTION: 3. Select balls on pop-up.
        DESCRIPTION: 4. Tap 'X' button
        EXPECTED: *   Select Numbers pop-up is closed
        EXPECTED: *   Selected numbers are not saved
        EXPECTED: *   Number line remains to be empty
        """
        pass

    def test_012_1_on_the_mail_lottery_page_number_line_contails_already_selected_numbers2_tap_any_ball_of_a_number_line3_select_numbers_on_pop_up4_tap_x_button(self):
        """
        DESCRIPTION: 1. On the mail lottery page number line contails already selected numbers
        DESCRIPTION: 2. Tap any ball of a number line
        DESCRIPTION: 3. Select numbers on pop-up
        DESCRIPTION: 4. Tap 'X' button
        EXPECTED: *   Select Numbers pop-up is closed
        EXPECTED: *   Selected numbers are not saved
        EXPECTED: *   Previously selected numbers are displayed in number line in ascending order
        """
        pass
