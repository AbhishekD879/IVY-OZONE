import json
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import do_request
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can not create events with surface bet module in prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C58836452_Verify_that_Outcome_details_are_taken_from_buildBet_for_Sport_selections_and_actions_in_Betslip(BaseBetSlipTest, BaseFeaturedTest):
    """
    TR_ID: C58836452
    NAME: Verify that Outcome details are taken from <buildBet>  for <Sport> selections and actions in Betslip
    DESCRIPTION: Test case verifies data source being set as BPP for certain actions regarding <Sport> selections within Betslip.
    PRECONDITIONS: * Upcoming events should be present for a chosen sport
    PRECONDITIONS: * Surface bet should be configured for the upcoming sport event, containing active selection
    PRECONDITIONS: * Oxygen app should be opened
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * QuickBet should be disabled for mobile responsive mode
    PRECONDITIONS: DevTools should be opened (Click on 'Inspect') -> 'Network' tab -> 'XHR' filter
    PRECONDITIONS: 'Simple' value should be set within Filter for XHR requests list in DevTools
    PRECONDITIONS: **SLP** = Sports Landing Page
    PRECONDITIONS: **EDP** = Event Details Page
    PRECONDITIONS: **NOTE:** EDP 'Simple' SS request is sent once the page is opened; Also 'Simple' SS request is present when SLP is opened - this is a correct behavior.
    """
    keep_browser_open = True
    headers = {'Content-Type': 'application/json'}

    def get_build_bet_request_data(self):
        url = f'{tests.settings.BETTINGMS}v1/buildBet'
        placebet_request = self.get_web_socket_response_by_url(url=url)
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
        data = json.dumps(post_data)
        req = do_request(url=url, data=data, headers=self.headers)
        self.__class__.event_ids = []
        self.__class__.outcome_details = req['outcomeDetails']
        for outcome in self.outcome_details:
            ss_request = self.ss_req.ss_event_to_outcome_for_event(event_id=outcome['eventId'])
            ss_event = ss_request[0]['event']
            self.event_ids.append(ss_event['id'])

    def test_000_preconditions(self):
        self.__class__.category_id = self.ob_config.football_config.category_id
        cms_surface_bet = self.cms_config.get_sport_module(sport_id=self.category_id,
                                                           module_type='SURFACE_BET')[0]
        if cms_surface_bet['disabled']:
            self.cms_config.change_sport_module_state(sport_module=cms_surface_bet)

        event = self.ob_config.add_autotest_premier_league_football_event()
        surface_bet_event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_id = event.event_id
        selection_ids, team1 = surface_bet_event.selection_ids, surface_bet_event.team1
        surface_bet = self.cms_config.add_surface_bet(selection_id=selection_ids[team1],
                                                      eventIDs=self.event_id, edpOn=True)
        self.__class__.surface_bet_title = surface_bet.get('title').upper()

    def test_001_navigate_to_slp_of_any_sport_with_event_cardsand_selections_being_shown_on_the_page(self):
        """
        DESCRIPTION: Navigate to SLP of any 'sport' with event cards(and selections) being shown on the page
        EXPECTED: Page contains event(s)/list(s) with selections
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state('Football')
        self.__class__.sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='Sections not found')
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.all_selection_ids = list(event.selection_ids.values())

    def test_002_clear_the_requests_table_in_devtools_via_clear_buttonindexphpattachmentsget114053615(self):
        """
        DESCRIPTION: Clear the requests table in DevTools via 'Clear' button
        DESCRIPTION: ![](index.php?/attachments/get/114053615)
        EXPECTED: Requests table in DevTools becomes empty
        """
        # Can not Automate this step

    def test_003_add_2_selections_into_betslip(self):
        """
        DESCRIPTION: Add 2 selections into Betslip
        EXPECTED: * BuildBet requests are sent to BPP
        EXPECTED: * Second request contains bet data regarding the price, status, etc. of both selections
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains added selection is not sent after this action
        EXPECTED: ![](index.php?/attachments/get/114053626) ![](index.php?/attachments/get/114053629)
        """
        self.open_betslip_with_selections(selection_ids=(self.all_selection_ids[0], self.all_selection_ids[1]))
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip was not opened')
        self.get_build_bet_request_data()

    def test_004_tap_on_x_button_in_the_betslip_to_remove_any_selection(self):
        """
        DESCRIPTION: Tap on 'X' button in the Betslip to remove any selection
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of the remaining selection
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains removed selection is not sent after this action
        EXPECTED: ![](index.php?/attachments/get/114053638) ![](index.php?/attachments/get/114053641)
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        self.stake = list(singles_section.values())[0]
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip was not opened')
        self.stake.remove_button.click()
        self.get_build_bet_request_data()
        self.assertNotIn(self.event_id, self.event_ids, msg='removed selection is present in SS request')

    def test_005_close_betslip_and_open_edp_of_the_event_that_contains_surface_betindexphpattachmentsget114053649(self):
        """
        DESCRIPTION: Close Betslip and open EDP of the event that contains 'Surface Bet'
        DESCRIPTION: ![](index.php?/attachments/get/114053649)
        EXPECTED: * Event details page is opened
        EXPECTED: * 'Surface Bet' container is shown above the first market
        """
        self.site.close_betslip()
        self.navigate_to_edp(self.event_id, timeout=15)
        self.assertTrue(self.site.sport_event_details.tab_content.has_surface_bets(),
                        msg=f'Surface Bet module is not shown on the EDP with event_id: {self.event_id}')
        surface_bets = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='There are no surface bet in the container')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" is not found in "{list(surface_bets.keys())}"')

    def test_006_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED:
        """
        # Can not Automate this step

    def test_007_add_surface_bet_selection_into_betslip_by_tappingclicking_on_it(self):
        """
        DESCRIPTION: Add Surface Bet selection into BetSlip by tapping/clicking on it
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of both new and previously added selections
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains added selection is not sent after this action
        EXPECTED: ![](index.php?/attachments/get/114053654) ![](index.php?/attachments/get/114053658)
        """
        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertEqual(1, len(surface_bets), msg=f'Only one Surface Bet should be shown not "{len(surface_bets)}"')
        self.__class__.surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(self.surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')
        self.assertTrue(self.surface_bet.has_bet_button(), msg=f'Bet Button is not shown for {self.surface_bet_title}')
        self.surface_bet.bet_button.click()
        self.get_build_bet_request_data()

    def test_008_click_on_selection_within_surface_bet_again(self):
        """
        DESCRIPTION: Click on selection within Surface Bet again
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of the remaining selection
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains removed selection is not sent after this action
        EXPECTED: ![](index.php?/attachments/get/114053662) ![](index.php?/attachments/get/114053660)
        """
        self.get_build_bet_request_data()
        self.assertNotIn(self.event_id, self.event_ids, msg='removed selection is present in SS request')
