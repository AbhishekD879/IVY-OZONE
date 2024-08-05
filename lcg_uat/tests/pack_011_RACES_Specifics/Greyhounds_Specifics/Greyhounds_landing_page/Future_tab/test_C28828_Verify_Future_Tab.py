import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
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
class Test_C28828_Verify_Future_Tab(BaseBetSlipTest, BaseGreyhound):
    """
    TR_ID: C28828
    NAME: Verify 'Future' Tab
    DESCRIPTION: This test case verifies 'Future' tab
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

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the Sports Menu Ribbon
        EXPECTED: <Race> landing page is opened
        """
        sport_name = vec.sb.GREYHOUND if tests.settings.brand == 'ladbrokes' else vec.sb.GREYHOUND.upper()
        self.site.open_sport(name=sport_name, timeout=15)

    def test_003_tap_future_tab(self):
        """
        DESCRIPTION: Tap 'Future' tab
        EXPECTED: 1.  'Future' tab is opened
        EXPECTED: 2.  'By Meeting' sorting type is selected by default
        """
        if self.brand == 'ladbrokes':
            future = vec.sb.TABS_NAME_FUTURE.upper()
        else:
            future = vec.sb.SPORT_DAY_TABS.future
        self.site.greyhound.tabs_menu.click_button(future)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(future).is_selected(),
                        msg='"future tab" is not present')

    def test_004_verify_future_tab(self):
        """
        DESCRIPTION: Verify 'Future' tab
        EXPECTED: 1.  Two sorting types are present: 'By Meeting' and 'By Time'
        EXPECTED: 2.  Race Meeting sections first section should be expanded by default and remaining should be collapsed by default
        """
        if self.brand != 'ladbrokes':
            actual_sub_tabs = self.site.greyhound.tab_content.items_names
            self.assertEqual(actual_sub_tabs, vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING,
                             msg=f'Actual tabs: "{actual_sub_tabs}" is not equal with the'
                                 f'Expected tabs: "{vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING}"')
        if self.brand == 'ladbrokes':
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        else:
            sections = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found in future tab')
        sections_names = list(sections.keys())
        sections = list(sections.values())
        self.assertTrue(sections[0].is_expanded(expected_result=True), msg=f'first section {sections_names[0]} is not expanded by default ')
        for i in range(1, len(sections)):
            self.assertFalse(sections[i].is_expanded(expected_result=False), msg=f'Event "{sections_names[i]}" is expanded by default')

    def test_005_check_portrait_and_landscape_modes_for_devices(self):
        """
        DESCRIPTION: Check portrait and landscape modes for devices
        EXPECTED: All page is displayed correctly
        """
        # cannot automate
