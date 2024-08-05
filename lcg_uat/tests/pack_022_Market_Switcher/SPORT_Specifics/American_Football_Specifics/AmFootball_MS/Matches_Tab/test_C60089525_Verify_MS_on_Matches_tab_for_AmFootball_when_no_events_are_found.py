import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_ob_client.utils.date_time import get_date_time_as_string


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.market_switcher_no_events
@vtest
class Test_C60089525_Verify_MS_on_Matches_tab_for_AmFootball_when_no_events_are_found(Common):
    """
    TR_ID: C60089525
    NAME: Verify MS on Matches tab for Am.Football when no events are found
    DESCRIPTION: This test case verifies 'Market Selector' drop down in American Football on Matches page when no events are found
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: No events are configured for Am football on Matches Tab
    """
    keep_browser_open = True
    all_events = []
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Suspend all the events
        """
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        category_id = self.ob_config.backend.ti.american_football.category_id
        class_ids = self.get_class_ids_for_category(category_id=category_id)
        start_date = f'{get_date_time_as_string(days=0)}T00:00:00.000Z'
        events = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, str(category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      start_date))
        live_events = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_LIVE_NOW_EVENT, OPERATORS.IS_TRUE))

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=category_id)
        self.all_events.extend(ss_req.ss_event_to_outcome_for_class(query_builder=events, class_id=class_ids))
        self.all_events.extend(ss_req.ss_event_to_outcome_for_class(query_builder=live_events, class_id=class_ids))

        for event in self.all_events:
            self.ob_config.change_event_state(event_id=event['event']['id'])

    def test_001_navigate_to_american_football(self):
        """
        DESCRIPTION: Navigate to American Football
        EXPECTED: Matches Tab is displayed by default
        """
        if self.brand == 'bma':
            self.__class__.days_list = [vec.sb.TABS_NAME_TODAY.upper(),
                                        vec.sb.TABS_NAME_TOMORROW.upper(),
                                        vec.sb.TABS_NAME_FUTURE.upper()]
        else:
            self.__class__.days_list = [vec.sb.TABS_NAME_TODAY.title(),
                                        vec.sb.TABS_NAME_TOMORROW.title(),
                                        vec.sb.TABS_NAME_FUTURE.title()]
        self.navigate_to_page(name='sport/american-football')
        self.site.wait_content_state('american-football')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.american_football_config.category_id)
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')

    def test_002_verify_displaying_of_market_selectortoday_tab(self):
        """
        DESCRIPTION: Verify displaying of Market Selector(Today Tab)
        EXPECTED: • Market Selector dropdown should not be displayed
        EXPECTED: • 'No events found' message should be displayed
        """
        market_switcher = self.site.american_football.tab_content.has_dropdown_market_selector()
        self.assertFalse(market_switcher, msg='"Market Selector dropdown" is displaying for american football')
        no_events = self.site.american_football.tab_content.has_no_events_label()
        self.assertTrue(no_events, msg=f'"{vec.SB.NO_EVENTS_FOUND}" message is not displayed')

    def test_003_repeat_step2_for_tomorrow_and_future_tab_steps_12_and_3_are_applicable_for_desktop(self):
        """
        DESCRIPTION: Repeat Step2 for Tomorrow and Future Tab (Steps 1,2 and 3 are applicable for desktop)
        """
        self.site.american_football.tab_content.grouping_buttons.items_as_ordered_dict.get(self.days_list[1]).click()
        self.test_002_verify_displaying_of_market_selectortoday_tab()
        self.site.american_football.tab_content.grouping_buttons.items_as_ordered_dict.get(self.days_list[2]).click()
        self.test_002_verify_displaying_of_market_selectortoday_tab()

    def test_004_verify_matches_tab_in_mobile(self):
        """
        DESCRIPTION: Verify Matches Tab in Mobile
        EXPECTED: Matches Tab should not display when there are no events
        """
        # not navigating to SLP when there are no events available (in Mobile)

    @classmethod
    def custom_tearDown(cls):
        ob_config = cls.get_ob_config()
        for event in cls.all_events:
            ob_config.change_event_state(event_id=event['event']['id'], displayed=True, active=True)
