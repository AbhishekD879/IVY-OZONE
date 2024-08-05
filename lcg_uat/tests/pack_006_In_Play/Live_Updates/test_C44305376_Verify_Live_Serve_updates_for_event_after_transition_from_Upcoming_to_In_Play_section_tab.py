import pytest
import json
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.pages.shared import get_device
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot make upcoming event to inplay event in OB
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44305376_Verify_Live_Serve_updates_for_event_after_transition_from_Upcoming_to_In_Play_section_tab(Common):
    """
    TR_ID: C44305376
    NAME: Verify Live Serve updates for event after transition from 'Upcoming' to  'In-Play' section/tab
    DESCRIPTION: This case verifies subscription to Live Serve updates for event after transition from 'Upcoming' to  'In-Play' section/tab without refresh
    PRECONDITIONS: * Load Oxygen app
    PRECONDITIONS: * Navigate to 'In-Play' page from the Sports Menu Ribbon Mobile/Tablet or 'Main Navigation' menu at the 'Universal Header' (**Desktop**) and choose any Sport
    PRECONDITIONS: * Make sure that Live events are present in 'Live Now' section Mobile/Tablet or when 'Live Now' switcher is selected Desktop
    PRECONDITIONS: *To reach upcoming events scroll the page down to 'Upcoming' section Mobile/Tablet or select 'Upcoming' switcher Desktop
    PRECONDITIONS: Note! To check Live Serv notifications open Dev tools -> Network tab -> WS tab -> Frames section -> choose ?EIO=3&transport=websocket record
    """
    keep_browser_open = True

    def get_inplay_structure(self, event_id, delimiter='42', subscribe=True):
        logs = get_device().get_performance_log()
        for entry in logs[::-1]:
            try:
                payload_data = entry[1]['message']['message']['params']['response']['payloadData']
                if subscribe:
                    if f'{event_id}' in payload_data and 'subscribe' in payload_data:
                        message = payload_data.split(str(delimiter), maxsplit=1)[1]
                        return json.loads(message)[1]
                else:
                    if f'{event_id}' in payload_data and 'publishedDate' in payload_data:
                        message = payload_data.split(str(delimiter), maxsplit=1)[1]
                        return json.loads(message)[1]
            except KeyError:
                continue
        return {}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create upcoming event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True)
        self.__class__.eventID = event_params.event_id
        self.__class__.market_id = event_params.default_market_id
        self.navigate_to_page('in-play/football')
        self.site.wait_content_state_changed()

    def test_001_for_any_upcoming_event_verify_subscription_to_liveserv_updates(self):
        """
        DESCRIPTION: For any Upcoming event verify subscription to LiveServ updates
        EXPECTED: Subscription is present in EIO=3&transport=websocket record
        """
        if self.device_type not in ['mobile', 'tablet']:
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
            grouping_buttons = self.site.inplay.tab_content
            self.assertTrue(grouping_buttons,
                            msg=f'"Upcoming" events are not available in inplay tab for football')
            sport = list(grouping_buttons.accordions_list.items_as_ordered_dict.values())
        else:
            grouping_buttons = self.site.inplay.tab_content.upcoming
            self.assertTrue(grouping_buttons, msg=f'"Upcoming" events are not available in inplay tab for football')
            sport = list(grouping_buttons.items_as_ordered_dict.values())
        sport[0].click()
        sleep(7)
        response = self.get_inplay_structure(event_id=self.eventID)
        self.assertTrue(response, msg='Subscription is not present in inplay football page')

    def test_002_update_any_marketselection_for_the_event_in_step_1_eg_price_change_suspend(self):
        """
        DESCRIPTION: Update any market/selection for the event in Step 1 (e.g. price change, suspend)
        EXPECTED: Update is received in WS: 42["eventID",{"publishedDate":<date>,"type":<type>
        EXPECTED: * for market: type: "EVMKT"
        EXPECTED: * for event: type: "EVENT"
        EXPECTED: * for selection: type: "SELCN"
        EXPECTED: * for price: type: "PRICE"
        """
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.market_id,
                                           displayed=False,
                                           active=False)
        sleep(10)
        response = self.get_inplay_structure(event_id=self.eventID, subscribe=False)
        self.assertEqual(response['type'], "EVMKT", msg='Response is not equal for Update is received in WS'
                                                        f'"Actual :"{response["type"]}" Expected:  "EVMKT" ')
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.market_id,
                                           displayed=True,
                                           active=True)

    def test_003_modify_event_to_be_defined_by_attributes_is_off__y_and_event_attribute_isstarted(self):
        """
        DESCRIPTION: Modify event to be defined by attributes is_off = 'Y' and event attribute isStarted
        EXPECTED: * Event disappears from 'Upcoming' section
        EXPECTED: * Event is displayed in 'In-Play' section
        """
        self.ob_config.make_event_live(market_id=self.market_id, event_id=self.eventID)
        sleep(7)
        response = self.get_inplay_structure(event_id=self.eventID)
        self.assertTrue(response, msg='Subscription is not present in inplay football page live section')
        sleep(7)
        response1 = self.get_inplay_structure(event_id=self.eventID, subscribe=False)
        self.assertEqual('Y', response1['event']['is_off'], msg=f'Event not present in live now section actual event "Y"'
                                                                f'expected event list "{response1["event"]["is_off"]}"')

    def test_004_for_the_event_which_transited_from_upcoming_to_in_play_verify_subscription_to_liveserv_updatesnote_event_should_be_visible_in_expanded_section_to_get_liveserv_updates(self):
        """
        DESCRIPTION: For the event which transited from 'Upcoming' to 'In-Play' verify subscription to LiveServ updates
        DESCRIPTION: NOTE: Event should be visible (in expanded section) to get LiveServ updates
        EXPECTED: Subscription is present in EIO=3&transport=websocket record
        """
        # covered in step 3

    def test_005_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: Result is the same
        """
        self.test_002_update_any_marketselection_for_the_event_in_step_1_eg_price_change_suspend()

    def test_006_repeat_steps_1_5_for_the_following_sections_home_page__in_play_tab_mobiletablet_sports_landing_page__in_play_tab_desktop_home_page_for_in_play__live_stream_section_for_both_switchers(self):
        """
        DESCRIPTION: Repeat steps 1-5 for the following sections:
        DESCRIPTION: * Home page > 'In-Play' tab Mobile/Tablet
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        DESCRIPTION: * [Desktop] Home page for 'In-play & Live Stream' section for both switchers
        """
        # This step is not applicable for In-play& live stream as we are not converting upcoming event to live event
        if self.device_type == 'mobile':
            event_params = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, perform_stream=True)
            self.__class__.eventID = event_params.event_id
            self.__class__.market_id = event_params.default_market_id
            self.navigate_to_page('/home/in-play')
            self.site.wait_content_state_changed(timeout=10)
            self.site.home.tabs_menu.click_button('IN-PLAY')
            self.site.wait_content_state_changed(timeout=10)
            grouping_buttons = self.site.home.tab_content.upcoming
            self.assertTrue(grouping_buttons, msg='"Upcoming" events are not available in inplay tab')
            inplay_list_upcoming = list(grouping_buttons.items_as_ordered_dict.values())
            inplay_list_upcoming[0].click()
            sleep(7)
            response = self.get_inplay_structure(event_id=self.eventID)
            self.assertTrue(response, msg='Subscription is not present in home page inplay tab football sport')
            self.test_002_update_any_marketselection_for_the_event_in_step_1_eg_price_change_suspend()
            self.test_003_modify_event_to_be_defined_by_attributes_is_off__y_and_event_attribute_isstarted()
            self.test_005_repeat_step_2()
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, perform_stream=True)
        self.__class__.eventID = event_params.event_id
        self.__class__.market_id = event_params.default_market_id
        self.navigate_to_page('sport/football/live')
        self.site.wait_content_state_changed(timeout=30)
        if self.device_type not in ['mobile', 'tablet']:
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
        sleep(10)
        response = self.get_inplay_structure(event_id=self.eventID)
        self.assertTrue(response, msg='Subscription is not present in SLP inplay tab football page')
        self.test_002_update_any_marketselection_for_the_event_in_step_1_eg_price_change_suspend()
        self.test_003_modify_event_to_be_defined_by_attributes_is_off__y_and_event_attribute_isstarted()
        self.test_005_repeat_step_2()
