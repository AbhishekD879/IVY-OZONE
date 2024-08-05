import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.bpg
@pytest.mark.medium
@pytest.mark.racing
@pytest.mark.bet_placement
@pytest.mark.betslip
@pytest.mark.login
@vtest
class Test_C29118_Guaranteed_price_is_sent_for_a_bet_from_BPG_market(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C29118
    NAME: Guaranteed price is sent for a bet from BPG market
    PRECONDITIONS: GP available checkbox is selected on market level in TI (isGpAvailable="true" attribute is returned for the market from SiteServer)
    PRECONDITIONS: Event has SP and LP prices available
    """
    keep_browser_open = True
    expected_price_type_ref = {'id': 'GUARANTEED'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event and log in
        """
        self.__class__.max_number_of_selections = self.get_initial_data_system_configuration().get('Betslip', {}).get('maxBetNumber', 20)

        if tests.settings.backend_env == 'prod':
            event = self.get_event_details(gp=True)
            self.__class__.eventID = event.event_id
            self.__class__.selection_ids = {}
            selections_count = 0
            for outcome_name, outcome in event.outcomes_info.items():
                if 'Unnamed' not in outcome_name and selections_count < int(self.max_number_of_selections):
                    self.selection_ids[outcome_name] = outcome
                    selections_count += 1
        else:
            event = self.ob_config.add_UK_racing_event(number_of_runners=1, gp=True, lp_prices=['1/2'])
            self.__class__.eventID = event.event_id
            self.__class__.selection_ids = event.selection_ids

        self.site.login()

    def test_001_add_selection_from_bpg_market_to_the_betslip_enter_stake_and_place_a_bet(self):
        """
        DESCRIPTION: Add selection from BPG market to the Betslip, enter stake and place a bet
        EXPECTED: Bet is placed
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values()))
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_002_verify_placebet_request_in_network(self):
        """
        DESCRIPTION: Verify placeBet request in Network
        EXPECTED: The following parameter is present:
        EXPECTED: priceTypeRef: {id: "GUARANTEED"}
        """
        url = f'{tests.settings.BETTINGMS}v1/placeBet'
        placebet_request = self.get_web_socket_response_by_url(url=url)
        self._logger.debug(f'*** Got {placebet_request} from placeBet request')
        post_data = placebet_request.get('postData')
        self.assertTrue(post_data, msg='Post Data is not found in placeBet request')
        legs = post_data.get('leg')
        self.assertTrue(legs, msg='No Legs found in placeBet request')
        for leg in legs:
            sports_leg = leg.get('sportsLeg')
            self.assertTrue(sports_leg, msg='No sportsLeg found in placeBet request')
            price = sports_leg.get('price')
            self.assertTrue(price, msg='No price found in placeBet request')
            price_type_ref = price.get('priceTypeRef')
            self.assertTrue(price_type_ref, msg='No priceTypeRef found in placeBet request')
            self.assertDictEqual(self.expected_price_type_ref, price_type_ref)
