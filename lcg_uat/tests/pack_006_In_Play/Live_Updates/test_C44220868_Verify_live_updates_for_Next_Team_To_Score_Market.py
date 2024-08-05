import pytest
import json
from tests.base_test import vtest
from tests.Common import Common
from selenium.webdriver.support.ui import Select
from time import sleep
from voltron.pages.shared import get_device


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot suspend selection in OB for prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44220868_Verify_live_updates_for_Next_Team_To_Score_Market(Common):
    """
    TR_ID: C44220868
    NAME: Verify live updates for Next Team To Score Market
    DESCRIPTION: This test case verifies that live updates are received only for Next Team To Score markets that are visible on UI
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose any Sport
    PRECONDITIONS: 3. Select Football sport on Sports Ribbon
    PRECONDITIONS: 4. Select 'Next Team to Score' in Market selector
    PRECONDITIONS: 4. Make sure that there is event with primary market and few markets created by template 'Next Team to Score',  attributes is_off = 'Y' and Bet In Running (event attribute isStarted)
    PRECONDITIONS: 5. Open Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket
    PRECONDITIONS: 6. Open OB TI tool
    PRECONDITIONS: Note:
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: OB TI:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True
    market_name_lowest_order = 'Next Team to Score'
    market_name_higest_order = 'Both Teams to Score'
    price = '6/4'

    def get_inplay_structure(self, event_id, selection_id, delimiter='42'):
        sleep(8)
        logs = get_device().get_performance_log(preserve=False)
        for entry in logs[::-1]:
            try:
                payload_data = entry[1]['message']['message']['params']['response']['payloadData']
                if f'{event_id}' in payload_data and 'publishedDate' in payload_data and f'{selection_id}' in payload_data:
                    message = payload_data.split(str(delimiter), maxsplit=1)[1]
                    return json.loads(message)[1]
            except KeyError:
                continue
        return {}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events with primary market and few markets created by template 'Next Team to Score',  attributes is_off = 'Y' and Bet In Running (event attribute isStarted)
        """
        markets = [('both_teams_to_score',), ('next_team_to_score',)]
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, markets=markets)
        self.__class__.event_id = event_params.event_id
        self.__class__.selection_id = event_params.selection_ids['next_team_to_score']['Draw']
        self.__class__.eventName = event_params.ss_response['event']['name']

    def test_001_in_timake_price_updatessuspension_for_selection_from_market_next_team_to_score_with_the_lowest_displayordernote_this_market_is_displayed_on_in_play_page(self):
        """
        DESCRIPTION: In TI:
        DESCRIPTION: Make price updates/suspension for selection from market 'Next Team to Score' with the lowest displayOrder
        DESCRIPTION: NOTE: this market is displayed on In Play page
        EXPECTED: Changes are saved
        """
        self.navigate_to_page('in-play/football')
        self.site.wait_content_state_changed(timeout=15)
        if self.device_type == 'desktop' and self.brand == 'bma':
            select = Select(self.site.football.tab_content.market_selector_element)
            select.select_by_visible_text(self.market_name_lowest_order)
        else:
            self.site.football.tab_content.dropdown_market_selector.select_value(self.market_name_lowest_order)
        if self.device_type not in ['mobile', 'tablet']:
            grouping_buttons = self.site.inplay.tab_content
            self.assertTrue(grouping_buttons,
                            msg=f'"Live" events are not available in inplay tab for sport ""')
            actual_sport_type = grouping_buttons.accordions_list.items_as_ordered_dict['AUTO TEST - AUTOTEST PREMIER LEAGUE']
        else:
            self.site.wait_content_state_changed(timeout=5)
            grouping_buttons = self.site.inplay.tab_content.live_now
            self.assertTrue(grouping_buttons, msg=f'"Live" events are not available in inplay tab for sport "')
            actual_sport_type = grouping_buttons.items_as_ordered_dict['AUTOTEST PREMIER LEAGUE']
        events = list(actual_sport_type.items_names)
        self.assertTrue(self.eventName in events,
                        msg=f'Expected event:"{self.eventName}" is not in Actual events: "{events}"')
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=False, active=False)
        sleep(7)

    def test_002_in_appcheck_updates_are_received_in_web_sockets___eio3transportwebsocket(self):
        """
        DESCRIPTION: In App:
        DESCRIPTION: Check Updates are received in Web Sockets -> ?EIO=3&transport=websocket
        EXPECTED: Price updates/suspension are received
        """
        self.site.wait_content_state_changed(timeout=9)
        sleep(7)
        response = self.get_inplay_structure(event_id=self.event_id, selection_id=self.selection_id)
        status = response['event']['market']['outcome']['displayed']
        self.assertEqual(status, 'N', msg=f'Actual status "{status}" is not equal to expected status "N" '
                                          f'for event: "{self.event_id}-{self.eventName}"')

    def test_003_verify_updates_are_displayed_for_event(self):
        """
        DESCRIPTION: Verify updates are displayed for event
        EXPECTED: * If price update was received, new price is displayed within Odds button
        EXPECTED: * If suspension was received, Odds button is disabled
        """
        if self.device_type not in ['mobile', 'tablet']:
            grouping_buttons = self.site.inplay.tab_content
            self.assertTrue(grouping_buttons,
                            msg=f'"Live" events are not available in inplay tab for sport ""')
            actual_sport_type = grouping_buttons.accordions_list.items_as_ordered_dict['AUTO TEST - AUTOTEST PREMIER LEAGUE']
        else:
            self.site.wait_content_state_changed(timeout=5)
            grouping_buttons = self.site.inplay.tab_content.live_now
            self.assertTrue(grouping_buttons, msg=f'"Live" events are not available in inplay tab for sport "')
            actual_sport_type = grouping_buttons.items_as_ordered_dict['AUTOTEST PREMIER LEAGUE']
        events = actual_sport_type.items_as_ordered_dict[self.eventName]
        prices = events.template.items_names
        self.assertTrue(self.price not in prices,
                        msg=f'Expected price:"{self.price}" is in Actual prices: "{prices}"'
                            f'for event: "{self.event_id}-{self.eventName}"')

    def test_004_in_timake_price_updatessuspension_for_selection_from_market_next_team_to_score_with_the_highest_or_higher_displayordernote_this_market_is_not_displayed_on_in_play_page(self):
        """
        DESCRIPTION: In TI:
        DESCRIPTION: Make price updates/suspension for selection from market 'Next Team to Score' with the highest or higher displayOrder
        DESCRIPTION: NOTE: this market is not displayed on In Play page
        EXPECTED: Changes are saved
        """
        self.navigate_to_page('in-play/football')
        self.site.wait_content_state_changed(timeout=15)
        if self.device_type == 'desktop' and self.brand == 'bma':
            select = Select(self.site.football.tab_content.market_selector_element)
            select.select_by_visible_text(self.market_name_higest_order)
        else:
            self.site.football.tab_content.dropdown_market_selector.select_value(self.market_name_higest_order)
        self.site.wait_content_state_changed(timeout=4)
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=False, active=False)

    def test_005_in_appcheck_updates_are_not_received_in_web_sockets___eio3transportwebsocket(self):
        """
        DESCRIPTION: In App:
        DESCRIPTION: Check Updates are not received in Web Sockets -> ?EIO=3&transport=websocket
        EXPECTED: Price updates/suspension are NOT received
        """
        response = self.get_inplay_structure(event_id=self.event_id, selection_id=self.selection_id)
        self.assertFalse(response, msg='Price updates/suspension are received '
                                       f'for event: "{self.event_id}-{self.eventName}"')
