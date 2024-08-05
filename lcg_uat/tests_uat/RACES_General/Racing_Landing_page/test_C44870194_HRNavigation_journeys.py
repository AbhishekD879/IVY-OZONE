import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C44870194_HRNavigation_journeys(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C44870194
    NAME: HRNavigation journeys
    DESCRIPTION: "HR Navigation journeys: Home page, Highlights tab or Next Races Tab -> Tap on ""View All Horse Racing Betting"" - will lead to landing page
    DESCRIPTION: Home page, carousel link or Tab bar - App Sports (Menu) -> Tap on HR will lead to landing page
    DESCRIPTION: User is able to navigate smooth forward and backwards between the tabs and toward EDP, page is loading fine, all elements are properly displayed and is Sorted by Odds/Racecard( Filters DropDown)
    DESCRIPTION: Landing page displays races under different tabs and each tab respect display rules under Type, areas are expandable, meetings carousel are scrollable and user can see the tace status and add selections to bet slip as per requirements/GDs
    DESCRIPTION: Also verify below,
    DESCRIPTION: Verify below sections on the HR
    DESCRIPTION: UK & IRE (events with typeFlagCodes 'UK' or 'IE')
    DESCRIPTION: International (events with typeFlagCodes 'INT')
    DESCRIPTION: Virtual (events with typeFlagCodes 'VR')
    DESCRIPTION: Specials Tab
    DESCRIPTION: Next Events module
    DESCRIPTION: Tomorrow Tab"
    PRECONDITIONS: Roxanne app / site is is loaded,
    PRECONDITIONS: User is on Home Page
    """
    keep_browser_open = True

    def test_001_for_desktop_only__scroll_down_on_home_page_to_next_races_and_click_on_view_all_horse_racing_events(self):
        """
        DESCRIPTION: For Desktop only : Scroll down on home page to 'NEXT RACES' and click on 'VIEW ALL HORSE RACING EVENTS'
        EXPECTED: User should navigate to Horse Racing Landing Page.
        """
        self.site.login()
        self.site.wait_content_state('HomePage')
        if self.device_type == 'desktop':
            self.site.home.desktop_modules.next_races_module.view_all_horse_racing_events.click()
            self.site.wait_content_state('Horseracing')

    def test_002_for_desktop_only___tap_on_horse_racing_from1_header_menu2_a_z_sports(self):
        """
        DESCRIPTION: For Desktop only :  Tap on Horse Racing from
        DESCRIPTION: 1. Header menu
        DESCRIPTION: 2. A-Z Sports
        EXPECTED: User should navigate to Horse Racing Landing Page.
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='Home')
            self.site.header.sport_menu.items_as_ordered_dict['HORSE RACING'].click()
            self.site.wait_content_state('Horseracing')
            self.navigate_to_page(name='Home')
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertIn('Horse Racing', sports.keys(), msg='Horse racing NOT available in A-Z sports left-hand menu')
            sports.get('Horse Racing').click()
            self.site.wait_content_state('Horseracing')

    def test_003_for_mobile__tablet_only__tap_on_horses_from1_sports_carousal2_all_sports__horses3_any_quick_link_if_configured_on_home_page_eg__todays_racing(self):
        """
        DESCRIPTION: For Mobile / Tablet only : Tap on Horses from
        DESCRIPTION: 1. Sports carousal
        DESCRIPTION: 2. All Sports > Horses
        DESCRIPTION: 3. Any Quick Link if configured on Home Page eg : 'Today's Racing'
        EXPECTED: User should navigate to Horse Racing Landing Page.
        """
        if not self.device_type == 'desktop':
            self.site.open_sport(name=vec.SB.HORSERACING.upper())
            self.site.wait_content_state('Horseracing')
            self.navigate_to_page(name='Home')

            self.site.home.menu_carousel.click_item(vec.SB.ALL_SPORTS)
            self.site.all_sports.a_z_sports_section.items_as_ordered_dict['Horse Racing'].click()
            self.site.wait_splash_to_hide(4)
            self.site.wait_content_state('Horseracing')

    def test_004_verify_various_tabs_on_hr_landing_page1_meetings2_next_races3_futures4_specials(self):
        """
        DESCRIPTION: Verify various tabs on HR Landing Page
        DESCRIPTION: 1. Meetings
        DESCRIPTION: 2. Next Races
        DESCRIPTION: 3. Futures
        DESCRIPTION: 4. Specials
        EXPECTED: User should be able to move forward and backward between the tabs smoothly. all the elements of the tab should properly displayed.
        """
        available_tabs = self.site.horse_racing.tabs_menu.items_as_ordered_dict
        self.assertTrue(available_tabs, msg='No tabs found on Horse Racing page')
        for tabs, tabs_name in available_tabs.items():
            tabs_name.click()
            self.site.wait_content_state_changed(timeout=15)
            selected_tab = self.site.horse_racing.tabs_menu.current
            self.assertEqual(tabs, selected_tab, msg=f'"{tabs}" tab is not active, active is "{selected_tab}"')
            if selected_tab == 'YOURCALL':
                static_block = self.site.horse_racing.tab_content.accordions_list.static_block
                self.assertTrue(static_block, msg='Can not find Static Block')
                self.assertTrue(static_block.tweet_now_button, msg='Can not find "Tweet Now" button')
            else:
                sleep(5)
                self.site.wait_content_state_changed(timeout=15)
                accordions_list = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(accordions_list, msg=f'No event section found on "{tabs}" tabs page')

    def test_005_verify_meetings_tab(self):
        """
        DESCRIPTION: Verify Meetings tab
        EXPECTED: Meetings tab should display all the meetings grouped under
        EXPECTED: 1. Offers and Featured Races ( If any available)
        EXPECTED: 2. UK & IRE (events with typeFlagCodes 'UK' or 'IRE')
        EXPECTED: 3. International (events with typeFlagCodes 'INT')
        EXPECTED: 4. Virtual (events with typeFlagCodes 'VR')
        EXPECTED: User should be able to expand / collapse the grouping accordions.
        """
        self.navigate_to_page('horse-racing')
        self.site.wait_content_state('Horseracing')
        accordions_list = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(accordions_list, msg=f'No event section found on "{vec.racing.RACING_DEFAULT_TAB_NAME}" tabs page')
        for meeting_name, meeting in accordions_list.items():
            self.site.wait_content_state_changed(timeout=15)
            meeting.scroll_to()
            self.assertTrue(meeting.is_displayed(), msg='meeting is not displayed')
            self.assertTrue(meeting.is_expanded(), msg=f'Event "{meeting_name}" is not Expanded by default')
            meeting.collapse()
            self.assertFalse(meeting.is_expanded(), msg=f'Event "{meeting_name}" is not Collapsed')

    def test_006_click_on_any_meeting(self):
        """
        DESCRIPTION: Click on any meeting
        EXPECTED: User is landed on the respecting Meeting(Event) Landing Page.
        EXPECTED: Should be able to scroll across the Meeting carousal.
        EXPECTED: User should be able to see the race Status
        EXPECTED: User should be able to add selections to bet slip if the race is not suspended.
        EXPECTED: User should be able to change the display Sort order : Price / Racecard (for Win/Each Way )
        """
        expected_event = None
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing', timeout=30)
        sleep(5)
        accordions_list = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        for section_name, section in accordions_list.items():
            if section_name in vec.racing.COUNTRY_SKIP_LIST:
                continue
            else:
                meetings = section.items_as_ordered_dict
                for meeting_name, meeting in meetings.items():
                    events = meeting.items_as_ordered_dict
                    for event_name, event in events.items():
                        race_started = event.is_resulted or event.has_race_off()
                        if not race_started:
                            expected_event = event
                            break
                    if expected_event is not None:
                        break
                if expected_event is not None:
                    break

        selections_racecard = []
        if expected_event is not None:
            self.navigate_to_edp(expected_event.event_id, 'horse-racing')
            self.site.wait_content_state('RacingEventDetails', timeout=30)
            self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab('WIN OR E/W')
            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            section = list(sections.values())[0]
            horses_details = section.items_as_ordered_dict
            selections_price = list(horses_details.keys())
            first_horse = list(horses_details.values())[0]
            first_horse.bet_button.click()

            if self.device_type == 'desktop':
                result = first_horse.bet_button.is_selected(timeout=2)
                self.assertTrue(result, msg=f'Bet button is not active after selection')
                singles_section = self.get_betslip_sections().Singles
                self.assertTrue(singles_section, msg='There is no bet sections available')
                for stake_name, stake in singles_section.items():
                    stake.amount_form.input.clear()
                    stake.amount_form.input.value = self.bet_amount
                self.get_betslip_content().bet_now_button.click()
                self.check_bet_receipt_is_displayed()
            else:
                quick_bet = self.site.quick_bet_panel.selection.content
                quick_bet.amount_form.input.clear()
                quick_bet.amount_form.input.value = self.bet_amount
                self.site.quick_bet_panel.place_bet.click()
                bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
                self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
                self.site.quick_bet_panel.close()

            if self.site.racing_event_details.tab_content.has_sorting_toggle():
                self.site.racing_event_details.tab_content.choose_sorting_option(option=vec.racing.CARD_SORTING_OPTION)
                sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
                self.assertTrue(sections, msg='There is no Event Market List available')
                section = list(sections.values())[0]
                horses_details = section.items_as_ordered_dict
                for horse, outcome in horses_details.items():
                    selections_racecard.append(outcome.output_price)
                self.assertNotEquals(selections_price, selections_racecard,
                                     msg='Same selection order shown after selecting racecard option')

    def test_007_while_on_hr_landing_page_tap_on_next_races(self):
        """
        DESCRIPTION: While on HR Landing page, tap on 'NEXT RACES'
        EXPECTED: All the next races that are about to start should load in order of start time, earliest being on the top.
        EXPECTED: Each event displays the first 3 entries with an option to view the full racecard by clicking on 'MORE'
        """
        self.navigate_to_page(name='horse-racing')
        sleep(5)
        if self.brand == 'bma':
            sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
            all_sections = (x.lower() for x in list(sections.keys()))
            self.assertIn(vec.racing.NEXT_RACES.lower(), all_sections, msg='Next Races tab is NOT available')
        else:
            tab = self.site.horse_racing.tabs_menu.click_button(button_name=vec.racing.NEXT_RACES.upper())
            self.assertTrue(tab, msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')
            sections = self.get_sections('horse-racing')

        self.assertTrue(sections, msg='Sections on Horse Racing page are not found')
        for section_name, section in sections.items():
            if section_name.lower() == vec.racing.NEXT_RACES.lower():
                events = section.items_as_ordered_dict
                for entries_name, entries in events.items():
                    self.assertTrue(entries.event_name, msg='Event Name not available')
                    self.assertTrue(entries.has_view_full_race_card(), msg='Full race card is not available')
                    self.assertTrue(entries.items_as_ordered_dict,
                                    msg=f'Horses Rows are not available for "{entries.event_name}"')
                break

    def test_008_while_on_hr_landing_page_verify_future_tab(self):
        """
        DESCRIPTION: While on HR landing page, Verify Future tab
        EXPECTED: User should be able to see the information related to Future events
        """
        # covered in test_004_verify_various_tabs_on_hr_landing_page1_meetings2_next_races3_futures4_specials

    def test_009_while_on_hr_landing_page_verify_specials_tab(self):
        """
        DESCRIPTION: While on HR landing page, Verify Specials Tab
        EXPECTED: User should see the information related to Special HR events
        """
        # covered in test_004_verify_various_tabs_on_hr_landing_page1_meetings2_next_races3_futures4_specials
