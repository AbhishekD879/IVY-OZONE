import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C16408290_Verify_My_Bets_counter_after_Sport_Bet_Placement(Common):
    """
    TR_ID: C16408290
    NAME: Verify My Bets counter after Sport Bet Placement
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after Sport Bet Placement
    DESCRIPTION: Autotest: [C58634254]
    PRECONDITIONS: - Load Oxygen/Roxanne Application and login
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True

    def test_001_add_sport_selection__eg_football_to_quickbetbetslip_and_place_bet(self):
        """
        DESCRIPTION: Add sport selection ( e.g. Football) to Quickbet/Betslip and place bet
        EXPECTED: Bets is placed successfully
        """
        pass

    def test_002__close_quickbetbetslip_verify_my_bets_counter_at_the_footer_panel(self):
        """
        DESCRIPTION: * Close Quickbet/Betslip
        DESCRIPTION: * Verify 'My Bets' counter at the Footer panel
        EXPECTED: My bets counter icon is increased by one
        """
        pass

    def test_003_repeat_steps_1_4_for_multiples(self):
        """
        DESCRIPTION: Repeat steps #1-4 for multiples
        EXPECTED: Results are the same:
        EXPECTED: My bets counter icon is increased by one
        """
        pass
