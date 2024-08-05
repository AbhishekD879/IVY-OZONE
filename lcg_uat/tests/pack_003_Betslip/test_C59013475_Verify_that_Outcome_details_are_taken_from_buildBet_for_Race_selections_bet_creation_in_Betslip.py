import json
import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import do_request


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can not create events with surface bet module in prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59013475_Verify_that_Outcome_details_are_taken_from_buildBet_for_Race_selections_bet_creation_in_Betslip(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C59013475
    NAME: Verify that Outcome details are taken from <buildBet> for <Race> selections bet creation in Betslip
    DESCRIPTION: Test case verifies data source being set as BPP for certain actions regarding <Race> selections within Betslip.
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
        """
        PRECONDITIONS: * Upcoming events should be present for a chosen Race type
        PRECONDITIONS: * Selections that have both 'SP' and 'LP' values should be available within the chosen 'Race' event
        PRECONDITIONS: * 'Next Races' module should be configured, containing active selections for upcoming events
        PRECONDITIONS: * Oxygen app should be opened
        PRECONDITIONS: * User should be logged in
        PRECONDITIONS: * QuickBet should be disabled for mobile responsive mode
        PRECONDITIONS: DevTools should be opened (Click on 'Inspect') -> 'Network' tab -> 'XHR' filter
        PRECONDITIONS: 'Simple' value should be set within Filter for XHR requests list in DevTools
        PRECONDITIONS: SLP = Sports Landing Page
        PRECONDITIONS: EDP = Event Details Page
        """
        if tests.settings.cms_env != 'prd0':
            self.setup_cms_next_races_number_of_events()
        self.__class__.is_desktop = False if self.device_type == 'mobile' else True
        next_races_toggle_config = self.get_initial_data_system_configuration().get('NextRacesToggle')
        if not next_races_toggle_config:
            next_races_toggle_config = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle_config.get('nextRacesComponentEnabled'):
            raise CmsClientException('Next Races component disabled in CMS')
        self.__class__.next_races_selections_number = self.get_next_races_selections_number_from_cms()

        event_1 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=2, time_to_start=10, lp=False, sp=True)
        self.__class__.event_id_1 = event_1.event_id
        self.__class__.selection_id_1 = list(event_1.selection_ids.values())

        event_2 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=2, time_to_start=10, lp=False, sp=True)
        self.__class__.event_id_2 = event_1.event_id
        self.__class__.selection_id_2 = list(event_2.selection_ids.values())

        event_3 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=2, time_to_start=10, lp_prices={0: '1/5', 1: '1/17'})
        self.__class__.event_id_3 = event_3.event_id
        self.__class__.selection_id_3 = list(event_3.selection_ids.values())
        self.site.login()
        self.site.wait_content_state(state_name='HomePage')

    def test_001_navigate_to_horse_racinggreyhounds_slphorse_racingfeaturedgreyhound_racingtoday(self):
        """
        DESCRIPTION: Navigate to Horse Racing/Greyhounds SLP
        DESCRIPTION: '/horse-racing/featured'
        DESCRIPTION: '/greyhound-racing/today'
        EXPECTED: Page contains 'Next Races' module with selections
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing', timeout=25)
        sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.next_races_section = sections.get(self.next_races_title, None)
        self.assertTrue(self.next_races_section, msg=f'{self.next_races_title} is not present')

    def test_002_add_2_selections_into_betslip(self):
        """
        DESCRIPTION: Add 2 selections into Betslip
        EXPECTED: * BuildBet requests are sent to BPP
        EXPECTED: * Second request contains bet data regarding the price, status, etc. of both selections
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains added selection is not sent
        EXPECTED: ![](index.php?/attachments/get/113549377)
        EXPECTED: ![](index.php?/attachments/get/113549378)
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1[0], self.selection_id_2[0]))
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip was not opened')
        self.get_build_bet_request_data()

    def test_003_tap_on_the_x_button_in_the_betslip_to_remove_the_selection(self):
        """
        DESCRIPTION: Tap on the 'X' button in the Betslip to remove the selection
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of the remaining selection
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains removed selection is not sent
        EXPECTED: ![](index.php?/attachments/get/113549379)
        EXPECTED: ![](index.php?/attachments/get/113549381)
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        self.stake = list(singles_section.values())[0]
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip was not opened')
        self.stake.remove_button.click()
        self.get_build_bet_request_data()
        self.assertNotIn(self.event_id_1, self.event_ids, msg='removed selection is present in SS request')

    def test_004__close_betslip_open_edp_of_the_event_that_contains_selections_that_have_both_sp_and_lp_values(self):
        """
        DESCRIPTION: * Close Betslip
        DESCRIPTION: * Open EDP of the event that contains selections that have both 'SP' and 'LP' values
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(self.event_id_1, sport_name='greyhound-racing', timeout=15)
        racing_event_tab_content = self.site.greyhound_event_details.tab_content.event_markets_list
        racing_event_tab_content.market_tabs_list.open_tab(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        sections = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg=f'No sections found for racing event tab')
        section_name, section = list(sections.items())[0]
        outcomes = list(section.items_as_ordered_dict.items())
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')

    def test_005_add_selection_that_has_both_sp_and_lp_values_into_betslip_by_tapping_on_it(self):
        """
        DESCRIPTION: Add selection that has both 'SP' and 'LP' values into BetSlip by tapping on it
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of both new and previously added selections
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains added selection is not sent
        EXPECTED: ![](index.php?/attachments/get/112736528)
        EXPECTED: ![](index.php?/attachments/get/112736525)
        """
        self.site.open_betslip()
        self.clear_betslip()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.selection_id_3[0]))

    def test_006__open_betslip_change_selection_type_from_live_price_value_to_sp_within_the_dropdown_of_stake_cell_for_the_step_5_selection(self):
        """
        DESCRIPTION: * Open Betslip
        DESCRIPTION: * Change selection type from Live Price '#value' to 'SP' within the dropdown of stake cell for the step #5 selection
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of both new and previously added selections
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains added selection is not sent
        EXPECTED: ![](index.php?/attachments/get/112736527)
        EXPECTED: ![](index.php?/attachments/get/112736524)
        """
        self.assertTrue(self.site.has_betslip_opened(), msg=f'Betslip was not opened')
        self.get_build_bet_request_data()
        self.assertNotIn(self.event_id_1, self.event_ids, msg=f'Removed selection is present in SS request')
