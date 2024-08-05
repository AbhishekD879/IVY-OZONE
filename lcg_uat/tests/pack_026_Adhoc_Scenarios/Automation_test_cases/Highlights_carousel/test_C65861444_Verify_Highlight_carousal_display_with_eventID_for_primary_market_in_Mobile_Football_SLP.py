import pytest
from crlat_cms_client.utils.exceptions import CMSException
import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    BaseHighlightsCarouselTest, generate_highlights_carousel_name
from voltron.utils.waiters import wait_for_cms_reflection, wait_for_haul


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
@pytest.mark.adhoc_suite
@pytest.mark.highlights_carousel
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C65861444_Verify_Highlight_carousal_display_with_eventID_for_primary_market_in_Mobile_Football_SLP(BaseHighlightsCarouselTest):
    """
    TR_ID: C65861444
    NAME: Verify Highlight carousal display with eventID for primary market in Mobile Football SLP
    DESCRIPTION: This test case is to verify Highlight carousal display with eventID for primary market in Mobile Football SLP
    PRECONDITIONS: 1. User should have admin access to CMS.
    PRECONDITIONS: 2. CMS Navigation:
    PRECONDITIONS: CMS &gt; sports pages &gt;Sports Category&gt;Football&gt; Highlights Carousel and click on Create Highlights Carousel CTA.
    PRECONDITIONS: 3. Configure HC as below by giving all the fields.
    PRECONDITIONS: *Enable "Active" Check box
    PRECONDITIONS: *Title=Football - SLP
    PRECONDITIONS: *Set events by=Event IDs
    PRECONDITIONS: *Event IDs= 240767310,240778313
    PRECONDITIONS: *Select Market & Market Type = Primary Market
    PRECONDITIONS: *Display from & Display to time period (eg: from 7/6/2023 11:05:34 to 7/7/2023 11:05:34)
    PRECONDITIONS: *SVG Icon=football
    PRECONDITIONS: *No. of Events = 2
    PRECONDITIONS: *Select Universal view
    """
    keep_browser_open = True
    svg_icon = "football"

    def check_hc_module_status_and_create_hightlight_carousel(self, hc_title=None, events_list=[], events_count=1,
                                                              svg_icon=svg_icon):
        sports_module = self.cms_config.get_sport_module(module_type=None,sport_id=16)
        hc_module_cms = None
        for module in sports_module:
            if module['moduleType'] == 'HIGHLIGHTS_CAROUSEL':
                hc_module_cms = module
                break
        if hc_module_cms is None:
            raise CMSException("Highlight carousel module not found in CMS")
        else:
            highlights_module_status = next((module['disabled'] for module in sports_module
                                        if module['moduleType'] == 'HIGHLIGHTS_CAROUSEL'), None)
            if highlights_module_status:
                self.cms_config.change_sport_module_state(sport_module=hc_module_cms)
        highlights_carousel = self.cms_config.create_highlights_carousel(
            title=hc_title,
            events=events_list, limit=events_count, svgId=svg_icon, sport_id=16, displayOnDesktop=True)
        return highlights_carousel

    def verify_highlight_carousel_on_football_slp(self, highlights_carousel_title=None, expected_result=True,
                                                  refresh_count=3,
                                                  timeout=1):
        if expected_result:
            HC = wait_for_cms_reflection(
                lambda: self.site.football.tab_content.highlight_carousels.get(highlights_carousel_title),
                refresh_count=refresh_count, ref=self, timeout=timeout, haul=5)
            self.assertTrue(HC,
                            msg=f'{highlights_carousel_title} is not available')
            return HC
        else:
            hcs = self.site.football.tab_content.highlight_carousels
            if hcs:
                section = wait_for_cms_reflection(
                    lambda: self.site.football.tab_content.highlight_carousels.get(highlights_carousel_title),
                    refresh_count=3, ref=self, expected_result=False)
                self.assertFalse(section,
                                 msg=f'{highlights_carousel_title} is available')

    def test_000_preconditions(self):
        """
        User should have admin access to CMS.
        CMS Navigation:
        CMS > sports pages >Sports Category>Football> Highlights Carousel and click on Create Highlights Carousel CTA.
        """
        self.__class__.highlights_carousel_title = self.convert_highlights_carousel_title(
            title=generate_highlights_carousel_name())
        self.__class__.expected_highlights_carousel_events = []
        self.__class__.events_start_time = {}
        if tests.settings.backend_env == 'prod':
            # ******** Getting Events ********
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)
            # ******** Getting event id  ********
            self.__class__.eventID1 = events[0]['event']['id']
            self.__class__.eventID2 = events[1]['event']['id']
            self.__class__.eventID3 = events[2]['event']['id']
            # ******** Getting Selection IDs ********
            outcomes = next(((market['market']['children']) for market in events[0]['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(event_selection.values())[0]
            # ******** Events list and Events start time ********
            for i in range(2):
                # ******** events list ********
                self.expected_highlights_carousel_events.append(events[i]['event']['name'].upper().strip())
                # ******** events start time list ********
                self.events_start_time[events[i]['event']['name'].upper()] = events[i]['event']['startTime']

        else:
            # ******** Getting Events ********
            event1 = self.ob_config.add_tennis_event_to_autotest_trophy()
            event2 = self.ob_config.add_tennis_event_to_autotest_trophy()
            event3 = self.ob_config.add_tennis_event_to_autotest_trophy()
            # ******** Getting Event id ********
            self.__class__.eventID1 = event1.event_id
            self.__class__.eventID2 = event2.event_id
            self.__class__.eventID3 = event3.event_id
            # ******** Getting Selection IDs ********
            self.__class__.selection_id = event1.selection_ids[event1.team1]
            # ******** Events list and Events start time ********
            event1_name = event1.team1 + ' v ' + event1.team2
            event2_name = event2.team1 + ' v ' + event2.team2
            self.__class__.expected_highlights_carousel_events = [event1_name.upper(), event2_name.upper()]
            self.events_start_time[0] = event1.event_date_time
            self.events_start_time[1] = event2.event_date_time

        self.__class__.highlights_carousel_event_ids = [self.eventID1, self.eventID2]
        # ******** Creation of Highlights Carousel *************************
        self.__class__.highlights_carousel_response = self.check_hc_module_status_and_create_hightlight_carousel(
                hc_title=self.highlights_carousel_title, events_list=self.highlights_carousel_event_ids, events_count=2,
                svg_icon=self.svg_icon)

    def test_001_launch_bma_ladbrokescoral_application_on_mobile(self):
        """
        DESCRIPTION: Launch BMA Ladbrokes/Coral Application on mobile
        EXPECTED: User should  be able to launch successfully
        """
        self.site.login()
        self.site.wait_content_state("HOMEPAGE")

    def test_002_navigate_to_football_sport(self):
        """
        DESCRIPTION: Navigate to Football Sport
        EXPECTED: Football SLP is loaded
        """
        self.navigate_to_page("sport/football")
        self.site.wait_content_state("football")

    def test_003_verify_created_highlight_carousal_displaying_on_fe(self):
        """
        DESCRIPTION: Verify Created Highlight carousal displaying on FE
        EXPECTED: Created HC should display on Football SLP.
        """
        # ******** Verification of Highlight Carousel *************************
        self.__class__.section = self.verify_highlight_carousel_on_football_slp(
            highlights_carousel_title=self.highlights_carousel_title)
        # ******** Verification of Highlight Carousel events *************************
        actual__highlights_carousel_events = [item_name.upper() for item_name in self.section.items_names]
        self.assertListEqual(self.expected_highlights_carousel_events, actual__highlights_carousel_events,
                             msg=f'actual highlights carousel events {actual__highlights_carousel_events} not equals to expected highlights carousel events {self.expected_highlights_carousel_events}')
        # ******** Verification of SVG icon *************************
        self.assertEqual(self.section.svg_icon_text,
                         f'#{self.svg_icon}', f'Svg icon {self.svg_icon} is not displayed')

    def test_004_verify_the_order_of_the_highlights_carousel_module_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the Highlights Carousel module is as per order in the CMS
        EXPECTED: The order should be as per CMS
        """
        #covered in test case C65861232

    def test_005_change_the_order_in_the_cms_in_the_application_refresh_the_page_and_verify_the_order_is_updated(self):
        """
        DESCRIPTION: Change the order in the CMS. In the application refresh the page and verify the order is updated
        EXPECTED: The order is updated and is as defined in the CMS
        """
        #covered in test case C65861232

    def test_006_verify_title_amp_svg_icon(self):
        """
        DESCRIPTION: Verify title &amp; SVG Icon
        EXPECTED: HC title  &amp; SVG Icon should be as per cms. Title should be in capitals
        """
        # Covered in test_002_verify_created_highlight_carousal_displaying_on_football_slp

    def test_007_go_to_cms_and_edit_the_title_amp_svg_icon_and_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS and Edit the title &amp; SVG Icon and save changes. Verify on FE
        EXPECTED: Title &amp; SVG Icon should be updated on Football SLP as per cms changes
        """
        #covered in test case C65861232

    def test_008_verify_hc_display_from_amp__to_as_per_cms(self):
        """
        DESCRIPTION: Verify HC display from &amp;  to as per CMS
        EXPECTED: Highlights Carousel is displayed as current date and time belong to time box set by Display from and Display to date and time fields
        """
        #covered in test case C65861232

    def test_009_go_to_cms_set_display_from_and_display_to_date_and_time_as_time_range_from_the_pastfuture_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' and 'Display to' date and time as time range from the past/future and save changes.
        EXPECTED: The changes are saved
        """
        #covered in test case C65861232

    def test_010_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: Highlights Carousel should not be displayed
        """
        #covered in test case C65861232

    def test_011_go_to_cms_set_display_from_from_the_past_and_display_to_in_a_few_mins_from_the_current_time_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' from the past and 'Display to' in a few mins from the current time and save changes.
        EXPECTED: Changes are saved
        """
        #covered in test case C65861232

    def test_012_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display to' is passed Highlights Carousel is no more shown on Football SLP
        """
        #covered in test case C65861232

    def test_013_go_to_cms_set_display_from_in_a_few_mins_from_current_time_and_display_to_from_the_future_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' in a few mins from current time and 'Display to' from the future and save changes.
        EXPECTED: Changes are saved
        """
        #covered in test case C65861232

    def test_014_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display from' is passed Highlights Carousel should appears
        """
        #covered in test case C65861232

    def test_015_verify_hc_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify HC left and right scroll
        EXPECTED: User should able to scroll from left to right &amp; from right to left
        """
        # covered in C65861228 test case

    def test_016_verify_the_chevron_on_hc_event_card_amp_navigation(self):
        """
        DESCRIPTION: Verify the chevron on HC event card &amp; navigation
        EXPECTED: Chevron should be in blue color and aligned to right &amp; upon clicking on it should redirect to EDP of that event
        """
        # ******** Verification of Highlight Carousel Events Navigation *************************
        highlight_carousel_events = self.section.items_as_ordered_dict
        self.assertTrue(highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_title}"')
        highlight_carousel_events = {key.upper(): value for key, value in highlight_carousel_events.items()}
        highlight_carousel_events.get(self.expected_highlights_carousel_events[0]).click()
        self.site.wait_content_state(state_name='EventDetails')
        current_url = self.device.get_current_url()
        self.assertIn(self.highlights_carousel_event_ids[0], current_url, msg="event details page not displayed")
        self.site.back_button_click()
        self.site.wait_content_state(state_name='football', timeout=10)
        section = self.verify_highlight_carousel_on_football_slp(highlights_carousel_title=self.highlights_carousel_title)
        self.__class__.highlight_carousel_events = section.items_as_ordered_dict
        self.assertTrue(self.highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_title}"')

    def test_017_verify_the_date_amp_time_of_event_on_hc_event_card(self):
        """
        DESCRIPTION: Verify the date &amp; time of event on HC event card
        EXPECTED: Date &amp; time should display on event card(eg:21:45 Today/00:30 10July)
        """
        # ******** Verification of Highlight Carousel events Date and Time *************************
        self.highlight_carousel_events = {key.upper(): value for key, value in self.highlight_carousel_events.items()}
        for event_name, event in self.highlight_carousel_events.items():
            actual_event_date_time = event.event_time
            future_datetime_format = '%H:%M, %d %b' if self.brand == 'bma' else '%H:%M %d %b'
            ui_format_pattern = '%H:%M, Today' if self.brand == 'bma' else '%H:%M Today'
            expected_event_start_date_time = self.convert_time_to_local(
                date_time_str=self.events_start_time.get(event_name.upper()),
                ob_format_pattern=self.ob_format_pattern,
                ss_data=True, future_datetime_format=future_datetime_format,
                ui_format_pattern=ui_format_pattern)
            self.assertEqual(expected_event_start_date_time, actual_event_date_time,
                             msg=f"expected event start date time {expected_event_start_date_time} is not matched with actual event start date time {actual_event_date_time}")
        # ******** Verification of Highlight Carousel event odds header *************************
        bet_buttons = list(self.highlight_carousel_events.values())[0].get_all_prices()
        expected_list = ['HOME', 'DRAW', 'AWAY']
        actual_list = [button.name.split('\n')[0].upper() for button_name, button in bet_buttons.items()]
        self.assertListEqual(expected_list, actual_list,
                             f'actual headers of odds is {actual_list} is not same as expected odds headers {expected_list}')
        bet_button = next(iter(bet_buttons.values()))
        bet_button.click()
        if self.device_type == 'mobile':
            self.site.quick_bet_panel.close()
        self.assertTrue(bet_button.is_selected(), f'bet button is not selected')

    def test_018_verify_hc_no_of_events_display(self):
        """
        DESCRIPTION: Verify HC No of events display
        EXPECTED: No of events should display on HC should be as per cms value
        """
        #covered in test case C65861232

    def test_019_go_to_cms_change_no_of_events_amp_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, change No of events &amp; save changes. Verify on FE
        EXPECTED: No of events on HC should update as per cms changes
        """
        #covered in test case C65861232

    def test_020_verify_hc_display_as_per_cms_entry_as_per_comma_separation(self):
        """
        DESCRIPTION: Verify HC display as per CMS entry as per comma separation
        EXPECTED: Hc events should display as per comma seperation (eg: if two event id's configured in cms, the first configured event should display first in FE, second configured event should diplay in second place)
        """
        #covered in test_003_verify_created_highlight_carousal_displaying_on_fe

    def test_021_verify_selections_are_displaying_properly_according_to_the_sportsmarkets_in_hc(self):
        """
        DESCRIPTION: Verify selections are displaying properly according to the sports/markets in HC
        EXPECTED: Selections should display according to the sports/markets (eg: for football HOME DRAW AWAY,for tennis 1 2)
        """
        # covered in test_017_verify_the_date_amp_time_of_event_on_hc_event_card

    def test_022_verify_hc_sorting_order_as_per_cms(self):
        """
        DESCRIPTION: Verify HC sorting order as per cms
        EXPECTED: HC should display as per cms sort order
        """
        #covered in test case C65861232

    def test_023_change_the_hc_order_in_highlights_carousel_module_page_in_cms_verify_on_fe(self):
        """
        DESCRIPTION: Change the HC order in Highlights Carousel module page in cms. Verify on FE
        EXPECTED: HC order should change &amp; display as per cms order on FE
        """
        #covered in test case C65861232

    def test_024_verify_user_can_able_to_select_the_selections_on_hc(self):
        """
        DESCRIPTION: Verify user can able to select the selections on HC
        EXPECTED: User should able to select &amp; selections should be highlighted
        """
        #covered in test_017_verify_the_date_amp_time_of_event_on_hc_event_card

    def test_025_verify_univeral_view_for_hc(self):
        """
        DESCRIPTION: Verify Univeral view for HC
        EXPECTED: HC should display for all  loggedin &amp; loggedout users
        """
        # ******** Verification of Highlight Carousel for logged out user *************************
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')
        self.navigate_to_page("sport/football")
        self.site.wait_content_state("football")
        self.verify_highlight_carousel_on_football_slp(highlights_carousel_title=self.highlights_carousel_title)

    def test_026_go_to_cms_change_to_segment_view_amp_select_any_segment_from_inclusion_segments_and_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to cms, change to segment view &amp; select any segment from inclusion segments and save changes. Verify on FE
        EXPECTED: HC should display to only segmented users which configured in cms
        """
        #not applicable for highlight carousel created for sports slp

    def test_027_verify_team_namesplayer_names_on_hc(self):
        """
        DESCRIPTION: Verify Team names/Player names on HC
        EXPECTED: Team names/Player names should properly display &amp; aligned to the left
        """
        #covered in test_003_verify_created_highlight_carousal_displaying_on_fe

    def test_028_verify_hc_navigation_when_the_user_clicks_anywhere_on_the_event_card_except_the_odds_button(self):
        """
        DESCRIPTION: Verify HC navigation when the user clicks anywhere on the event card (except the odds button
        EXPECTED: User should navigate to the EDP of the event
        """
        #covered in test_016_verify_the_chevron_on_hc_event_card_amp_navigation

    def test_029_verify_team_kits_when_hc_is_configured_using_the_event_id_for_the_football_premier_or_champions_league(self):
        """
        DESCRIPTION: Verify team kits when HC is configured using the event ID for the football premier or Champions league
        EXPECTED: HC with the team kits should display
        """
        #covered in test case C6587284

    def test_030_go_to_cms_deactivate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, deactivate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousels should not be displayed
        """
        #Can't deactivate the whole highlight carousel module,it will impact other Hightlight Carousel test cases

    def test_031_go_to_cms_activate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, activate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousel should display on Football SLP
        """
        #Can't deactivate the whole highlight carousel module,it will impact other Hightlight Carousel test cases

    def test_032_verify_display_of_event_cards_when_the_event_is_resulted_in_hc(self):
        """
        DESCRIPTION: Verify display of event cards when the event is resulted in HC
        EXPECTED: The card of the resulted event should be removed from the HC automatically
        """
        #not applicable as it requires settled event

    def test_033_verify_display_of_hc_when_there_is_only_1_event_card_available_to_be_displayed__amp_that_event_is_resulted(self):
        """
        DESCRIPTION: Verify display of HC when there is only 1 event card available to be displayed  &amp; that event is resulted
        EXPECTED: The card should be removed from HC and the HC should be removed from the page
        """
        #not applicable as it requires settled event

    def test_034_go_back_to_the_same_highlights_carousel_in_cms_unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Highlights Carousel in CMS, unselect 'Active' checkbox and save changes
        EXPECTED: a)Existing Highlights Carousel is inactive
        EXPECTED: b)Changes is saved successfully
        """
        #Can't deactivate the whole highlight carousel module,it will impact other Hightlight Carousel test cases

    def test_035_load_oxygen_app_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Highlights Carousel displaying
        EXPECTED: a) Highlights Carousel is NOT displayed on Front End
        EXPECTED: b) If we have other Highlights Carousel with valid date it should display
        """
        #Can't deactivate the whole highlight carousel module,it will impact other Hightlight Carousel test cases

    def test_036_go_to_cms_remove_created_hc_amp_confirm_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, Remove created HC &amp; confirm. Verify on FE
        EXPECTED: HC should disappear on FE
        """
        # ******** Removing Highlight Carousel *************************
        highlight_carousel_id = self.highlights_carousel_response["id"]
        self.cms_config.delete_highlights_carousel(highlight_carousel_id)
        self.cms_config._created_highlights_carousels.remove(highlight_carousel_id)
        wait_for_haul(15)
        # ******** Verification of Highlight Carousel *************************
        self.verify_highlight_carousel_on_football_slp(highlights_carousel_title=self.highlights_carousel_title,
                                                       expected_result=False)
