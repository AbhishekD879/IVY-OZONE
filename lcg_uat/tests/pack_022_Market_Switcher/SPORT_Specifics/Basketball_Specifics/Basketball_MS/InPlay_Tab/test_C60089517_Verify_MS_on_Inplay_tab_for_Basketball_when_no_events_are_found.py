import pytest
import tests

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.environments import constants as vec
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot be created in Prod/Beta
@pytest.mark.market_switcher_no_events
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C60089517_Verify_MS_on_Inplay_tab_for_Basketball_when_no_events_are_found(BaseSportTest):
    """
    TR_ID: C60089517
    NAME: Verify MS on Inplay tab for Basketball when no events are found
    DESCRIPTION: This test case verifies 'Market Selector' drop down in Basketball on in-Play page when no events are found
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: No Live events are configured for BasketBall on Inplay Tab
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Basketball ->Inplay Tab and Inplay from (Desktop - Inplay tab(Sub header menu) -> Basketball) and in Mobile (Inplay (Sports ribbon menu) ->Basketball)
    """
    keep_browser_open = True
    live_now_switcher = vec.inplay.LIVE_NOW_SWITCHER.upper()
    all_events = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Suspend all inplay events
        """
        category_id = self.ob_config.backend.ti.basketball.category_id
        class_ids = self.get_class_ids_for_category(category_id=category_id)
        live_events = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_LIVE_NOW_EVENT, OPERATORS.IS_TRUE))

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=category_id)
        self.all_events.extend(ss_req.ss_event_to_outcome_for_class(query_builder=live_events, class_id=class_ids))

        for event in self.all_events:
            self.ob_config.change_event_state(event_id=event['event']['id'])

    def test_001_navigate_to_basketball_and_click_on_inplay(self):
        """
        DESCRIPTION: Verify market selector toggle in CMS
        EXPECTED: Market selector is enabled in CMS
        DESCRIPTION: Navigate to Basketball and click on Inplay
        EXPECTED: Inplay page is loaded
        """
        all_sport_MS_Status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                       status=True)
        self.assertTrue(all_sport_MS_Status, msg='Market switcher is disabled for all sport')
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='basketball',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for basketball sport')
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        expected_tab = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play
        self.site.basketball.tabs_menu.click_button(self.expected_sport_tabs.in_play)
        expected_tab_name = self.get_sport_tab_name(expected_tab, self.ob_config.basketball_config.category_id)
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')

    def test_002_verify_displaying_of_market_selector(self):
        """
        DESCRIPTION: Verify displaying of Market Selector
        EXPECTED: • Market Selector dropdown should not be displayed with Arrow pointing downwards
        EXPECTED: • 'There are currently no Live events available' message should be displayed
        """
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(self.live_now_switcher)
            actual_btn = self.site.inplay.tab_content.grouping_buttons.current
            self.assertEqual(actual_btn, self.live_now_switcher, msg=f'"{self.live_now_switcher}" is not selected')
        inplay_tab_content = self.site.inplay.tab_content
        self.assertTrue(inplay_tab_content.has_no_events_label(),
                        msg=f'"There are currently no Live events available" message not displayed')
        self.assertFalse(inplay_tab_content.has_dropdown_market_selector(),
                         msg='"Market Selector" drop-down is displayed on basketball Inplay tab')

    @classmethod
    def custom_tearDown(cls):
        ob_config = cls.get_ob_config()
        for event in cls.all_events:
            ob_config.change_event_state(event_id=event['event']['id'], displayed=True, active=True)
