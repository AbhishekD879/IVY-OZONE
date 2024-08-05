import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from faker import Faker
from voltron.utils.waiters import wait_for_haul, wait_for_cms_reflection


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.back_button
@pytest.mark.desktop
@pytest.mark.navigation
@pytest.mark.Big_Competition
@pytest.mark.adhoc24thJan24
@vtest
class Test_C66017357_Verify_the_URL_for_Big_Competition_when_user_navigates_to_default_page(Common):
    """
    TR_ID: C66017357
    NAME: Verify the URL for Big Competition when user navigates to default page
    DESCRIPTION: Verify the URL for BigC when user navigates to default page
    PRECONDITIONS: In CMS BigC should be configured properly
    PRECONDITIONS: In CMS the Target Uri-&gt;big-competition/world-cup(for example)
    """
    keep_browser_open = True
    faker = Faker()
    competition_name = f'Auto C66017357 {faker.city()}'
    new_id = faker.random.randint(200, 1000)

    def create_big_competition_and_sport_category(self, type_id):

        # Create a new big competition
        new_competition = self.cms_config.create_big_competition(type_Id=type_id,
                                                                 competition_name=self.competition_name)
        # Assign IDs and URIs from the new competition data
        self.__class__.new_competition_id = f"{new_competition.get('id')}"
        self.__class__.new_competition_uri = new_competition.get('uri')
        self.__class__.competition_name = new_competition.get('name')
        # Construct the URL for the new category
        new_category_ulr = f'big-competition{self.new_competition_uri}'
        # Create a new tab under the created Big competition
        first_tab = self.cms_config.create_tab_for_big_competition(
            competition_id=self.new_competition_id,
            tab_name='highlight'
        )
        first_tab_id = first_tab.get('id')
        self.__class__.first_tab_name = first_tab.get('name').lower()

        second_tab = self.cms_config.create_tab_for_big_competition(
            competition_id=self.new_competition_id,
            tab_name='Results'
        )
        second_tab_id = second_tab.get('id')
        self.__class__.second_tab_name = second_tab.get('name').lower()

        wait_for_haul(2)  # Wait for a short time

        # Create a new module under the previously created big competition tab.
        first_tab_module_id = self.cms_config.create_module_for_big_competation(
            competition_id=self.new_competition_id,
            tab_id=first_tab_id, module_name='events',
            module_type='NEXT_EVENTS'
        ).get('id')

        # Updating the newly created module with a type ID.
        self.cms_config.update_next_events_module_for_big_competition(
            module_name='events',
            module_type='NEXT_EVENTS',
            module_id=first_tab_module_id,
            type_id=type_id
        )

        wait_for_haul(2)  # Wait for a short time

        # Create a new sport category for the Big competition which is created
        self.cms_config.create_sport_category(title=self.competition_name, categoryId=self.new_id,
                                              ssCategoryCode=self.new_id, targetUri=new_category_ulr,
                                              tier='UNTIED', showInAZ=True, showInHome=True)

    def get_sub_tab_items(self):
        all_tabs_menu = self.site.big_competitions.tabs_menu.items_as_ordered_dict
        return {key.lower(): value for key, value in all_tabs_menu.items()}

    def navigate_to_edp_and_verify_back_button(self, back_button_type='browser'):
        accordions_list = self.site.big_competitions.tab_content.big_competition_accordions_list.items_as_ordered_dict
        accordian, accordian_type = next(iter(accordions_list.items()))

        events = accordian_type.items_as_ordered_dict
        event, event_type = next(iter(events.items()))

        event_type.template.event_name_we.click()
        self.assertTrue(self.site.wait_content_state(state_name='EventDetails', timeout=20), msg='Not able to navigate to EDP')

        if back_button_type == 'browser':
            self.device.go_back()
        else:
            self.site.back_button_click()

        actual_url = self.device.get_current_url().split("?")[0]
        self.assertEqual(actual_url, self.big_competition_url,
                         msg=f'actual url: {actual_url} is not same as expected URL: {self.big_competition_url},'
                             f' currentely verifying back button in {back_button_type}')

    def test_000_launch_the_front_end_application(self):
        """
        DESCRIPTION: Launch the front end application
        EXPECTED: Homepage is loaded successfully
        """
        if tests.settings.backend_env == 'prod':
            # Get an active event for the given category ID
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            # Assign event ID and type ID from the retrieved event data
            event_id = event['event']['id']
            type_id = event['event']['typeId']
        else:
            # Add a new football event to the England Premier League and Assign event ID based on the added event
            event = self.ob_config.add_football_event_to_england_premier_league()
            event_id = event.event_id
            type_id = event.ss_response['event']['typeId']

        self.create_big_competition_and_sport_category(type_id=type_id)
        self.__class__.big_competition_url = f'https://{tests.HOSTNAME}/big-competition{self.new_competition_uri}'

        self.site.wait_content_state('HomePage')
        wait_for_cms_reflection(lambda: self.competition_name in self.home.menu_carousel.keys(), ref=self, timeout=5)

    def test_001_navigate_to_bigc_in_front_end(self):
        """
        DESCRIPTION: Navigate to BigC in front end
        EXPECTED: User navigated to BigC page successfully and default tab will be loaded
        EXPECTED: The BigC URL is displayed in the below format: 'https://sports.ladbrokes.com/big-competition/world-cup'
        """
        self.site.wait_content_state('HomePage')
        self.site.open_sport(name=self.competition_name, timeout=10, content_state='BASECONTENT')
        actual_url = self.device.get_current_url().split("?")[0]
        self.assertEqual(actual_url, self.big_competition_url,
                         msg=f'actual url: {actual_url} is not same as expected URL: {self.big_competition_url}')

    def test_002_navigate_to_any_other_sub_tabs_like_resultsstandings_and_come_back_to_default_tab_by_using_browser_back_button(
            self):
        """
        DESCRIPTION: Navigate to any other sub tabs like: Results/Standings and come back to 'default' tab by using browser back button
        EXPECTED: User successfully navigated to other tab
        EXPECTED: The BigC URL is displayed in below format: 'https://sports.ladbrokes.com/big-competition/world-cup'' once came back to default tab by using browser back button
        """
        all_tabs_menu = self.get_sub_tab_items()
        all_tabs_menu[self.second_tab_name].click()

        expected_url = f'{self.big_competition_url}/{self.second_tab_name}'
        actual_url = self.device.get_current_url().split("?")[0]
        self.assertEqual(actual_url, expected_url,
                         msg=f'actual url: {actual_url} is not same as expected URL: {expected_url}')

        self.device.go_back()

        actual_url = self.device.get_current_url().split("?")[0]
        self.assertEqual(actual_url, self.big_competition_url,
                         msg=f'actual url: {actual_url} is not same as expected URL: {self.big_competition_url}')

    def test_003_navigate_to_any_edp_page_and_come_back_by_using_browser_back_button(self):
        """
        DESCRIPTION: Navigate to any EDP page and come back by using browser back button
        EXPECTED: User successfully navigated to EDP page
        EXPECTED: The BigC URL is displayed in below format: 'https://sports.ladbrokes.com/big-competition/world-cup' once came back to default tab by using browser back button
        """
        self.navigate_to_edp_and_verify_back_button(back_button_type='browser')
    def test_004_navigate_to_any_edp_page_and_come_back_by_using_edp_page_back_button(self):
        """
        DESCRIPTION: Navigate to any EDP page and come back by using EDP page back button
        EXPECTED: User successfully navigated to EDP page
        EXPECTED: The BigC URL is displayed in below format: 'https://sports.ladbrokes.com/big-competition/world-cup' once came back to default tab by using EDP page back button
        """
        self.navigate_to_edp_and_verify_back_button(back_button_type='EDP')

    def test_005_refresh_the_bigc_page(self):
        """
        DESCRIPTION: Refresh the BigC page
        EXPECTED: The BigC URL is displayed in below format: 'https://sports.ladbrokes.com/big-competition/world-cup'
        """
        self.device.refresh_page()

        actual_url = self.device.get_current_url().split("?")[0]
        self.assertEqual(actual_url, self.big_competition_url,
                         msg=f'actual url: {actual_url} is not same as expected URL: {self.big_competition_url}')

    def test_006_duplicate_the_page_and_check_the_other_duplicated_page(self):
        """
        DESCRIPTION: Duplicate the page and check the other duplicated page
        EXPECTED: The BigC URL is displayed in below format: 'https://sports.ladbrokes.com/big-competition/world-cup'
        """
        self.device.driver.execute_script(f"window.open('https://{tests.HOSTNAME}/big-competition{self.new_competition_uri}', '_blank');")

        actual_url = self.device.get_current_url().split("?")[0]
        self.assertEqual(actual_url, self.big_competition_url,
                         msg=f'actual url: {actual_url} is not same as expected URL: {self.big_competition_url}')

        self.device.close_current_tab()
        self.device.open_tab(tab_index=0)

    def test_007_edit_the_bigc_page_url_to_httpssportsladbrokescombig_competitionworld_cuptest(self):
        """
        DESCRIPTION: Edit the BigC page URL to: 'https://sports.ladbrokes.com/big-competition/world-cup/test'
        EXPECTED: The BigC URL is displayed in below format: 'https://sports.ladbrokes.com/big-competition/world-cup/default tab name'.
        """
        self.navigate_to_page(f'big-competition{self.new_competition_uri}/test', timeout=10, test_automation=False)

        expected_url = f'{self.big_competition_url}/{self.first_tab_name}'
        actual_url = self.device.get_current_url().split("?")[0]
        self.assertEqual(actual_url, expected_url,
                         msg=f'actual url: {actual_url} is not same as expected URL: {expected_url}')

    def test_008_edit_the_bigc_page_url_to_httpssportsladbrokescombig_competitiontest(self):
        """
        DESCRIPTION: Edit the BigC page URL to: 'https://sports.ladbrokes.com/big-competition/test'
        EXPECTED: User is navigated to Homepage.
        """
        self.navigate_to_page('big-competition/test', timeout=10, test_automation=False)
        self.assertTrue(self.site.wait_content_state('HomePage'), msg=f'Home page is not loading after navigating to URL: "{tests.HOSTNAME}big-competition/test" ')

    def test_009_navigate_to_bigc_ampgtclick_any_other_sub_tab_and_come_back_to_default_tab_by_directly_clicking_on_default_tab(
            self):
        """
        DESCRIPTION: Navigate to BigC-&amp;gt;click any other sub tab and come back to 'default' tab by directly clicking on 'default' tab
        EXPECTED: User navigates to other tab successfully
        EXPECTED: The BigC URL is displayed in below format: 'https://sports.ladbrokes.com/sport/football/big-competition/world-cup/default tab name'
        """
        self.site.open_sport(name=self.competition_name, timeout=10, content_state='BASECONTENT')
        actual_url = self.device.get_current_url().split("?")[0]
        self.assertEqual(actual_url, self.big_competition_url,
                         msg=f'actual url: {actual_url} is not same as expected URL: {self.big_competition_url}')

        all_tabs_menu = self.get_sub_tab_items()
        all_tabs_menu[self.second_tab_name].click()

        expected_url = f'{self.big_competition_url}/{self.second_tab_name}'
        actual_url = self.device.get_current_url().split("?")[0]
        self.assertEqual(actual_url, expected_url,
                         msg=f'actual url: {actual_url} is not same as expected URL: {expected_url}')

        all_tabs_menu = self.get_sub_tab_items()
        all_tabs_menu[self.first_tab_name].mouse_over()
        all_tabs_menu[self.first_tab_name].click()

        actual_url = self.device.get_current_url().split("?")[0]
        expected_url = f'{self.big_competition_url}/{self.first_tab_name}'
        self.assertEqual(actual_url, expected_url,
                         msg=f'actual url: {actual_url} is not same as expected URL: {expected_url}')

    def test_010_repeat_above_all_steps_by_logging_into_the_front_end_application(self):
        """
        DESCRIPTION: Repeat above all steps by logging into the front end application
        EXPECTED: The expected result should be as above.
        """
        self.site.login(username=tests.settings.betplacement_user)
        self.navigate_to_page('/')
        self.test_001_navigate_to_bigc_in_front_end()
        self.test_002_navigate_to_any_other_sub_tabs_like_resultsstandings_and_come_back_to_default_tab_by_using_browser_back_button()
        self.test_003_navigate_to_any_edp_page_and_come_back_by_using_browser_back_button()
        self.test_004_navigate_to_any_edp_page_and_come_back_by_using_edp_page_back_button()
        self.test_005_refresh_the_bigc_page()
        self.test_006_duplicate_the_page_and_check_the_other_duplicated_page()
        self.test_007_edit_the_bigc_page_url_to_httpssportsladbrokescombig_competitionworld_cuptest()
        self.test_008_edit_the_bigc_page_url_to_httpssportsladbrokescombig_competitiontest()
        self.test_009_navigate_to_bigc_ampgtclick_any_other_sub_tab_and_come_back_to_default_tab_by_directly_clicking_on_default_tab()
