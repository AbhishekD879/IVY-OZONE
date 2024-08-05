import pytest
from crlat_siteserve_client.constants import ATTRIBUTES

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.slow
@pytest.mark.streaming
@pytest.mark.racing
@pytest.mark.sports
@pytest.mark.event_details
@pytest.mark.desktop
@vtest
class Test_C29221_Stream_icon_and_streaming_text_displaying(BaseSportTest, BaseRacing):
    """
    TR_ID: C29221
    NAME: 'Stream' icon and streaming text displaying
    DESCRIPTION: This test case verifies Stream icon  and streaming text displaying on <Sport> Landing and Details pages.
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   XX - Sport Category ID.
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. For each **Class **retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?translationLang=LL
    PRECONDITIONS: *   XXX -  comma separated list of **Class **ID's
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: *   **'name'** to define event name
    PRECONDITIONS: *   **'drilldownTagNames'** to determine WHICH stream provider has been mapped to the event
    PRECONDITIONS: **'drilldownTagNames'**** ***Streaming flags are:*
    PRECONDITIONS: 1.  *EVFLAG_IVM -  IMG Video Mapped for this event*
    PRECONDITIONS: 2.  *EVFLAG_PVM - Perform Video Mapped for this event*
    PRECONDITIONS: 3.  *EVFLAG_AVA - At The Races stream available*
    PRECONDITIONS: 4.  *EVFLAG_RVA - RacingUK stream available*
    PRECONDITIONS: 5.  *EVFLAG_RPM - RPGTV Greyhound streaming Mapped*
    PRECONDITIONS: 6.  EVFLAG_GVM' - igamemedia
    """
    keep_browser_open = True
    stream_flags = ['EVFLAG_PVM', 'EVFLAG_AVA']
    sport_page = '/sport/football/matches'
    racing_page = 'horse-racing'

    def get_event_from_ss(self, event_id: str):
        """
        Gets event for given event_id from SS response
        :param event_id: specifies event id
        :return: event
        """
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        event = resp[0]['event']
        return event

    def verify_drilldown_tag_names(self, event: dict, expected_flag: list, tag_names_enabled: bool = True) -> None:
        """
        Verifies whether given flags (for example, EVFLAG_IVM, EVFLAG_PVM, EVFLAG_AVA, etc.)
        are set for given event with live stream available
        :param event: event to check
        :param expected_flag: flag to check
        :param tag_names_enabled: flags enabled or disabled
        """
        if tag_names_enabled:
            self.assertIn(ATTRIBUTES.DRILLDOWN_TAG_NAMES, event.keys(),
                          msg=f'There is no property "{ATTRIBUTES.DRILLDOWN_TAG_NAMES}" '
                          f'in SS response: "{event.keys()}"')
            self.assertIn(expected_flag, event[ATTRIBUTES.DRILLDOWN_TAG_NAMES],
                          msg=f'There are no proper flags: {self.stream_flags} '
                          f'in SS response: "{event[ATTRIBUTES.DRILLDOWN_TAG_NAMES]}""')
        else:
            self.assertIn(ATTRIBUTES.DRILLDOWN_TAG_NAMES, event.keys(),
                          msg=f'There is no property "{ATTRIBUTES.DRILLDOWN_TAG_NAMES}" '
                          f'in SS response: "{event.keys()}"')
            self.assertNotIn(expected_flag, event[ATTRIBUTES.DRILLDOWN_TAG_NAMES],
                             msg=f'Flags: {self.stream_flags} '
                             f'should not be in SS response: "{event[ATTRIBUTES.DRILLDOWN_TAG_NAMES]}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events: with and without stream available
        """
        event_1 = self.ob_config.add_autotest_premier_league_football_event(is_live=True, perform_stream=True)
        self.__class__.event_name_1, self.__class__.event_id_1 = \
            event_1.team1 + ' vs ' + event_1.team2, event_1.event_id

        event_2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_name_2, self.__class__.event_id_2 = \
            event_2.team1 + ' vs ' + event_2.team2, event_2.event_id

        self.__class__.name_pattern = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern

        event_3 = self.ob_config.add_UK_racing_event(is_live=True, at_races_stream=True, number_of_runners=1)
        self.__class__.event_name_3, self.__class__.event_id_3 = \
            f'{event_3.event_off_time} {self.name_pattern}', event_3.event_id

        event_4 = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.event_name_4, self.__class__.event_id_4 = \
            f'{event_4.event_off_time} {self.name_pattern}', event_4.event_id

        self.__class__.league = tests.settings.football_autotest_league

        # Scoreboard" config should have property "showScoreboard" as "Yes"
        # and only then there will be displayed 'Match Live' and 'Watch Live' buttons
        scoreboard_config = self.get_initial_data_system_configuration().get('Scoreboard')
        if not scoreboard_config:
            scoreboard_config = self.cms_config.get_system_configuration_item('Scoreboard')
        if scoreboard_config:
            self.__class__.show_scoreboard = scoreboard_config.get('showScoreboard')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_go_to_sport_landing_page(self):
        """
        DESCRIPTION: Go to <Sport> Landing page
        EXPECTED: <Sport> Landing page is opened
        """
        self.navigate_to_page(name=self.sport_page)
        self.site.wait_content_state(state_name='Football')

    def test_003_verify_sport_events_which_have_stream_icon_displayed(self):
        """
        DESCRIPTION: Verify <Sport> events which have 'Stream' icon displayed
        EXPECTED: 'Stream' icon is displayed on Sport Landing Page and 'Watch' button is displayed on Event Details page if event has the following attribute:
        EXPECTED: *   **'drilldownTagNames'**="<one or more flags from the list in Preconditions>"
        """
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No section found on page')
        section = sections.get(self.league)
        self.assertTrue(section, msg=f'Section: "{self.league}" is not found')

        section.expand()

        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No section found on page')
        section = sections.get(self.league)
        self.assertTrue(section, msg=f'Section: "{self.league}" is not found')

        events = sections.get(self.league).items_as_ordered_dict
        self.assertTrue(events, msg=f'*** No events found in section')

        if self.event_name_1 not in list(events.keys()):
            self._logger.info(f'*** Event name: "{self.event_name_1 }" not found in section: "{self.league}"')
        else:
            self.assertTrue(events.get(self.event_name_1).has_stream(),
                            msg=f'Event: "{self.event_name_1}" has no stream available')

        self.navigate_to_edp(event_id=self.event_id_1, sport_name='football')
        if self.device_type == 'desktop' and self.show_scoreboard == 'Yes':
            self.assertTrue(self.site.sport_event_details.has_watch_live_button(),
                            msg=f'Event: "{self.event_name_1}" has no "Watch Live" button')
        else:
            if self.get_scoreboard_sport_status(sport_id=self.ob_config.backend.ti.football.category_id):

                self.assertTrue(self.site.sport_event_details.has_watch_live_icon,
                                msg=f'Event: "{self.event_name_1}" has no "Watch Live" icon')
            else:
                event_user_tabs = self.site.sport_event_details.event_user_tabs_list.items_as_ordered_dict
                self.assertTrue(event_user_tabs, msg='User Tabs are not found')
                self.assertIn(vec.sb.WATCH_LIVE_LABEL.title(), event_user_tabs.keys())

        ss_event = self.get_event_from_ss(self.event_id_1)
        self.verify_drilldown_tag_names(ss_event, expected_flag=self.stream_flags[0], tag_names_enabled=True)

    def test_004_verify_sport_events_which_have_no_stream_icon_displayed(self):
        """
        DESCRIPTION: Verify <Sport> events which have no 'Stream' icon displayed
        EXPECTED: 'Stream' icon is NOT displayed on Sport Landing Page and 'Watch' button is NOT displayed on Event Details pages if event has the following attribute:
        EXPECTED: *   **'drilldownTagNames'**="<NO values from the list in Preconditions>"
        """
        self.navigate_to_page(name=self.sport_page)
        self.site.wait_content_state(state_name='Football')

        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No section found on page')
        section = sections.get(self.league)
        self.assertTrue(section, msg=f'Section: "{self.league}" is not found')

        section.expand()

        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No section found on page')
        section = sections.get(self.league)
        self.assertTrue(section, msg=f'Section: "{self.league}" is not found')

        events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'*** No events found in section')

        if self.event_name_1 not in list(events.keys()):
            self._logger.info(f'*** Event name: "{self.event_name_1}" not found in section: "{self.league}"')
        else:
            self.assertFalse(events.get(self.event_name_1).has_stream(expected_result=False),
                             msg=f'Event: "{self.event_name_1}" has stream available')

        self.navigate_to_edp(event_id=self.event_id_2, sport_name='football')

        if self.device_type == 'desktop':
            self.assertFalse(self.site.sport_event_details.has_watch_live_button(),
                             msg=f'Event: "{self.event_name_1}" has "Watch Live" button')
        else:
            self.assertFalse(self.site.sport_event_details.has_watch_live_icon,
                             msg=f'Event: "{self.event_name_1}" has "Watch Live" icon')

        ss_event = self.get_event_from_ss(self.event_id_2)
        self.verify_drilldown_tag_names(ss_event, expected_flag=self.stream_flags[0], tag_names_enabled=False)

    def test_005_go_to_race_landing_page(self):
        """
        DESCRIPTION: Go to <Race> Landing page
        EXPECTED: <Race> Landing page is opened
        """
        self.navigate_to_page(name=self.racing_page)
        self.site.wait_content_state('Horseracing')

    def test_006_verify_race_meeting_which_have_stream_icon_displayed(self):
        """
        DESCRIPTION: Verify <Race> meeting which have 'Stream' icon displayed
        EXPECTED: 'Stream' icon is displayed for a race if at least one of events within the race has stream mapped:
        EXPECTED: *   **'drilldownTagNames'**="<one or more flags from the list in Preconditions>"  (for the event)
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found on page')

        name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern
        meeting_name = name.upper() if self.brand != 'ladbrokes' else name

        section = sections.get(self.uk_and_ire_type_name)
        self.assertTrue(section, msg=f'Section: "{self.uk_and_ire_type_name}" is not found')
        if not section.is_expanded():
            section.expand()

        meeting = section.items_as_ordered_dict.get(meeting_name)
        if not (self.device_type == 'desktop' and self.brand == 'ladbrokes'):
            self.assertTrue(meeting.has_live_stream,
                            msg=f'Meeting: "{meeting_name}" has no stream icon')

    def test_007_verify_race_events_which_have_stream_icon_displayed(self):
        """
        DESCRIPTION: Verify <Race> events which have 'Stream' icon displayed
        EXPECTED: 'Stream' icon and **'(Possible delay: 10 seconds)'** text are displayed on <Race> Event Details pages if event has the following attribute:
        EXPECTED: *   **'drilldownTagNames'**="<one or more flags from the list in Preconditions>"
        """
        self.navigate_to_edp(event_id=self.event_id_3, sport_name=self.racing_page)
        self.assertTrue(self.site.racing_event_details.tab_content.has_video_stream_button(),
                        msg=f'Event: "{self.event_name_3}" has no "Watch Live" icon')

        ss_event = self.get_event_from_ss(self.event_id_3)
        self.verify_drilldown_tag_names(ss_event, expected_flag=self.stream_flags[1], tag_names_enabled=True)

    def test_008_verify_race_events_which_have_no_stream_icon_displayed(self):
        """
        DESCRIPTION: Verify <Race> events which have no 'Stream' icon displayed
        EXPECTED: 'Stream' icon is NOT displayed on Race Event Landing Page
        EXPECTED: 'Stream' icon and **'(Possible delay: 10 seconds)'** text are NOT displayed on Event Details pages if event has the following attribute:
        EXPECTED: *   **'drilldownTagNames'**="<NO values from the list in Preconditions>"
        """
        self.navigate_to_edp(event_id=self.event_id_4, sport_name=self.racing_page)
        self.assertFalse(self.site.racing_event_details.tab_content.has_video_stream_button(expected_result=False),
                         msg=f'Event: "{self.event_name_4}" should NOT contain "Watch Live" icon')

        ss_event = self.get_event_from_ss(self.event_id_4)
        self.verify_drilldown_tag_names(ss_event, expected_flag=self.stream_flags[1], tag_names_enabled=False)
