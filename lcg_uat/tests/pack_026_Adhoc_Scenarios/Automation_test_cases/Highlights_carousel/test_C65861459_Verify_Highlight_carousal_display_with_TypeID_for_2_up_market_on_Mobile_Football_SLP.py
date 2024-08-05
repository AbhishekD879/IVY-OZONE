from datetime import datetime
import pytest
import voltron.environments.constants as vec
from crlat_cms_client.utils.date_time import get_date_time_as_string
import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    BaseHighlightsCarouselTest, generate_highlights_carousel_name
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_cms_reflection

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.highlights_carousel
@pytest.mark.adhoc_suite
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@vtest
class Test_C65861459_Verify_Highlight_carousal_display_with_TypeID_for_2_up_market_on_Mobile_Football_SLP(BaseHighlightsCarouselTest):
    """
    TR_ID: C65861459
    NAME: Verify Highlight carousal display with TypeID for 2 up market on Mobile Football SLP
    DESCRIPTION: This test case is to verify Highlight carousal display with TypeID for 2 up market on Mobile Football SLP
    PRECONDITIONS: 1. User should have admin access to CMS.
    PRECONDITIONS: 2. CMS Navigation:
    PRECONDITIONS: CMS > sports pages >Sports Category>Football> Highlights Carousel and click on Create Highlights Carousel CTA.
    PRECONDITIONS: 3. Configure HC as below by giving all the fields.
    PRECONDITIONS: *Enable "Active" Check box
    PRECONDITIONS: *Title=Football - SLP
    PRECONDITIONS: *Set events by=Event IDs
    PRECONDITIONS: *Event IDs= 240767310,240778313
    PRECONDITIONS: *Select Market & Market Type = 2UP Market
    PRECONDITIONS: *Display from & Display to time period (eg: from 7/6/2023 11:05:34 to 7/7/2023 11:05:34)
    PRECONDITIONS: *SVG Icon=football
    PRECONDITIONS: *No. of Events = 2
    PRECONDITIONS: *Select Universal view
    """
    keep_browser_open = True
    highlights_carousels_title = generate_highlights_carousel_name()
    now = datetime.now()
    svg_icon = "football"
    segment = vec.bma.CSP_CMS_SEGEMENT
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    csp_user = tests.settings.betplacement_user
    end_date = f'{get_date_time_as_string(days=5)}T00:00:00.000Z'

    def convert_highlights_carousel_title(self, title):
        return title if not self.brand == 'ladbrokes' else title.upper()

    def is_expected_market(self, event, market_name):
        if event.get('event') and event['event'].get('children'):
            markets = event['event']['children']
            for market in markets:
                if market['market']['templateMarketName'].replace('|', '') == market_name:
                    return True
        return False

    def get_active_events_for_market(self, events, market_name):
        return [event for event in events if self.is_expected_market(event, market_name)]

    def get_events_for_type(self, all_type_ids, market_name):
        all_events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)
        events_for_type_ids = [event for event in all_events if event['event']['typeId'] in all_type_ids]

        dict_events = {}

        for event in events_for_type_ids:
            if self.is_expected_market(event, market_name):
                if event['event']['typeId'] in dict_events:
                    dict_events[event['event']['typeId']].append(event)
                else:
                    dict_events[event['event']['typeId']] = [event]

        max_type_id, max_events = None, []

        for type_id, events in dict_events.items():
            if len(events) > len(max_events):
                max_type_id = type_id
                max_events = events

        other_events = [event for event in all_events if
                        event['event']['typeId'] == max_type_id and event not in max_events]

        return [max_type_id, max_events, other_events]

    def verify_highlight_carousel_on_football_slp(self, highlights_carousel_title=None, expected_result=True,
                                                  refresh_count=3, timeout=5):
        if expected_result:
            section = wait_for_cms_reflection(
                lambda: self.site.football.tab_content.highlight_carousels.get(highlights_carousel_title),
                refresh_count=refresh_count, ref=self, timeout=timeout, haul=5)
            self.assertTrue(section,
                            msg=f'{highlights_carousel_title} is not available')
            return section
        else:
            section = wait_for_cms_reflection(
                lambda: self.site.football.tab_content.highlight_carousels.get(highlights_carousel_title),
                refresh_count=refresh_count, ref=self ,timeout=timeout, haul=5, expected_result=expected_result)
            self.assertFalse(section,
                             msg=f'{highlights_carousel_title} is available')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: CMS > sports pages >Sports Category>Football> Highlights Carousel and click on Create Highlights Carousel CTA.
        PRECONDITIONS: 3. Configure HC as below by giving all the fields.
        PRECONDITIONS: *Enable "Active" Check box
        PRECONDITIONS: *Title=Football - SLP
        PRECONDITIONS: *Set events by=Event IDs
        PRECONDITIONS: *Event IDs= 240767310,240778313
        PRECONDITIONS: *Select Market & Market Type = 2UP Market
        PRECONDITIONS: *Display from & Display to time period (eg: from 7/6/2023 11:05:34 to 7/7/2023 11:05:34)
        PRECONDITIONS: *SVG Icon=football
        PRECONDITIONS: *No. of Events = 2
        PRECONDITIONS: *Select Universal view
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.expected_template_market = '2Up&Win Early Payout' if self.brand != 'bma' else '2Up - Instant Win'
            all_events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                             all_available_events=True)
            filtered_events = self.get_active_events_for_market(events=all_events,
                                                                market_name=self.expected_template_market)
            if not filtered_events:
                raise SiteServeException(f'there is no active events for {self.expected_template_market}')
            else:
                events = filtered_events
            self.__class__.all_type_ids = [event['event']['typeId'] for event in events]
            self.__class__.type_id, self.__class__.two_up_events, self.__class__.other_events = self.get_events_for_type(self.all_type_ids, self.expected_template_market)
            self.__class__.expected_type_name = self.two_up_events[0]['event']['typeName']
            self.__class__.event_names_for_type_id = [event['event']['name'] for event in self.two_up_events]
            self.__class__.events_for_type_id = {event['event']['name']: event for event in self.two_up_events}
            self.__class__.other_events = {event['event']['name']: event for event in self.other_events}
        else:
            event1 = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets_params)
            event2 = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets_params)
            # getting type id
            self.__class__.type_id = event1[7]['event']['typeId']
            # getting type name
            self.__class__.expected_type_name = event1[7]['event']['typeName']
            # getting event name for type id
            self.__class__.event_names_for_type_id = list()
            self.event_names_for_type_id.append(event1[7]['event']['name'])
            self.event_names_for_type_id.append(event2[7]['event']['name'])
            # getting events for type id
            self.__class__.events_for_type_id = {event1[7]['event']['name']: event1[7],
                                                 event2[7]['event']['name']: event2[7]}
        limit = len(self.events_for_type_id) if len(self.events_for_type_id)<2 else 2
        self.__class__.highlights_carousels = self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title,
                                                                                        typeId=self.type_id,
                                                                                        displayMarketType='2UpMarket',
                                                                                        page_type='sport',
                                                                                        sport_id=self.ob_config.football_config.category_id,
                                                                                        limit=limit,
                                                                                        svgId=self.svg_icon,
                                                                                        displayOnDesktop=True
                                                                                        )
        self.__class__.highlights_carousels_title_name=self.convert_highlights_carousel_title(title=self.highlights_carousels_title)

    def test_001_launch_bma_ladbrokescoral_application_on_mobile(self):
        """
        DESCRIPTION: Launch BMA Ladbrokes/Coral Application on Mobile
        EXPECTED: User should able to launch successfully
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
        EXPECTED: Created HC should display on Football SLP
        """
        self.__class__.section = self.verify_highlight_carousel_on_football_slp(highlights_carousel_title=self.highlights_carousels_title_name)

    def test_004_verify_the_order_of_the_highlights_carousel_module_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the Highlights Carousel module is as per order in the CMS
        EXPECTED: The order should be as per CMS
        """
        # covered in C65861457

    def test_005_change_the_order_in_the_cms_in_the_application_refresh_the_page_and_verify_the_order_is_updated(self):
        """
        DESCRIPTION: Change the order in the CMS. In the application refresh the page and verify the order is updated
        EXPECTED: The order is updated and is as defined in the CMS
        """
        # covered in C65861457

    def test_006_verify_title_amp_svg_icon(self):
        """
        DESCRIPTION: Verify title &amp; SVG Icon
        EXPECTED: HC title  &amp; SVG Icon should be as per cms. Title should be in capitals
        """
        # validating the title
        hc=self.site.football.tab_content.highlight_carousels.keys()
        hc_names = [name.upper() for name in hc]
        self.assertIn(self.highlights_carousels_title.upper(), hc_names,
                      f'{self.highlights_carousels_title.upper()} is not fount in {hc_names}')
        # ******** Verification of SVG icon *************************
        self.assertEqual(self.section.svg_icon_text,
                         f'#{self.svg_icon}', f'Svg icon {self.svg_icon} is not displayed')

    def test_007_go_to_cms_and_edit_the_title_amp_svg_icon_and_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS and Edit the title &amp; SVG Icon and save changes. Verify on FE
        EXPECTED: Title &amp; SVG Icon should be updated on Football SLP as per cms changes
        """
        highlights_carousels_title_modified=f'{self.highlights_carousels_title}_Modified'
        self.__class__.svg_icon_new = f'background-{self.svg_icon}'
        self.cms_config.update_highlights_carousel(self.highlights_carousels,
                                                   title=highlights_carousels_title_modified,
                                                   svgId=self.svg_icon_new)
        self.__class__.highlights_carousels_title_modified_name = self.convert_highlights_carousel_title(
            title=highlights_carousels_title_modified)
        # ******** Verification of Highlight Carousel title and SVG icon *************************
        self.__class__.modified_highlight_carousel = self.verify_highlight_carousel_on_football_slp(highlights_carousel_title=self.highlights_carousels_title_modified_name)
        self.assertEqual(self.modified_highlight_carousel.svg_icon_text,
                         f'#{self.svg_icon_new}', f'Svg icon {self.svg_icon_new} is not displayed')

    def test_008_verify_hc_see_all_link_amp_navigation(self):
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

    def test_009_click_on_back(self):
        """
        DESCRIPTION: Click on Back
        EXPECTED: It should redirect to Football SLP &amp; HC order should be same
        """
        self.site.back_button_click()
        self.site.wait_content_state("football")

    def test_010_verify_hc_display_from_amp__to_as_per_cms(self):
        """
        DESCRIPTION: Verify HC display from &amp;  to as per CMS
        EXPECTED: Highlights Carousel is displayed as current date and time belong to time box set by Display from and Display to date and time fields
        """
        # taking now time
        now = datetime.now()
        # formatting the now time as CMS time format
        now = get_date_time_as_string(date_time_obj=now, time_format='%Y-%m-%dT%H:%M:%S.%f', url_encode=False,
                                      hours=-10)[:-3] + 'Z'
        # getting "display from" time from CMS for Highlight Carousel which is created by script
        display_from = self.highlights_carousels['displayFrom']
        # getting "display to" time from CMS for  Highlight Carousel which is created by script
        display_to = self.highlights_carousels['displayTo']

        # checking now time is in between "display from" and "display to"
        status = display_from < now < display_to
        self.assertTrue(status,
                        f'highlights carousels is not displayed as per CMS configurations(in between start 'f'time and end time)')

    def test_011_go_to_cms_set_display_from_and_display_to_date_and_time_as_time_range_from_the_pastfuture_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' and 'Display to' date and time as time range from the past/future and save changes.
        EXPECTED: The changes are saved
        """
        # covered in C65861457 in step 9

    def test_012_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: Highlights Carousel should not be displayed
        """
        # covered in C65861457 in step 10

    def test_013_go_to_cms_set_display_from_from_the_past_and_display_to_in_a_few_mins_from_the_current_time_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' from the past and 'Display to' in a few mins from the current time and save changes.
        EXPECTED: Changes are saved
        """
        # covered in C65861457 in step 11

    def test_014_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display to' is passed Highlights Carousel is no more shown on Football SLP
        """
        # covered in C65861457 in step 12

    def test_015_go_to_cms_set_display_from_in_a_few_mins_from_current_time_and_display_to_from_the_future_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' in a few mins from current time and 'Display to' from the future and save changes.
        EXPECTED: Changes are saved
        """
        # covered in C65861457 in step 13

    def test_016_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display from' is passed Highlights Carousel should appears
        """
        # covered in C65861457 in step 14

    def test_017_verify_hc_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify HC left and right scroll
        EXPECTED: User should able to scroll from left to right &amp; from right to left
        """
        # covered in C65861228 test case

    def test_018_verify_the_chevron_on_hc_event_cardamp_navigation(self):
        """
        DESCRIPTION: Verify the chevron on HC event card&amp; navigation
        EXPECTED: Chevron should be in blue color and aligned to right &amp; upon clicking on it should redirect to EDP of that event
        """
        section=self.site.football.tab_content.highlight_carousels.get(self.highlights_carousels_title_modified_name)
        event = list(section.items_as_ordered_dict.items())[0][1]
        chevron=event
        chevron.click()
        self.site.wait_content_state("EVENTDETAILS")
        self.site.back_button_click()
        self.site.wait_content_state(state_name="football", timeout=20)

    def test_019_verify_hc_no_of_events_display(self):
        """
        DESCRIPTION: Verify HC No of events display
        EXPECTED: No of events should display on HC should be as per cms value
        """
        # already covered in C65861228 in step 23

    def test_020_go_to_cms_change_no_of_events_amp_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, change No of events &amp; save changes. Verify on FE
        EXPECTED: No of events on HC should update as per cms changes
        """
        # already covered in C65861228 in step 24

    def test_021_verify_the_date_amp_time_of_event_on_hc_event_card(self):
        """
        DESCRIPTION: Verify the date &amp; time of event on HC event card
        EXPECTED: Date &amp; time should display on event card(eg:21:45 Today/00:30 10July)
        """
        # covered in C65861457 in step 17

    def test_022_verify_selections_are_displaying_properly_according_to_the_sportsmarkets_in_hc(self):
        """
        DESCRIPTION: Verify selections are displaying properly according to the sports/markets in HC
        EXPECTED: Selections should display according to the sports/markets (eg: for football HOME DRAW AWAY,for tennis 1 2)
        """
        # covered in C65861457 in step 17

    def test_023_verify_hc_sorting_order_as_per_cms(self):
        """
        DESCRIPTION: Verify HC sorting order as per cms
        EXPECTED: HC should display as per cms sort order
        """
        # Covered In another testcase C5861232

    def test_024_change_the_hc_order_in_highlights_carousel_module_page_in_cms_verify_on_fe(self):
        """
        DESCRIPTION: Change the HC order in Highlights Carousel module page in cms. Verify on FE
        EXPECTED: HC order should change &amp; display as per cms order on FE
        """
        # Covered In another testcase C5861232

    def test_025_verify_user_can_able_to_select_the_selections_on_hc(self):
        """
        DESCRIPTION: Verify user can able to select the selections on HC
        EXPECTED: User should able to select &amp; selections should be highlighted
        """
        # Covered In another testcase C5861232

    def test_026_verify_univeral_view_for_hc(self):
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
        self.verify_highlight_carousel_on_football_slp(highlights_carousel_title=self.highlights_carousels_title_modified_name)

    def test_027_go_to_cms_change_to_segment_view_amp_select_any_segment_from_inclusion_segments_and_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to cms, change to segment view &amp; select any segment from inclusion segments and save changes. Verify on FE
        EXPECTED: HC should display to only segmented users which configured in cms
        """
        # not applicable for slp

    def test_028_verify_team_namesplayer_names_on_hc(self):
        """
        DESCRIPTION: Verify Team names/Player names on HC
        EXPECTED: Team names/Player names should properly display &amp; aligned to the left
        """
        # covered in above test steps

    def test_029_verify_hc_navigation_when_the_user_clicks_anywhere_on_the_event_card_except_the_odds_button(self):
        """
        DESCRIPTION: Verify HC navigation when the user clicks anywhere on the event card (except the odds button
        EXPECTED: User should navigate to the EDP of the event
        """
        # Covered in 8th step

    def test_030_verify_2_up_signposting_display_on_hc_event_cards(self):
        """
        DESCRIPTION: Verify 2 up signposting display on HC event cards
        EXPECTED: 2 up signposting should diplay on event cards
        """
        hc=self.site.football.tab_content.highlight_carousels.get(self.highlights_carousels_title_modified_name)
        hc_events = hc.items_as_ordered_dict
        event_key, event = next(iter(hc_events.items()))
        event.scroll_to_we()
        self.assertTrue(event.has_market_sign_post(expected_result=True), '2 Up Sign posting id not available')

    def test_031_verify_team_kits_when_hc_is_configured_using_the_type_id_for_the_football_premier_or_champions_league(self):
        """
        DESCRIPTION: Verify team kits when HC is configured using the Type ID for the football premier or Champions league
        EXPECTED: HC with the team kits should display
        """
        # covered in C65861231

    def test_032_go_to_cms_deactivate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, deactivate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousels should not be displayed
        """
        # covered in C65861231

    def test_033_go_to_cms_activate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, activate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousel should display on Football SLP
        """
        # covered in C65861231

    def test_034_verify_display_of_event_cards_when_the_event_is_resulted_in_hc(self):
        """
        DESCRIPTION: Verify display of event cards when the event is resulted in HC
        EXPECTED: The card of the resulted event should be removed from the HC automatically
        """
        # not applicable as it requires to be settled event

    def test_035_verify_display_of_hc_when_there_is_only_1_event_card_available_to_be_displayed__amp_that_event_is_resulted(self):
        """
        DESCRIPTION: Verify display of HC when there is only 1 event card available to be displayed  &amp; that event is resulted
        EXPECTED: The card should be removed from HC and the HC should be removed from the page
        """
        # not applicable as it requires to be settled event

    def test_036_go_back_to_the_same_highlights_carousel_in_cms_unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Highlights Carousel in CMS, unselect 'Active' checkbox and save changes
        EXPECTED: a)Existing Highlights Carousel is inactive
        EXPECTED: b)Changes is saved successfully
        """
        self.cms_config.update_highlights_carousel(self.highlights_carousels, disabled=True)

    def test_037_load_oxygen_app_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Highlights Carousel displaying
        EXPECTED: a) Highlights Carousel is NOT displayed on Front End
        EXPECTED: b) If we have other Highlights Carousel with valid date it should display
        """
        # ******** Verification of Highlight Carousel *************************
        self.verify_highlight_carousel_on_football_slp(highlights_carousel_title=self.highlights_carousels_title_modified_name, expected_result=False, refresh_count=5)
        # ******** Updation of Highlight Carousel to Active State *************************
        self.cms_config.update_highlights_carousel(self.highlights_carousels, disabled=False)
        # ******** Verification of Highlight Carousel *************************
        self.verify_highlight_carousel_on_football_slp(highlights_carousel_title=self.highlights_carousels_title_modified_name, refresh_count=10)

    def test_038_go_to_cms_remove_created_hc_amp_confirm_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, Remove created HC &amp; confirm. Verify on FE
        EXPECTED: HC should disappear on FE
        """
        # ******** Removing Highlight Carousel *************************
        highlight_carousel_id = self.highlights_carousels["id"]
        self.cms_config.delete_highlights_carousel(highlight_carousel_id)
        self.cms_config._created_highlights_carousels.remove(highlight_carousel_id)
        # ******** Verification of Highlight Carousel *************************
        self.verify_highlight_carousel_on_football_slp(highlights_carousel_title=self.highlights_carousels_title_modified_name, expected_result=False, refresh_count=5)