from random import choice

import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.event_details
@pytest.mark.evergage
@pytest.mark.bet_placement
@pytest.mark.my_bets
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.login
@vtest
class Test_C119840_Verify_eventID_attribute_in_DOM_on_EventDetails_My_Bets_Tab(BaseBetSlipTest):
    """
    TR_ID: C119840
    NAME: Verify 'eventid' attribute in the DOM/HTML on Event Details My Bets Tab
    DESCRIPTION: This Test Case verifies 'eventid' attribute in the DOM/HTML on Event Details My Bets Tab.
    """
    keep_browser_open = True
    bet_amount = 1.00

    def test_001_create_test_event_and_place_bet(self):
        """
        DESCRIPTION: Create event and place bet using its selections
        EXPECTED: Event is created and bet is placed on its selections
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)
            event = choice(events)
            self.__class__.eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            selection_id = next(i['outcome']['id'] for i in outcomes)
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event.event_id
            selection_id = list(event.selection_ids.values())[0]

        self.site.login()
        self.open_betslip_with_selections(selection_ids=selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_002_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event Details page
        EXPECTED: Event Details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_003_verify_event_id_on_my_bets_tab(self):
        """
        DESCRIPTION: Verify event id on My Bets tab
        EXPECTED: Event id is present on My Bets tab
        """
        self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)
        bet_sections = self.site.sport_event_details.my_bets.accordions_list.items_as_ordered_dict
        self.assertTrue(bet_sections, msg='No bet section was found')
        bet_section = list(bet_sections.values())[0]
        bet_legs = bet_section.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No bet leg was found in "{bet_legs}"')
        for bet_leg_name, bet_leg in bet_legs.items():
            self._logger.info(f'*** Verifying event id for bet leg "{bet_leg_name}", '
                              f'event id is "{bet_leg.event_id}"')
            self.assertEqual(bet_leg.event_id, self.eventID,
                             msg=f'Actual event ID: "{bet_leg.event_id}" is not equal to expected: "{self.eventID}"')
