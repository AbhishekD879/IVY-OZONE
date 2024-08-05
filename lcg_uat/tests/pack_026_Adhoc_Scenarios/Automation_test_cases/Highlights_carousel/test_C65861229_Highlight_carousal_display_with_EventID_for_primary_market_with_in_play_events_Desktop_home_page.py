import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from datetime import datetime
from crlat_ob_client.utils.date_time import get_date_time_as_string
from voltron.utils.waiters import wait_for_cms_reflection, wait_for_haul
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    generate_highlights_carousel_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.highlights_carousel
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.other
@pytest.mark.last
@vtest
class Test_C65861229_Highlight_carousal_display_with_EventID_for_primary_market_with_in_play_events_Desktop_home_page(Common):
    """
    TR_ID: C65861229
    NAME: Highlight carousal display with EventID for primary market with in-play events-Desktop home page
    DESCRIPTION: This test case is to verify Highlight carousal display with EventID for primary market with in-play events-Desktop Homepage
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS Navigation:
    PRECONDITIONS: CMS > sports pages >home page> Highlights Carousel and click on Create Highlights Carousel CTA.
    PRECONDITIONS: Configure HC as below by giving all the fields.
    PRECONDITIONS: *Enable "Active & Display on Desktop" check boxes
    PRECONDITIONS: *Title=TENNIS - FEATURED MATCHES
    PRECONDITIONS: *Set events by=Event IDs
    PRECONDITIONS: *Event IDs= 240767310,240778313 (Inplay events)
    PRECONDITIONS: *Select Market & Market Type = Primary Market
    PRECONDITIONS: *Display from & Display to time period (eg: from 7/6/2023 11:05:34 to 7/7/2023 11:05:34)
    PRECONDITIONS: *SVG Icon=tennis
    PRECONDITIONS: *No. of Events = 2
    PRECONDITIONS: *Enable Display In-Play checkbox
    PRECONDITIONS: *Select Universal view
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    svg_icon = 'football'

    def get_highlight_carousel(self, name=None, expected_result=True):
        highlight_carousal = wait_for_cms_reflection(lambda: self.site.home.desktop_modules.items_as_ordered_dict.get(
            'FEATURED').tab_content.highlight_carousels.get(name), ref=self, timeout=3, refresh_count=3, haul=3,
                                                     expected_result=expected_result)
        return highlight_carousal

    def convert_highlights_carousel_title(self, title):
        return title if not self.brand == 'ladbrokes' else title.upper()

    def test_000_preconditions(self):
        """
        DESCRIPTION: "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
        DESCRIPTION: 2 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel
        """
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.football_config.category_id
            live_event = self.get_active_events_for_category(category_id=category_id, in_play_event=True,
                                                             number_of_events=2, raise_exceptions=False)
            if not live_event:
                category_id = self.ob_config.tennis_config.category_id
                live_event = self.get_active_events_for_category(category_id=category_id, in_play_event=True,
                                                                 number_of_events=2)
                self.__class__.svg_icon = 'tennis'
            self.__class__.event = self.get_active_events_for_category(category_id=category_id, in_play_event=False,
                                                                       number_of_events=3)

            self._logger.info(f"events length {len(live_event)}")

            event_response_1 = live_event[0]['event']
            event_response_2 = self.event[0]['event']
            event_response_3 = self.event[1]['event']
            event_response_4 = self.event[2]['event']

        else:
            self.__class__.event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.event1 = self.ob_config.add_football_event_to_england_premier_league(is_live=True)
            self.__class__.event_2 = self.ob_config.add_autotest_premier_league_football_event(team1='Man City',
                                                                                               team2='Chelsea')
            self.__class__.event_3 = self.ob_config.add_autotest_premier_league_football_event()

            event_response_1 = self.event.ss_response['event']
            event_response_2 = self.event1.ss_response['event']
            event_response_3 = self.event_2.ss_response['event']
            event_response_4 = self.event_3.ss_response['event']

        self.__class__.highlights_carousel_title = self.convert_highlights_carousel_title(
            title=generate_highlights_carousel_name())
        self.__class__.expected_highlights_carousel_events = [event_response_1['name'].upper().strip(),
                                                              event_response_2['name'].upper().strip(),
                                                              event_response_3['name'].upper().strip(),
                                                              event_response_4['name'].upper().strip()]

        self.__class__.highlights_carousel_event_ids = [event_response_1['id'], event_response_2['id'],
                                                        event_response_3['id'], event_response_4['id']]

        self.__class__.highlights_carousel = self.cms_config.create_highlights_carousel(
            title=self.highlights_carousel_title, events=self.highlights_carousel_event_ids, displayOnDesktop=True,
            svgId=self.svg_icon, inplay=True)

    def test_001_launch_bma_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch BMA Ladbrokes/Coral Application
        EXPECTED: User should be able to launch successfully
        """
        self.site.wait_content_state(state_name='Homepage', timeout=15)

    def test_002_verify_created_highlight_carousal_displaying_on_fe(self):
        """
        DESCRIPTION: Verify Created Highlight carousal displaying on FE
        EXPECTED: Created HC should display on Homepage
        """
        self.__class__.actual_highlight_carousel = self.get_highlight_carousel(name=self.highlights_carousel_title)
        self.assertTrue(self.actual_highlight_carousel,
                        msg=f"Created Highlight Carousel {self.highlights_carousel_title} is not displayed")

        # Verification of Highlight Carousel events
        actual_highlights_carousel_events = [item_name.upper() for item_name in
                                             self.actual_highlight_carousel.items_names]
        self.assertListEqual(self.expected_highlights_carousel_events, actual_highlights_carousel_events,
                             msg=f'actual highlights carousel events {actual_highlights_carousel_events} not equals '
                                 f'to expected highlights carousel events {self.expected_highlights_carousel_events}')

    def test_003_verify_the_order_of_the_highlights_carousel_module_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the Highlights Carousel module is as per order in the CMS
        EXPECTED: The order should be as per CMS
        """
        # This step is covered in C65861232 testcase 003 step

    def test_004_change_the_order_in_the_cms_in_the_application_refresh_the_page_and_verify_the_order_is_updated(self):
        """
        DESCRIPTION: Change the order in the CMS. In the application refresh the page and verify the order is updated
        EXPECTED: The order is updated and is as defined in the CMS
        """
        # This step is covered in C65861232 testcase 004 step

    def test_005_verify_title_amp_svg_icon(self):
        """
        DESCRIPTION: Verify title &amp; SVG Icon
        EXPECTED: HC title  &amp; SVG Icon should be as per cms. Title should be in capitals
        """
        expected_title = self.highlights_carousel_title
        self.__class__.actual_highlight_carousel = self.get_highlight_carousel(name=self.highlights_carousel_title)
        self.assertEqual(expected_title, self.actual_highlight_carousel.name,
                         msg=f"Highlight carousels title should be '{expected_title}'"
                             f" but got '{self.actual_highlight_carousel.name}'")
        expected_svg_icon = f'#{self.svg_icon}'
        actual_svg_icon = self.actual_highlight_carousel.svg_icon_text
        self.assertEqual(expected_svg_icon, actual_svg_icon,
                         f'{expected_svg_icon} Svg icon is not displayed {actual_svg_icon} is displayed')

    def test_006_go_to_cms_and_edit_the_title_amp_svg_icon_and_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS and Edit the title &amp; SVG Icon and save changes. Verify on FE
        EXPECTED: Title &amp; SVG Icon should be updated on Homepage as per cms changes
        """
        self.__class__.highlights_carousel_title = self.convert_highlights_carousel_title(
            generate_highlights_carousel_name())
        if self.svg_icon == 'football':
            self.svg_icon = 'background-football'
        else:
            self.svg_icon = 'icon-tennis'

        self.cms_config.update_highlights_carousel(self.highlights_carousel, title=self.highlights_carousel_title,
                                                   svgId=self.svg_icon)

        self.assertEqual(self.get_highlight_carousel(name=self.highlights_carousel_title).svg_icon_text,
                         f'#{self.svg_icon}', f'Svg icon {self.svg_icon} is not displayed')

    def test_007_verify_live_watch_live_icons_display(self):
        """
        DESCRIPTION: Verify live, watch live icons display
        EXPECTED: Live, watch live icons should display for inplay events
        """
        # This step is covered in C65857284 step 11

    def test_008_verify_hc_price_and_score_updates_color_change_as_per_brand_for_in_play_event(self):
        """
        DESCRIPTION: Verify HC price and score updates, color change as per brand for in-play event
        EXPECTED: Price and score updates, color change should happen
        """
        # Only for Stage

    def test_009_verify_hc_display_from_amp__to_as_per_cms(self):
        """
        DESCRIPTION: Verify HC display from &amp;  to as per CMS
        EXPECTED: Highlights Carousel is displayed as current date and time belong to time box set by Display from and Display to date and time fields
        """
        # This step covered in step 06

    def test_010_go_to_cms_set_display_from_and_display_to_date_and_time_as_time_range_from_the_pastfuture_and_save_changes(
            self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' and 'Display to' date and time as time range from the past/future and save changes.
        EXPECTED: The changes are saved
        """
        self.__class__.time_format = '%Y-%m-%dT%H:%M:%S.%f'
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-4.5)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=-2)[:-3] + 'Z'
        self.cms_config.update_highlights_carousel(highlight_carousel=self.highlights_carousel, start_time=start_time,
                                                   end_time=end_time)

    def test_011_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: Highlights Carousel should not be displayed
        """
        highlights_carousel = self.get_highlight_carousel(self.highlights_carousel_title, expected_result=False)
        self.assertFalse(highlights_carousel, msg=f'{self.highlights_carousel_title} is not displayed')

    def test_012_go_to_cms_set_display_from_from_the_past_and_display_to_in_a_few_mins_from_the_current_time_and_save_changes(
            self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' from the past and 'Display to' in a few mins from the current time and save changes.
        EXPECTED: Changes are saved
        """
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-6)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format, minutes=1,
                                           url_encode=False, )[:-3] + 'Z'
        self.cms_config.update_highlights_carousel(highlight_carousel=self.highlights_carousel, start_time=start_time,
                                                   end_time=end_time)

    def test_013_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display to' is passed Highlights Carousel is no more shown on Homepage
        """
        highlights_carousel = self.get_highlight_carousel(self.highlights_carousel_title)
        self.assertTrue(highlights_carousel, msg=f'{self.highlights_carousel_title} is not displayed')
        wait_for_haul(60)
        highlights_carousel = self.get_highlight_carousel(self.highlights_carousel_title, expected_result=False)
        self.assertFalse(highlights_carousel, msg=f'{self.highlights_carousel_title} is not displayed')

    def test_014_go_to_cms_set_display_from_in_a_few_mins_from_current_time_and_display_to_from_the_future_and_save_changes(
            self):
        """
        DESCRIPTION: Go to CMS, set 'Display from' in a few mins from current time and 'Display to' from the future
        and save changes. EXPECTED: Changes are saved
        """
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format, minutes=1,
                                             url_encode=False)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format, days=2,
                                           url_encode=False, hours=-5.5)[:-3] + 'Z'
        self.cms_config.update_highlights_carousel(self.highlights_carousel, start_time=start_time,
                                                   end_time=end_time)

    def test_015_verify_on_fe(self):
        """
        DESCRIPTION: Verify on FE
        EXPECTED: After time set in 'Display from' is passed Highlights Carousel should appears
        """
        wait_for_haul(60)
        highlights_carousel = self.get_highlight_carousel(self.highlights_carousel_title)
        self.assertTrue(highlights_carousel, msg=f'{self.highlights_carousel_title} is not displayed')

    def test_016_verify_carousel_display_if_hc_has_more_than_3_eventsconfig_4_event_ids_in_cms_amp_no_of_event4_on_hc(
            self):
        """
        DESCRIPTION: Verify Carousel display if HC has more than 3 events(config 4 event id's in cms &amp; No of event=4) on HC
        EXPECTED: Carousel should display only if HC has more than 3 events
        """
        self.cms_config.update_highlights_carousel(self.highlights_carousel, limit=2)
        actual_events_count = 0
        for i in range(3):
            wait_for_haul(10)
            self.device.driver.refresh()
            highlight_carousel = self.get_highlight_carousel(self.highlights_carousel_title)
            self.assertTrue(highlight_carousel.is_displayed(),
                            msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_title}')
            actual_events_count = len(highlight_carousel.items_as_ordered_dict)
            if actual_events_count == 2:
                break
        highlight_carousel = self.get_highlight_carousel(self.highlights_carousel_title)
        actual_events_count = len(highlight_carousel.items_as_ordered_dict)
        self.assertEqual(actual_events_count, 2,
                         msg=f' actual displayed no.of events {actual_events_count} . But expected no.of events are {2}')

    def test_017_verify_hc_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify HC left and right scroll
        EXPECTED: User should be able to scroll from left to right &amp; from right to left
        """
        # This step is covered in C65857286 step 17

    def test_018_verify_hc_display_with_greencoralorangelads_dots_for_inplay_events(self):
        """
        DESCRIPTION: Verify HC display with green(coral)/orange(lads) dots for inplay events
        EXPECTED: HC should display with green(coral)/orange(lads) dots
        """
        # This step is covered in C65857284 step 13

    def test_019_verify_the_chevron_on_hc_event_card_amp_navigation(self):
        """
        DESCRIPTION: Verify the chevron on HC event card &amp; navigation
        EXPECTED: Chevron should be in blue color and aligned to right &amp; upon clicking on it should redirect to EDP of that event
        """
        highlight_carousel_events = self.get_highlight_carousel(self.highlights_carousel_title).items_as_ordered_dict
        self.assertTrue(highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_title}"')
        highlight_carousel_events = {key.upper(): value for key, value in highlight_carousel_events.items()}
        highlight_carousel_events.get(self.expected_highlights_carousel_events[1]).click()
        self.site.wait_content_state(state_name='EventDetails', timeout=10)
        current_url = self.device.get_current_url()
        self.assertIn(self.highlights_carousel_event_ids[1], current_url, msg="event details page not displayed")
        self.site.back_button_click()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        section = self.get_highlight_carousel(self.highlights_carousel_title)
        self.__class__.highlight_carousel_events = section.items_as_ordered_dict
        self.assertTrue(self.highlight_carousel_events,
                        msg=f'No events in Highlights Carousel named "{self.highlights_carousel_title}"')

    def test_020_verify_the_set_details_amp_score_detailssgp_fot_tennis_inplay_events(self):
        """
        DESCRIPTION: Verify the set details &amp; score details(S,G,P) fot tennis inplay events
        EXPECTED: Set 'n' and S,G,P scores should display &amp; align properly
        """
        # This step is covered in C65861231

    def test_021_verify_hc_no_of_events_display(self):
        """
        DESCRIPTION: Verify HC No of events display
        EXPECTED: No of events should display on HC should be as per cms value
        """
        # This step is Covered in  step 16

    def test_022_go_to_cms_change_no_of_events_amp_save_changes_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, change No of events &amp; save changes. Verify on FE
        EXPECTED: No of events on HC should update as per cms changes
        """
        # This step is covered in step 16

    def test_023_verify_hc_display_as_per_cms_entry_as_per_comma_separation(self):
        """
        DESCRIPTION: Verify HC display as per CMS entry as per comma separation
        EXPECTED: Hc events should display as per comma seperation (eg: if two event id's configured in cms, the first congigured event should display first in FE, second configured event should diplay in second place)
        """
        # # This step is Covered in precondition

    def test_024_verify_hc_display_in_play(self):
        """
        DESCRIPTION: Verify HC display in play
        EXPECTED: HC with inplay events should display on FE only if display inplay is enabled in cms
        """
        self.cms_config.update_highlights_carousel(self.highlights_carousel, inPlay=True)
        highlight_carousel = self.get_highlight_carousel(self.highlights_carousel_title)
        active_events = [item_name.upper() for item_name in highlight_carousel.items_names]
        self.assertIn(self.expected_highlights_carousel_events[0], active_events,
                      msg=f'{self.expected_highlights_carousel_events[0]} event is not available in highlight '
                          f'carousel events {active_events}')

    def test_025_go_to_cms_disable_display_in_play_checkbox_verify_on_fe(self):
        """
        DESCRIPTION: Go to cms, disable display in play checkbox. Verify on FE
        EXPECTED: HC with In play events should not display on Homepage
        """
        self.cms_config.update_highlights_carousel(self.highlights_carousel, inPlay=False)
        wait_for_haul(15)
        self.device.driver.refresh()
        highlight_carousel = self.get_highlight_carousel(self.highlights_carousel_title)
        active_events = [item_name.upper() for item_name in highlight_carousel.items_names]
        self.assertNotIn(self.expected_highlights_carousel_events[0], active_events,
                         msg=f'{self.expected_highlights_carousel_events[0]} event is available in highlight '
                             f'carousel events{active_events}')

    def test_026_verify_the_match_time_on_event_card_for_football_inplay_events(self):
        """
        DESCRIPTION: Verify the match time on event card for Football inplay events
        EXPECTED: Match time should display on HC event card
        """
        # This step is covered in C65861231

    def test_027_verify_selections_are_displaying_properly_according_to_the_sportsmarkets_in_hc(self):
        """
        DESCRIPTION: Verify selections are displaying properly according to the sports/markets in HC
        EXPECTED: Selections should display according to the sports/markets (eg: for football HOME DRAW AWAY,for tennis 1 2)
        """
        # This step is covered in C65861232

    def test_028_verify_hc_sorting_order_as_per_cms(self):
        """
        DESCRIPTION: Verify HC sorting order as per cms
        EXPECTED: HC should display as per cms sort order
        """
        # This step is covered in C65861232

    def test_029_change_the_hc_order_in_highlights_carousel_module_page_in_cms_verify_on_fe(self):
        """
        DESCRIPTION: Change the HC order in Highlights Carousel module page in cms. Verify on FE
        EXPECTED: HC order should change &amp; display as per cms order on FE
        """
        # This step is covered in C65861232

    def test_030_verify_user_can_able_to_select_the_selections_on_hc(self):
        """
        DESCRIPTION: Verify user can select the selections on HC
        EXPECTED: User should be able to select &amp; selections should be highlighted
        """
        highlight_carousel_events = self.get_highlight_carousel(self.highlights_carousel_title).items_as_ordered_dict
        highlight_carousel_events = {key.upper(): value for key, value in highlight_carousel_events.items()}
        event = highlight_carousel_events.get(self.expected_highlights_carousel_events[2])
        bet_button = event.first_player_bet_button
        bet_button.click()
        self.assertTrue(bet_button.is_selected(), f'bet button is not selected')
        bet_button_2 = event.second_player_bet_button
        bet_button_2.click()
        self.assertTrue(bet_button_2.is_selected(), f'bet button is not selected')

    def test_031_verify_univeral_view_for_hc(self):
        """
        DESCRIPTION: Verify Universal view for HC
        EXPECTED: HC should display for all  logged in &amp; loggedout users
        """
        self.site.login()
        after_login_HC = self.get_highlight_carousel(self.highlights_carousel_title)
        self.assertTrue(after_login_HC, msg=' Highlights carousel not displayed after login the user')

    def test_032_go_to_cms_change_to_segment_view_amp_select_any_segment_from_inclusion_segments_and_save_changes_verify_on_fe(
            self):
        """
        DESCRIPTION: Go to cms, change to segment view &amp; select any segment from inclusion segments and save changes. Verify on FE
        EXPECTED: HC should display to only segmented users which configured in cms
        """
        # This step is covered in C65861232

    def test_033_verify_team_namesplayer_names_on_hc(self):
        """
        DESCRIPTION: Verify Team names/Player names on HC
        EXPECTED: Team names/Player names should properly display &amp; aligned to the left
        """
        # This step is covered in step 02

    def test_034_verify_hc_navigation_when_the_user_clicks_anywhere_on_the_event_card_except_the_odds_button(self):
        """
        DESCRIPTION: Verify HC navigation when the user clicks anywhere on the event card (except the odds button
        EXPECTED: User should navigate to the EDP of the event
        """
        # This step is covered in step 19

    def test_035_verify_team_kits_when_hc_is_configured_using_the_event_id_for_the_football_premier_or_champions_league(
            self):
        """
        DESCRIPTION: Verify team kits when HC is configured using the event ID for the football premier or Champions league
        EXPECTED: HC with the team kits should display
        """
        highlight_carousel_events = self.get_highlight_carousel(self.highlights_carousel_title).items_as_ordered_dict
        highlight_carousel_events = {key.upper(): value for key, value in highlight_carousel_events.items()}
        self.assertTrue(highlight_carousel_events,
                        msg=f'No events in Highlights Carousel "{self.highlights_carousel_title}"')
        self.assertIn(self.expected_highlights_carousel_events[2], highlight_carousel_events,
                      msg=f'Event "{self.expected_highlights_carousel_events[2]}" is not displayed in Carousel "{self.highlights_carousel_title}" '
                          f'among events "{highlight_carousel_events}"')

        event = highlight_carousel_events.get(self.expected_highlights_carousel_events[2])
        if tests.settings.backend_env != 'prod':
            self.assertTrue(event.has_team_kits,
                            msg=f'Team kits are not displayed for event "{self.expected_highlights_carousel_events[1]}"')

    def test_036_go_to_cms_deactivate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, deactivate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousels should not be displayed
        """
        cms_hc_homepage = self.cms_config.get_sport_module(sport_id=0, module_type='HIGHLIGHTS_CAROUSEL')[0]
        if not cms_hc_homepage['disabled']:
            self.cms_config.change_sport_module_state(sport_module=cms_hc_homepage, active=False)

    def test_037_go_to_cms_activate_the_whole_highlights_carousel_module_go_to_fe_refresh_amp_verify_hc(self):
        """
        DESCRIPTION: Go to cms, activate the whole Highlights carousel module. Go to FE, Refresh &amp; verify HC
        EXPECTED: Highlights Carousel should display on homepage
        """
        cms_hc_homepage = self.cms_config.get_sport_module(sport_id=0, module_type='HIGHLIGHTS_CAROUSEL')[0]
        if cms_hc_homepage['disabled']:
            self.cms_config.change_sport_module_state(sport_module=cms_hc_homepage)

    def test_038_verify_display_of_event_cards_when_the_event_is_resulted_in_hc(self):
        """
        DESCRIPTION: Verify display of event cards when the event is resulted in HC
        EXPECTED: The card of the resulted event should be removed from the HC automatically
        """
        # we can't get the event which is already resulted in beta

    def test_039_verify_display_of_hc_when_there_is_only_1_event_card_available_to_be_displayed__amp_that_event_is_resulted(
            self):
        """
        DESCRIPTION: Verify display of HC when there is only 1 event card available to be displayed  &amp; that event is resulted
        EXPECTED: The card should be removed from HC and the HC should be removed from the page
        """
        # we can't get the event which is already resulted in beta

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
        highlight_carousel = self.get_highlight_carousel(name=self.highlights_carousel_title,
                                                         expected_result=False)
        self.assertFalse(highlight_carousel, msg=f"Expected HC to disappear on FE after deletion but found on FE")

    def test_042_go_to_cms_remove_created_hc_amp_confirm_verify_on_fe(self):
        """
        DESCRIPTION: Go to CMS, Remove created HC &amp; confirm. Verify on FE
        EXPECTED: HC should disappear on FE
        """
        highlight_carousel_id = self.highlights_carousel["id"]
        self.cms_config.delete_highlights_carousel(highlight_carousel_id)
        self.cms_config._created_highlights_carousels.remove(highlight_carousel_id)
        highlight_carousel = self.get_highlight_carousel(name=self.highlights_carousel_title, expected_result=False)
        self.assertFalse(highlight_carousel, msg=f"Expected HC to disappear on FE after deletion but found on FE")
