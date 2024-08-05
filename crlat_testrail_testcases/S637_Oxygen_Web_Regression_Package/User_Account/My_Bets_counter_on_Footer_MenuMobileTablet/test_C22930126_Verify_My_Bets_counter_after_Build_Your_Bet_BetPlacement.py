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
class Test_C22930126_Verify_My_Bets_counter_after_Build_Your_Bet_BetPlacement(Common):
    """
    TR_ID: C22930126
    NAME: Verify My Bets counter after Build Your Bet  BetPlacement
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after BYB Bet Placement
    PRECONDITIONS: - Load Oxygen/Roxanne Application and login
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True

    def test_001_navigate_to_byb_tab_and_place_bet_for_any_byb_market(self):
        """
        DESCRIPTION: Navigate to BYB tab and place bet for any BYB market
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_002__close_byb_betslip_verify_my_bets_counter_on_the_footer_panel(self):
        """
        DESCRIPTION: * Close BYB Betslip
        DESCRIPTION: * Verify 'My Bets' counter on the Footer panel
        EXPECTED: My bets counter icon is increased by one
        """
        pass
