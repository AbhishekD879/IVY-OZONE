from datetime import datetime
import pytest
from crlat_cms_client.utils.exceptions import CMSException
import re
from collections import OrderedDict
import voltron.environments.constants as vec
from crlat_ob_client.utils.date_time import get_date_time_as_string
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.pages.shared.components.home_page_components.highlight_carousel import HighlightCarousel
from voltron.utils.waiters import wait_for_cms_reflection, wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.highlights_carousel
@pytest.mark.adhoc_suite
@pytest.mark.mobile_only
@pytest.mark.other
@vtest
class Test_C65861231_Verify_Highlight_carousal_display_with_EventID_for_primary_market_with_in_play_events_Mobile_Homepage(Common):
    """
    TR_ID: C65861231
    NAME: Verify Highlight carousal display with EventID for primary market with in-play events_Mobile Homepage
    DESCRIPTION: This test case is to verify Highlight carousal display with EventID for primary market with in-play events_Mobile Homepage
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS Navigation:
    PRECONDITIONS: CMS > sports pages >home page> Highlights Carousel and click on Create Highlights Carousel CTA.
    PRECONDITIONS: Configure HC as below by giving all the fields.
    PRECONDITIONS: *Enable "Active & Display on Desktop" check boxes
    PRECONDITIONS: *Title=TENNIS - FEATURED MATCHES
    PRECONDITIONS: *Set events by=Event IDs
    PRECONDITIONS: *Event IDs= 240767310,240778313(in-play)
    PRECONDITIONS: *Select Market & Market Type = Primary Market
    PRECONDITIONS: *Display from & Display to time period (eg: from 7/6/2023 11:05:34 to 7/7/2023 11:05:34)
    PRECONDITIONS: *SVG Icon=tennis
    PRECONDITIONS: *No. of Events = 2
    PRECONDITIONS: *Enable Display In-Play checkbox
    PRECONDITIONS: *Select Universal view
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT

    def check_hc_module_status_and_create_hightlight_carousel(self, hc_title=None, events_list=[], events_count=1,
                                                              svg_icon=""):
        sports_module = self.cms_config.get_sport_module(module_type=None)
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
        highlights_carousel = self.cms_config.create_highlights_carousel(title=hc_title,events=events_list, limit=events_count, svgId=svg_icon,inplay=True)
        return highlights_carousel

    def verify_highlight_carousel_on_fe(self, highlights_carousel_title=None, expected_result=True):
        if expected_result:
            section = wait_for_cms_reflection(
                lambda: self.site.home.tab_content.highlight_carousels.get(highlights_carousel_title),
                refresh_count=4, ref=self)
            self.assertTrue(section,
                            msg=f'{highlights_carousel_title} is not available')
            return section
        else:
            if self.site.home.tab_content.has_highlight_carousels():
                section = wait_for_cms_reflection(
                    lambda: self.site.home.tab_content.highlight_carousels.get(highlights_carousel_title),
                    refresh_count=4, ref=self, expected_result=False)
                self.assertFalse(section,
                                 msg=f'{highlights_carousel_title} is available')

    def get_current_live_events_for_created_highlight_carousel(self, highlight_carousel: HighlightCarousel = None):
        pattern = r'\d+-\d+'  # Regular expression pattern to match the number1-number2 format

        def replace_random_number(match):
            return ' V '  # Replacing the matched number1-number2 format with ' v '

        filtered_events = []
        for event in self.all_live_events_for_type:
            is_watch_live = any(tag in event['event']['drilldownTagNames'] for tag in
                                ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM'])

            filtered_event = {
                'name': re.sub(pattern, replace_random_number, event['event']['name'].upper()),
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

    def convert_highlights_carousel_title(self, title):
        return title if not self.brand == 'ladbrokes' else title.upper()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS Navigation:
        PRECONDITIONS: CMS > sports pages >home page> Highlights Carousel and click on Create Highlights Carousel CTA.
        PRECONDITIONS: Configure HC as below by giving all the fields.
        PRECONDITIONS: *Enable "Active & Display on Desktop" check boxes
        PRECONDITIONS: *Title=TENNIS - FEATURED MATCHES
        PRECONDITIONS: *Set events by=Event IDs
        PRECONDITIONS: *Event IDs= 240767310,240778313(in-play)
        PRECONDITIONS: *Select Market & Market Type = Primary Market
        PRECONDITIONS: *Display from & Display to time period (eg: from 7/6/2023 11:05:34 to 7/7/2023 11:05:34)
        PRECONDITIONS: *SVG Icon=tennis
        PRECONDITIONS: *No. of Events = 2
        PRECONDITIONS: *Enable Display In-Play checkbox
        PRECONDITIONS: *Select Universal view
        """
        self.__class__.highlights_carousel_title = self.convert_highlights_carousel_title(
            title="Auto C65861231 hc")
        self.__class__.svg_icon = "tennis"
        self.__class__.expected_highlights_carousel_events = []
        self.__class__.events_start_time = {}
        self.__class__.highlights_carousel_event_ids = []
        if tests.settings.backend_env == 'prod':
            # ******** Getting Events ********
            events = self.get_active_events_for_category(category_id=self.ob_config.tennis_config.category_id,
                                                         all_available_events=True,in_play_event=True)
            self.__class__.all_live_events_for_type = events
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
                self.expected_highlights_carousel_events.append(events[i]['event']['name'].upper())
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
            event1_name = event1.team1+ ' v ' + event1.team2
            event2_name = event2.team1+ ' v ' + event2.team2
            self.__class__.expected_highlights_carousel_events = [event1_name.upper(), event2_name.upper()]
            self.events_start_time[0] = event1.event_date_time
            self.events_start_time[1] = event2.event_date_time

        self.__class__.highlights_carousel_event_ids = [self.eventID1, self.eventID2]
        # ******** Creation of Highlights Carousel *************************
        self.__class__.highlights_carousel = self.check_hc_module_status_and_create_hightlight_carousel(
            hc_title=self.highlights_carousel_title, events_list=self.highlights_carousel_event_ids, events_count=2,
            svg_icon=self.svg_icon)

    def test_001_launch_bma_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch BMA Ladbrokes/Coral Application
        EXPECTED: User should able to launch successfully
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage', timeout=20)

    def test_002_verify_created_highlight_carousal_displaying_on_fe(self):
        """
        DESCRIPTION: Verify Created Highlight carousal displaying on FE
        EXPECTED: Created HC should display on Homepage
        """
        # ******** Verification of Highlight Carousel *************************
        self.__class__.section = self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title)
        # ******** Verification of Highlight Carousel events *************************
        actual__highlights_carousel_events = [item_name.upper() for item_name in self.section.items_names]
        self.assertListEqual(self.expected_highlights_carousel_events, actual__highlights_carousel_events,
                             msg=f'actual highlights carousel events {actual__highlights_carousel_events} not equals to expected highlights carousel events {self.expected_highlights_carousel_events}')
        # ******** Verification of SVG icon *************************
        self.assertEqual(self.section.svg_icon_text,
                         f'#{self.svg_icon}', f'Svg icon {self.svg_icon} is not displayed')

    def test_003_verify_the_order_of_the_highlights_carousel_module_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the Highlights Carousel module is as per order in the CMS
        EXPECTED: The order should be as per CMS
        """
        # covered in C6581232

    def test_004_change_the_order_in_the_cms_in_the_application_refresh_the_page_and_verify_the_order_is_updated(self):
        """
        DESCRIPTION: Change the order in the CMS. In the application refresh the page and verify the order is updated
        EXPECTED: The order is updated and is as defined in the CMS
        """
        # covered in C6581232

    def test_005_verify_title_amp_svg_icon(self):
        """
        DESCRIPTION: Verify title &amp; SVG Icon
        EXPECTED: HC title  &amp; SVG Icon should be as per cms. Title should be in capitals
        """
        # ******** Verification of Highlight Carousel *************************
        self.__class__.section = self.verify_highlight_carousel_on_fe(
            highlights_carousel_title=self.highlights_carousel_title)
        # ******** Verification of SVG icon *************************
        self.assertEqual(self.section.svg_icon_text,
                         f'#{self.svg_icon}', f'Svg icon {self.svg_icon} is not displayed')

    def test_006_go_to_cms_and_edit_the_title_amp_svg_icon_and_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS and Edit the title &amp; SVG Icon and save changes. Verify on FE
        EXPECTED: Title &amp; SVG Icon should be updated on Homepage as per cms changes
        """
        # ******** Updation of Highlight Carousel title and SVG icon *************************
        self.__class__.highlights_carousel_title = self.convert_highlights_carousel_title(
            title="Auto C65861231 modified hc")
        self.svg_icon = "icon-tennis"
        self.cms_config.update_highlights_carousel(self.highlights_carousel, title=self.highlights_carousel_title,
                                                   svgId=self.svg_icon,inPlay=True)
        # ******** Verification of Highlight Carousel title and SVG icon *************************
        wait_for_haul(5)
        self.device.refresh_page()
        section = self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title)
        self.assertEqual(section.svg_icon_text,
                         f'#{self.svg_icon}', f'Svg icon {self.svg_icon} is not displayed')

    def test_007_verify_live_watch_live_icons_display(self, check_live=True):
        """
        DESCRIPTION: Verify live, watch live icons display
        EXPECTED: Live, watch live icons should display for inplay events
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.modified_highlights_carousel = self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title)
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
        else:
            pass

    def test_008_verify_hc_price_and_score_updates_color_change_as_per_brand_for_in_play_event(self):
        """
        DESCRIPTION: Verify HC price and score updates, color change as per brand for in-play event
        EXPECTED: Price and score updates, color change should happen
        """
        # covered in above step

    def test_009_verify_hc_display_from_amp__to_as_per_cms(self):
        """
        DESCRIPTION: Verify HC display from &amp;  to as per CMS
        EXPECTED: Highlights Carousel is displayed as current date and time belong to time box set by Display from and Display to date and time fields
        """
        # covered in test_002_verify_created_highlight_carousal_displaying_on_fe

    def test_010_go_to_cms_set_display_from_and_display_to_date_and_time_as_time_range_from_the_pastfuture_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' and 'Display to' date and time as time range from the past/future and save changes.
        EXPECTED: The changes are saved
        """
        # ******** Updation of Highlight Carousel Display dates to Past dates *************************
        self.__class__.time_format = '%Y-%m-%dT%H:%M:%S.%f'
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-8.5)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=-6.5)[:-3] + 'Z'
        self.cms_config.update_highlights_carousel(self.highlights_carousel, start_time=start_time,
                                                   end_time=end_time)

    def test_011_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: Highlights Carousel should not be displayed
        """
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title,
                                             expected_result=False)

    def test_012_go_to_cms_set_display_from_from_the_past_and_display_to_in_a_few_mins_from_the_current_time_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' from the past and 'Display to' in a few mins from the current time and save changes.
        EXPECTED: Changes are saved
        """
        # ******** Updation of Highlight Carousel From date to Past and To date to Future *************************
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-6.5)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=10)[:-3] + 'Z'
        self.cms_config.update_highlights_carousel(self.highlights_carousel, start_time=start_time,
                                                   end_time=end_time)

    def test_013_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display to' is passed Highlights Carousel is no more shown on Homepage
        """
        self.device.refresh_page()
        wait_for_haul(5)
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title)

    def test_014_go_to_cms_set_display_from_in_a_few_mins_from_current_time_and_display_to_from_the_future_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' in a few mins from current time and 'Display to' from the future and save changes.
        EXPECTED: Changes are saved
        """
        # ******** Updation of Highlight Carousel Display dates to Future dates *************************
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=2)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=5)[:-3] + 'Z'
        self.cms_config.update_highlights_carousel(self.highlights_carousel, start_time=start_time,
                                                   end_time=end_time)

    def test_015_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display from' is passed Highlights Carousel should appears
        """
        # ******** Verification of Highlight Carousel *************************
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title,
                                             expected_result=False)
        # ******** Updation of Highlight Carousel From date to Past and To date to Future *************************
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-10)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=5.5)[:-3] + 'Z'
        self.cms_config.update_highlights_carousel(self.highlights_carousel, start_time=start_time,
                                                   end_time=end_time)
        # ******** Verification of Highlight Carousel *************************
        wait_for_haul(5)
        self.__class__.section = self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title)

    def test_016_verify_hc_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify HC left and right scroll
        EXPECTED: User should able to scroll from left to right &amp; from right to left
        """
        # covered in C65861228 test case

    def test_017_verify_hc_display_with_greencoralorangelads_dots_for_inplay_events(self):
        """
        DESCRIPTION: Verify HC display with green(coral)/orange(lads) dots for inplay events
        EXPECTED: HC should display with green(coral)/orange(lads) dots
        """
        # Covered in above step

    def test_018_verify_the_chevron_on_hc_event_card_amp_navigation(self):
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
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        section = self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title)
        self.__class__.highlight_carousel_events = section.items_as_ordered_dict
        self.assertTrue(self.highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_title}"')

    def test_019_verify_the_set_details_amp_score_detailssgp_fot_tennis_inplay_events(self):
        """
        DESCRIPTION: Verify the set details &amp; score details(S,G,P) fot tennis inplay events
        EXPECTED: Set 'n' and S,G,P scores should display &amp; align properly
        """
        highlight_carousel = self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title)
        event = list(highlight_carousel.items_as_ordered_dict.items())[0][1]
        column_headers = event.score_column_headers
        for header in ["S", "G", "P"]:
            self.assertIn(header, column_headers.keys(), msg=f"{header} is not in {column_headers.keys()}")

    def test_020_verify_hc_no_of_events_display(self):
        """
        DESCRIPTION: Verify HC No of events display
        EXPECTED: No of events should display on HC should be as per cms value
        """
        expected_event_count = self.highlights_carousel['limit']
        highlight_carousel = self.verify_highlight_carousel_on_fe(
            highlights_carousel_title=self.highlights_carousel_title)
        actual_event_length = len(highlight_carousel.items)
        self.assertLessEqual(actual_event_length, expected_event_count,
                             msg=f"Expected event count :{expected_event_count}"
                                 f"is not equal to :{actual_event_length}")

    def test_021_go_to_cms_change_no_of_events_amp_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, change No of events &amp; save changes. Verify on FE
        EXPECTED: No of events on HC should update as per cms changes
        """
        # ******** Updation of Highlight Carousel Number of Events to 1 *************************
        updated_limit = 1
        self.cms_config.update_highlights_carousel(self.highlights_carousel, limit=updated_limit, inPlay=True)
        # ******** Verification of Highlight Carousel events count *************************
        is_events_count_equal = wait_for_cms_reflection(
            lambda: len(self.site.home.tab_content.highlight_carousels.get(self.highlights_carousel_title).items_names) == updated_limit, timeout=2,
                refresh_count=5, ref=self, expected_result=True)
        self.assertTrue(is_events_count_equal,
                        msg=f"updated events limit count is not matched with expected events limit count {updated_limit} ")

    def test_022_verify_hc_display_as_per_cms_entry_as_per_comma_separation(self):
        """
        DESCRIPTION: Verify HC display as per CMS entry as per comma separation
        EXPECTED: Hc events should display as per comma seperation (eg: if two event id's configured in cms, the first congigured event should display first in FE, second configured event should diplay in second place)
        """
        # Covered in test_002_verify_created_highlight_carousal_displaying_on_fe

    def test_023_verify_hc_display_in_play(self):
        """
        DESCRIPTION: Verify HC display in play
        EXPECTED: HC with inplay events should display on FE only if display inplay is enabled in cms
        """
        self.assertTrue(self.highlights_carousel['inPlay'], msg=f'Inplay is Not enabled '
                                                                 f'in cms for HC {self.highlights_carousel_title}')

    def test_024_go_to_cms_disable_display_in_play_checkbox_verify_on_fe(self):
        """
        DESCRIPTION: Go to cms, disable display in play checkbox. Verify on FE
        EXPECTED: HC with In play events should not display on Homepage
        """
        self.cms_config.update_highlights_carousel(self.highlights_carousel, inPlay=False)
        wait_for_haul(10)
        self.device.refresh_page()
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.highlights_carousel_title, expected_result=False)

    def test_025_verify_the_match_time_on_event_card_for_football_inplay_events(self):
        """
        DESCRIPTION: Verify the match time on event card for Football inplay events
        EXPECTED: Match time should display on HC event card
        """
        # Cannot verify time on event card for live tennis

    def test_026_verify_selections_are_displaying_properly_according_to_the_sportsmarkets_in_hc(self):
        """
        DESCRIPTION: Verify selections are displaying properly according to the sports/markets in HC
        EXPECTED: Selections should display according to the sports/markets (eg: for football HOME DRAW AWAY,for tennis 1 2)
        """
        # Covered in test_018_verify_the_date_amp_time_of_event_on_hc_event_card

    def test_027_verify_hc_sorting_order_as_per_cms(self):
        """
        DESCRIPTION: Verify HC sorting order as per cms
        EXPECTED: HC should display as per cms sort order
        """
        # already covered in C65861232

    def test_028_change_the_hc_order_in_highlights_carousel_module_page_in_cms_verify_on_fe(self):
        """
        DESCRIPTION: Change the HC order in Highlights Carousel module page in cms. Verify on FE
        EXPECTED: HC order should change &amp; display as per cms order on FE
        """
        self.__class__.hc2_title = self.convert_highlights_carousel_title(title="Auto C65861231 hc2")
        self.check_hc_module_status_and_create_hightlight_carousel(
            hc_title=self.hc2_title, events_list=[self.eventID3], events_count=1,
            svg_icon=self.svg_icon)
        self.device.refresh_page()
        wait_for_haul(5)
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.hc2_title)

    def test_029_verify_user_can_able_to_select_the_selections_on_hc(self):
        """
        DESCRIPTION: Verify user can able to select the selections on HC
        EXPECTED: User should able to select &amp; selections should be highlighted
        """
        # covered in test_018_verify_the_date_amp_time_of_event_on_hc_event_card

    def test_030_verify_univeral_view_for_hc(self):
        """
        DESCRIPTION: Verify Univeral view for HC
        EXPECTED: HC should display for all  logged in &amp; logged out users
        """
        # ******** Verification of Highlight Carousel for logged in user *************************
        self.site.login()
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.hc2_title)

    def test_031_go_to_cms_change_to_segment_view_amp_select_any_segment_from_inclusion_segments_and_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to cms, change to segment view &amp; select any segment from inclusion segments and save changes. Verify on FE
        EXPECTED: HC should display to only segmented users which configured in cms
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),msg='User has not logged out!')
        # ******** Updation of Highlight Carousel to segment view *************************
        self.cms_config.update_highlights_carousel(self.highlights_carousel, inclusionList=[self.segment])
        # ******** Verification of Highlight Carousel for logged in user *************************
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.hc2_title)

    def test_032_verify_team_namesplayer_names_on_hc(self):
        """
        DESCRIPTION: Verify Team names/Player names on HC
        EXPECTED: Team names/Player names should properly display &amp; aligned to the left
        """
        # covered in test_002_verify_created_highlight_carousal_displaying_on_fe

    def test_033_verify_hc_navigation_when_the_user_clicks_anywhere_on_the_event_card_except_the_odds_button(self):
        """
        DESCRIPTION: Verify HC navigation when the user clicks anywhere on the event card (except the odds button
        EXPECTED: User should navigate to the EDP of the event
        """
        # Covered in test_015_verify_the_chevron_on_hc_event_card_amp_navigation

    def test_034_verify_team_kits_when_hc_is_configured_using_the_event_id_for_the_football_premier_or_champions_league(self):
        """
        DESCRIPTION: Verify team kits when HC is configured using the event ID for the football premier or Champions league
        EXPECTED: HC with the team kits should display
        """
        # created event with tennis and this step is covered in test case C6587284

    def test_035_go_to_cms_deactivate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, deactivate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousels should not be displayed
        """
        # Can't deactivate the whole highlight carousel module, It will impact other HC test cases

    def test_036_go_to_cms_activate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, activate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousel should display on homepage
        """
        # Covered in test_002_verify_created_highlight_carousal_displaying_on_fe

    def test_037_verify_display_of_event_cards_when_the_event_is_resulted_in_hc(self):
        """
        DESCRIPTION: Verify display of event cards when the event is resulted in HC
        EXPECTED: The card of the resulted event should be removed from the HC automatically
        """
        # Need resulted event

    def test_038_verify_display_of_hc_when_there_is_only_1_event_card_available_to_be_displayed__amp_that_event_is_resulted(self):
        """
        DESCRIPTION: Verify display of HC when there is only 1 event card available to be displayed  &amp; that event is resulted
        EXPECTED: The card should be removed from HC and the HC should be removed from the page
        """
        # Need resulted event

    def test_039_go_back_to_the_same_highlights_carousel_in_cms_unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Highlights Carousel in CMS, unselect 'Active' checkbox and save changes
        EXPECTED: a)Existing Highlights Carousel is inactive
        EXPECTED: b)Changes is saved successfully
        """
        # ******** Updation of Highlight Carousel to Inactive State *************************
        # Covered in C65827284

    def test_040_load_oxygen_app_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Highlights Carousel displaying
        EXPECTED: a) Highlights Carousel is NOT displayed on Front End
        EXPECTED: b) If we have other Highlights Carousel with valid date it should display
        """
        # coverd in C65827284

    def test_041_go_to_cms_remove_created_hc_amp_confirm_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, Remove created HC &amp; confirm. Verify on FE
        EXPECTED: HC should disappear on FE
        """
        # ******** Removing Highlight Carousel *************************
        highlight_carousel_id = self.highlights_carousel["id"]
        self.cms_config.delete_highlights_carousel(highlight_carousel_id)
        self.cms_config._created_highlights_carousels.remove(highlight_carousel_id)
        # ******** Verification of Highlight Carousel *************************
        wait_for_haul(5)
        self.verify_highlight_carousel_on_fe(highlights_carousel_title=self.hc2_title,
                                             expected_result=False)

