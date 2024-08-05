import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C29003_Verify_Greyhound_Special_Event_Types(BaseRacing):
    """
    TR_ID: C29003
    NAME: Verify 'Greyhound Special' Event Types
    DESCRIPTION: This test case verifies which events are related to the 'Greyhound Special' events and how they should be displayed in the 'Invictus' application
    PRECONDITIONS: To retrieve an information from the Site Server (*TST2 (CI-TEST2)*) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/201?translationLang=LL
    PRECONDITIONS: Where *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **Class id** = 201 - Greyhound specails
    PRECONDITIONS: **'typeName'** on event level to identify needed event types to be displayed on the application
    PRECONDITIONS: **The full request to check data:**
    PRECONDITIONS: Ladbrokes
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/198,201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T14:17:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: Coral
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-26T00:00:00.000Z&simpleFilter=event.startTime:lessThan:2020-08-27T00:00:00.000Z&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T13:35:30.000Z&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: **Greyhounds Specials present only for Today tab and only on 'By Meeting' sorting type**
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load 'Invictus' application
        """
        self.site.wait_content_state("Homepage")
        if tests.settings.backend_env != 'prod':
            params = self.ob_config.add_greyhound_racing_specials_event(number_of_runners=2,
                                                                        ew_terms=self.ew_terms, time_to_start=20)
            self.__class__.event_id = params.event_id

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: Greyhounds landing page is opened
        """
        self.navigate_to_page('greyhound-racing')
        self.site.wait_content_state('greyhound-racing', timeout=20)

    def test_003_go_to_the_today_tab(self):
        """
        DESCRIPTION: Go to the 'Today' tab
        EXPECTED: 'Today' tab is opened
        EXPECTED: **'By Meeting'** sorting type is selected by default
        """
        if self.brand == 'ladbrokes':
            today = vec.sb.TABS_NAME_TODAY
        else:
            today = vec.sb.SPORT_DAY_TABS.today
        self.site.greyhound.tabs_menu.click_button(today)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(today).is_selected(),
                        msg='"Today tab" is not present')
        # Due to this story point OZONE-3455 by meeting and by time will not available in today tab
        # if self.brand == 'bma':
        #     actual_sub_tabs = self.site.greyhound.tab_content.items_names
        #     self.assertEqual(actual_sub_tabs, vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING,
        #                      msg=f'Actual tabs: "{actual_sub_tabs}" is not equal with the'
        #                          f'Expected tabs: "{vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING}"')

    def test_004_verify_special_event_types(self):
        """
        DESCRIPTION: Verify special event types
        EXPECTED: All available special event types are shown
        EXPECTED: Special events are shown below the 'All Races' group
        """
        if self.brand == 'ladbrokes':
            specials = vec.racing.RACING_SPECIALS_TAB_NAME
            self.site.greyhound.tabs_menu.click_button(specials)
            self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(specials).is_selected(),
                            msg='Specials tab is not present')
        else:
            events = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict.get("TRAP CHALLENGES")
            self.assertTrue(events, msg='No special events found races tab')
            events.click()
            current = self.device.get_current_url()
            expected_value = 'greyhounds-specials'
            self.assertIn(expected_value, current, msg='User is not navigated to Specials EDP')

    def test_005_verify_special_event_types_displaying(self):
        """
        DESCRIPTION: Verify special event types displaying
        EXPECTED: Special event sections are expanded by default
        EXPECTED: It is possible to collapse / expand section by tapping section header
        EXPECTED: Each section contains events withing it
        """
        if self.brand == 'ladbrokes':
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found on Specials tab')
            first_section_name, first_section = list(sections.items())[0]
            first_section.expand()
            first_section_events = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(first_section_events, msg='Special tab has no events')
            self.__class__.event_name, event = list(first_section_events.items())[0]
            event.click()
            current = self.device.get_current_url()
            expected_value = 'greyhounds-specials'
            self.assertIn(expected_value, current, msg='User is not navigated to Specials EDP')

    def test_006_verify_section_headers(self):
        """
        DESCRIPTION: Verify section headers
        EXPECTED: The section headers correspond to **'typeName' **attributes on the Site Server
        """
        # Covered in step 5

    def test_007_verify_special_events_if_they_are_not_available_on_the_site_server(self):
        """
        DESCRIPTION: Verify special events if they are not available on the Site Server
        EXPECTED: If events for event type are not available -> sections should not be shown at all
        """
        # Covered in step 5

    def test_008_go_to_the_today_tab(self):
        """
        DESCRIPTION: Go to the 'Today' tab
        EXPECTED: 'Today' tab is opened
        EXPECTED: **'By Meeting'** sorting type is selected by default
        """
        self.device.go_back()
        self.test_003_go_to_the_today_tab()
