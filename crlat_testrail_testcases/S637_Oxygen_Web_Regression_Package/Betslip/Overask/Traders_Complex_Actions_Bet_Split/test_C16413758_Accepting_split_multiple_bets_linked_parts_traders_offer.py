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
class Test_C16413758_Accepting_split_multiple_bets_linked_parts_traders_offer(Common):
    """
    TR_ID: C16413758
    NAME: Accepting split multiple bets & linked parts trader's offer
    DESCRIPTION: This test case verifies accepting split multiple bets & linked parts trader's offer
    DESCRIPTION: Instruction how to split & link Overask bets: https://confluence.egalacoral.com/display/SPI/How+to+split+a+Bet+in+Overask+functionality
    PRECONDITIONS: - For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: - User is logged in to application
    """
    keep_browser_open = True

    def test_001_add_3_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add 3 selections from different events to the Betslip
        EXPECTED: Selections are successfully added
        """
        pass

    def test_002__enter_stake_value_into_treble_field_which_is_higher_than_the_maximum_limit_for_added_selections_tap_button_place_bet(self):
        """
        DESCRIPTION: * Enter stake value into 'Treble' field which is higher than the maximum limit for added selections
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: * Overask is triggered for the User
        EXPECTED: * The bet review notification is shown to the User
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
        EXPECTED: * The Bet parts are shown to the user with the changed values highlighted
        EXPECTED: * The bet parts are stacked:
        EXPECTED: * Parent selection doesn't have a Remove button
        EXPECTED: * Remove button displays only on the child selection
        EXPECTED: *   Buttons 'Cancel' and 'Place Bet' are displayed
        EXPECTED: ![](index.php?/attachments/get/34134) ![](index.php?/attachments/get/34135)
        """
        pass

    def test_005_tap_button_place_bet(self):
        """
        DESCRIPTION: Tap button 'Place Bet'
        EXPECTED: * Linked bets are placed successfully
        EXPECTED: * Bet receipt page is displayed and placed bets are displayed as multiples
        """
        pass
