import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2 #cannot have streaming events
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.in_play
@vtest
class Test_C2727610_Archived_Verify_event_card_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C2727610
    NAME: [Archived] Verify event card on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies event card on 'In-Play Watch Live' page.
    PRECONDITIONS: 1. Live now/Upcoming events* with attached Live Stream should be preconfigured in TI.
    PRECONDITIONS: *events should be configured for different Sports and different Types of individual Sport (e.g Football - England Football League Trophy)
    PRECONDITIONS: 2. Load Oxygen application
    PRECONDITIONS: 3. Load application and navigate to In-pLay - Watch Live section in Sports Menu Ribbon
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_choose_live_now_switcher(self):
        """
        DESCRIPTION: Choose 'Live Now' switcher
        EXPECTED: The list of live events is displayed on the page
        """
        self.navigate_to_page('in-play')
        self.site.wait_content_state(state_name='InPlay')
        if self.device_type == 'mobile':
            self.__class__.leagues = self.site.inplay.tab_content.live_now.items_as_ordered_dict
        else:
            self.__class__.leagues = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict

        self.assertTrue(self.leagues,
                        msg='"Events" are not displayed.')

    def test_002_verify_event_name(self, upcoming=False):
        """
        DESCRIPTION: Verify Event Name
        EXPECTED: *   Event name corresponds to 'name' attribute
        EXPECTED: *   Event name is displayed in format:
        EXPECTED: <Team1/Player1> and <Team2/Player2> below
        EXPECTED: *   Name of outright/race event is displayed in format: '<Name> 'LIVE' label'
        """
        length = len(list(self.leagues.keys()))
        number_of_leagues = 2 if length > 3 else length
        for league in list(self.leagues.values())[:number_of_leagues]:
            if not league.is_expanded():
                league.expand()
            self.__class__.events = league.items_as_ordered_dict
            for event in list(self.events.values())[:1]:
                self.__class__.event = event
                event_id = event.template.event_id
                ui_event_name = list(self.events.keys())[0].split('v ')
                self.__class__.event_details = \
                    self.ss_req.ss_event_to_outcome_for_event(event_id=event_id,
                                                              query_builder=self.ss_query_builder)[0]['event']
                for team in ui_event_name:
                    self.assertIn(team, self.event_details['name'],
                                  msg=f'Actual event name "{team}" is '
                                      f'not in "{self.event_details["name"]}"')
                if not upcoming:
                    self.assertTrue(event.template.is_live_now_event,
                                    msg=f'Event "{ui_event_name}" does not have "LIVE" label')
                    sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
                    for sport_name, sport in sports.items():
                        if sport.is_selected():
                            self.__class__.sport_name = sport_name
                            break
                    for tag in ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM']:
                        if tag in self.event_details['drilldownTagNames']:
                            self.assertTrue(event.template.has_watch_live_icon,
                                            msg='No Watch live icon for the event ')
                            break
                else:
                    pattern = '%H:%M, %d %b'
                    expected_event_time = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                                     date_time_str=self.event_details['startTime'],
                                                                     future_datetime_format=pattern,
                                                                     ss_data=True)
                    event_time = event.template.event_time
                    self.assertEqual(event_time.replace(',', ''), expected_event_time.replace(',', ''),
                                     msg=f'Actual Event time "{event_time}" is not same as '
                                         f'Expected Event time "{expected_event_time}"')

    def test_003_verify_match_timesetslive_labelevent_start_time(self):
        """
        DESCRIPTION: Verify 'Match Time'/'Sets'/'Live' label/'Event Start Time'
        EXPECTED: *   'Event start time' corresponds to 'startTime' attribute
        EXPECTED: *   For events that occur **Today** date format is: **24 hours, Today**
        EXPECTED: *   For events that occur **Tomorrow** date format is: **24 hours, DD-MMM**
        EXPECTED: *   For events that occur in the **Future** (including tomorrow) date format is: **24 hours, DD-MMM**
        EXPECTED: *   Event **'Match Time'/'Sets'/'Live' label** is shown if available instead of event Start Time
        EXPECTED: *   **'Match Time'/'Sets'/'Live' label/'Event Start Time'** is displayed below the Event name for Coral and Under Event name for Ladbrokes.
        """
        # Covered in step 2

    def test_004_verify_watch_live_icon_and_inscription(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and inscription
        EXPECTED: * 'Watch live' icon and inscription (inscription and 'Watch Live' icon **for Desktop**) are shown if ‘drilldownTagNames’ attribute is available (one or more of following flags):
        EXPECTED: - EVFLAG_AVA
        EXPECTED: - EVFLAG_IVM
        EXPECTED: - EVFLAG_PVM
        EXPECTED: - EVFLAG_RVA
        EXPECTED: - EVFLAG_RPM
        EXPECTED: - EVFLAG_GVM
        EXPECTED: * 'Watch live' icon and inscription are displayed next to 'Match Time'/'Sets'/'Live' label/'Event Start Time'
        """
        # covered in step 2

    def test_005_clicktapanywhere_on_event_section(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event section
        EXPECTED: Event Details Page is opened
        """
        self.event.click()
        self.site.wait_content_state('EventDetails', timeout=20)

    def test_006_choose_upcoming_switcher(self):
        """
        DESCRIPTION: Choose 'Upcoming' switcher
        EXPECTED: The list of pre-match events is displayed on the page
        """
        self.navigate_to_page('in-play')
        self.site.wait_content_state(state_name='InPlay')
        if self.device_type == 'mobile':
            upcoming = self.site.inplay.tab_content.upcoming
        else:
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
            upcoming = self.site.inplay.tab_content.accordions_list
        self.__class__.leagues = upcoming.items_as_ordered_dict
        self.assertTrue(self.leagues, msg='There are no upcoming events displayed')

    def test_007_verify_event_name(self):
        """
        DESCRIPTION: Verify Event Name
        EXPECTED: *   Event name corresponds to 'name' attribute
        EXPECTED: *   Event name is displayed in the next format:
        EXPECTED: <Team1/Player1>
        EXPECTED: <Team2/Player2>
        EXPECTED: *   Name of outright/race event is displayed in format: '<Name>'
        """
        self.test_002_verify_event_name(upcoming=True)

    def test_008_clicktapanywhere_on_event_section(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event section
        EXPECTED: Event Details Page is opened
        """
        self.test_005_clicktapanywhere_on_event_section()
