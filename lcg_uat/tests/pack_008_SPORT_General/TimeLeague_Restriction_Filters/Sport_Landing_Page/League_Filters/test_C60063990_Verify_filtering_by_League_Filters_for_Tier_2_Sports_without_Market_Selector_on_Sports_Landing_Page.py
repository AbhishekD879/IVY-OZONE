import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.time_league_filters_negative
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C60063990_Verify_filtering_by_League_Filters_for_Tier_2_Sports_without_Market_Selector_on_Sports_Landing_Page(Common):
    """
    TR_ID: C60063990
    NAME: Verify filtering by League Filters for Tier 2 Sports without Market Selector on Sports Landing Page
    DESCRIPTION: This Test Case verifies filtering by League Filters for Tier 2 Sports without Market Selector on Sports Landing Page
    PRECONDITIONS: * 'Enabled League Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * The following League Filters are configured in CMS: 'Top Leagues' (with a few valid leagues), 'Test League' (with only one valid league), 'Invalid League' (with an invalid league or with league without available events) (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
    PRECONDITIONS: Notes:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
    PRECONDITIONS: Designs for filters:
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e718f6c5d6903075e47d8 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e71ac900a50b2123a003b - Ladbrokes
    PRECONDITIONS: **League Filters are available for Desktop only on Today Tab**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page (market selector should be absent for this sport), e.g. Cricket
    """
    keep_browser_open = True

    def verify_selected_filters(self, expected_filters):
        sleep(1.5)
        active_filters = self.timeline_filters.selected_filters
        self.assertEqual(list(active_filters.keys()), expected_filters,
                         msg=f'"selected time filter {list(active_filters.keys())} "'
                             f'does not match expected time filter "{expected_filters}"')

    def verify_event_sort_time(self):
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values()
        if len(sections) > 0:
            for section in sections:
                if not section.is_expanded():
                    section.expand()
                meetings = list(section.items_as_ordered_dict.values())
                self.assertTrue(meetings, msg='No meetings was found on page')
                actual_time_list = []
                for event_data in meetings:
                    if event_data.is_live_now_event:
                        continue
                    else:
                        time = event_data.event_time.split(",")[0]
                        actual_time_list.append(time)
                expected_sort_list = sorted(actual_time_list)
                self.assertEqual(sorted(actual_time_list), expected_sort_list,
                                 msg=f'Actual text: "{actual_time_list}" is not equal with the'
                                     f'Expected text: "{expected_sort_list}"')
        else:
            no_events = self.site.sports_page.tab_content.has_no_events_label()
            self.assertTrue(no_events, msg=' "No Events Found" msg not displayed')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: * 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Matches)
        PRECONDITIONS: * The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages > Sport Categories > Sport > Matches)
        PRECONDITIONS: * The following League Filters are configured in CMS: 'Top Leagues' (with a few valid leagues), 'Test League' (with only one valid league), 'Invalid League' (with an invalid league or with league without available events) (Sports Pages > Sport Categories > Sport > Matches)
        PRECONDITIONS: * Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
        PRECONDITIONS: **Time Filters are available for Desktop only up to 12 hours and only on Today Tab**
        PRECONDITIONS: **League Filters are available for Desktop only on Today Tab**
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Navigate to Sports Landing page (Today tab)
        """
        self.cms_config.verify_and_update_market_switcher_status(sport_name='cricket', status=False)
        self.cms_config.update_sports_event_filters(tab_name='matches', sport_id=10, enabled=True, top_league_ids='29147',
                                                    test_league_ids='85404', invalid_league_ids='1234', league_enabled=True,
                                                    league_required=True, event_filters_values=[1, 3, 6, 12, 24, 48])
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=2))
            self.ob_config.add_autotest_cricket_event(start_time=self.get_date_time_formatted_string(hours=4))
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state(state_name='Cricket')

    def test_001_select_some_league_filter_eg_top_leagues(self):
        """
        DESCRIPTION: Select some League Filter (e.g. 'Top Leagues')
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        self.__class__.timeline_filters = self.site.cricket.tab_content.timeline_filters
        self.__class__.leagues_and_times = self.timeline_filters.items_as_ordered_dict
        self.__class__.top_leagues = self.leagues_and_times.get('Top Leagues')
        self.top_leagues.click()
        self.verify_selected_filters(expected_filters=['Top Leagues'])
        self.verify_event_sort_time()

    def test_002_click_on_the_selected_league_filter(self):
        """
        DESCRIPTION: Click on the selected League Filter
        EXPECTED: * Any League Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        self.top_leagues.click()
        sleep(1.5)
        active_filters = self.timeline_filters.selected_filters
        self.assertFalse(active_filters, msg='Filters are selected')
        self.verify_event_sort_time()

    def test_003_select_some_league_filter_eg_test_league(self):
        """
        DESCRIPTION: Select some League Filter (e.g. 'Test League')
        EXPECTED: * Selected League Filter is highlighted
        EXPECTED: * Page loads only events that are in line to selected League Filter for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        self.leagues_and_times.get('Test Leagues').click()
        self.verify_selected_filters(expected_filters=['Test Leagues'])
        self.verify_event_sort_time()

    def test_004_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Any League Filter is not highlighted
        EXPECTED: * Page loads all events
        EXPECTED: * Events are sorted by Start Time
        """
        self.device.refresh_page()
        active_filters = self.site.cricket.tab_content.timeline_filters.selected_filters
        self.assertFalse(active_filters, msg='Filters are selected even after page refresh')
        self.verify_event_sort_time()
