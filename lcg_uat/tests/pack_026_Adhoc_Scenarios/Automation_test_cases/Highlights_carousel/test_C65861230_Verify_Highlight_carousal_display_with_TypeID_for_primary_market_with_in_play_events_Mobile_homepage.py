import re
import voltron.environments.constants as vec
import tests
import pytest
from collections import OrderedDict
from datetime import datetime
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    BaseHighlightsCarouselTest, generate_highlights_carousel_name
from voltron.pages.shared.components.home_page_components.highlight_carousel import HighlightCarousel
from voltron.utils.waiters import wait_for_cms_reflection, wait_for_result

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.highlights_carousel
@pytest.mark.adhoc_suite
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65861230_Verify_Highlight_carousal_display_with_TypeID_for_primary_market_with_in_play_events_Mobile_homepage(BaseHighlightsCarouselTest):
    """
    TR_ID: C65861230
    NAME: Verify Highlight carousal display with TypeID for primary market with in-play events_Mobile homepage
    DESCRIPTION: This test case is to verify Highlight carousal display with TypeID for primary market with in-play events_Mobile homepage
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS Navigation:
    PRECONDITIONS: CMS > sports pages >home page> Highlights Carousel and click on Create Highlights Carousel CTA.
    PRECONDITIONS: Configure HC as below by giving all the fields.
    PRECONDITIONS: *Enable "Active & Display on Desktop" check boxes
    PRECONDITIONS: *Title=TENNIS - POLAND TT ELITE SERIES MEN'S
    PRECONDITIONS: *Set events by=TypeID
    PRECONDITIONS: *TypeID= 102263 (with inplay events)
    PRECONDITIONS: *Select Market & Market Type = Primary Market
    PRECONDITIONS: *Display from & Display to time period (eg: from 7/6/2023 11:05:34 to 7/7/2023 11:05:34)
    PRECONDITIONS: *SVG Icon=tennis
    PRECONDITIONS: *No. of Events = 5
    PRECONDITIONS: *Enable Display In-Play checkbox
    PRECONDITIONS: *Select Universal view
    """
    keep_browser_open = True
    highlights_carousels_title = generate_highlights_carousel_name()
    highlights_carousels_typeID = None
    type_id_to_exclude = ['117307', '127189', '127197']
    segment = vec.bma.CSP_CMS_SEGEMENT
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    csp_user = tests.settings.betplacement_user

    def reset_and_verify_hc(self, name=None):
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        start_time = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                             hours=-10)[
                     :-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, days=1,
                                           hours=-10)[
                   :-3] + 'Z'
        self.cms_config.update_highlights_carousel(self.highlights_carousel, start_time=start_time, end_time=end_time,
                                                   disabled=False)
        highlights_carousel = self.get_highlight_carousel(name=name)
        self.assertTrue(highlights_carousel, msg=f"Highlight carousel with name '{name}' not found after reset time")

    def get_current_live_events_for_created_highlight_carousel(self, highlight_carousel: HighlightCarousel = None):
        pattern = r'\d+-\d+'  # Regular expression pattern to match the number1-number2 format

        def replace_random_number(match):
            return ' V '  # Replacing the matched number1-number2 format with ' v '

        filtered_events = []
        for event in self.all_live_events_for_type:
            is_watch_live = any(tag in event['drilldownTagNames'] for tag in
                                ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM'])

            filtered_event = {
                'name': re.sub(pattern, replace_random_number, event['name'].upper()),
                'isWatchLive': is_watch_live
            }
            filtered_events.append(filtered_event)

        live_hc_items = OrderedDict()
        for name, value in highlight_carousel.items_as_ordered_dict.items():
            for event in filtered_events:
                if event['name'].upper() == name.upper():
                    live_hc_items[name] = {
                        "value": value,
                        "isWatchLive": event['isWatchLive']
                    }

        return live_hc_items

    def get_highlight_carousel(self, name=None, expected_result=True):
        if self.site.brand == 'ladbrokes':
            name = name.upper()
        highlight_carousal = wait_for_cms_reflection(
            lambda: self.site.home.tab_content.highlight_carousels.get(name),
            ref=self,
            timeout=5,
            haul=0,
            refresh_count=3,
            expected_result=expected_result
        )
        return highlight_carousal

    def get_type_id_for_HC(self):
        all_events_for_tennis = self.get_active_events_for_category(
            category_id=self.ob_config.tennis_config.category_id,
            all_available_events=True, in_play_event=True)

        # Remove duplicates based on the 'name' property
        unique_events = []
        seen_event_names = set()
        for event in all_events_for_tennis:
            event_name = event['event']['name']
            if event_name not in seen_event_names:
                unique_events.append(event)
                seen_event_names.add(event_name)

        type_dict = {}
        for event in unique_events:
            event = event['event']
            if event['typeId'] not in self.type_id_to_exclude:
                if type_dict.get(event['typeId']):
                    type_dict[event['typeId']].append(event)
                else:
                    type_dict[event['typeId']] = [event]

        max_type = max(type_dict, key=lambda x: len(type_dict[x]))
        max_events = type_dict[max_type]
        max_events_length = len(max_events)

        return max_type, max_events_length, max_events

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create Event hub and tag this event hub to Module ribbon tab,
        PRECONDITIONS: Event Hub - Highlights Carousel Creation in CMS:
        """
        if tests.settings.backend_env != 'prod':
            self.__class__.all_live_events_for_type = []
            self.__class__.highlights_carousels_typeID = self.ob_config.tennis_config \
                .tennis_autotest.autotest_trophy.type_id
            for i in range(1, 9):
                response = self.ob_config.add_tennis_event_to_autotest_trophy(is_live=True, perform_stream=True)
                self.all_live_events_for_type.append(response.ss_response['event'])
            self.__class__.events_length = len(self.all_live_events_for_type)
        else:
            self.__class__.highlights_carousels_typeID, self.__class__.events_length, \
                self.__class__.all_live_events_for_type = self.get_type_id_for_HC()
        self.__class__.svg_icon = 'tennis'
        self.__class__.highlights_carousel = self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title,
                                                                         typeId=self.highlights_carousels_typeID,
                                                                         page_type='sport',
                                                                         limit=self.events_length,
                                                                         displayOnDesktop=True,
                                                                         svgId=self.svg_icon,
                                                                         inplay=True)

    def test_001_launch_bma_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch BMA Ladbrokes/Coral Application
        EXPECTED: User should able to launch successfully
        """
        self.site.login()
        self.site.wait_content_state(state_name='Homepage')

    def test_002_verify_created_highlight_carousal_displaying_on_fe(self):
        """
        DESCRIPTION: Verify created Highlight carousal displaying on FE
        EXPECTED: Created HC should display on featured/highlights tab
        """
        self.__class__.actual_highlight_carousel = self.get_highlight_carousel(name=self.highlights_carousels_title)
        self.assertTrue(self.actual_highlight_carousel,
                        msg=f"Created Highlight Carousel {self.highlights_carousels_title} is not displayed")

    def test_003_verify_the_order_of_the_highlights_carousel_module_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the Highlights Carousel module is as per order in the CMS
        EXPECTED: The order should be as per CMS
        """
        # Covered In another testcase C5861232

    def test_004_change_the_order_in_the_cms_in_the_application_refresh_the_page_and_verify_the_order_is_updated(self):
        """
        DESCRIPTION: Change the order in the CMS. In the application refresh the page and verify the order is updated
        EXPECTED: The order is updated and is as defined in the CMS
        """
        # Covered In another testcase C5861232

    def test_005_verify_title_amp_svg_icon(self):
        """
        DESCRIPTION: Verify title &amp; SVG Icon
        EXPECTED: HC title  &amp; SVG Icon should be as per cms. Title should be in capitals
        """

        expected_title = self.highlights_carousels_title.upper()
        actual_title = self.actual_highlight_carousel.name.upper()
        self.assertEqual(expected_title, actual_title, msg=f"Highlight carousels title should be {expected_title}"
                                                           f"but got {actual_title}")
        expected_svg_icon = f'#{self.svg_icon}'
        actual_svg_icon = self.actual_highlight_carousel.svg_icon_text
        self.assertEqual(expected_svg_icon, actual_svg_icon, msg=f"Highlight carousels svg icon"
                                                                 f"should be{expected_svg_icon}"
                                                                 f"but found {actual_svg_icon}")

    def test_006_go_to_cms_and_edit_the_title_amp_svg_icon_and_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS and Edit the title &amp; SVG Icon and save changes. Verify on FE
        EXPECTED: Title &amp; SVG Icon should be updated on Homepage as per cms changes
        """
        self.__class__.modified_highlights_carousel_title = f'{self.highlights_carousels_title} modified'
        modified_svg_icon = "icon-tennis"
        self.cms_config.update_highlights_carousel(self.highlights_carousel, title=self.modified_highlights_carousel_title,
                                                   svgId=modified_svg_icon, disabled=False)
        # ******** Verification of Highlight Carousel title and SVG icon *************************
        self.__class__.modified_highlight_carousel = self.get_highlight_carousel(name=self.modified_highlights_carousel_title)
        self.assertTrue(self.modified_highlight_carousel, msg=f'{self.modified_highlights_carousel_title} '
                                                         f'highlight carousel is not available')
        self.assertEqual(self.modified_highlight_carousel.svg_icon_text,
                         f'#{modified_svg_icon}', f'Svg icon {modified_svg_icon} is not displayed')

    def test_007_verify_hc_see_all_link_amp_navigation(self):
        """
        DESCRIPTION: Verify HC SEE ALL link &amp; Navigation
        EXPECTED: SEE ALL link should display &amp; upon clicking it should navigate to competition detail page
        """
        self.assertTrue(self.modified_highlight_carousel.has_see_all_link(),
                        msg=f"See all link for {self.modified_highlight_carousel.name}"
                            f"is not displayed")
        see_all_link = self.modified_highlight_carousel.see_all_link
        see_all_link.click()
        self.site.wait_content_state('CompetitionLeaguePage', timeout=10)

    def test_008_click_on_back(self):
        """
        DESCRIPTION: Click on Back
        EXPECTED: It should redirect to Homepage &amp; HC order should be same
        """
        self.site.back_button_click()
        self.site.wait_content_state("Home")

    def test_009_verify_live_watch_live_icons_display(self, check_live=True):
        """
        DESCRIPTION: Verify live, watch live icons display
        EXPECTED: Live, watch live icons should display for inplay events
        """
        self.__class__.modified_highlights_carousel = self.get_highlight_carousel(
            name=self.modified_highlights_carousel_title)
        live_events_for_HC = self.get_current_live_events_for_created_highlight_carousel(
            highlight_carousel=self.modified_highlights_carousel)
        for event_name, event in live_events_for_HC.items():
            event_object = event['value']
            live_icon = wait_for_result(lambda: event_object.live_button, expected_result=True, timeout=1)
            # watch_live_button
            if check_live:
                self.assertTrue(live_icon, msg=f"Live icon for event inplay '{event_name} not found'")
                if event['isWatchLive']:
                    self.assertTrue(event_object.watch_live_button,
                                    msg=f"Watch Live icon for event inplay '{event_name} not found'")
            else:
                self.assertFalse(live_icon, msg=f"Live icon for event inplay '{event_name} Found'")

    def test_010_verify_hc_price_and_score_updates_color_change_as_per_brand_for_in_play_event(self):
        """
        DESCRIPTION: Verify HC price and score updates, color change as per brand for in-play event
        EXPECTED: Price and score updates, color change should happen
        """
        # Only for Stage

    def test_011_verify_hc_display_from_amp__to_as_per_cms(self):
        """
        DESCRIPTION: Verify HC display from &amp;  to as per CMS
        EXPECTED: Highlights Carousel is displayed as current date and time belong to time box set by Display from and Display to date and time fields
        """
        # covered in step 2
        self.reset_and_verify_hc(name=self.modified_highlights_carousel_title)

    def test_012_go_to_cms_set_display_from_and_display_to_date_and_time_as_time_range_from_the_pastfuture_and_save_changes(
            self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' and 'Display to' date and time as time range from the past/future and save changes.
        EXPECTED: The changes are saved
        """
        # already covered in C65861228 in 12th step

    def test_013_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: Highlights Carousel should not be displayed
        """
        # already covered in C65861228 in 13 step

    def test_014_go_to_cms_set_display_from_from_the_past_and_display_to_in_a_few_mins_from_the_current_time_and_save_changes(
            self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' from the past and 'Display to' in a few mins from the current time and save changes.
        EXPECTED: Changes are saved
        """
        # already covered in C65861228 in 14 step

    def test_015_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display to' is passed Highlights Carousel is no more shown on Homepage
        """
        # already covered in C65861228 in 15 step

    def test_016_go_to_cms_set_display_from_in_a_few_mins_from_current_time_and_display_to_from_the_future_and_save_changes(
            self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' in a few mins from current time and 'Display to' from the future and save changes.
        EXPECTED: Changes are saved
        """
        # already covered in C65861228 in step 16

    def test_017_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display from' is passed Highlights Carousel should appears
        """
        # already covered in C65861228 in step 17

    def test_018_verify_hc_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify HC left and right scroll
        EXPECTED: User should able to scroll from left to right &amp; from right to left
        """
        number_of_events = len(wait_for_result(lambda: self.modified_highlights_carousel.items_as_ordered_dict,
                                               timeout=5))
        if number_of_events > 3:
            next_scroll = self.modified_highlights_carousel.scroll_next_button
            first_event_name, first_event = self.modified_highlights_carousel.items_as_ordered_dict[0]
            self.assertTrue(first_event.is_displayed(), msg=f'First event with name {first_event_name} is not displayed'
                                                            f'even if next scroll action is not performed')
            next_scroll.click()
            self.assertFalse(first_event.is_displayed(), msg=f'First event with name {first_event_name} is displayed'
                                                             f'even if next scroll action is not performed')
            prev_scroll = self.modified_highlights_carousel.scroll_previous_button
            prev_scroll.click()
            self.assertTrue(first_event.is_displayed(), msg=f'First event with name {first_event_name} is not displayed'
                                                            f'even if previous scroll action is not performed')
        else:
            self.site._logger.info(f"Cannot verify HC: {self.modified_highlights_carousel_title} "
                                   f"left and right scroll since number of events is less than 3 for")

    def test_019_verify_hc_display_with_greencoralorangelads_dots_for_inplay_events(self):
        """
        DESCRIPTION: Verify HC display with green(coral)/orange(lads) dots for inplay events
        EXPECTED: HC should display with green(coral)/orange(lads) dots
        """
    #     can not automate

    def test_020_verify_the_chevron_on_hc_event_cardamp_navigation(self):
        """
        DESCRIPTION: Verify the chevron on HC event card&amp; navigation
        EXPECTED: Chevron should be in blue color and aligned to right &amp; upon clicking on it should redirect to EDP of that event
        """
        highlight_carousel = self.get_highlight_carousel(name=self.modified_highlights_carousel_title)
        event = list(highlight_carousel.items_as_ordered_dict.items())[0][1]
        blue_chevron = event
        blue_chevron.click()
        self.site.wait_content_state("EVENTDETAILS")
        self.site.back_button_click()
        self.site.wait_content_state(state_name='Homepage', timeout=20)

    def test_021_verify_the_set_details_amp_score_detailssgp_fot_tennis_inplay_events(self):
        """
        DESCRIPTION: Verify the set details &amp; score details(S,G,P) fot tennis inplay events
        EXPECTED: Set 'n' and S,G,P scores should display &amp; align properly
        """
        highlight_carousel = self.get_highlight_carousel(name=self.modified_highlights_carousel_title)
        event = list(highlight_carousel.items_as_ordered_dict.items())[0][1]
        column_headers = event.score_column_headers
        for header in ["S", "G", "P"]:
            self.assertIn(header, column_headers.keys(), msg=f"{header} is not in {column_headers.keys()}")

    def test_022_verify_hc_no_of_events_display(self):
        """
        DESCRIPTION: Verify HC No of events display
        EXPECTED: No of events should display on HC should be as per cms value
        """
        #can not verified because after event is suspended it wont be visible in ui

    def test_023_go_to_cms_change_no_of_events_amp_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, change No of events &amp; save changes. Verify on FE
        EXPECTED: No of events on HC should update as per cms changes
        """
        expected_event_count = 1
        self.cms_config.update_highlights_carousel(self.highlights_carousel, limit=expected_event_count)
        modified_highlights_carousel_title_name = self.modified_highlights_carousel_title.upper() if self.brand == 'ladbrokes' else self.modified_highlights_carousel_title
        is_events_count_equal = wait_for_cms_reflection(
            lambda: len(self.site.home.tab_content.highlight_carousels.get(
                modified_highlights_carousel_title_name).items_names) == expected_event_count, timeout=5,
            refresh_count=2, ref=self, expected_result=True)
        self.assertTrue(is_events_count_equal,
                        msg=f"updated events limit count is not matched with expected events limit count {expected_event_count} ")

    def test_024_verify_hc_display_in_play(self):
        """
        DESCRIPTION: Verify HC display in play
        EXPECTED: HC with inplay events should display on FE only if display inplay is enabled in cms
        """
        self.assertTrue(self.highlights_carousel['inPlay'], msg=f'Inplay is Not enabled '
                                                                 f'in cms for HC {self.modified_highlights_carousel_title}')
        self.test_009_verify_live_watch_live_icons_display()

    def test_025_go_to_cms_disable_display_in_play_checkbox_verify_on_fe(self):
        """
        DESCRIPTION: Go to cms, disable display in play checkbox. Verify on FE
        EXPECTED: HC with In play events should not display on Homepage
        """
        # already covered in C65861228 in step 25
        # self.cms_config.update_highlights_carousel(self.highlights_carousel, inPlay=False)
        # self.test_009_verify_live_watch_live_icons_display(check_live=False)

    def test_026_verify_the_match_time_on_event_card_for_football_inplay_events(self):
        """
        DESCRIPTION: Verify the match time on event card for Football inplay events
        EXPECTED: Match time should display on HC event card
        """
        # Cannot verify time on event card for live tennis

    def test_027_verify_selections_are_displaying_properly_according_to_the_sportsmarkets_in_hc(self):
        """
        DESCRIPTION: Verify selections are displaying properly according to the sports/markets in HC
        EXPECTED: Selections should display according to the sports/markets (eg: for football HOME DRAW AWAY,for tennis 1 2)
        """
        # Covered In another testcase C5861232

    def test_028_verify_hc_sorting_order_as_per_cms(self):
        """
        DESCRIPTION: Verify HC sorting order as per cms
        EXPECTED: HC should display as per cms sort order
        """
        # Covered In another testcase C5861232

    def test_029_change_the_hc_order_in_highlights_carousel_module_page_in_cms_verify_on_fe(self):
        """
        DESCRIPTION: Change the HC order in Highlights Carousel module page in cms. Verify on FE
        EXPECTED: HC order should change &amp; display as per cms order on FE
        """
        # Covered In another testcase C5861232

    def test_030_verify_user_can_able_to_select_the_selections_on_hc(self):
        """
        DESCRIPTION: Verify user can able to select the selections on HC
        EXPECTED: User should able to select &amp; selections should be highlighted
        """
        # Covered In another testcase C5861232

    def test_031_verify_univeral_view_for_hc(self):
        """
        DESCRIPTION: Verify Univeral view for HC
        EXPECTED: HC should display for all  loggedin &amp; loggedout users
        """
        # ******** Verification of Highlight Carousel for logged out user *************************
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')
        hc = self.get_highlight_carousel(name=self.modified_highlights_carousel_title)
        self.assertTrue(hc, msg=f"{self.modified_highlights_carousel_title} highlight carousel is not displayed")

    def test_032_go_to_cms_change_to_segment_view_amp_select_any_segment_from_inclusion_segments_and_save_changes_verify_on_fe(
            self):
        """
        DESCRIPTION: Go to cms, change to segment view &amp; select any segment from inclusion segments and save changes. Verify on FE
        EXPECTED: HC should display to only segmented users which configured in cms
        """
        if self.device_type == 'mobile':
            # ******** Updation of Highlight Carousel to segment view *************************
            self.cms_config.update_highlights_carousel(self.highlights_carousel, inclusionList=[self.segment])
            # ******** Verification of Highlight Carousel for logged in user *************************
            self.site.login(username=self.csp_user)
            self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
            hc_view_for_segmented = self.get_highlight_carousel(self.modified_highlights_carousel_title)
            self.assertTrue(hc_view_for_segmented, msg=f"Highlight Carousel for segmented user is not displayed")

    def test_033_verify_team_namesplayer_names_on_hc(self):
        """
        DESCRIPTION: Verify Team names/Player names on HC
        EXPECTED: Team names/Player names should properly display &amp; aligned to the left
        """
       # covered in test_002_verify_created_highlight_carousal_displaying_on_fe

    def test_034_verify_hc_navigation_when_the_user_clicks_anywhere_on_the_event_card_except_the_odds_button(self):
        """
        DESCRIPTION: Verify HC navigation when the user clicks anywhere on the event card (except the odds button
        EXPECTED: User should navigate to the EDP of the event
        """
        # Covered in 20th step

    def test_035_verify_team_kits_when_hc_is_configured_using_the_type_id_for_the_football_premier_or_champions_league(
            self):
        """
        DESCRIPTION: Verify team kits when HC is configured using the Type ID for the football premier or Champions league
        EXPECTED: HC with the team kits should display
        """
        # Covered in Football HC test

    def test_036_go_to_cms_deactivate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, deactivate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousels should not be displayed
        """
        # Cannot deactivate module

    def test_037_go_to_cms_activate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, activate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousel should display on homepage
        """
        # Cannot deactivate module

    def test_038_verify_display_of_event_cards_when_the_event_is_resulted_in_hc(self):
        """
        DESCRIPTION: Verify display of event cards when the event is resulted in HC
        EXPECTED: The card of the resulted event should be removed from the HC automatically
        """
        # Cannot Verify since we cannot suspend/set the event in beta

    def test_039_verify_display_of_hc_when_there_is_only_1_event_card_available_to_be_displayed__amp_that_event_is_resulted(
            self):
        """
        DESCRIPTION: Verify display of HC when there is only 1 event card available to be displayed  &amp; that event is resulted
        EXPECTED: The card should be removed from HC and the HC should be removed from the page
        """
        # Cannot Verify since we cannot suspend/set the event in beta

    def test_040_go_back_to_the_same_highlights_carousel_in_cms_unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Highlights Carousel in CMS, unselect 'Active' checkbox and save changes
        EXPECTED: a)Existing Highlights Carousel is inactive
        EXPECTED: b)Changes is saved successfully
        """
        self.cms_config.update_highlights_carousel(self.highlights_carousel, disabled=True)

    def test_041_load_oxygen_app_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Highlights Carousel displaying
        EXPECTED: a) Highlights Carousel is NOT displayed on Front End
        EXPECTED: b) If we have other Highlights Carousel with valid date it should display
        """
        # ******** Verification of Highlight Carousel *************************
        hc = self.get_highlight_carousel(name=self.modified_highlights_carousel_title,
                                    expected_result=False)
        self.assertFalse(hc, msg=f"{self.modified_highlights_carousel_title} highlight carousel is displayed")
        # ******** Updation of Highlight Carousel to Active State *************************
        self.cms_config.update_highlights_carousel(self.highlights_carousel, disabled=False)
        # ******** Verification of Highlight Carousel *************************
        hc = self.get_highlight_carousel(name=self.modified_highlights_carousel_title)
        self.assertTrue(hc, msg=f"{self.modified_highlights_carousel_title} highlight carousel is not displayed")

    def test_042_go_to_cms_remove_created_hc_amp_confirm_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, Remove created HC &amp; confirm. Verify on FE
        EXPECTED: HC should disappear on FE
        """
        # ******** Removing Highlight Carousel *************************
        highlight_carousel_id = self.highlights_carousel["id"]
        self.cms_config.delete_highlights_carousel(highlight_carousel_id)
        self.cms_config._created_highlights_carousels.remove(highlight_carousel_id)
        # ******** Verification of Highlight Carousel *************************
        hc = self.get_highlight_carousel(name=self.modified_highlights_carousel_title, expected_result = False)
        self.assertFalse(hc, msg=f"{self.modified_highlights_carousel_title} highlight carousel is displayed")