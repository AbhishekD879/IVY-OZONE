import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C18574309_Verify_number_of_legs_in_placeBet_response_for_Multiple_bet_placement(BaseCashOutTest, BaseBetSlipTest):
    """
    TR_ID: C18574309
    NAME: Verify number of legs in 'placeBet' response for Multiple bet placement
    DESCRIPTION: This test case verify number of legs in 'placeBet' response for Multiple bet placement
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Log in app with the user that has a positive balance
    PRECONDITIONS: 3. Add at least 2 selections from different evennt to the Betslip
    PRECONDITIONS: 4. Make Bet Placement
    PRECONDITIONS: 5. Check data in 'placeBet' response
    PRECONDITIONS: **Note:**
    PRECONDITIONS: For checking the data find the 'placeBet' response in Dev Tools -> Network -> Preview
    PRECONDITIONS: ![](index.php?/attachments/get/35972)
    """
    keep_browser_open = True
    number_of_events = 2

    def test_000_preconditions(self):
        """
       PRECONDITIONS: 1. Load Oxygen app
       PRECONDITIONS: 2. Log in app with the user that has a positive balance
       PRECONDITIONS: 3. Add at least 2 selections from different evennt to the Betslip
       PRECONDITIONS: 4. Make Bet Placement
       PRECONDITIONS: 5. Check data in 'placeBet' response
       """
        self.site.login()
        if tests.settings.backend_env == 'prod':

            event1 = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True,
                                                         number_of_events=self.number_of_events)[0]
            outcomes = next(((market['market']['children']) for market in event1['event']['children']), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            all_selection_ids1 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id1 = list(all_selection_ids1.values())[0]

            event2 = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True,
                                                         number_of_events=self.number_of_events)[1]

            outcomes = next(((market['market']['children']) for market in event2['event']['children']), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            all_selection_ids2 = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id2 = list(all_selection_ids2.values())[0]
        else:
            event1 = self.ob_config.add_autotest_premier_league_football_event()
            event2 = self.ob_config.add_autotest_premier_league_football_event()
            selection_id1 = list(event1.selection_ids.values())[0]
            selection_id2 = list(event2.selection_ids.values())[0]
        self.open_betslip_with_selections(selection_ids=(selection_id1, selection_id2))
        self.place_multiple_bet()

    def test_001_open_placebet_response_and_check_the_number_of_received_legs_for_multiple_betsplacebet___bet___bettyperef_id_eg_dbl___leg(self):
        """
        DESCRIPTION: Open 'placeBet' response and check the number of received legs for Multiple bets
        DESCRIPTION: placeBet -> bet -> betTypeRef: {id: "e.g. DBL"} -> leg
        EXPECTED: 'leg' section contains ids of all selections from particular Multiple bets
        EXPECTED: (e.g.
        EXPECTED: 2 selections ids for Double
        EXPECTED: 3 selections ids for Treble
        EXPECTED: etc.)
        """
        url = f'{tests.settings.BETTINGMS}v1/placeBet'
        placebet_request = self.get_web_socket_response_by_url(url=url)
        self._logger.debug(f'*** Got {placebet_request} from placeBet request')
        post_data = placebet_request.get('postData')
        self.assertTrue(post_data, msg='Post Data is not found in placeBet request')
        legs = post_data.get('leg')
        self.assertTrue(legs, msg='No Legs found in placeBet request')
        selections = []
        for leg in legs:
            sports_leg = leg.get('sportsLeg')
            self.assertTrue(sports_leg, msg='No sportsLeg found in placeBet request')
            leg_parts = sports_leg.get('legPart')
            self.assertTrue(leg_parts, msg='No Outcomes are displayed')
            outcome_ref = leg_parts[0].values()
            selections.append(list(outcome_ref))
        self.assertTrue(selections, msg=f'No selections "{selections}" ids are displayed')
