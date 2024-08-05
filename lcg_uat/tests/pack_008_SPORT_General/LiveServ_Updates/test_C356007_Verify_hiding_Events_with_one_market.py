import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.desktop
@pytest.mark.market_selector
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.slow
@pytest.mark.timeout(800)
@pytest.mark.sports
@pytest.mark.safari
@vtest
class Test_C356007_Verify_hiding_Events_with_one_market_depending_on_Displayed_attribute_for_selections(BaseSportTest):
    """
    TR_ID: C356007
    NAME: Verify hiding Events with one market depending on 'Displayed' attribute for selections
    DESCRIPTION: This test case verifies hiding Events with one market depending on 'Displayed' attribute for selections
    PRECONDITIONS: 1. To display/undisplay event/market/selection use http://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. **Updates are received via push notifications**: Dev tools > Network> XHR
    PRECONDITIONS: 3. Create event that has only ONE market
    """
    keep_browser_open = True
    market = vec.siteserve.EXPECTED_MARKETS_NAMES.to_qualify

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football event
        EXPECTED: * Football landing page is opened
        """
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper() if \
            (self.device_type == 'desktop' and self.brand == 'ladbrokes') else vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default
        event_params = self.ob_config.add_football_event_to_special_league(markets=[('to_qualify', {'cashout': True})])
        self.ob_config.add_football_event_to_special_league(markets=[('to_qualify', {'cashout': True})])
        self.__class__.selection_ids = event_params.selection_ids

        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.event_name}"')

        market_short_name = self.ob_config.football_config. \
            autotest_class.special_autotest_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.ob_config.market_ids[self.eventID][market_short_name],
                                           displayed=False, active=True)

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

    def test_001_tap_football_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        EXPECTED: * Football landing page is opened
        EXPECTED: * Match Result value is selected by default in the Market Selector
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')

    def test_002_choose_market_from_preconditions_in_the_market_selector_and_check_that_event_is_present(self):
        """
        DESCRIPTION: Verify all events are present
        DESCRIPTION: Choose market from Preconditions in the Market Selector and make sure that only ONE event with particular market is available on the page
        EXPECTED: * Selected Market is displayed in Market selector
        EXPECTED: * Only ONE event is displayed for selected market
        """
        market_selector = self.site.football.tab_content.dropdown_market_selector
        market_selector.scroll_to()
        selected_market = market_selector.selected_market_selector_item
        self.assertEqual(selected_market, self.market_selector_default_value,
                         msg=f'Default market name from market selector "{selected_market}" '
                         f'is not the same as expected "{self.market_selector_default_value}"')

        market_selector.items_as_ordered_dict[self.market].click()
        expected_market = vec.siteserve.EXPECTED_MARKETS_NAMES.to_qualify.upper() if \
            (self.device_type == 'desktop' and self.brand == 'ladbrokes') else vec.siteserve.EXPECTED_MARKETS_NAMES.to_qualify
        result = wait_for_result(lambda: self.site.football.tab_content.dropdown_market_selector.selected_market_selector_item == expected_market,
                                 name='Market being selected', timeout=5)

        selected_market = self.site.football.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertTrue(result, msg=f'Market name from market selector "{selected_market}" '
                                    f'is not the same as expected "{expected_market}"')

        event = self.get_event_from_league(section_name=self.section_name, event_id=self.eventID)
        self.assertTrue(event, msg=f'Event "{self.event_name}" is not found in "{self.section_name}"')
        self.site.football.tab_content.dropdown_market_selector.collapse()

    def test_003_in_ti_tool_undisplay_selections_for_the_event_from_preconditions_and_save_changes(self):
        """
        DESCRIPTION: In TI tool undisplay selections for the event from preconditions and save changes
        EXPECTED: Changes are saved successfully
        """
        for market, market_selections in self.selection_ids.items():
            for selection_name, selection_id in market_selections.items():
                self.ob_config.change_selection_state(selection_id=selection_id, displayed=False, active=True)

    def test_004_go_to_oxygen_application_and_verify_that_event_disappears_and_information_received_in_push(self):
        """
        DESCRIPTION: Go to Oxygen application and verify that event disappears and information received in push
        EXPECTED: * displayed:"N" attribute is received in push
        EXPECTED: * event stops to display on the page in real time
        """
        self.device.refresh_page()
        self.site.wait_content_state_changed()
        if self.get_section(self.section_name) is not None:
            is_event_present = wait_for_result(lambda: self.get_event_from_league(section_name=self.section_name,
                                                                                  event_id=self.eventID,
                                                                                  raise_exceptions=False) is None,
                                               name=f'Event "{self.event_name}" to disappear',
                                               timeout=10)
            self.assertTrue(is_event_present,
                            msg=f'Event "{self.event_name}" is still displayed in section "{self.section_name}"')

    def test_005_verify_market_selector(self):
        """
        DESCRIPTION: Verify Market Selector
        EXPECTED: * Chosen market stops to display within the Market selector
        EXPECTED: * Default value starts to display within the Market selector
        EXPECTED: * Events for default market starts to display on the page
        """
        selected_market = self.site.football.tab_content.dropdown_market_selector.selected_market_selector_item
        if selected_market == self.market:
            pass
        else:
            wait_for_result(lambda: self.market_selector_default_value in selected_market, timeout=1)
            sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='Can not find any section')
            section = next((iter(sections.values())))
            events = section.items_as_ordered_dict
            self.assertTrue(events, msg=f'Can not find any events in "{self.market_selector_default_value}"')

    def test_006_in_ti_tool_display_selections_for_the_event_from_preconditions_and_save_changes(self):
        """
        DESCRIPTION: In TI tool display selections for the event from preconditions and save changes
        EXPECTED: Changes are saved successfully
        """
        for market, market_selections in self.selection_ids.items():
            for selection_name, selection_id in market_selections.items():
                self.ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=True)

    def test_007_go_to_oxygen_application_and_verify_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: Go to Oxygen application and verify event displaying and information received in push
        EXPECTED: * displayed:"Y" attribute is received in push
        EXPECTED: * event does NOT start to display in real time
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        if self.get_section(self.section_name) is not None:
            is_event_present = wait_for_result(lambda: self.get_event_from_league(section_name=self.section_name,
                                                                                  event_id=self.eventID,
                                                                                  raise_exceptions=False) is None,
                                               name=f'Event "{self.event_name}" to disappear',
                                               timeout=10)
            self.assertTrue(is_event_present,
                            msg=f'Event "{self.event_name}" is still displayed in section "{self.section_name}"')

    def test_008_refresh_the_page_and_verify_the_event_displaying(self):
        """
        DESCRIPTION: Refresh the page and verify the event displaying
        EXPECTED: Event starts to display on the page
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.test_002_choose_market_from_preconditions_in_the_market_selector_and_check_that_event_is_present()

    def test_009_verify_market_selector(self):
        """
        DESCRIPTION: Verify Market Selector
        EXPECTED: Market for event from the previous steps is visible within Market Selector
        """
        # verified in step test_002_choose_market_from_preconditions
