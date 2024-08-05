import pytest
import tests
from datetime import datetime
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from voltron.utils.helpers import normalize_name
from voltron.environments import constants as vec
from crlat_ob_client.utils.date_time import validate_time
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests


@pytest.mark.prod
@pytest.mark.hl
# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.navigation
@vtest
class Test_C2594315_Verify_Football_Event_Details_page_Header(BaseBetSlipTest, BaseFeaturedTest):
    """
    TR_ID: C2594315
    NAME: Verify Football Event Details page Header
    DESCRIPTION: This test case verifies header on Football EDP (event details page)
    """
    keep_browser_open = True

    def basic_active_events_filter(self):
        return self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_LIVE_NOW_EVENT, OPERATORS.IS_FALSE))

    def test_000_preconditions(self):
        """
        PRECONDITIONS: You can find New Designs here:
        PRECONDITIONS: https://app.zeplin.io/project/5c86355fe1c597198e2a34f9/dashboard
        PRECONDITIONS: To retrieve information about event use:
        PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
        PRECONDITIONS: where,
        PRECONDITIONS: XXX - the event ID
        PRECONDITIONS: X.XX - current supported version of OpenBet release
        PRECONDITIONS: LL - language (e.g. en, ukr)
        PRECONDITIONS: **Note! Oxygen header is shown in case Opta Scoreboard isn't mapped to event** (status code 404 (not found) is received in response to **<OpenBet event id>?&api-key=COMc368624411e44b6e80e83c5a7f7c03c8** request)
        PRECONDITIONS: 1. Load Oxygen application
        PRECONDITIONS: 2. Navigate to Football Landing page
        PRECONDITIONS: 3. This case should be confirmed for all sports.
        """
        class_ids = self.get_class_ids_for_category(category_id=self.ob_config.football_config.category_id)
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   class_id=class_ids,
                                   brand=self.brand)
        events_filter = self.basic_active_events_filter().add_filter(simple_filter
                                                                     (LEVELS.EVENT,
                                                                      ATTRIBUTES.EVENT_SORT_CODE,
                                                                      OPERATORS.INTERSECTS,
                                                                      vec.siteserve.OUTRIGHT_EVENT_SORT_CODES))
        resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
        event = next((event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')), None)
        if not event:
            raise SiteServeException(
                f'No active events found for category id "{self.ob_config.football_config.category_id}"')
        self.__class__.outright_name = normalize_name(event['event']['name'])
        self.__class__.outright_eventID = event['event']['id']
        outright_class_name = event['event']['className'].split()[-1]
        outright_type_name = event['event']['typeName']
        self.__class__.outright_section_name = f'{outright_class_name} - {outright_type_name}'

    def test_001_navigate_to_edp_of_football_in_play_event(self):
        """
        DESCRIPTION: Navigate to EDP of football in-play event
        EXPECTED: * EDP is loaded
        EXPECTED: * Oxygen header is present
        """
        self.__class__.football_category_id = self.ob_config.football_config.category_id
        self.site.wait_content_state('Homepage')
        self.navigate_to_page('in-play')
        self.site.wait_content_state(state_name='InPlay')
        if self.device_type == 'mobile':
            self.__class__.leagues = self.site.inplay.tab_content.live_now.items_as_ordered_dict
        else:
            self.__class__.leagues = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict

        self.assertTrue(self.leagues,
                        msg='"Events" are not displayed.')

    def test_002_verify_elements_within_header(self, upcoming=False):
        """
        DESCRIPTION: Verify elements within header
        EXPECTED: Header contains:
        EXPECTED: - 'Live' label and event 'start time' in one line
        EXPECTED: - Event name in second line
        EXPECTED: - Watch icon (as access point to watch stream)
        EXPECTED: - Done icon (If the user taps on the Done button
        EXPECTED: then user should see sub header return to original state with Watch icon)
        EXPECTED: - Notifications icon (if the event has  match notification available the user can see the bell icon for notifications, only on Wrappers)
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
                                                                     ss_data=True,
                                                                     utcoffset=0)
                    event_time = event.template.event_time
                    self.assertEqual(event_time.replace(',', ''), expected_event_time.replace(',', ''),
                                     msg=f'Actual Event time "{event_time}" is not same as '
                                         f'Expected Event time "{expected_event_time}"')

    def test_003_verify_event_start_datetime(self):
        """
        DESCRIPTION: Verify Event start date/time
        EXPECTED: * Event start date corresponds to **startTime** attribute
        EXPECTED: * Event start time/date is shown in the following format: 24 hours - DD/MM/YY. E.g. 19:30 - 26/02/18
        """
        # covered in step 2

    def test_004_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
        EXPECTED: * Event name corresponds to **name** attribute
        EXPECTED: * Long event name is displayed in 2 lines; text is centered
        """
        # covered in step 2

    def test_005_navigate_to_edp_of_football_pre_match_event(self):
        """
        DESCRIPTION: Navigate to EDP of football pre-match event
        EXPECTED: * EDP is loaded
        EXPECTED: * Oxygen header is present
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

    def test_006_verify_elements_within_header(self):
        """
        DESCRIPTION: Verify elements within header
        EXPECTED: Header contains:
        EXPECTED: - 'Live' label and event 'start time' in one line
        EXPECTED: - Event name in second line
        EXPECTED: - Watch icon (as access point to watch stream)
        EXPECTED: - Done icon (If the user taps on the Done button
        EXPECTED: then user should see sub header return to original state with Watch icon)
        EXPECTED: - Notifications icon (if the event has  match notification available the user can see the bell icon for notifications, only on Wrappers)
        """
        self.test_002_verify_elements_within_header(upcoming=True)

    def test_007_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        """
        # covered in step 6

    def test_008_navigate_to_edp_of_football_outrights_event_and_verify_header(self):
        """
        DESCRIPTION: Navigate to EDP of football Outrights event and verify header
        EXPECTED: Header contains:
        EXPECTED: - Event 'start time' in one line
        EXPECTED: - Event name in second line
        """
        outrights_cms_name = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights
        if self.is_tab_present(tab_name=outrights_cms_name, category_id=self.football_category_id):
            self.navigate_to_page(name='sport/football/outrights')
            self.site.wait_content_state(state_name=self.sport_name)

            current_tab = self.site.football.tabs_menu.current
            expected_tab = self.expected_sport_tabs.outrights
            self.assertEqual(current_tab, expected_tab,
                             msg=f'Actual tab: "{current_tab}" '
                                 f'is not as expected: "{expected_tab}')
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            league = self.outright_section_name
        else:
            league = self.outright_section_name.upper()
        self.__class__.section = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(league)
        self.section.expand()

    def test_009_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        """
        outright = self.section.items_as_ordered_dict.get(self.outright_name)
        outright.click()
        self.site.wait_content_state('EventDetails')
        event_name_on_EDP = self.site.sport_event_details.event_title_bar.event_name.title()
        expected_outright_name = self.outright_name.title()
        self.assertEqual(event_name_on_EDP, expected_outright_name,
                         msg=f'Event name "{event_name_on_EDP}" on details page doesn\'t match with '
                             f'event name "{expected_outright_name}" on Football page')

        event_time_ui = self.site.sport_event_details.event_title_bar.event_time
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.outright_eventID)[0][
            'event']
        event_time_resp = event_resp['startTime']
        if self.device_type == 'desktop':
            pattern = '%A, %d-%b-%y, %I:%M %p' if self.brand == 'ladbrokes' else '%A, %d-%b-%y. %H:%M'
            date_time_obj = datetime.strptime(event_time_ui, pattern)
            new_date = date_time_obj.replace(date_time_obj.year - 1)
            event_time_ui_new = datetime.strftime(new_date, pattern)
            event_time_resp_converted = self.convert_time_to_local(
                ob_format_pattern=self.ob_format_pattern,
                date_time_str=event_time_resp,
                ui_format_pattern=self.event_card_today_time_format_pattern,
                future_datetime_format=self.event_card_coupon_and_competition_future_time_format_pattern,
                ss_data=True,
                utcoffset=60)
            validate_time(actual_time=event_time_ui_new, format_pattern=pattern)
            self.compare_date_time(item_time_ui=event_time_ui_new, event_date_time_ob=event_time_resp_converted,
                                   format_pattern="%A, %d-%b-%y, %I:%M %p", dayfirst=False)
        else:
            event_time_resp_converted = self.convert_time_to_local(
                ob_format_pattern=self.ob_format_pattern,
                date_time_str=event_time_resp,
                ui_format_pattern=self.event_card_today_time_format_pattern,
                future_datetime_format=self.event_card_coupon_and_competition_future_time_format_pattern,
                ss_data=True,
                utcoffset=60)
            validate_time(actual_time=event_time_ui, format_pattern=self.event_card_future_time_format_pattern)
            self.compare_date_time(item_time_ui=event_time_ui, event_date_time_ob=event_time_resp_converted,
                                   format_pattern=self.event_card_future_time_format_pattern, dayfirst=False)

        rawIsOffCode = event_resp['rawIsOffCode']
        is_started = wait_for_result(lambda: 'isStarted' in [event_resp.keys()], timeout=0.5)
        if rawIsOffCode in ['-' or 'Y'] and is_started:
            is_live_event = self.site.sport_event_details.event_title_bar.is_live_now_event
            self.assertTrue(is_live_event, msg='"LIVE" label is not shown on the screen')

    def test_010_navigate_to_edp_of_football_specials_event_and_verify_header(self):
        """
        DESCRIPTION: Navigate to EDP of football Specials event and verify header
        EXPECTED: Header contains:
        EXPECTED: - Event 'start time' in one line
        EXPECTED: - Event name in second line
        """
        specials_cms_name = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials
        if self.is_tab_present(tab_name=specials_cms_name, category_id=self.football_category_id):
            self.navigate_to_page(name='sport/football/specials')
            self.site.wait_content_state(state_name=self.sport_name)

            current_tab = self.site.football.tabs_menu.current
            expected_tab = self.expected_sport_tabs.specials
            self.assertEqual(current_tab, expected_tab,
                             msg=f'Actual tab: "{current_tab}" '
                                 f'is not as expected: "{expected_tab}')

    def test_011_verify_that_red_bar_is_not_displayed_on_the_ui(self):
        """
        DESCRIPTION: Verify that red bar is not displayed on the UI
        EXPECTED: Red bar should be absent on UI(it was situated below the scoreboard on EDP)
        EXPECTED: Design(https://app.zeplin.io/project/5c86355fe1c597198e2a34f9/screen/5d2f2aaafd92de63c05f3ba9 )
        """
        # Can not automate it is not present

    def test_012_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        """
        league = list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        events = league.items_as_ordered_dict
        event = list(events.values())[0]
        event.click()
        self.site.wait_content_state(state_name='EventDetails', timeout=20)
        if self.device_type == 'desktop':
            event_on_EDP = self.site.sport_event_details.header_line.page_title.title
        else:
            event_on_EDP = self.site.sport_event_details.event_name
        event_time = self.site.sport_event_details.event_title_bar.event_time_we
        self.assertTrue(event_on_EDP.title(),
                        msg=f'Current EDP page with event: "{event_on_EDP.title()}" is not displayed')
        self.assertTrue(event_time, msg=f'Current EDP page with event: "{event_time}" is not displayed')
