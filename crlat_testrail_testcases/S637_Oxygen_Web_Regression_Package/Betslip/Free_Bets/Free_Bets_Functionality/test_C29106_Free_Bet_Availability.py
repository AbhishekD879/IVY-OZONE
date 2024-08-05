import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29106_Free_Bet_Availability(Common):
    """
    TR_ID: C29106
    NAME: Free Bet Availability
    DESCRIPTION: This test case verifies Free Bet availability in Betslip
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-10318 update an error message
    DESCRIPTION: AUTOTEST [C527783]
    PRECONDITIONS: 1. User should be logged in
    PRECONDITIONS: 2. User should have Free Bets available on their account
    PRECONDITIONS: 3. User should have at least one selection added to the Betslip
    PRECONDITIONS: NOTE: Contact Coral UAT for assistance with applying free bet tokens to the relevant test accounts
    PRECONDITIONS: OR
    PRECONDITIONS: - For DEV/TST env. - https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: - For PROD/HL envs:
    PRECONDITIONS: Coral: https://sports.coral.co.uk/promotions/details/new-customer-offer (Open a new online, mobile or telephone account with Coral. Place a £5+ Win or £5+ Each Way bet on any sport. Coral will give you an instant four x £5 free bets.)
    PRECONDITIONS: Ladbrokes: https://m.ladbrokes.com/en-gb/#!/promotions/0 (Register a new Ladbrokes account on mobile or online using promo code '20FREE'. Place cumulative qualifying stakes to a total of £5 win or £5 each-way at odds totalling 1/2 or greater.)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Betslip is open
        """
        pass

    def test_003_verify_free_bet_available_drop_down(self):
        """
        DESCRIPTION: Verify 'Free Bet Available' drop down
        EXPECTED: * 'Free Bet Available' drop down is displayed below Est.Returns
        EXPECTED: * All available free bets are shown in drop down list
        EXPECTED: * Free Bet text and amount in following format: Free Bet £11.00 is shown for each available free bet
        """
        pass

    def test_004_verify_use_free_bet_link_is_present_under_selection_and_press_on_it(self):
        """
        DESCRIPTION: Verify "Use Free Bet" link is present under selection and press on it
        EXPECTED: Free Bet Pop up is shown with list of Free Bets available
        """
        pass

    def test_005_choose_one_of_available_free_bets_from_free_bet_available_drop_down_listselect_one_of_available_free_bets_from_free_bet_pop_upselect_one_of_available_free_bets_from_free_bet_pop_up_and_click_on_add_button(self):
        """
        DESCRIPTION: Choose one of available free bets from 'Free Bet Available' drop down list
        DESCRIPTION: Select one of available Free Bets from Free Bet pop up
        DESCRIPTION: Select one of available Free Bets from Free Bet pop up AND click on 'ADD' button.
        EXPECTED: * Chosen free bet is selected successfully
        EXPECTED: * 'Don't Use Free Bet' item appear in the drop down list instead of 'Free Bet Available' text
        EXPECTED: * Selected Free Bet has check box marked as selected
        EXPECTED: * Pop up is closed (in 0.2 sec)
        EXPECTED: * "Use Free Bet" link is changed to "- Remove Free Bet" link
        EXPECTED: * Chosen Free Bet has radio button marked as selected
        EXPECTED: * 'ADD' button becomes active:
        EXPECTED: Coral Popup Design:
        EXPECTED: ![](index.php?/attachments/get/36071)
        EXPECTED: Ladbrokes Popup Design:
        EXPECTED: ![](index.php?/attachments/get/36072)
        EXPECTED: * Chosen Free Bet successfully added
        EXPECTED: * "Use Free Bet" link is changed to "- Remove Free Bet" link
        EXPECTED: * Free Bet signposting icon and stake are displayed below the stake box
        EXPECTED: * Free Bet signposting icon and stake are displayed in the total stake section
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/36083)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/36078)
        """
        pass

    def test_006_verify_estimated_returnsvalue_when_free_bet_is_selected(self):
        """
        DESCRIPTION: Verify 'Estimated Returns' value when free bet is selected
        EXPECTED: 'Estimated Returns' is calculated based on formula:
        EXPECTED: **Free Bet Value * Odds** - if odds have a fractional format
        EXPECTED: **Free Bet Value * Odds - Free Bet Value** - if odds have a decimal format
        """
        pass

    def test_007_select_dont_use_free_bet_optionpress_on___remove_free_bet_link(self):
        """
        DESCRIPTION: Select 'Don't Use Free Bet' option
        DESCRIPTION: Press on "- Remove Free Bet" link
        EXPECTED: * The previous selected value is cleared
        EXPECTED: * 'Free Bet Available' appear when the option is selected
        EXPECTED: * "- Remove Free Bet" link is changed to "Use Free Bet" link
        EXPECTED: * 'Estimated Returns' is changed to 0.00
        """
        pass

    def test_008_add_few_more_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add few more selections to the Betslip
        EXPECTED: Betslip counter is increased, added selection are present in the Betslip
        """
        pass

    def test_009_1_go_to_selection_1_free_bet_available_drop_down_and_choose_one_of_available_free_bets2_go_to_selection_2_free_bet_available_drop_down_and_verify_if_free_bet_chosen_for_selection_1_is_present_in_the_list3_tap_bet_now_when_the_same_free_bet_is_chosen_for_two_selections4_for_one_of_the_bet_select_do_not_use_free_bet_option(self):
        """
        DESCRIPTION: 1) Go to selection #1 'Free Bet Available' drop down and choose one of available free bets
        DESCRIPTION: 2) Go to selection #2 'Free Bet Available' drop down and verify if free bet chosen for selection #1 is present in the list
        DESCRIPTION: 3) Tap 'Bet Now' when the same free bet is chosen for two selections
        DESCRIPTION: 4) For one of the bet select 'Do not use Free Bet' option
        EXPECTED: 1) Free bet is chosen successfully
        EXPECTED: 2) Free bet chosen for selection #1 is STILL shown in the list of free bets for selection #2
        EXPECTED: 3) Error message is shown: 'You have attempted to apply the same free bet in more than one instance. Your free bet can only be used once.'
        EXPECTED: 4) Error message is not shown anymore
        """
        pass

    def test_010_go_to_selection_1_free_bet_pop_up_and_choose_one_of_available_free_bets(self):
        """
        DESCRIPTION: Go to selection #1 Free Bet pop up and choose one of available free bets
        EXPECTED: Free bet is chosen successfully
        """
        pass

    def test_011_go_to_selection_2_free_bet_pop_up_and_verify_if_free_bet_chosen_for_selection_1_is_present_in_the_list(self):
        """
        DESCRIPTION: Go to selection #2 'Free Bet pop up and verify if free bet chosen for selection #1 is present in the list
        EXPECTED: Free bet chosen for selection #1 isn't shown in the list of free bets for selection #2
        """
        pass

    def test_012_add_few_more_selections_to_the_betslip_so_quantity_of_selections_is_bigger_than_quantity_of_free_bets_available_for_user(self):
        """
        DESCRIPTION: Add few more selections to the Betslip, so quantity of selections is bigger than quantity of Free Bets available for User
        EXPECTED: Betslip counter is increased, added selection are present in the Betslip
        """
        pass

    def test_013_add_all_available_free_bets_to_selections(self):
        """
        DESCRIPTION: Add all available Free Bets to selections
        EXPECTED: * "Use Free Bet" link is changed to "- Remove Free Bet" link for selections with Free Bets added
        EXPECTED: * After User has added all available Free Bets to selections, "Use Free Bet" link for other selections is greyed out and non-clickable
        """
        pass
