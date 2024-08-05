import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.exceptions.precondition_not_met_exception import PreconditionNotMetException


# @pytest.mark.tst2 #cannot have streaming events
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@vtest
class Test_C1501375_Verify_event_card_on_In_Play_page_tab_section(Common):
    """
    TR_ID: C1501375
    NAME: Verify event card on 'In-Play' page/tab/section
    DESCRIPTION: This test case verifies event card on 'In-Play' page/tab/section
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach Upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To configure In-Play module on Sports Landing page: https://ladbrokescoral.testrail.com/index.php?/cases/view/8146654
    PRECONDITIONS: * To configure In-Play module on Home page: https://ladbrokescoral.testrail.com/index.php?/cases/view/3019589
    PRECONDITIONS: * 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: * To get SiteServer info about event use the following url: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL,
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get inplay events
        """
        self.navigate_to_page('in-play')
        self.site.wait_content_state(state_name='InPlay')
        if self.device_type == 'mobile':
            self.__class__.leagues = self.site.inplay.tab_content.live_now.items_as_ordered_dict
        else:
            self.__class__.leagues = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict

    def test_001_verify_event_name(self, upcoming=False, inplay_tab=True):
        """
        DESCRIPTION: Verify Event Name
        EXPECTED: *   Event name corresponds to 'name' attribute
        EXPECTED: *   Event name is displayed in format:
        EXPECTED: <Team1/Player1>
        EXPECTED: <Team2/Player2>
        EXPECTED: *   Name of outright event is displayed in format: '<Event name>'
        """
        if self.leagues:
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
                        self.assertTrue(event.template.is_live_now_event, msg=f'Event "{ui_event_name}" does not have "LIVE" label')
                        if inplay_tab:
                            sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
                            for sport_name, sport in sports.items():
                                if sport.is_selected():
                                    self.__class__.sport_name = sport_name
                                    break
                            if self.sport_name.upper() == 'TENNIS':
                                self.assertTrue(event.template.has_set_number, msg=f'Event "{ui_event_name}" does not have "Sets" label')
                            if self.sport_name.upper() == 'FOOTBALL':
                                self.assertTrue(event.template.has_favourite_icon, msg='No favourite icon for the event')
                        for tag in ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM']:
                            if tag in self.event_details['drilldownTagNames']:
                                self.assertTrue(event.template.has_watch_live_icon, msg='No Watch live icon for the event ')
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

    def test_002_verify_match_timesetslive_label(self):
        """
        DESCRIPTION: Verify 'Match Time'/'Sets'/'LIVE' label
        EXPECTED: *   Event **'Match Time'/'Sets'/'LIVE' label** is shown if available instead of event Start Time
        EXPECTED: *   **'Match Time'/'Sets'/'LIVE label** is displayed below Event name (for Coral) and above Event name (for Ladbrokes)
        """
        # covered in step 001

    def test_003_verify_watch_live_icon(self):
        """
        DESCRIPTION: Verify 'WATCH LIVE' icon
        EXPECTED: * 'WATCH' icon is displayed for **Ladbrokes**, 'WATCH LIVE' inscription and icon for **Coral**
        EXPECTED: * 'WATCH LIVE' icon/inscription is shown if ‘drilldownTagNames’ attribute is available (one or more of following flags):
        EXPECTED: - EVFLAG_AVA
        EXPECTED: - EVFLAG_IVM
        EXPECTED: - EVFLAG_PVM
        EXPECTED: - EVFLAG_RVA
        EXPECTED: - EVFLAG_RPM
        EXPECTED: - EVFLAG_GVM
        EXPECTED: * 'WATCH LIVE' inscription/icon is displayed next to 'Match Time'/'Sets'/'LIVE' label/'Event Start Time'
        """
        # covered in step 001

    def test_004_for_coralverify_favorites_icon(self):
        """
        DESCRIPTION: **For Coral:**
        DESCRIPTION: Verify 'Favorites' icon
        EXPECTED: 'Favorites' icon is displayed before 'Match Time'/'Sets'/'LIVE' label/'Event Start Time' on Football events only
        """
        # covered in step 001

    def test_005_clicktapanywhere_on_event_section(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event section
        EXPECTED: Event Details Page is opened
        """
        self.event.click()
        self.site.wait_content_state('EventDetails', timeout=20)

    def test_006_navigate_to_upcoming_events(self):
        """
        DESCRIPTION: Navigate to upcoming events
        EXPECTED: The list of upcoming events is displayed on the page
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
        EXPECTED: *   Event name is displayed in format **for Coral Mobile/Tablet** and **Ladbrokes all platforms**:
        EXPECTED: <Team1/Player1>
        EXPECTED: <Team2/Player2>
        EXPECTED: *   Event name is displayed in format **for Coral Desktop**:
        EXPECTED: <Team1/Player1> vs <Team2/Player2>
        EXPECTED: *   Name of outright event is displayed in format: '<Event name>'
        """
        self.test_001_verify_event_name(upcoming=True)

    def test_008_verify_event_start_time(self):
        """
        DESCRIPTION: Verify 'Event Start Time'
        EXPECTED: 'Event start time' corresponds to 'startTime' attribute and is displayed in the format '24 hours, Day (e.g. 21:45, Today OR 02:00, 23 Oct)'
        """
        # covered in step 007

    def test_009_clicktapanywhere_on_event_section(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event section
        EXPECTED: Event Details Page is opened
        """
        self.test_005_clicktapanywhere_on_event_section()

    def test_010_repeat_steps_1_5_on_sports_landing_page__matches_tab__in_play_module_for_mobiletablet_homepage__featured_tab__in_play__module_for_mobiletablet_homepage__in_play__live_stream_section__in_play_switcher_for_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-5 on:
        DESCRIPTION: * Sports Landing page > 'Matches' tab > 'In-play' module **For Mobile/Tablet**
        DESCRIPTION: * Homepage > 'Featured' tab > 'In-play'  module **For Mobile/Tablet**
        DESCRIPTION: * Homepage > 'In-Play & Live Stream ' section > 'In-Play' switcher **For Desktop**
        EXPECTED:
        """
        if self.device_type == 'mobile':
            self.navigate_to_page('sport/football')
            self.site.wait_content_state(state_name='FOOTBALL')
            try:
                self.__class__.leagues = self.site.football.tab_content.in_play_module.items_as_ordered_dict
            except VoltronException:
                raise PreconditionNotMetException('No inplay events found')
            self.test_001_verify_event_name(inplay_tab=False)
            self.test_005_clicktapanywhere_on_event_section()
        self.navigate_to_page('homepage')
        self.site.wait_content_state('homepage')
        if self.device_type == 'desktop':
            try:
                self.__class__.leagues = self.site.home.get_module_content('IN-PLAY AND LIVE STREAM').accordions_list.items_as_ordered_dict
            except VoltronException:
                raise PreconditionNotMetException('No events found in "INPLAY" section')
        else:
            self.__class__.leagues = self.site.home.tab_content.in_play_module.items_as_ordered_dict
        self.test_001_verify_event_name(inplay_tab=False)
        self.test_005_clicktapanywhere_on_event_section()
