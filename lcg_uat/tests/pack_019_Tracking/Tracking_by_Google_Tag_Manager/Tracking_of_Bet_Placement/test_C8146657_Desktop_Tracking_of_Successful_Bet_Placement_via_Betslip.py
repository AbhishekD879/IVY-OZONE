import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.pages.shared.components.base import ComponentBase
from time import sleep
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.reg157_fix
@vtest
class Test_C8146657_Desktop_Tracking_of_Successful_Bet_Placement_via_Betslip(BaseDataLayerTest, BaseBetSlipTest,
                                                                             ComponentBase):
    """
    TR_ID: C8146657
    NAME: Desktop. Tracking of Successful Bet Placement via Betslip
    DESCRIPTION: This test case verify tracking of successful bet placement on Desktop
    PRECONDITIONS: * App is loaded
    PRECONDITIONS: * Quick Bet functionality is disabled in CMS or user`s settings
    PRECONDITIONS: * User is logged out
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    actual_response = {}
    expected_response_football = {'event': 'trackEvent',
                                  'eventAction': 'place bet',
                                  'eventCategory': 'betslip',
                                  'eventLabel': "success",
                                  'location': "/sport/football"
                                  }

    expected_response_home = {'event': 'trackEvent',
                              'eventAction': 'place bet',
                              'eventCategory': 'betslip',
                              'eventLabel': "success",
                              'location': "/"
                              }

    def add_selection_and_check_bet_receipt(self):
        bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(bet_buttons_list, msg='No bet buttons on Home Page')
        length = len(bet_buttons_list)
        for index in range(length):
            bet_btn = bet_buttons_list[index]
            self.scroll_to_we(bet_btn)
            if bet_btn.is_enabled():
                try:
                    bet_btn.click()
                except:
                    continue
                self.place_single_bet()
                try:
                    if self.get_betslip_content().has_bet_now_button():
                        if 'ACCEPT' in self.get_betslip_content().bet_now_button.name:
                            self.get_betslip_content().bet_now_button.click()
                except VoltronException:
                    pass
                break
        self.check_bet_receipt_is_displayed()

    def verify_dataLayer_actual_and_expected_values(self, actual_response, expected_response):
        self.assertEqual(expected_response.get("eventAction"), actual_response.get("eventAction"),
                         msg=f'Expected eventAction value "{expected_response.get("eventAction")}" is not '
                             f'same as actual eventAction value "{actual_response.get("eventAction")}"')
        self.assertEqual(expected_response.get("event"), actual_response.get("event"),
                         msg=f'Expected event value "{expected_response.get("event")}" is not '
                             f'same as actual event value "{actual_response.get("event")}"')
        self.assertEqual(expected_response.get("eventCategory"), actual_response.get("eventCategory"),
                         msg=f'Expected eventCategory value "{expected_response.get("eventCategory")}" is not '
                             f'same as actual eventCategory value "{actual_response.get("eventCategory")}"')
        self.assertEqual(expected_response.get("eventLabel"), actual_response.get("eventLabel"),
                         msg=f'Expected eventLabel value "{expected_response.get("eventLabel")}" is not '
                             f'same as actual eventLabel value "{actual_response.get("eventLabel")}"')
        self.assertEqual(expected_response.get("location"), actual_response.get("location"),
                         msg=f'Expected location value "{expected_response.get("location")}" is not '
                             f'same as actual location value "{actual_response.get("location")}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Event creation for QA2
        """
        if tests.settings.backend_env != "prod":
            event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self._logger.info(f'*** Found Football event with selection ids "{event.event_id}"')

    def test_001_add_a_selections_to_betslip_from_home_screen(self):
        """
        DESCRIPTION: Add a selections to Betslip from Home screen
        EXPECTED: Selection(s) is added
        """
        self.site.login(username=tests.settings.betplacement_user)
        if tests.settings.backend_env != "prod":
            inplay_sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            football = inplay_sports.get(vec.inplay.IN_PLAY_FOOTBALL)
            self.assertTrue(football, msg=f'"{vec.inplay.IN_PLAY_FOOTBALL}" not found among "{inplay_sports.keys()}"')
            football.click()
        self.add_selection_and_check_bet_receipt()

    def test_002_enter_the_stake_and_place_a_bettype_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Enter the stake and place a bet
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: Data Layer contains action with the following parameters
        EXPECTED: betID: [ids_of_bets]
        EXPECTED: customerBuilt: "No"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "place bet"
        EXPECTED: eventCategory: "betslip"
        EXPECTED: eventLabel: "success"
        EXPECTED: gtm.uniqueEventId: id
        EXPECTED: location: "/"
        """
        sleep(5)
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='place bet')
        self.verify_dataLayer_actual_and_expected_values(actual_response, expected_response=self.expected_response_home)

    def test_003_navigate_to_different_location_for_ex_footballmatchestodayadd_selections_and_place_bettype_in_console_datalayer_tap_enter_and_check_the_response(
            self):
        """
        DESCRIPTION: Navigate to different location, for ex football/matches/today
        DESCRIPTION: Add selections and place bet
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: Data Layer contains action with the following parameters
        EXPECTED: betID: [bet_id]
        EXPECTED: customerBuilt: "No"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "place bet"
        EXPECTED: eventCategory: "betslip"
        EXPECTED: eventLabel: "success"
        EXPECTED: gtm.uniqueEventId:id
        EXPECTED: location: "/sport/football/matches/today"
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        current_tab_name = self.site.football.tabs_menu.current
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.football_config.category_id)
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Default tab is "{current_tab_name}", instead of "{expected_tab_name}"')
        current_tab_in_matches_tab = self.site.football.date_tab.current
        self.assertEqual(current_tab_in_matches_tab,
                         vec.sb.TODAY.upper() if self.brand == "bma" else vec.sb.TODAY.title(),
                         msg=f'Default tab is "{current_tab_in_matches_tab}", instead of "{expected_tab_name}"')
        self.add_selection_and_check_bet_receipt()
        sleep(5)
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='betslip')
        self.verify_dataLayer_actual_and_expected_values(actual_response,
                                                         expected_response=self.expected_response_football)
