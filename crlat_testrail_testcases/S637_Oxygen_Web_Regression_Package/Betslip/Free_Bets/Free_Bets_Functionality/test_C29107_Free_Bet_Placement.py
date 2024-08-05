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
class Test_C29107_Free_Bet_Placement(Common):
    """
    TR_ID: C29107
    NAME: Free Bet Placement
    DESCRIPTION: This test case verifies Free Bet Placement for Single and Multiple Selections
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User should be logged in
    PRECONDITIONS: 3. User should have Free Bets available on their account
    PRECONDITIONS: 4. User should have several selections added to the Betslip
    PRECONDITIONS: 5. Open the Betslip
    PRECONDITIONS: NOTE: Contact the Support team for assistance with applying free bet tokens to the relevant test accounts
    PRECONDITIONS: - OR -
    PRECONDITIONS: For DEV/TST env. - https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: For PROD/HL envs:
    PRECONDITIONS: Coral: https://sports.coral.co.uk/promotions/details/new-customer-offer (Open a new online, mobile or telephone account with Coral. Place a £5+ Win or £5+ Each Way bet on any sport. Coral will give you an instant four x £5 free bets.)
    PRECONDITIONS: Ladbrokes: https://m.ladbrokes.com/en-gb/#!/promotions/0 (Register a new Ladbrokes account on mobile or online using promo code '20FREE'. Place cumulative qualifying stakes to a total of £5 win or £5 each-way at odds totalling 1/2 or greater.)
    """
    keep_browser_open = True

    def test_001_for_a_single_selection_press_on_use_free_bet_link_and_select_one_of_available_free_bets(self):
        """
        DESCRIPTION: For a single selection: Press on "Use Free Bet" link and select one of available Free Bets
        EXPECTED: Free Bet is selected successfully
        EXPECTED: Stake field is NOT pre-populated by value of a free bet selected
        EXPECTED: *[Not actual from OX 99]*
        EXPECTED: Value of 'Stake' is not changed
        EXPECTED: Value of 'Free Bet Stake' is changed to amount of chosen Free bet
        EXPECTED: Value of 'Total Stake' = 'Free Bet Stake' + 'Stake'
        EXPECTED: *[From OX 99]*
        EXPECTED: 'Est. Returns' is calculated
        EXPECTED: *[From OX 100]*
        EXPECTED: * Free Bet signposting icon and stake are displayed below the stake box
        EXPECTED: * Free Bet signposting icon and stake are displayed in the total stake section
        EXPECTED: * Value of 'Total Stake' = 'Free Bet Stake' + 'Stake'
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/36083)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/36078)
        """
        pass

    def test_002_not_actual_from_ox_99_tap_bet_nowfrom_ox_99_tap_place_bet(self):
        """
        DESCRIPTION: *[Not actual from OX 99]* Tap 'Bet Now'
        DESCRIPTION: *[From OX 99]* Tap 'Place Bet'
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is shown
        EXPECTED: * User balance is NOT changed
        """
        pass

    def test_003_go_back_to_betslipenter_value_in_a_stake_field_and_add_a_free_bet_for_a_single_selection(self):
        """
        DESCRIPTION: Go back to Betslip
        DESCRIPTION: Enter value in a 'Stake' field and add a Free Bet for a single selection
        EXPECTED: Free Bet is selected
        EXPECTED: Stake entered is shown is "Stake" field
        EXPECTED: *[Not actual from OX 99]*
        EXPECTED: Value of 'Stake' is changed on amount entered in 'Stake' field
        EXPECTED: Value of 'Free Bet Stake' is changed on amount of chosen Free bet
        EXPECTED: Value of 'Total Stake' = 'Free Bet Stake' + 'Stake'
        EXPECTED: *[From OX 99]*
        EXPECTED: 'Est. Returns' is calculated
        EXPECTED: *[From OX 100]*
        EXPECTED: * Free Bet signposting icon and stake are displayed below the stake box
        EXPECTED: * Free Bet signposting icon and stake are displayed in the total stake section
        EXPECTED: * Value of 'Total Stake' = 'Free Bet Stake' + 'Stake'
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/36083)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/36078)
        """
        pass

    def test_004_not_actual_from_ox_99_tap_bet_nowfrom_ox_99_tap_place_bet(self):
        """
        DESCRIPTION: *[Not actual from OX 99]* Tap 'Bet Now'
        DESCRIPTION: *[From OX 99]* Tap 'Place Bet'
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is shown
        EXPECTED: * User balance is decreased on a value entered in a 'Stake' field
        """
        pass

    def test_005_not_actual_from_ox_99for_a_multiple_selection_go_tofree_bet_available_drop_down_and_select_one_of_available_free_betfrom_ox_99for_a_multiple_selection_press_on_use_free_bet_link_and_select_one_of_available_free_bets(self):
        """
        DESCRIPTION: *[Not actual from OX 99]*
        DESCRIPTION: For a Multiple selection: Go to 'Free Bet Available' drop down and select one of available Free bet
        DESCRIPTION: *[From OX 99]*
        DESCRIPTION: For a Multiple selection: Press on "Use Free Bet" link and select one of available Free Bets
        EXPECTED: Free Bet is selected successfully
        EXPECTED: Stake field is NOT pre-populated by value of a free bet selected
        EXPECTED: *[Not actual from OX 99]*
        EXPECTED: Value of 'Stake' is not changed
        EXPECTED: Value of 'Free Bet Stake' is changed to amount of chosen Free bet
        EXPECTED: Value of 'Total Stake' = 'Free Bet Stake' + 'Stake'
        EXPECTED: *[From OX 99]*
        EXPECTED: 'Est. Returns' is calculated
        EXPECTED: *[From OX 100]*
        EXPECTED: * Free Bet signposting icon and stake are displayed below the stake box
        EXPECTED: * Free Bet signposting icon and stake are displayed in the total stake section
        EXPECTED: * Value of 'Total Stake' = 'Free Bet Stake' + 'Stake'
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/36083)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/36078)
        """
        pass

    def test_006_not_actual_from_ox_99_tap_bet_nowfrom_ox_99_tap_place_bet(self):
        """
        DESCRIPTION: *[Not actual from OX 99]* Tap 'Bet Now'
        DESCRIPTION: *[From OX 99]* Tap 'Place Bet'
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is shown
        EXPECTED: * User balance is NOT changed
        """
        pass

    def test_007_go_back_to_betslipenter_value_in_a_stake_field_and_add_a_free_bet_for_a_multiple_selection(self):
        """
        DESCRIPTION: Go back to Betslip
        DESCRIPTION: Enter value in a 'Stake' field and add a Free Bet for a Multiple selection
        EXPECTED: Free Bet is selected
        EXPECTED: Stake entered is shown is "Stake" field
        EXPECTED: *[Not actual from OX 99]*
        EXPECTED: Value of 'Stake' is changed on amount entered in 'Stake' field
        EXPECTED: Value of 'Free Bet Stake' is changed on amount of chosen Free bet
        EXPECTED: Value of 'Total Stake' = 'Free Bet Stake' + 'Stake'
        EXPECTED: *[From OX 99]*
        EXPECTED: 'Est. Returns' is calculated
        EXPECTED: *[From OX 100]*
        EXPECTED: * Free Bet signposting icon and stake are displayed below the stake box
        EXPECTED: * Free Bet signposting icon and stake are displayed in the total stake section
        EXPECTED: * Value of 'Total Stake' = 'Free Bet Stake' + 'Stake' e.g. {Free Bet Signposting icon} {Free Bet Stake} {+} {Stake}
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/36087)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/36088)
        """
        pass

    def test_008_not_actual_from_ox_99_tap_bet_nowfrom_ox_99_tap_place_bet(self):
        """
        DESCRIPTION: *[Not actual from OX 99]* Tap 'Bet Now'
        DESCRIPTION: *[From OX 99]* Tap 'Place Bet'
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is shown
        EXPECTED: * User balance is decreased on a value entered in a 'Stake' field
        """
        pass
