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
class Test_C15931380_From_OX_99_Free_Bet_Pop_up(Common):
    """
    TR_ID: C15931380
    NAME: [From OX 99] Free Bet Pop up
    DESCRIPTION: This test case verifies Free Bets pop up
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has Free Bets available on their account
    PRECONDITIONS: * User has at least one selection added to the Betslip
    PRECONDITIONS: -----
    PRECONDITIONS: - For DEV/TST env. - https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: - For PROD/HL env.:
    PRECONDITIONS: Coral: https://sports.coral.co.uk/promotions/details/new-customer-offer (Open a new online, mobile or telephone account with Coral. Place a £5+ Win or £5+ Each Way bet on any sport. Coral will give you an instant four x £5 free bets.)
    PRECONDITIONS: Ladbrokes: https://m.ladbrokes.com/en-gb/#!/promotions/0 (Register a new Ladbrokes account on mobile or online using promo code '20FREE'. Place cumulative qualifying stakes to a total of £5 win or £5 each-way at odds totalling 1/2 or greater.)
    """
    keep_browser_open = True

    def test_001_open_bet_slip_and_press_on_use_free_bet_link(self):
        """
        DESCRIPTION: Open Bet Slip and press on "Use Free Bet" link
        EXPECTED: * Free Bet Pop up is shown with list of Free Bets available
        EXPECTED: * Each free bet is displayed in next format:
        EXPECTED: <Currency Symbol> <Free Bet Value> <Free Bet Name><Class/Type/Event etc for which this Free Bet can be applied>
        """
        pass

    def test_002_verify_list_of_free_bets_available_corresponds_to_list_of_free_bets_received_in_buildbet_request(self):
        """
        DESCRIPTION: Verify list of Free Bets available corresponds to list of Free Bets received in *buildBet request*
        EXPECTED: *[From OX99]*
        EXPECTED: Free Bets available corresponds to list of Free Bets received in *buildBet request*
        EXPECTED: *[After OX100.1]*
        EXPECTED: * Free Bets available corresponds to list of Free Bets received in *buildBet request*
        EXPECTED: * Only eligible Free Bets for selected bet are displayed. If [freebet value] / [lines number] is < 0.01 then filter out available freebets for this bet (e.g. if user has £0.10 free bet then it will NOT be available for multiple bets with x11 and more lines)
        """
        pass

    def test_003_from_ox99_select_one_of_available_free_bets_from_free_bet_pop_upfrom_ox100_select_one_of_available_free_bets_from_free_bet_pop_up_and_click_on_add_button(self):
        """
        DESCRIPTION: *[From OX99]* Select one of available Free Bets from Free Bet pop up
        DESCRIPTION: *[From OX100]* Select one of available Free Bets from Free Bet pop up AND click on 'ADD' button.
        EXPECTED: *[From OX99]*
        EXPECTED: * Selected Free Bet has check box marked as selected
        EXPECTED: * Pop up is closed (in 0.2 sec)
        EXPECTED: * "Use Free Bet" link is changed to "- Remove Free Bet" link
        EXPECTED: *[From OX100]*
        EXPECTED: * Chosen Free Bet has radio button marked as selected
        EXPECTED: * 'ADD' button becomes active:
        EXPECTED: Coral Popup Design:
        EXPECTED: ![](index.php?/attachments/get/36071)
        EXPECTED: Ladbrokes Popup Design:
        EXPECTED: ![](index.php?/attachments/get/36072)
        EXPECTED: * Chosen Free Bet successfully added
        EXPECTED: * "Use Free Bet" link is changed to "- Remove Free Bet" link
        """
        pass

    def test_004_press_on___remove_free_bet_link(self):
        """
        DESCRIPTION: Press on "- Remove Free Bet" link
        EXPECTED: * "- Remove Free Bet" link is changed to "Use Free Bet" link
        EXPECTED: * 'Estimated Returns' is changed to 0.00
        """
        pass
