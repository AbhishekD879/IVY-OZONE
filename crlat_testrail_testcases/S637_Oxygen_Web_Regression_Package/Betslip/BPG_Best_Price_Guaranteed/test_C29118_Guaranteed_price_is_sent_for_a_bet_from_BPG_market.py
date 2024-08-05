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
class Test_C29118_Guaranteed_price_is_sent_for_a_bet_from_BPG_market(Common):
    """
    TR_ID: C29118
    NAME: Guaranteed price is sent for a bet from BPG market
    DESCRIPTION: 
    PRECONDITIONS: GP available checkbox is selected on market level in TI (isGpAvailable="true" attribute is returned for the market from SiteServer)
    PRECONDITIONS: Event has SP and LP prices available
    PRECONDITIONS: **NOTE: BPG replaced to BOG ( https://jira.egalacoral.com/browse/BMA-49331 ) from Coral 101.2 / Ladbrokes 100.4 versions**
    """
    keep_browser_open = True

    def test_001_add_selection_from_bpg_market_to_the_betslip_enter_stake_and_place_a_bet(self):
        """
        DESCRIPTION: Add selection from BPG market to the Betslip, enter stake and place a bet
        EXPECTED: Bet is placed
        """
        pass

    def test_002_verify_placebet_request_in_network(self):
        """
        DESCRIPTION: Verify placebet request in Network
        EXPECTED: The following parameter is present:
        EXPECTED: priceTypeRef: {id: "GUARANTEED"}
        """
        pass
