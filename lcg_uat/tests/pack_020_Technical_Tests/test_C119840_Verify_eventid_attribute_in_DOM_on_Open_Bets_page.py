import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.evergage
@pytest.mark.open_bets
@pytest.mark.bet_placement
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.login
@vtest
class Test_C119840_Verify_eventID_attribute_in_DOM_on_OpenBets_page(BaseBetSlipTest):
    """
    TR_ID: C119840
    NAME: Verify 'eventid' attribute in the DOM/HTML on Open Bets page
    DESCRIPTION: This Test Case verifies 'eventid' attribute in the DOM/HTML on Open Bets page.
    """
    keep_browser_open = True

    def check_event_id_in_my_bets_bet_details(self, event_name):
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(event_names=event_name,
                                                                                bet_type='SINGLE',
                                                                                number_of_bets=1)
        bet_legs = bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found in section: "{bet_name}"')
        for leg_name, leg in bet_legs.items():
            event_id = leg.event_id
            self._logger.info(f'*** Verifying event id for bet "{leg.outcome_name}", event id is: "{leg.event_id}"')
            self.assertEqual(event_id, self.eventID)

    def test_000_create_test_event(self):
        """
        DESCRIPTION: Create test event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID, self.__class__.team1, self.__class__.team2, self.__class__.selection_ids\
            = event_params.event_id, event_params.team1, event_params.team2, event_params.selection_ids

        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'

    def test_001_login(self):
        """
        DESCRIPTION: Login as user that have bet history
        EXPECTED: User is successfully logged in
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_open_betslip_with_one_of_selections(self):
        """
        DESCRIPTION: Open BetSlip with one of selections
        EXPECTED: Betslip is opened and contains added selection
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_003_place_bet(self):
        """
        DESCRIPTION: Place bet
        EXPECTED: Bet is placed
        """
        self.place_single_bet()

    def test_004_wait_for_bet_receipt(self):
        """
        DESCRIPTION: Wait for Bet Receipt and close it
        EXPECTED: Bet Receipt is shown and is closed upon clicking 'Done' button
        """
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_005_open_my_bets_page(self):
        """
        DESCRIPTION: Go to My Bets page
        EXPECTED: My Bets page is opened, expected active tab is 'OPEN BETS'
        """
        self.site.open_my_bets_open_bets()

    def test_006_verify_event_id_on_open_bets_page(self):
        """
        DESCRIPTION: Verify event id on Open Bets page
        EXPECTED: Event id is present for bet on Open Bets page
        """
        self.check_event_id_in_my_bets_bet_details(event_name=self.event_name)
