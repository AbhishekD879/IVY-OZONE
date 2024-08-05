import random
import re
from collections import OrderedDict
import pytest
import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    generate_highlights_carousel_name, BaseHighlightsCarouselTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_cms_reflection, wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.cms
@pytest.mark.highlights_carousel
@pytest.mark.adhoc_suite
@vtest
class Test_C65861460_Verify_Highlight_carousal_display_with_TypeID_for_primary_market_with_in_play_events_on_Mobile_Football_SLP(BaseHighlightsCarouselTest):
    """
    TR_ID: C65861460
    NAME: Verify Highlight carousal display with TypeID for primary market  with in-play events on Mobile Football SLP
    DESCRIPTION: This test case is to verify Highlight carousal display with TypeID for primary market  with in-play events on Mobile Football SLP
    PRECONDITIONS: 1. User should have admin access to CMS.
    PRECONDITIONS: 2. CMS Navigation:
    PRECONDITIONS: CMS > sports pages >Sports Category>Football> Highlights Carousel and click on Create Highlights Carousel CTA.
    PRECONDITIONS: 3. Configure HC as below by giving all the fields.
    PRECONDITIONS: *Enable "Active" check box
    PRECONDITIONS: *Title=Football SLP
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
    highlights_carousels_title = generate_highlights_carousel_name()+f'{random.randint(1,1000)}'
    sport_name = vec.sb.FOOTBALL.title()
    svg_icon = "football"

    def get_current_live_events_for_created_highlight_carousel(self, highlight_carousel=None):
        # Regular expression pattern to match the number1-number2 format
        pattern = r'\d+-\d+'

        # Function to replace the matched number1-number2 format with ' V '
        def replace_random_number(match):
            return ' V '

        filtered_events = []
        for event in self.all_live_events_for_type:  # Getting response from the ss
            # Check if the event is marked as watch live based on certain tags
            is_watch_live = any(tag in event['drilldownTagNames'] for tag in
                                ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM'])
            # Filtered event with replaced numbers and isWatchLive status
            filtered_event = {
                'name': re.sub(pattern, replace_random_number, event['name'].upper()),
                'isWatchLive': is_watch_live
            }
            filtered_events.append(filtered_event)

        # Dictionary to store live highlight carousel items
        live_hc_items = OrderedDict()
        for name, value in highlight_carousel.items_as_ordered_dict.items():
            for event in filtered_events:
                if event['name'].upper() == name.upper():
                    live_hc_items[name] = {
                        "value": value,
                        "isWatchLive": event['isWatchLive']
                    }

        # Return the dictionary containing live highlight carousel items
        return live_hc_items

    def get_type_id_for_HC(self):
        # Fetching live events from ss for tennis
        all_events_for_football = self.get_active_events_for_category(
            category_id=self.ob_config.football_config.category_id,
            all_available_events=True, in_play_event=True)
        # Remove duplicates based on the 'name' property
        unique_events = []
        seen_event_names = set()
        for event in all_events_for_football:
            event_name = event['event']['name']
            if event_name not in seen_event_names:
                unique_events.append(event)
                seen_event_names.add(event_name)
        type_dict = {}
        for event in unique_events:
            event = event['event']
            if event['typeId']:
                if type_dict.get(event['typeId']):
                    type_dict[event['typeId']].append(event)
                else:
                    type_dict[event['typeId']] = [event]
        # Find the type with the maximum number of events
        max_type = max(type_dict, key=lambda x: len(type_dict[x]))
        max_events = type_dict[max_type]
        self.__class__.expected_type_name = max_events[0]['typeName'].upper()
        max_events_length = len(max_events)
        return max_type, max_events_length, max_events

    def verify_highlight_carousel_on_football_slp(self, highlights_carousel_title=None, expected_result=True,
                                                  refresh_count=2,
                                                  timeout=1):
        if expected_result:
            highlight_carousel = wait_for_cms_reflection(
                lambda: self.site.football.tab_content.highlight_carousels.get(highlights_carousel_title),
                refresh_count=refresh_count, ref=self, timeout=timeout, haul=5)
            self.assertTrue(highlight_carousel,
                            msg=f'{highlights_carousel_title} is not available')
            highlight_carousel.scroll_to()
            return highlight_carousel
        else:
            hcs = self.site.football.tab_content.highlight_carousels
            if hcs:
                section = wait_for_cms_reflection(
                    lambda: hcs.get(highlights_carousel_title),
                    refresh_count=3, ref=self, expected_result=False)
                self.assertFalse(section,
                                 msg=f'{highlights_carousel_title} is available')

    def create_check_status_hightlight_carousel(self, index_number: int = None):
        # Get all sports modules associated with the event hub
        sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(index_number)

        hc_module_cms = None
        for module in sports_module_event_hub:
            if module['moduleType'] == 'HIGHLIGHTS_CAROUSEL':
                hc_module_cms = module
                break

        # If there is no HIGHLIGHTS_CAROUSEL module, add one to the event hub
        if hc_module_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='HIGHLIGHTS_CAROUSEL', page_id=index_number)
        else:
            # Check if the HIGHLIGHTS_CAROUSEL module is disabled
            highlights_module_status = next((module['disabled'] for module in sports_module_event_hub
                                             if module['moduleType'] == 'HIGHLIGHTS_CAROUSEL'), None)
            # If the module is disabled, enable it
            if highlights_module_status is True:
                self.cms_config.change_sport_module_state(sport_module=hc_module_cms)

        # Create the HIGHLIGHTS_CAROUSEL
        highlights_carousels_response = self.cms_config.create_highlights_carousel(
            title=self.highlights_carousels_title,
            typeId=self.type_id,
            sport_id=index_number,
            limit=self.max_event_length,
            svgId=self.svg_icon,
            inplay=True, displayOnDesktop=True)
        return highlights_carousels_response

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create Event hub and tag this event hub to Module ribbon tab,
        PRECONDITIONS: Event Hub - Highlights Carousel Creation in CMS:
        PRECONDITIONS: 1. Login to Environment specific CMS
        PRECONDITIONS: 2. Navigate to Sports Pages -->Event Hub
        PRECONDITIONS: 3. Click on Create Event Hub
        PRECONDITIONS: 4. Enter title and click on Create button
        PRECONDITIONS: 5. Click on Add Sport Module --> Select option from dropdown as Highlights Carousel
        PRECONDITIONS: 6. Click on Create button
        PRECONDITIONS: 7. Click on Highlights Carousel module in newly created Event Hub --> Click on Create Highlight Carousel button
        PRECONDITIONS: 8. Enter All fields like
        PRECONDITIONS: - Active Checkbox
        PRECONDITIONS: - Title as 'Featured - Ladies Matches '
        PRECONDITIONS: - TypeId/EventId (Create with Inplay TypeId)
        PRECONDITIONS: - Select market and Market Type will be auto selected (Select Market as Primary Market)
        PRECONDITIONS: - Display From
        PRECONDITIONS: - Display To
        PRECONDITIONS: - SVG Icon
        PRECONDITIONS: - No.Of Events
        PRECONDITIONS: - Display Inplay
        PRECONDITIONS: 9. Click on Create button
        PRECONDITIONS: 10. Select Active checkbox for Highlight Carosel in Event hub and save the changes
        PRECONDITIONS: Module Ribbon Tab Creation(MRT) in CMS :
        PRECONDITIONS: 1. Navigate to Module Ribbon tab
        PRECONDITIONS: 2. Click on Create Module Ribbon tab and enter below fields
        PRECONDITIONS: - Module Ribbon tab Title
        PRECONDITIONS: - Directive name as Event Hub
        PRECONDITIONS: - Select Event Hub name(Which we created above)
        PRECONDITIONS: - Visible from,Visible To(User can change accordingly)
        PRECONDITIONS: 3. Click on Create button
        PRECONDITIONS: 4. Select Active checkbox,IOS,Android checkboxes
        PRECONDITIONS: 5. Select Show Tab on field and click on Save Changes button
        PRECONDITIONS: Check the Sort Order of Highlight Carousel Module in Event Hub:
        PRECONDITIONS: 1. Navigate to Sports Pages--> Event Hub--> Select newly Created Evnet Hub--> Check the Highlights Carousel order
        """
        self.__class__.type_id = None
        if tests.settings.backend_env == 'prod':
            # getting dictionary of events, with event name Key : event name, Value : event(ss response)
            self.__class__.type_id, self.__class__.max_event_length, self.__class__.all_live_events_for_type = self.get_type_id_for_HC()
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True, in_play_event=False)
            self.__class__.events_for_type = [event for event in events if event['event']['typeId'] == self.type_id]

        else:
            self.__class__.all_live_events_for_type = []
            self.__class__.type_id = self.football_config.autotest_class.autotest_premier_league.type_id
            for i in range(1, 3):
                response = self.ob_config.add_autotest_premier_league_football_event(is_live=True, perform_stream=True)
                self.all_live_events_for_type.append(response.ss_response['event'])
            self.ob_config.add_autotest_premier_league_football_event(is_live=False, perform_stream=True)
            self.__class__.max_event_length = len(self.all_live_events_for_type)
            # create or update the highlight carousel inn event hub
        self.__class__.highlights_carousels_response = self.create_check_status_hightlight_carousel(index_number=self.ob_config.football_config.category_id)
        self.__class__.highlights_carousel_name_1 = self.convert_highlights_carousel_title(
            self.highlights_carousels_title)

    def test_001_launch_bma_ladbrokescoral_application_on_mobile(self):
        """
        DESCRIPTION: Launch BMA Ladbrokes/Coral Application on mobile
        EXPECTED: User should able to launch successfully
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')

    def test_002_navigate_to_football_sport(self):
        """
        DESCRIPTION: Navigate to Football Sport
        EXPECTED: Football SLP is loaded
        """
        self.site.open_sport(self.sport_name)
        self.site.wait_content_state(state_name=self.sport_name)

    def test_003_verify_created_highlight_carousal_displaying_on_fe(self):
        """
        DESCRIPTION: Verify Created Highlight carousal displaying on FE
        EXPECTED: Created HC should display on Football SLP.
        """
        highlight_carousel = self.verify_highlight_carousel_on_football_slp(
            highlights_carousel_title=self.highlights_carousel_name_1)
        self.assertEqual(highlight_carousel.svg_icon_text,
                         f'#{self.svg_icon}', f'Svg icon {self.svg_icon} is not displayed')
        self.__class__.highlight_carousel_events = highlight_carousel.items_as_ordered_dict
        self.assertTrue(self.highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_name_1}"')
        self.assertLessEqual(len(self.highlight_carousel_events), self.max_event_length,
                               msg=f'actual length of events {len(self.highlight_carousel_events)} in created highlight carousel is not same as configured{self.max_event_length}')

    def test_004_verify_the_order_of_the_highlights_carousel_module_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the Highlights Carousel module is as per order in the CMS
        EXPECTED: The order should be as per CMS
        """
        # covered in test case C658614458

    def test_005_change_the_order_in_the_cms_in_the_application_refresh_the_page_and_verify_the_order_is_updated(self):
        """
        DESCRIPTION: Change the order in the CMS. In the application refresh the page and verify the order is updated
        EXPECTED: The order is updated and is as defined in the CMS
        """
        # covered in test case C658614458

    def test_006_verify_title_amp_svg_icon(self):
        """
        DESCRIPTION: Verify title &amp; SVG Icon
        EXPECTED: HC title  &amp; SVG Icon should be as per cms. Title should be in capitals
        """
        # covered in test case above test case

    def test_007_go_to_cms_and_edit_the_title_amp_svg_icon_and_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS and Edit the title &amp; SVG Icon and save changes. Verify on FE
        EXPECTED: Title &amp; SVG Icon should be updated on Football SLP as per cms changes
        """
        # ******** Updation of Highlight Carousel title and SVG icon *************************
        self.__class__.highlights_carousel_title = self.convert_highlights_carousel_title(
            title=generate_highlights_carousel_name()) + f'{random.randint(1,1000)}'
        self.svg_icon = "football_gold"
        self.cms_config.update_highlights_carousel(self.highlights_carousels_response,
                                                   title=self.highlights_carousel_title,
                                                   svgId=self.svg_icon)
        highlight_carousel = self.verify_highlight_carousel_on_football_slp(
            highlights_carousel_title=self.highlights_carousel_title,
            refresh_count=5, timeout=10)
        self.assertEqual(highlight_carousel.svg_icon_text,
                         f'#{self.svg_icon}', f'Svg icon {self.svg_icon} is not displayed')
        highlight_carousel_see_all_status = highlight_carousel.has_see_all_link(expected_result=True)
        self.assertTrue(highlight_carousel_see_all_status, msg="Highlight carousel not contains see all link")
        highlight_carousel.see_all_link.click()
        actual_type_name = self.site.competition_league.title_section.type_name.text.upper() # getting type name from Frontend
        # verifying the Frontend Type name with Expected Type( which is getting from OB)
        self.assertEqual(actual_type_name, self.expected_type_name,
                         f'actual_type_name {actual_type_name} is not same as expeceted type name {self.expected_type_name}')
        self.site.back_button_click()
        highlight_carousel = self.verify_highlight_carousel_on_football_slp(
            highlights_carousel_title=self.highlights_carousel_title, refresh_count=5, timeout=10)
        first_event = list(highlight_carousel.items_as_ordered_dict.values())[0]
        first_event.see_all.click()
        self.site.wait_content_state('EventDetails')

    def test_008_verify_hc_see_all_link_amp_navigation(self):
        """
        DESCRIPTION: Verify HC SEE ALL link &amp; Navigation
        EXPECTED: SEE ALL link should display &amp; upon clicking it should navigate to competition detail page
        """

    #     covered in test_007_go_to_cms_and_edit_the_title_amp_svg_icon_and_save_changes_verify_on_fe

    def test_009_click_on_back(self):
        """
        DESCRIPTION: Click on Back
        EXPECTED: It should redirect to Football SLP &amp; HC order should be same
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name=self.sport_name)

    def test_010_verify_live_watch_live_icons_display(self):
        """
        DESCRIPTION: Verify live, watch live icons display
        EXPECTED: Live, watch live icons should display for inplay events
        """
        highlight_carousel = self.verify_highlight_carousel_on_football_slp(
            highlights_carousel_title=self.highlights_carousel_title,
            refresh_count=5, timeout=10)
        live_events_for_HC = self.get_current_live_events_for_created_highlight_carousel(
            highlight_carousel=highlight_carousel)
        for event_name, event in live_events_for_HC.items():
            event_object = event['value']
            live_icon = wait_for_result(lambda: event_object.live_button, expected_result=True, timeout=1)
            # watch_live_button
            self.assertTrue(live_icon, msg=f"Live icon for event inplay '{event_name} not found'")
            if event['isWatchLive']:
                self.assertTrue(event_object.watch_live_button,
                                msg=f"Watch Live icon for event inplay '{event_name} not found'")
        events = highlight_carousel.items_as_ordered_dict
        expected_list = ['HOME', 'DRAW', 'AWAY']
        for event_name, event in events.items():
            bet_buttons = event.get_all_prices()
            self.__class__.actual_list = []
            if all(bet_buttons.values()):
                # ******** Verification of Highlight Carousel event odds header *************************
                self.actual_list = [button.name.split('\n')[0].upper() for button_name, button in bet_buttons.items()]
            else:
                self._logger.info(f'event {event_name} does not found bet buttons')
            if self.actual_list == expected_list:
                break
            else:
                self._logger.info(f'event {event_name} actuall {self.actual_list}does not match{expected_list}')
        self.assertListEqual(expected_list, self.actual_list,
                             f'actual headers of odds is {self.actual_list} is not same as expected odds headers {expected_list}')
        for event_name, event in events.items():
            bet_buttons = event.get_available_prices()
            self.bet_button = next(iter(bet_buttons.values()))
            self.__class__.event_name = event_name
            event.scroll_to()
            if self.bet_button:
                break
        self.bet_button.click()
        if self.device_type == 'mobile':
            self.site.quick_bet_panel.close()
        self.assertTrue(self.bet_button.is_selected(), f'unable to select bet buttons for {self.event_name}')

        # test_018_18_verify_highlights_carousel_left_and_right_scroll
        if len(events) > 3:
            highlight_carousel.scroll_to_we()
            wait_for_haul(2)
            self.assertTrue(highlight_carousel.has_next_button(expected_result=True), 'Next button is not displayed')
            highlight_carousel.scroll_next_button.click()
            highlight_carousel.scroll_to_we()
            wait_for_haul(2)
            self.assertTrue(highlight_carousel.has_prev_button(expected_result=True), 'prev button is not displayed')
            highlight_carousel.scroll_previous_button.click()

    def test_011_verify_hc_price_and_score_updates_color_change_as_per_brand_for_in_play_event(self):
        """
        DESCRIPTION: Verify HC price and score updates, color change as per brand for in-play event
        EXPECTED: Price and score updates, color change should happen
        """
        #   covered in test case id C65865601

    def test_012_verify_hc_display_from_amp__to_as_per_cms(self):
        """
        DESCRIPTION: Verify HC display from &amp;  to as per CMS
        EXPECTED: Highlights Carousel is displayed as current date and time belong to time box set by Display from and Display to date and time fields
        """
        # covered in above stpes

    def test_013_go_to_cms_set_display_from_and_display_to_date_and_time_as_time_range_from_the_pastfuture_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' and 'Display to' date and time as time range from the past/future and save changes.
        EXPECTED: The changes are saved
        """
        # covered in test case C658614458

    def test_014_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: Highlights Carousel should not be displayed
        """
        # covered in test case C658614458

    def test_015_go_to_cms_set_display_from_from_the_past_and_display_to_in_a_few_mins_from_the_current_time_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' from the past and 'Display to' in a few mins from the current time and save changes.
        EXPECTED: Changes are saved
        """
        # covered in test case C658614458

    def test_016_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display to' is passed Highlights Carousel is no more shown on Football SLP
        """
        # covered in test case C658614458

    def test_017_go_to_cms_set_display_from_in_a_few_mins_from_current_time_and_display_to_from_the_future_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' in a few mins from current time and 'Display to' from the future and save changes.
        EXPECTED: Changes are saved
        """
        # covered in test case C658614458

    def test_018_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display from' is passed Highlights Carousel should appears
        """
        # covered in test case C658614458

    def test_019_verify_hc_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify HC left and right scroll
        EXPECTED: User should able to scroll from left to right &amp; from right to left
        """
        # covered in above step test_010_verify_live_watch_live_icons_display

    def test_020_verify_hc_display_with_greencoralorangelads_dots_for_inplay_events(self):
        """
        DESCRIPTION: Verify HC display with green(coral)/orange(lads) dots for inplay events
        EXPECTED: HC should display with green(coral)/orange(lads) dots
        """
        # can't validate the dots are they are not stable

    def test_021_verify_the_chevron_on_hc_event_cardamp_navigation(self):
        """
        DESCRIPTION: Verify the chevron on HC event card&amp; navigation
        EXPECTED: Chevron should be in blue color and aligned to right &amp; upon clicking on it should redirect to EDP of that event
        """
        # covered in above step test_007_go_to_cms_and_edit_the_title_amp_svg_icon_and_save_changes_verify_on_fe

    def test_022_verify_the_set_details_amp_score_detailssgp_fot_tennis_inplay_events(self):
        """
        DESCRIPTION: Verify the set details &amp; score details(S,G,P) fot tennis inplay events
        EXPECTED: Set 'n' and S,G,P scores should display &amp; align properly
        """
        # created highlight carousel with football events

    def test_023_verify_hc_no_of_events_display(self):
        """
        DESCRIPTION: Verify HC No of events display
        EXPECTED: No of events should display on HC should be as per cms value
        """
        # coovered in test_003_verify_created_highlight_carousal_displaying_on_fe

    def test_024_go_to_cms_change_no_of_events_amp_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, change No of events &amp; save changes. Verify on FE
        EXPECTED: No of events on HC should update as per cms changes
        """

    #     covered in test_007_go_to_cms_and_edit_the_title_amp_svg_icon_and_save_changes_verify_on_fe

    def test_025_verify_hc_display_in_play(self):
        """
        DESCRIPTION: Verify HC display in play
        EXPECTED: HC with inplay events should display on FE only if display inplay is enabled in cms
        """

    #     covered in test case C658614458

    def test_026_go_to_cms_disable_display_in_play_checkbox_verify_on_fe(self):
        """
        DESCRIPTION: Go to cms, disable display in play checkbox. Verify on FE
        EXPECTED: HC with In play events should not display on Football SLP
        """
        new_limit = 1 if len(self.events_for_type) == 0 else len(self.events_for_type)
        self.cms_config.update_highlights_carousel(self.highlights_carousels_response,
                                                   limit=new_limit, inPlay=False)
        if len(self.events_for_type) != 0:
            highlight_carousel = self.verify_highlight_carousel_on_football_slp(highlights_carousel_title=self.highlights_carousel_title,
                                                                                refresh_count=5, timeout=5)
            # validating new limit
            highlight_carousel_events = highlight_carousel.items_as_ordered_dict
            for count in range(5):
                if len(highlight_carousel_events) != new_limit:
                    self.device.driver.refresh()
                    wait_for_haul(5)
                    highlight_carousel_events = highlight_carousel.items_as_ordered_dict
                else:
                    break
            highlight_carousel_events = highlight_carousel.items_as_ordered_dict
            self.assertEqual(len(highlight_carousel_events), new_limit,
                                   msg=f'actual length of events {len(self.highlight_carousel_events)} in created highlight carousel is not same as configured{new_limit}')
            for event_name, event in highlight_carousel_events.items():
                event_object = event
                live_icon = wait_for_result(lambda: event_object.live_button, expected_result=True, timeout=1)
                # watch_live_button
                self.assertFalse(live_icon, msg=f"Live icon for event non inplay '{event_name}  found'")
            event_name, event = next(iter(highlight_carousel_events.items()))
            # ***************validating whether the event contains bet buttons *******************************
            bet_buttons = event.get_all_prices()
            self.assertTrue(bet_buttons,
                            msg=f"event does not contain bet buttons for the event in the created highlight carousel{self.highlights_carousel_name_1}")
            # ******** Verification of Highlight Carousel event odds header *************************
            expected_list = ['HOME', 'DRAW', 'AWAY']
            actual_list = [button.name.split('\n')[0].upper() for button_name, button in bet_buttons.items()]
            self.assertListEqual(expected_list, actual_list,
                                 f'actual headers of odds is {actual_list} is not same as expected odds headers {expected_list}')
            for event_name, event in self.highlight_carousel_events.items():
                bet_buttons = event.get_available_prices()
                self.bet_button = next(iter(bet_buttons.values()))
                self.__class__.event_name = event_name
                if self.bet_button:
                    break
            self.bet_button.click()
            try:
                if self.device_type == 'mobile':
                    self.site.quick_bet_panel.close()
            except Exception:
                pass
            self.assertTrue(self.bet_button.is_selected(), f'unable to select bet buttons for {self.event_name}')
        else:
            self.verify_highlight_carousel_on_football_slp(highlights_carousel_title=self.highlights_carousel_title,
                                                           refresh_count=5, timeout=5, expected_result=False)
            self.cms_config.update_highlights_carousel(self.highlights_carousels_response,
                                                       svgId=self.svg_icon, limit=new_limit, inPlay=True)
    def test_027_verify_the_match_time_on_event_card_for_football_inplay_events(self):
        """
        DESCRIPTION: Verify the match time on event card for Football inplay events
        EXPECTED: Match time should display on HC event card
        """
        # covered in test_026_go_to_cms_disable_display_in_play_checkbox_verify_on_fe

    def test_028_verify_selections_are_displaying_properly_according_to_the_sportsmarkets_in_hc(self):
        """
        DESCRIPTION: Verify selections are displaying properly according to the sports/markets in HC
        EXPECTED: Selections should display according to the sports/markets (eg: for football HOME DRAW AWAY,for tennis 1 2)
        """
        # covered in test_026_go_to_cms_disable_display_in_play_checkbox_verify_on_fe

    def test_029_verify_hc_sorting_order_as_per_cms(self):
        """
        DESCRIPTION: Verify HC sorting order as per cms
        EXPECTED: HC should display as per cms sort order
        """
        # covered in test case C658614458

    def test_030_change_the_hc_order_in_highlights_carousel_module_page_in_cms_verify_on_fe(self):
        """
        DESCRIPTION: Change the HC order in Highlights Carousel module page in cms. Verify on FE
        EXPECTED: HC order should change &amp; display as per cms order on FE
        """
        # covered in test case C658614458

    def test_031_verify_user_can_able_to_select_the_selections_on_hc(self):
        """
        DESCRIPTION: Verify user can able to select the selections on HC
        EXPECTED: User should able to select &amp; selections should be highlighted
        """
        # covered in test_026_go_to_cms_disable_display_in_play_checkbox_verify_on_fe

    def test_032_verify_univeral_view_for_hc(self):
        """
        DESCRIPTION: Verify Univeral view for HC
        EXPECTED: HC should display for all  loggedin &amp; loggedout users
        """
        # covered in test_026_go_to_cms_disable_display_in_play_checkbox_verify_on_fe

    def test_033_go_to_cms_change_to_segment_view_amp_select_any_segment_from_inclusion_segments_and_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to cms, change to segment view &amp; select any segment from inclusion segments and save changes. Verify on FE
        EXPECTED: HC should display to only segmented users which configured in cms
        """

        # no segments in slp highlight carousels

    def test_034_verify_team_namesplayer_names_on_hc(self):
        """
        DESCRIPTION: Verify Team names/Player names on HC
        EXPECTED: Team names/Player names should properly display &amp; aligned to the left
        """
        # covered in above steps

    def test_035_verify_hc_navigation_when_the_user_clicks_anywhere_on_the_event_card_except_the_odds_button(self):
        """
        DESCRIPTION: Verify HC navigation when the user clicks anywhere on the event card (except the odds button
        EXPECTED: User should navigate to the EDP of the event
        """
        # covered in above steps

    def test_036_verify_team_kits_when_hc_is_configured_using_the_type_id_for_the_football_premier_or_champions_league(self):
        """
        DESCRIPTION: Verify team kits when HC is configured using the Type ID for the football premier or Champions league
        EXPECTED: HC with the team kits should display
        """
        # covered in test case C658614458

    def test_037_go_to_cms_deactivate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, deactivate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousels should not be displayed
        """
        # covered in test case C658614458

    def test_038_go_to_cms_activate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, activate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousel should display on Football SLP
        """
        # covered in test case C658614458

    def test_039_verify_display_of_event_cards_when_the_event_is_resulted_in_hc(self):
        """
        DESCRIPTION: Verify display of event cards when the event is resulted in HC
        EXPECTED: The card of the resulted event should be removed from the HC automatically
        """
        # can't automate this test as we won't have a resulted event

    def test_040_verify_display_of_hc_when_there_is_only_1_event_card_available_to_be_displayed__amp_that_event_is_resulted(self):
        """
        DESCRIPTION: Verify display of HC when there is only 1 event card available to be displayed  &amp; that event is resulted
        EXPECTED: The card should be removed from HC and the HC should be removed from the page
        """
        # can't automate this test as we won't have a resulted event

    def test_041_go_back_to_the_same_highlights_carousel_in_cms_unselect_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go back to the same Highlights Carousel in CMS, unselect 'Active' checkbox and save changes
        EXPECTED: a)Existing Highlights Carousel is inactive
        EXPECTED: b)Changes is saved successfully
        """
        self.cms_config.update_highlights_carousel(self.highlights_carousels_response, disabled=True)
        self.verify_highlight_carousel_on_football_slp(
            highlights_carousel_title=self.highlights_carousel_title, expected_result=False)

    def test_042_load_oxygen_app_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: Load Oxygen app and verify Highlights Carousel displaying
        EXPECTED: a) Highlights Carousel is NOT displayed on Front End
        EXPECTED: b) If we have other Highlights Carousel with valid date it should display
        """
        self.cms_config.update_highlights_carousel(self.highlights_carousels_response, disabled=False)
        self.verify_highlight_carousel_on_football_slp(
            highlights_carousel_title=self.highlights_carousel_title, timeout=5)

    def test_043_go_to_cms_remove_created_hc_amp_confirm_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, Remove created HC &amp; confirm. Verify on FE
        EXPECTED: HC should disappear on FE
        """
        highlight_carousel_id = self.highlights_carousels_response.get('id')
        self.cms_config.delete_highlights_carousel(highlight_carousel_id=highlight_carousel_id)
        self.cms_config._created_highlights_carousels.remove(highlight_carousel_id)
        self.verify_highlight_carousel_on_football_slp(
            highlights_carousel_title=self.highlights_carousel_title, expected_result=False)
