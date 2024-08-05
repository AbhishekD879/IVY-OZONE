import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C884014_Verify_Free_Bets_within_Quick_Bet(Common):
    """
    TR_ID: C884014
    NAME: Verify Free Bets within Quick Bet
    DESCRIPTION: This test case verifies Free Bets within Quick Bet
    PRECONDITIONS: 1.  Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2.  Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. The user should have free bets added
    PRECONDITIONS: 4. [How to add Free bets to user`s account] [1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: 5. Open Dev Tools -> Network -> XHR filter to see response of **user** request
    """
    keep_browser_open = True

    def test_001_log_in_with_user(self):
        """
        DESCRIPTION: Log in with user
        EXPECTED: * User is logged in
        EXPECTED: * All available Free bets are received in **user** response
        """
        pass

    def test_002_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        EXPECTED: * "Use Free Bet" link is displayed under event name
        EXPECTED: * "Place Bet" CTA is inactive, "Add to Betslip" active
        EXPECTED: ![](index.php?/attachments/get/31374)
        """
        pass

    def test_003_tap_use_free_bet_link(self):
        """
        DESCRIPTION: Tap "Use Free Bet" link
        EXPECTED: * Appears 'FreeBet' Pop up with a list of up available FreeBets with check box
        EXPECTED: * Header of the 'FreeBet' Pop up contains the quantity of available free bets (e.g. Free Bets Available (x1))
        EXPECTED: * Each free bet is displayed in next format:
        EXPECTED: <currency symbol> <free bet value> <Free bet name>
        EXPECTED: where <currency symbol>  - currency set during registration
        EXPECTED: ![](index.php?/attachments/get/31375)
        EXPECTED: *[From OX100]*
        EXPECTED: * 'ADD' CTA is displayed (inactive):
        EXPECTED: Coral design:
        EXPECTED: ![](index.php?/attachments/get/36073)
        EXPECTED: Ladbrokes design:
        EXPECTED: ![](index.php?/attachments/get/36074)
        """
        pass

    def test_004_verify_free_bet_token_name(self):
        """
        DESCRIPTION: Verify Free bet token name
        EXPECTED: Free bet token name corresponds to **freebets.data.[i].freebetOfferName** attribute received in **user** response
        EXPECTED: where i - number of free bets returned in response
        """
        pass

    def test_005_verify_free_bet_token_value(self):
        """
        DESCRIPTION: Verify Free bet token value
        EXPECTED: Free bet token value corresponds to **freebets.data.[i].freebetTokenValue** attribute received in **user** response
        EXPECTED: where i - number of free bets returned in response
        """
        pass

    def test_006_select_one_of_the_available_free_bets_from_free_bet_pop_upfrom_ox100_select_one_of_the_available_free_bets_from_free_bet_pop_up_and_click_on_add_button(self):
        """
        DESCRIPTION: Select one of the available Free Bets from Free Bet pop up
        DESCRIPTION: *[From OX100]* Select one of the available Free Bets from Free Bet pop up AND click on 'ADD' button.
        EXPECTED: *[Not actual from OX100]*
        EXPECTED: * Freebet checkbox is checked for applicable freebet and 'FreeBet' Pop up closes in a moment
        EXPECTED: * '- Remove Free Bet' link is displayed under the event name in the 'Quick bet'
        EXPECTED: * Total stake is updated with the Freebet value. Potential returns/Est returns based on odds taken also updated.
        EXPECTED: ![](index.php?/attachments/get/31376)
        EXPECTED: *[From OX100]*
        EXPECTED: * Freebet radiobutton is checked for applicable freebet
        EXPECTED: * 'ADD' CTA becomes active:
        EXPECTED: Coral design:
        EXPECTED: ![](index.php?/attachments/get/36075)
        EXPECTED: Ladbrokes design:
        EXPECTED: ![](index.php?/attachments/get/36076)
        EXPECTED: * Pop up is closed after tapping 'ADD' CTA
        EXPECTED: * '- Remove Free Bet' link is displayed under the event name in the 'Quick bet'
        EXPECTED: * Total stake is updated with the Freebet value
        EXPECTED: * Free bet icon is displayed near Freebet value in the total stake
        EXPECTED: * Potential returns/Est returns based on odds taken also updated
        EXPECTED: * Free bet icon below the stake box is displayed in the 'Quick bet'
        EXPECTED: Coral design:
        EXPECTED: ![](index.php?/attachments/get/36301)
        EXPECTED: Ladbrokes design:
        EXPECTED: ![](index.php?/attachments/get/36080)
        """
        pass

    def test_007_click___remove_free_bet_link(self):
        """
        DESCRIPTION: Click '- Remove Free Bet' link
        EXPECTED: * The previously selected value is cleared
        EXPECTED: * "Use Free Bet" link appears instead '- Remove Free Bet' link
        """
        pass
