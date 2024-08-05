import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import get_live_stream_sport_by_category, get_inplay_sport_by_category
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.desktop_specific
@pytest.mark.in_play
@vtest
class Test_C65949621_Inplay_and_Live_stream_module_display_for_desktop(BaseBetSlipTest):
    """
    TR_ID: C65949621
    NAME: Inplay and Live stream module display for desktop
    DESCRIPTION: This test case is to validate Inplay and Live Stream module display for desktop
    PRECONDITIONS: Inplay events should be available
    """
    enable_bs_performance_log = True
    device_name = tests.desktop_default
    keep_browser_open = True
    sports_categories = {}

    def get_sport_names_along_with_category_ids(self):
        all_sports_categories = self.cms_config.get_sport_categories()
        res = {sport_category['imageTitle'].upper(): sport_category['categoryId']
               for sport_category in all_sports_categories}
        return res

    def get_drill_down_tag_status_for_live_stream_event(self, ss_event):
        drill_down_tags = ss_event['event']['drilldownTagNames']
        return 'EVFLAG_BL' in drill_down_tags and (
                    'EVFLAG_IVM' in drill_down_tags or 'EVFLAG_PVM' in drill_down_tags or 'EVFLAG_GVM' in drill_down_tags)

    def check_events(self, sport_name, type_of_events="IN PLAY"):
        category_id = self.sports_categories.get(sport_name.upper())

        # network call
        if type_of_events == "IN PLAY":
            log_data_for_sport_name = get_inplay_sport_by_category(category_id=category_id).get('eventsByTypeName')
        else:
            log_data_for_sport_name = get_live_stream_sport_by_category(category_id=category_id).get('eventsByTypeName')

        if type_of_events == "LIVE STREAM" and not log_data_for_sport_name:
            self.assertTrue(self.in_play_live_stream.has_no_events_label(),
                            f'Events Are Not available but Some of events are displayed')
            return

        event_ids_for_type_name_fe = {
            f"{log.get('className')} - {log.get('typeName')}".upper(): [str(id) for id in log.get('eventsIds')] for log
            in log_data_for_sport_name}

        # for validating events displayed
        accordions = self.in_play_live_stream.tab_content.accordions_list.items_as_ordered_dict

        number_of_events = sum([len(event_ids) for name, event_ids in event_ids_for_type_name_fe.items()])

        # verifying event attributes of ss response
        for type_name, event_ids in event_ids_for_type_name_fe.items():
            if type_name in accordions:
                for event_id in event_ids:
                    try:
                        ss_event = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0]
                    except:
                        number_of_events -= 1
                        continue
                    self.assertTrue('M' in ss_event['event']['siteChannels'],
                                    f"M is not available in siteChanels : {ss_event['event']['siteChannels']} for event_id:{event_id}")
                    self.assertTrue(ss_event['event']['isStarted'],
                                    f'Event id : {event_id} Event is not started but it is shown in inplay events')
                    self.assertTrue(ss_event['event']['isLiveNowEvent'],
                                    'event is not low event but it is displayed under inplay tab')
                    status_bet_in_run = next(
                        (True for market in ss_event['event']['children'] if market['market']['isMarketBetInRun']),
                        False)
                    self.assertTrue(status_bet_in_run, 'is not in run but it is shown in fe')
                    status_of_resulted = next(
                        (True for market in ss_event['event']['children'] if not market['market'].get('isResulted')),
                        False)
                    self.assertTrue(status_of_resulted, 'all markets resulted but it is shown in fe')

                    if type_of_events == "IN PLAY":
                        self.assertTrue('EVFLAG_BL' in ss_event['event']['drilldownTagNames'],
                                        'Drill down tag is not same as expected')
                    else:
                        status = self.get_drill_down_tag_status_for_live_stream_event(ss_event)
                        self.assertTrue(status, 'Drill Down Tag is not correct but')

        total_events_displayed = sum([len(accordian.items_as_ordered_dict) for accordian_name, accordian in
                                      accordions.items()])
        total_events_status = True if (number_of_events >= 4 and total_events_displayed == 4) or number_of_events == total_events_displayed else False
        self.assertTrue(total_events_status,
                        f'total events displayed on fe : {total_events_displayed} expected number of events displayed : {number_of_events}')

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Inplay events should be available
        """
        self.__class__.sports_categories = self.get_sport_names_along_with_category_ids()

    def test_001_load_oxygen_app_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen app on Desktop
        EXPECTED: Homepage is opened
        """
        self.site.go_to_home_page()

    def test_002_scroll_the_page_down_to_view_in_play_and_live_stream_section(self):
        """
        DESCRIPTION: Scroll the page down to view 'In-play and Live Stream' section
        EXPECTED: In-play and Live Stream' section is displayed below 'Enhances Multiples' carousel
        EXPECTED: Two switchers are visible: 'In-Play' and 'Live Stream'
        EXPECTED: 'In-Play' switcher is selected by default
        EXPECTED: First 'Sport' tab is selected by default
        """
        self.__class__.in_play_live_stream = self.site.home.desktop_modules.inplay_live_stream_module
        self.assertEqual('IN-PLAY AND LIVE STREAM', self.in_play_live_stream.name,
                         f'Actual Name of module : {self.in_play_live_stream.name} is not same as '
                         f'Expected Name of Module : {"IN-PLAY AND LIVE STREAM"}')

        tabs = self.in_play_live_stream.tabs_menu.items_as_ordered_dict
        self.assertTrue(tabs, '"Switchers" is not displayed in "IN-PLAY AND LIVE STREAM" MODULE')
        default_tab = self.in_play_live_stream.tabs_menu.current
        self.assertEqual(default_tab.upper(), 'IN-PLAY', f'Actual Selected Tab is "{default_tab}" is not same as '
                                                         f'Expected Selected Tab is "IN-PLAY"')
        in_play_tab_name, in_play_tab = next(([tab_name, tab] for tab_name, tab in tabs.items() if
                                              tab_name.upper() == 'IN-PLAY'),
                                             [None, None])
        live_stream_name, live_stream_tab = next(([tab_name, tab] for tab_name, tab in tabs.items() if
                                                  tab_name.upper() == 'LIVE STREAM'),
                                                 [None, None])
        self.assertIsNotNone(live_stream_name, '"LIVE STREAM" is not displayed inside "IN-PLAY AND LIVE STREAM" MODULE')
        live_stream_tab.click()
        self.assertTrue(live_stream_tab.is_selected(), f'{live_stream_name} is not selected after clicking on it')
        in_play_tab.click()
        self.assertTrue(in_play_tab.is_selected(), f'{in_play_tab} is not selected after clicking on it')

    def test_003_verify_header(self):
        """
        DESCRIPTION: Verify header
        EXPECTED: Header consist of:
        EXPECTED: 'In-Play and Live Stream' section name
        EXPECTED: In-play Sports Ribbon
        """
        # covered in above step

    def test_004_verify_in_play_view(self, type="IN PLAY"):
        """
        DESCRIPTION: Verify 'In-play' view
        EXPECTED: Max 4 events are shown
        EXPECTED: Events are grouped by 'typeId'
        EXPECTED: It is possible to collapse/expand all of the accordions by clicking the accordion's header
        EXPECTED: 'Cash out' icon is displayed if available
        """
        try:
            self.__class__.sports = self.in_play_live_stream.menu_carousel.items_as_ordered_dict
        except:
            self.__class__.sports = {}
        if not self.sports:
            raise SiteServeException("Live Events Are Not Present for Now. Can You Please Verify When Live Events Available")
        checked_sports = 0
        for sport_name, sport in self.sports.items():
            sport.click()
            wait_for_haul(5)
            self.check_events(sport_name=sport_name, type_of_events=type)
            checked_sports += 1
            if checked_sports == 2:
                break

    def test_005_verify_events_that_are_shown_when_in_play_is_selected(self):
        """
        DESCRIPTION: Verify events that are shown when 'In-play' is selected
        EXPECTED: All events with attributes:
        EXPECTED: Event's/market's/outcome's attribute 'siteCannels' contains 'M'
        EXPECTED: Attribute 'isStarted="true"' is present
        EXPECTED: Event's attribute 'drilldownTagNames' contains "EVFLAG_BL"
        EXPECTED: Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: At least one market is displayed (available in the response)
        """
        # covered in above step

    def test_006_verify_in_play_view_footer(self):
        """
        DESCRIPTION: Verify 'In-play' view footer
        EXPECTED: Footer link redirects to In-play page with 'All sports' or specific &lt;sport&gt; tab selected, depending on number of events
        """
        in_play_live_stream_sports_counters = {}
        for sport_name, sport in self.sports.items():
            if sport.counter >= 2:
                in_play_live_stream_sports_counters[sport_name] = sport.counter
        try:
            footer_link = self.site.home.desktop_modules.inplay_live_stream_module.view_all_live_stream_sport_events_button
        except:
            footer_link = None

        self.assertIsNotNone(footer_link, "footer link is not displayed")
        footer_link.click()
        self.site.wait_content_state_changed()

        in_play_page_sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        for sport_name, event_count in in_play_live_stream_sports_counters.items():
            self.assertAlmostEqual(in_play_page_sports[sport_name].counter, event_count,
                             msg=f'Actual Event Count {in_play_page_sports[sport_name].counter} is not same as Expected Event Count {event_count}')

    def test_007_verify_live_stream_view(self):
        """
        DESCRIPTION: Verify 'Live Stream' view
        EXPECTED: Max 4 events are shown
        EXPECTED: Events are grouped by 'typeId'
        EXPECTED: It is possible to collapse/expand all of the accordions by clicking the accordion's header
        EXPECTED: 'Cash out' icon is displayed if available
        """
        self.site.back_button.click()
        self.site.wait_content_state_changed()
        self.__class__.in_play_live_stream = self.site.home.desktop_modules.inplay_live_stream_module
        tabs = self.in_play_live_stream.tabs_menu.items_as_ordered_dict
        live_stream_name, live_stream_tab = next(([tab_name, tab] for tab_name, tab in tabs.items() if
                                                  tab_name.upper() == 'LIVE STREAM'),
                                                 [None, None])
        live_stream_tab.click()
        self.test_004_verify_in_play_view(type="LIVE STREAM")

    def test_008_verify_events_that_are_shown_when_live_stream_is_selected(self):
        """
        DESCRIPTION: Verify events that are shown when 'Live Stream' is selected
        EXPECTED: Event's/market's/outcome's attribute 'siteCannels' contains 'M'
        EXPECTED: Attribute 'isStarted="true"' is present
        EXPECTED: drilldownTagNames **should include the following attributes: {EVFLAGBL and EVFLAGIVM} OR {EVFLAGBL, EVFLAGPVM} OR {EVFLAGBL, EVFLAGIVM, EVFLAGPVM} OR {EVFLAGBL, EVFLAGGVM}(on the Event level) **
        EXPECTED: Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: event startTime is today
        """
        # covered in above step

    def test_009_verify_live_stream_view_footer(self):
        """
        DESCRIPTION: Verify 'Live Stream' view footer
        EXPECTED: Footer link is always shown and redirects to 'Live Stream' page
        """
        in_play_and_live_stream_sports = self.in_play_live_stream.menu_carousel.items_as_ordered_dict
        sport_name_counter = {sport_name: sport.counter for sport_name, sport in in_play_and_live_stream_sports.items()
                              if sport.counter != 0}
        live_stream_events_count_on_home_page = sum(list(sport_name_counter.values()))
        try:
            footer_link = self.site.home.desktop_modules.inplay_live_stream_module.view_all_live_stream_sport_events_button
        except:
            footer_link = None

        self.assertIsNotNone(footer_link, "footer link is not displayed")
        footer_link.click()
        self.site.wait_content_state_changed()

        tabs = self.site.live_stream.tabs_menu.items_as_ordered_dict
        live_now = next((tab for tab_name, tab in tabs.items() if tab_name.upper() == "LIVE NOW"), None)
        live_stream_events_count_on_live_stream_page = live_now.event_count
        self.assertEqual(int(live_stream_events_count_on_live_stream_page), live_stream_events_count_on_home_page,
                         f'Actual Live Stream Events Count "{live_stream_events_count_on_live_stream_page}" in not same as Expected Live Stream Event Count "{live_stream_events_count_on_home_page}" ')

    def test_010_click_on_any_selection_from_the_widget(self):
        """
        DESCRIPTION: Click on any selection from the widget
        EXPECTED: Selection is successfully added to Betslip
        EXPECTED: Selection is marked as added in 'In-Play &amp; Live Stream' section
        """
        self.site.back_button.click()
        self.site.login()
        self.__class__.in_play_live_stream = self.site.home.desktop_modules.inplay_live_stream_module
        sections = self.in_play_live_stream.tab_content.accordions_list.items_as_ordered_dict
        section_name, section = next(iter(sections.items()))
        event_name, event = next(iter(section.items_as_ordered_dict.items()))
        selections = event.template.items_as_ordered_dict
        selection_name, random_selection = next(
            ((selection_name, random_selection) for selection_name, random_selection in selections.items() if
             selection_name.upper() not in["SUSP","N/A"]), None)
        random_selection.click()
        self.assertTrue(random_selection.is_selected(),
                        f'bet button "{selection_name}" is not selected after clicking odd')
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.assertFalse(random_selection.is_selected(),
                         f'bet button "{selection_name}" is still selected after bet placed')
        event.click()
        self.site.wait_content_state("EVENTDETAILS")
        event_name_on_edp = self.site.sport_event_details.header_line.page_title.text.upper()
        self.assertEqual(event_name_on_edp, event_name.upper(),
                         f'Actual Event Detail Page : "{event_name_on_edp}" Expected Event Detail Page : "{event_name}"')

    def test_011_place_a_bet_for_added_selection(self):
        """
        DESCRIPTION: Place a bet for added selection
        EXPECTED: Bet is placed successfully
        EXPECTED: Selection is unmarked in 'In-Play &amp; Live Stream' section
        """
        # covered in above step

    def test_012_click_on_event_card_section(self):
        """
        DESCRIPTION: Click on Event card section
        EXPECTED: User is redirected to Event Details page
        """
        # covered in above step
