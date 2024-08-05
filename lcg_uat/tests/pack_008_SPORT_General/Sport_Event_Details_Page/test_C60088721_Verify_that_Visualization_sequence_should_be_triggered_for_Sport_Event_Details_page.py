import pytest
from voltron.utils.waiters import wait_for_result
from json import JSONDecodeError
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2
# @pytest.mark.stg2 --Feed for Scoreboards can't be available for QA2/QA3
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
@pytest.mark.reg160_fix
class Test_C60088721_Verify_that_Visualization_sequence_should_be_triggered_for_Sport_Event_Details_page(Common):
    """
    TR_ID: C60088721
    NAME: Verify that  Visualization sequence should be triggered for <Sport>  Event Details page
    DESCRIPTION: Test cases verifies presence of calls for 'bymapping' and 'scoreboard' when user is on <Sport> Event Details page
    PRECONDITIONS: 1) load app
    PRECONDITIONS: 2) navigate to <Sport> landing page
    PRECONDITIONS: 3) <Sport> events are present
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def get_response_url(self, url):
        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_001__navigate_to_tier_1__sport_event_details_pageeg_open_football_event(self):
        """
        DESCRIPTION: * Navigate to 'Tier 1'  <Sport> Event Details Page
        DESCRIPTION: (E.g.: open Football event)
        EXPECTED: * <Sport> Event Details Page is opened
        EXPECTED: * Scoreboard displays
        """
        self.site.login()
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        switchers = self.site.football.tabs_menu.items_as_ordered_dict
        self.assertIn('IN-PLAY', switchers.keys(), msg=f'In Play Switcher not present in the Actual switcers: "{switchers}"')
        switchers.get('IN-PLAY').click()
        no_events = self.site.football.tab_content.has_no_events_label()
        self.assertFalse(no_events, msg='Football live events are not present')

    def test_002__verify_that_there_are_successful__calls_for_bymapping_and_scoreboardegindexphpattachmentsget122251547indexphpattachmentsget122187839(self):
        """
        DESCRIPTION: * Verify that there are successful  calls for 'bymapping' and 'scoreboard'
        DESCRIPTION: E.g.:
        DESCRIPTION: ![](index.php?/attachments/get/122251547)
        DESCRIPTION: ![](index.php?/attachments/get/122187839)
        EXPECTED: * Calls for 'bymapping' and 'scoreboard' are present
        """
        events = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        list(events.values())[0].click()
        self.site.wait_content_state(state_name='EventDetails')
        wait_for_result(lambda: self.get_response_url('/bymapping/'), timeout=10)
        bymapping_call = self.get_response_url('/bymapping/')
        if bymapping_call is None:
            self.device.refresh_page()
            bymapping_call = self.get_response_url('/bymapping/')
        self.assertTrue(bymapping_call, msg='"bymapping call" was not present')
        scoreboard_call = self.get_response_url('/scoreboard')
        if scoreboard_call is None:
            self.device.refresh_page()
            scoreboard_call = self.get_response_url('/scoreboard')
        self.assertTrue(scoreboard_call, msg='"scoreboard call" was not present')

    def test_003__navigate_to_tier_2_sport_event_details_pageeg_cricket_make_sure_that__calls_for_bymapping_and_scoreboard_present(self):
        """
        DESCRIPTION: * Navigate to 'Tier 2' <Sport> Event Details page
        DESCRIPTION: (E.g.: Cricket)
        DESCRIPTION: * Make sure that  calls for 'bymapping' and 'scoreboard' present
        EXPECTED: * Calls for 'bymapping' and 'scoreboard'  are present
        """
        self.navigate_to_page('sport/table-tennis')
        self.site.wait_content_state('table-tennis')
        if self.device_type == "mobile":
            # For tire two sports in-play is present inside matches tab
            current_tab = self.site.sports_page.tabs_menu.current
            expected_tab_name = 'MATCHES'
            self.assertEqual(current_tab.upper(), expected_tab_name, msg=f'Current tab {current_tab.upper()} is not same as Expected tab {expected_tab_name}')
            in_play_module_status = self.site.sports_page.tab_content.has_inplay_module()
            self.assertTrue(bool(in_play_module_status), msg='In-Play Module is not available')
            in_play_module = self.site.sports_page.tab_content.in_play_module
            first_accordion_name, first_accordion = in_play_module.first_item
            event_name, event = first_accordion.first_item
            event.click()
        else:
            switchers = self.site.sports_page.tabs_menu.items_as_ordered_dict
            self.assertIn('IN-PLAY', switchers.keys(),
                          msg=f'In Play Switcher not present in the Actual switcers: "{switchers}"')
            switchers.get('IN-PLAY').click()
            no_events = self.site.sports_page.tab_content.has_no_events_label()
            self.assertFalse(no_events, msg='Table tennis live events are not present')
            accordion_name, accordion = self.site.sports_page.tab_content.accordions_list.first_item
            event_name, event = accordion.first_item
            event.click()
        # waiting for Event-Details page to load
        self.site.wait_content_state(state_name='EventDetails')
        wait_for_result(lambda: self.get_response_url('/bymapping/'), timeout=10)
        bymapping_call = self.get_response_url('/bymapping/')
        if bymapping_call is None:
            self.device.refresh_page()
            bymapping_call = self.get_response_url('/bymapping/')
        self.assertTrue(bymapping_call, msg='"bymapping call" was not present')
        scoreboard_call = self.get_response_url('/scoreboard')
        if scoreboard_call is None:
            self.device.refresh_page()
            scoreboard_call = self.get_response_url('/scoreboard')
        self.assertTrue(scoreboard_call, msg='"scoreboard call" was not present')