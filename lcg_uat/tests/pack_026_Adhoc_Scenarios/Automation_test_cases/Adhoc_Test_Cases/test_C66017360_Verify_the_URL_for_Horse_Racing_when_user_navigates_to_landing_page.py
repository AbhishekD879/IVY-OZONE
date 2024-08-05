import pytest
import voltron.environments.constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import tests
from tests.base_test import vtest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.navigation
@pytest.mark.adhoc_suite
@pytest.mark.back_button
@pytest.mark.horseracing
@pytest.mark.adhoc24thJan24
@pytest.mark.timeout(1000)
@vtest
class Test_C66017360_Verify_the_URL_for_Horse_Racing_when_user_navigates_to_landing_page(BaseRacing):
    """
    TR_ID: C66017360
    NAME: Verify the URL for Horse Racing when user navigates to landing page
    DESCRIPTION: Verify the URL for Horse Racing when user navigates to landing page
    PRECONDITIONS: In CMS-&gt;Sport Category-&gt;Horse Racing-&gt;Target Uri-&gt;/horse-racing
    """
    keep_browser_open = True

    def compare_url(self):
        url = self.device.get_current_url()
        actual_url = url.replace('?automationtest=true','')
        self.assertEqual(actual_url, self.default_page_url, msg=f'User is not redirected to HorseRacing page and Actual URL is '
                                f'{actual_url} & the Expected URL is: {self.default_page_url}')


    def check_empty_strings(self, sections):
        """
        DESCRIPTION:  This condition ensures that the sections itself is not empty
                      and also checks if all keys in the section,
                      after stripping any whitespace, are non-empty strings.
        """
        section_name = sections.keys()
        return sections if sections and all(item.strip() != '' for item in section_name) else False

    def test_000_preconditions(self):
        """
            PRECONDITIONS: In CMS-&gt;Sport Category-&gt;Horse Racing-&gt;Target Uri-&gt;/horse-racing
        """
        sports = self.cms_config.get_sport_categories()
        sport_category = next((category for category in sports if category.get('imageTitle').strip().title() == 'Horse Racing'),None)
        self.assertIsNotNone(sport_category, 'horse racing Sport is not configured in CMS')
        actual_targetUri = sport_category['targetUri']
        expected_targetUri = 'horse-racing'
        self.assertEqual(actual_targetUri, expected_targetUri,
                         f'Actual targetUri is : "{actual_targetUri}" is not same as '
                         f'Expected targetUri : "{expected_targetUri}" in CMS')
        self.__class__.default_page_url = f'https://{tests.HOSTNAME}/horse-racing'
        self.__class__.page_url_after_back = f'https://{tests.HOSTNAME}/horse-racing/featured'

    def test_001_launch_the_front_end_application(self):
        """
        DESCRIPTION: Launch the front end application
        EXPECTED: Homepage is loaded successfully
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to Horse Racing landing page
        EXPECTED: HR landing page is successfully launched
        EXPECTED: The HR URL is displayed in the below format: 'https://sports.ladbrokes.com/horse-racing'
        """
        # Navigate to horse racing page
        self.navigate_to_page(name='horse-racing')
        # Wait for the content state to change
        self.site.wait_content_state(state_name='HorseRacing')

    def test_003_navigate_to_any_other_sub_tabs_like_next_racesfuturespecials_and_come_back_to_meetingsfeatured_tab_by_using_browser_back_button(self,back_button_type='page'):
        """
        DESCRIPTION: Navigate to any other sub tabs like: Next races/Future/Specials and come back to 'Meetings/Featured' tab by using browser back button
        EXPECTED: User successfully navigated to other tabs
        EXPECTED: The HR URL is displayed in below format: 'https://sports.ladbrokes.com/horse-racing' once came back to Featured/Meetings tab by using browser back button
        """
        tabs = self.site.horse_racing.tabs_menu.items_as_ordered_dict
        self.assertTrue(tabs, msg='No tab was found on page')
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Current tab "{current_tab}" is not the same as expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')
        next_tab = list(tabs.values())[1]
        next_tab.click()
        wait_for_haul(5)
        if back_button_type == 'browser':
            self.device.driver.back()
        if back_button_type == 'page':
            if self.brand == 'ladbrokes' and self.device_type == 'mobile':
                self.site.back_button_click()
            else:
                self.site.horse_racing.header_line.back_button.click()
        if back_button_type == 'breadcrumbs':
            breadcrumbs = self.site.horse_racing.tab_content.breadcrumbs.items_as_ordered_dict
            breadcrumbs.get('Horse Racing').click()
        self.navigate_to_page(name='horse-racing')
        # Wait for the content state to change
        self.site.wait_content_state(state_name='HorseRacing')

    def test_004_navigate_to_any_edp_page_and_come_back_by_using_browser_back_button(self,back_button_type='page'):
        """
        DESCRIPTION: Navigate to any EDP page and come back by using browser back button
        EXPECTED: User successfully navigated to EDP page
        EXPECTED: The HR URL is displayed in below format: 'https://sports.ladbrokes.com/horse-racing' once came back to Featured/Meetings tab by using browser back button
        """
        tabs = self.site.horse_racing.tabs_menu.items_as_ordered_dict
        tab = next((tab for name, tab in tabs.items() if (name.upper() == 'MEETINGS' and self.brand != 'bma') or (
                name.upper() == 'FEATURED' and self.brand == 'bma')), None)
        tab.click()
        # Getting a specific Meeting
        sections = wait_for_result(lambda: self.check_empty_strings(
            self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict),
                                   name='sections list is not loaded',
                                   timeout=20)
        uk_irish_races = next(
            (ele for item, ele in sections.items() if item.upper() == vec.racing.UK_AND_IRE_TYPE_NAME.upper()), None)
        self.assertTrue(uk_irish_races, msg='UK AND IRISH RACES meeting is not available in Horse Racing SLP')

        # click on the Meeting's event time
        meetings = wait_for_result(lambda: list(uk_irish_races.items_as_ordered_dict.values()), timeout=10)
        self.__class__.meetings_length = len(meetings)
        meeting = meetings[0]
        events = meeting.items_as_ordered_dict
        event = next(iter(events.values()))
        event.scroll_to_we()
        event.click()
        if back_button_type == 'browser':
            self.device.driver.back()
        if back_button_type == 'page':
            if self.brand == 'ladbrokes' and self.device_type == 'mobile':

                wait_for_result(lambda: self.site.back_button,
                                name="waiting for edp back button", bypass_exceptions=VoltronException, timeout=1)
                self.site.back_button.click()
            else:
                wait_for_result(lambda:self.site.racing_event_details.header_line.back_button,name = "waiting for edp back button", bypass_exceptions=VoltronException,timeout=1)
                self.site.racing_event_details.back_button_click()
        if back_button_type == 'breadcrumbs':
            breadcrumbs = self.site.racing_event_details.tab_content.breadcrumbs.items_as_ordered_dict
            breadcrumbs.get('Horse Racing').click()


    def test_005_desktop_build_your_race_card_by_selecting_few_races_and_come_back_by_using_browser_back_button(self,back_button_type='page'):
        """
        DESCRIPTION: Desktop:-
        DESCRIPTION: 'Build Your Race Card' by selecting few races and come back by using browser back button
        EXPECTED: Selected races are displayed on the Build Your Racecard page
        EXPECTED: The HR URL is displayed in below format: 'https://sports.ladbrokes.com/horse-racing' once came back to Featured/Meetings tab by using browser back button
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='horse-racing')
            self.site.wait_content_state(state_name='HorseRacing')
            self.compare_url()
            wait_for_haul(10)
            build_card = self.site.horse_racing.tab_content.build_card
            self.assertTrue(build_card, msg='Build card section is not found')
            self.assertTrue(build_card.build_race_card_button.is_displayed(), msg=f'"{vec.racing.BUILD_YOUR_RACECARD_BUTTON}" is not shown')
            build_card.build_race_card_button.click()

            self.assertTrue(build_card.exit_builder_button.is_displayed(), msg='"Exit Builder" button is not shown')
            self.assertTrue(build_card.close_icon.is_displayed(), msg='Close Button is not shown')
            self.assertTrue(build_card.clear_all_selections_button.is_displayed(), msg='"Clear all selections" button is not shown')

            # Getting a specific Meeting
            sections = wait_for_result(lambda: self.check_empty_strings(
                self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict),
                                       name='sections list is not loaded',
                                       timeout=10)
            uk_irish_races = next(
                (ele for item, ele in sections.items() if item.upper() == vec.racing.UK_AND_IRE_TYPE_NAME.upper()),
                None)
            self.assertTrue(uk_irish_races, msg='UK AND IRISH RACES meeting is not available in Horse Racing SLP')

            # click on the Meeting's event time
            meetings = wait_for_result(lambda: list(uk_irish_races.items_as_ordered_dict.values()), timeout=10)
            self.__class__.meetings_length = len(meetings)
            meeting = meetings[0]
            events = meeting.items_as_ordered_dict
            event = next(iter(events.values()))
            event.scroll_to_we()
            event.check_box.click()

            self.site.horse_racing.tab_content.build_card.build_your_race_card_button.click()
            if back_button_type == 'browser':
                self.device.driver.back()
            if back_button_type == 'page':
                if self.brand == 'ladbrokes' and self.device_type == 'mobile':
                    self.site.back_button_click()
                else:
                    wait_for_result(lambda: self.site.horse_racing.header_line.back_button.click(), name="waiting for back button", bypass_exceptions=VoltronException, timeout=1)
                    # self.site.horse_racing.header_line.back_button.click()
            if back_button_type == 'breadcrumbs':
                breadcrumbs = wait_for_result(lambda: self.site.horse_racing.tab_content.breadcrumbs.items_as_ordered_dict, name="waiting for breadcrumbs", bypass_exceptions=VoltronException, timeout=1)
                breadcrumbs.get('Horse Racing').click()
            self.navigate_to_page(name='horse-racing')
            self.site.wait_content_state(state_name='HorseRacing')

    def test_006_repeat_step_345_by_using_horse_racing_page_back_button(self):
        """
        DESCRIPTION: Repeat step-3,4,5 by using Horse Racing page back button
        EXPECTED: 
        """
    # covered in above steps

    def test_007_repeat_step_345_by_using_horse_racing_breadcrumb(self):
        """
        DESCRIPTION: Repeat step-3,4,5 by using Horse Racing' breadcrumb
        EXPECTED: 7. The HR URL is displayed in below format: 'https://sports.ladbrokes.com/horse-racing/featured'
        EXPECTED: '
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='horse-racing')
            self.site.wait_content_state(state_name='HorseRacing')
            self.test_003_navigate_to_any_other_sub_tabs_like_next_racesfuturespecials_and_come_back_to_meetingsfeatured_tab_by_using_browser_back_button(back_button_type='breadcrumbs')
            self.test_004_navigate_to_any_edp_page_and_come_back_by_using_browser_back_button(back_button_type='breadcrumbs')

    def test_008_navigate_to_homepage_and_again_navigate_to_horse_racing_page_then_refresh_the_page(self):
        """
        DESCRIPTION: Navigate to homepage and again navigate to horse racing page then refresh the page
        EXPECTED: The HR URL is displayed in below format: 'https://sports.ladbrokes.com/horse-racing'
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')
        # Navigate to horse racing page
        self.navigate_to_page(name='horse-racing')
        # Wait for the content state to change
        self.site.wait_content_state(state_name='HorseRacing')
        # refresh the page
        self.device.refresh_page()
        # Get the current URL after navigating to the sport's page
        self.compare_url()

    def test_009_duplicate_the_page_and_check_the_other_duplicated_page(self):
        """
        DESCRIPTION: Duplicate the page and check the other duplicated page
        EXPECTED: The HR URL is displayed in below format: 'https://sports.ladbrokes.com/horse-racing
        """
        # Not automable
