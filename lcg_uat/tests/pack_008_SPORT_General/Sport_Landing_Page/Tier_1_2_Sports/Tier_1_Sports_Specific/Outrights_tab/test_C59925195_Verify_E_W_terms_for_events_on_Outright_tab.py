import pytest
import voltron.environments.constants as vec
import tests
from faker import Faker
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - can't create events on prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C59925195_Verify_E_W_terms_for_events_on_Outright_tab(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C59925195
    NAME: Verify E/W terms for events on Outright tab
    DESCRIPTION: This test case verifies E/W terms data on Outright page
    PRECONDITIONS: 1) At least 1 available 'Outright' should be created and active for the chosen sport category
    PRECONDITIONS: 2) Load Oxygen app
    PRECONDITIONS: 3) Navigate to a chosen Sports Landing Page
    PRECONDITIONS: 4) Switch to 'Outrights' tab
    """
    keep_browser_open = True

    def get_market_from_ss(self, event_id: str) -> dict:
        """
        Gets market for given event from SS response
        :param event_id: specifies event id
        :return: dict with market attributes and their values
        """
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        markets = resp[0]['event']['children'] if 'event' in resp[0] and 'children' in resp[0]['event'] else []

        self.assertEquals(len(markets), 1,
                          msg=f'Only one market is expected in SS response. Now there are {len(markets)} of them.')
        return markets[0]['market']

    def get_markets_from_events(self, event_id):
        self.navigate_to_edp(event_id=event_id, sport_name='football')
        self.__class__.market = self.get_market_from_ss(event_id)
        self.__class__.markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create outright event which has market with Each Way terms available
        """
        fake = Faker()
        self.__class__.ew_event_name = f'Event {fake.city()} with each way'
        self.__class__.event_name = f'Event {fake.name_female()} without each way'
        ew_event = self.ob_config.add_autotest_premier_league_football_outright_event(event_name=self.ew_event_name, ew_terms=self.ew_terms)
        event = self.ob_config.add_autotest_premier_league_football_outright_event(event_name=self.event_name)
        self.__class__.eventID = ew_event.event_id
        self.__class__.event_id = event.event_id
        self.__class__.section_name = tests.settings.football_autotest_league
        self.site.login()

    def test_001__expand_any_event_available_sport_type_accordion_pick_available_outright_event(self):
        """
        DESCRIPTION: * Expand any event available sport type accordion
        DESCRIPTION: * Pick available 'Outright' event
        EXPECTED: * Outright page is opened
        EXPECTED: * First two markets are expanded. Other markets accordions are collapsed if present
        """
        self.site.open_sport('Football')
        self.site.football.tabs_menu.click_button(self.expected_sport_tabs.outrights)
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        if self.brand == "ladbrokes" and self.device_type == 'desktop':
            self.section_name = self.section_name.title()
        self.assertIn(self.section_name, sections, msg=f'Section "{self.section_name}" is not present in sections')
        section = sections[self.section_name]
        if not section.is_expanded():
            section.expand()
        is_section_expanded = section.is_expanded()
        self.assertTrue(is_section_expanded, msg=f'Section "{self.section_name}" is not expanded')
        outrights = section.items_as_ordered_dict
        self.assertTrue(outrights, msg=f'*** No event outright is present in section: "{self.section_name}"')
        self.assertIn(self.ew_event_name, outrights, msg=f'Section "{self.ew_event_name}" is not present in outrights')
        outright = outrights[self.ew_event_name]
        outright.click()
        if self.device_type == 'desktop' and self.brand != 'ladbrokes':
            expected_event_name = self.ew_event_name.upper()
        elif self.device_type == 'desktop' and self.brand == 'ladbrokes':
            expected_event_name = self.ew_event_name.title()
        else:
            expected_event_name = self.ew_event_name
        event_name = self.site.sport_event_details.event_title_bar.event_name
        self.assertEqual(event_name, expected_event_name,
                         msg='Incorrect EDP is opened.\nActual event name is "%s"\nExpected: "%s"'
                             % (event_name, expected_event_name))

    def test_002_check_ew_terms_for_any_available_market(self):
        """
        DESCRIPTION: Check E/W terms for any available market
        EXPECTED: * If market has isEachWayAvailable: "true" parameter, E/W terms are displayed
        EXPECTED: * If market has no 'isEachWayAvailable' parameter at all, E/W terms are NOT displayed
        EXPECTED: ![](index.php?/attachments/get/119596593)
        EXPECTED: ![](index.php?/attachments/get/119596592)
        """
        market = self.get_market_from_ss(self.eventID)
        self.assertIn('isEachWayAvailable', market.keys(),
                      msg=f'There\'s no property "isEachWayAvailable" in SS response. '
                          f'See all available properties: {market.keys()}')
        self.assertEquals(market['isEachWayAvailable'], 'true',
                          msg='Incorrect value for "isEachWayAvailable" in SS response.\nActual: "%s"\nExpected: "%s'
                              % (market['isEachWayAvailable'], 'true'))
        self.assertIn('eachWayFactorNum', market.keys(),
                      msg=f'There\'s no property "eachWayFactorNum" in SS response. '
                          f'See all available properties: {market.keys()}')
        self.assertEquals(market['eachWayFactorNum'], str(self.ew_terms['ew_fac_num']),
                          msg='Incorrect value for "eachWayFactorNum" in SS response.\nActual: "%s"\nExpected: "%s'
                              % (market['eachWayFactorNum'], str(self.ew_terms['ew_fac_num'])))
        self.assertIn('eachWayFactorDen', market.keys(),
                      msg=f'There\'s no property "eachWayFactorDen" in SS response. '
                          f'See all available properties: {market.keys()}')
        self.assertEquals(market['eachWayFactorDen'], str(self.ew_terms['ew_fac_den']),
                          msg='Incorrect value for "eachWayFactorDen" in SS response.\nActual: "%s"\nExpected: "%s'
                              % (market['eachWayFactorDen'], str(self.ew_terms['ew_fac_den'])))
        self.assertIn('eachWayPlaces', market.keys(),
                      msg=f'There\'s no property "eachWayPlaces" in SS response. '
                          f'See all available properties: {market.keys()}')
        self.assertEquals(market['eachWayPlaces'], str(self.ew_terms['ew_places']),
                          msg='Incorrect value for "eachWayPlaces" in SS response.\nActual: "%s"\nExpected: "%s'
                              % (market['eachWayPlaces'], str(self.ew_terms['ew_places'])))

        self.get_markets_from_events(self.event_id)
        self.assertNotIn('isEachWayAvailable', self.market.keys())
        if self.brand == 'bma' and self.device_type == 'desktop':
            self.__class__.outright_name = vec.siteserve.OUTRIGHT.upper()
        else:
            self.__class__.outright_name = vec.siteserve.OUTRIGHT
        self.assertFalse(self.markets[self.outright_name].outcomes.has_terms,
                         msg='Each way terms should not be displayed')

    def test_003_for_mobile_add_any_selection_from_outrights_page_to_quickbet(self):
        """
        DESCRIPTION: **[For mobile]** Add any selection from 'Outrights' page to QuickBet
        EXPECTED: * If market has isEachWayAvailable: "true" parameter, E/W checkbox is present for market with chosen selection
        EXPECTED: * User could tick E/W checkbox and place a bet
        EXPECTED: * If market of the selection has no 'isEachWayAvailable' parameter at all, E/W checkbox is NOT present
        """
        self.get_markets_from_events(self.eventID)
        self.markets[self.outright_name].outcomes.items[0].bet_button.click()
        self.assertIn('isEachWayAvailable', self.market.keys(),
                      msg=f'There\'s no property "isEachWayAvailable" in SS response. '
                          f'See all available properties: {self.market.keys()}')
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            quick_bet = self.site.quick_bet_panel.selection.content
            self.assertTrue(quick_bet.has_each_way_checkbox(), msg='eachway checkbox is not displayed')
            quick_bet.each_way_checkbox.click()
            self.assertTrue(quick_bet.each_way_checkbox.is_selected(), msg='Each Way is not selected')
            quick_bet.amount_form.input.value = self.bet_amount
            self.site.quick_bet_panel.place_bet.click()
            bet_receipt = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt, msg='Bet Receipt is not displayed')
        else:
            singles_section = self.get_betslip_sections().Singles
            stake_name, stake = list(singles_section.items())[0]
            self.assertTrue(stake.has_each_way_checkbox(),
                            msg=f'Stake "{stake_name}" does not have Each Way checkbox')
            stake.amount_form.input.value = self.bet_amount
            self.get_betslip_content().bet_now_button.click()
            self.check_bet_receipt_is_displayed()

        self.get_markets_from_events(self.event_id)
        self.assertNotIn('isEachWayAvailable', self.market.keys(), msg='iseachwayAvailable is displayed')
        self.markets[self.outright_name].outcomes.items[0].bet_button.click()
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            quick_bet = self.site.quick_bet_panel.selection.content
            self.assertFalse(quick_bet.has_each_way_checkbox(), msg='eachway checkbox is displayed')
        else:
            singles_section = self.get_betslip_sections().Singles
            stake_name, stake = list(singles_section.items())[0]
            self.assertFalse(stake.has_each_way_checkbox(),
                             msg=f'Stake "{stake_name}" have Each Way checkbox')

    def test_004_add_any_selection_from_outrights_page_to_betslip(self):
        """
        DESCRIPTION: Add any selection from 'Outrights' page to Betslip
        EXPECTED: * If market has isEachWayAvailable: "true" parameter, E/W checkbox is present for market with chosen selection
        EXPECTED: * User could tick E/W checkbox and place a bet
        EXPECTED: * If market of the selection has no 'isEachWayAvailable' parameter at all, E/W checkbox is NOT present
        """
        # Covered in test_003
