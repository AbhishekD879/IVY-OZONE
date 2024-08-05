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
class Test_C29144_Accepting_split_bets_linked_parts_traders_offer(Common):
    """
    TR_ID: C29144
    NAME: Accepting split bets & linked parts trader's offer
    DESCRIPTION: This test case verifies bet split and linking within Overask functionality
    DESCRIPTION: Instruction how to split & link Overask bets: https://confluence.egalacoral.com/display/SPI/How+to+split+a+Bet+in+Overask+functionality
    DESCRIPTION: AUTOTEST DESKTOP PART1 [C9698450]
    DESCRIPTION: AUTOTEST MOBILE PART1 [C9690085]
    PRECONDITIONS: - For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: - User is logged in to application
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip__open_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip > Open Betslip
        EXPECTED: Selection is successfully added
        """
        pass

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection__tap_bet_now_buttonfrom_ox_99_tap_button_place_bet(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection > Tap 'Bet Now' button
        DESCRIPTION: **From OX 99**
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        pass

    def test_003_in_ti_trigger__bet_split__link_parts_of_split_bet__stakeoddsprice_type_modification_submit_changes(self):
        """
        DESCRIPTION: In TI trigger:
        DESCRIPTION: - Bet split
        DESCRIPTION: - Link parts of split bet
        DESCRIPTION: - Stake/Odds/Price Type modification
        DESCRIPTION: > Submit changes
        EXPECTED: 
        """
        pass

    def test_004_in_app_verify_bet_parts_with_modified_values_displaying_in_betslip(self):
        """
        DESCRIPTION: In app: Verify bet parts with modified values displaying in Betslip
        EXPECTED: *  The Bet parts are shown to the user with the changed values highlighted
        EXPECTED: *  The bet parts are linked with 'link' symbol
        EXPECTED: *  'Accept & Bet' and 'Cancel' buttons are displayed
        EXPECTED: *  Bets are selected by default and 'Accept & Bet' button is enabled
        EXPECTED: **From OX 99**
        EXPECTED: *   The Bet parts are shown to the user with the changed values highlighted
        EXPECTED: *   The bet parts are stacked:
        EXPECTED: *   Parent selection doesn't have a Remove button
        EXPECTED: *   Remove button displays only on the child selection
        EXPECTED: *   Buttons 'Cancel' and 'Place Bet' are displayed
        EXPECTED: New Design!
        EXPECTED: ![](index.php?/attachments/get/33780) ![](index.php?/attachments/get/33781)
        """
        pass

    def test_005_unselect_one_of_bet_partsfrom_ox_99remove_one_of_the_bet_parts_child_part(self):
        """
        DESCRIPTION: Unselect one of Bet parts
        DESCRIPTION: **From OX 99**
        DESCRIPTION: REMOVE one of the Bet parts (Child part)
        EXPECTED: * The other part of Bet is unselected automatically
        EXPECTED: * 'Accept & Bet' button becomes disabled
        EXPECTED: **From OX 99**
        EXPECTED: * Only child part of bet can be removed
        EXPECTED: * Button 'Place Bet' enabled
        """
        pass

    def test_006_select_one_of_bet_partsfrom_ox_99_tap_button_place_betundo_one_of_the_child_bet_parts(self):
        """
        DESCRIPTION: Select one of Bet parts
        DESCRIPTION: **From OX 99**
        DESCRIPTION: * Tap button 'Place Bet'
        DESCRIPTION: UNDO one of the child Bet parts
        EXPECTED: * The other part of Bet is selected automatically
        EXPECTED: * 'Accept & Bet' button becomes enabled
        EXPECTED: **From OX 99**
        EXPECTED: *  'Place Bet' button remains enabled
        EXPECTED: *  Child selection is restored
        """
        pass

    def test_007_tap_accept__bet_buttonfrom_ox_99_tap_button_place_bet(self):
        """
        DESCRIPTION: Tap 'Accept & Bet' button
        DESCRIPTION: **From OX 99**
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: *   Linked bets are placed successfully
        EXPECTED: *   Bet receipt page is displayed and placed bets are displayed as separate singles
        """
        pass
