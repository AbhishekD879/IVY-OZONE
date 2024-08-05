import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C28832_Verify_Race_Meetings_Order(BaseGreyhound):
    """
    TR_ID: C28832
    NAME: Verify 'Race Meetings' Order
    DESCRIPTION: This test case verifies an order of race Meetings when 'By Meeting' filter is selected
    PRECONDITIONS: Request to check data:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/198,201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-14T00:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2020-08-12T10:37:30.000Z&simpleFilter=event.classId:notIntersects:201&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create greyhound events
        EXPECTED: Events are created
        """
        if tests.settings.backend_env != 'prod':
            start_time = self.get_date_time_formatted_string(days=2, hours=2)
            self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, start_time=start_time)

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED:
        """
        self.site.wait_content_state('homepage')

    def test_002_from_the_sports_menu_ribbon_tap_race_icon(self):
        """
        DESCRIPTION: From the sports menu ribbon tap <Race> icon
        EXPECTED: <Race> landing page is opened
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')

    def test_003_tap_future_tab(self):
        """
        DESCRIPTION: Tap 'Future' tab
        EXPECTED: 'Future' tab is opened
        EXPECTED: 'By Meeting' sorting type is selected by default
        """
        future = vec.sb.TABS_NAME_FUTURE if self.brand == 'ladbrokes' else vec.sb.SPORT_DAY_TABS.future
        self.site.greyhound.tabs_menu.click_button(future)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(future).is_selected(),
                        msg='"future tab" is not present')
        actual_sub_tab = self.site.greyhound.tab_content.current
        self.assertEqual(actual_sub_tab.upper(), vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING,
                         msg=f'Actual tabs: "{actual_sub_tab}" is not equal with the'
                             f'Expected tab: "{vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING}"')

    def test_004_check_order_of_race_meetings_when_by_meeting_filter_is_selected(self):
        """
        DESCRIPTION: Check order of race meetings when 'By Meeting' filter is selected
        EXPECTED: Race meetings are ordered in ascending alphabetical order (A-Z)
        """
        sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict if self.brand == 'ladbrokes' else self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict
        try:
            self.assertTrue(sections, msg='No sections found in future tab')
        except:
            self.device.refresh_page()
            self.site.wait_content_state('Greyhoundracing')
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict if self.brand == 'ladbrokes' else self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found in future tab')
        sorted_sections = sorted(list(sections.keys()))
        self.assertEqual(list(sections.keys()), sorted_sections,
                         msg=f'Actual sections: "{list(sections.keys())}" is not same as '
                             f'Expected sections: "{sorted_sections}"')
