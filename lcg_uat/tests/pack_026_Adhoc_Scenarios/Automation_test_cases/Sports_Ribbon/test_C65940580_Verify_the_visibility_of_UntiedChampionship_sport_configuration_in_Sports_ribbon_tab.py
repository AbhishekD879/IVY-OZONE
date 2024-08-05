import pytest
from faker import Faker
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.menu_ribbon
@pytest.mark.mobile_only
@vtest
# this test case also covers C65940581
class Test_C65940580_Verify_the_visibility_of_UntiedChampionship_sport_configuration_in_Sports_ribbon_tab(Common):
    """
    TR_ID: C65940580
    NAME: Verify the visibility of Untied(Championship) sport configuration  in Sports ribbon tab
    DESCRIPTION: This test case is to validate About  sports ribbon tab as per cms configuration
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default
    faker = Faker()
    competition_name = f'Auto big competition {faker.name()}'
    competition_title = f'Auto{faker.name()}'
    new_id = faker.random.randint(200, 1000)

    def verify_the_presence_of_sport_in_sports_ribbon_FE(self, expected=True, name=False):
        import time
        wait_time = 1  # Wait time in seconds
        max_polling_time = 60  # Maximum polling time in seconds (2 minutes)
        if expected:
            start_time = time.time()
            while time.time() - start_time < max_polling_time:
                self.device.refresh_page()
                self.site.wait_content_state_changed()
                all_items = self.site.home.menu_carousel.items_as_ordered_dict
                self.assertTrue(all_items, msg='No items on MenuCarousel found')
                all_items_names = [sport.upper() for sport in all_items.keys()]
                if self.competition_name.upper() in all_items_names:
                    break
                wait_for_haul(wait_time)
            self.assertIn(self.competition_name.upper(), all_items_names,
                          msg=f'\nExpected: "{self.competition_name}". \n is not in UI sports Ribbon: "{all_items_names}"')
            if name:
                return next((sport for sport in all_items.keys() if sport.upper() == self.competition_name.upper()),None)
        else:
            start_time = time.time()
            while time.time() - start_time < max_polling_time:
                self.device.refresh_page()
                self.site.wait_content_state_changed()
                all_items = self.site.home.menu_carousel.items_as_ordered_dict
                self.assertTrue(all_items, msg='No items on MenuCarousel found')
                all_items_names = [sport.upper() for sport in all_items.keys()]
                if self.competition_name.upper() not in all_items_names:
                    break
                wait_for_haul(wait_time)
            self.assertNotIn(self.competition_name.upper(), all_items_names,
                          msg=f'\nNot Expected: "{self.competition_name}". \n is  in UI sports Ribbon: "{all_items_names}"')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User should have oxygen CMS access 2) Configuration for  Untied(Championship) in LHNsport page->sport categories. 3)Click on Untied(Championship) sport category 4)Enter All mandatory Fields and click on save button: -Image title -Category id -SS category id
        PRECONDITIONS: -Target URI-Tier Should be selected as Untied 5)Check below required fields in general sport configuration: -Active -In App-Show In Play-Show in Sports Ribbon-Show in AZ-And Enter below required fields -Title
        PRECONDITIONS: -Category I,-SS Category Code,-Target Uri,-Odds card header type,-SVG Icon, -Filename,-Icon,-Segmentation
        """
        # Check if the environment is 'prod'
        if tests.settings.backend_env == 'prod':
            # Get an active event for the given category ID
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            # Assign event ID and type ID from the retrieved event data
            self.__class__.typeid = event['event']['typeId']
        else:
            event = self.ob_config.add_football_event_to_england_premier_league()
            self.__class__.typeid=self.football_config.england.premier_league.type_id

        # Create a new big competition
        new_competition = self.cms_config.create_big_competition(type_Id=self.typeid,
                                                                 competition_name=self.competition_name,
                                                                 title=self.competition_title)
        # Assign IDs and URIs from the new competition data
        new_competition_id = new_competition.get('id')
        new_competition_uri = new_competition.get('uri')
        # Construct the URL for the new category
        self.__class__.new_category_ulr = f'big-competition{new_competition_uri}'
        # Create a new tab under the created Big competition
        new_tab_id = self.cms_config.create_tab_for_big_competition(competition_id=new_competition_id,
                                                                    tab_name='highlight').get('id')
        # Wait for a short time
        wait_for_haul(2)
        # Create a new module under the tab which is created
        new_module = self.cms_config.create_module_for_big_competation(competition_id=new_competition_id,
                                                                       tab_id=new_tab_id, module_name='surfaceBet',
                                                                       module_type='SURFACEBET')
        # Wait for a short time
        wait_for_haul(2)
        # Create a new sport category for the Big competition which is created
        sport_category=self.cms_config.create_sport_category(title=self.competition_name, categoryId=self.new_id,
                                                           ssCategoryCode=self.new_id,
                                                           targetUri=self.new_category_ulr,
                                                           tier='UNTIED', showInAZ=True, showInHome=True,isTopSport=True)
        self.__class__.sport_category_id = sport_category.get('id')

    def test_001_launch_coralladbrokes_application(self):
        """
        DESCRIPTION: Launch Coral/Ladbrokes Application.
        EXPECTED: Application should be launched
        EXPECTED: Home page should be opened and sports ribbon tab should be displayed.
        """
        self.navigate_to_page("/")

    def test_002_verify_presence_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify presence of Sports ribbon tab
        EXPECTED: Sports ribbon tab is applicable for Both logged in and Logged out user.
        """
        # Check if the Sports Ribbon is displayed for non-logged users
        self.assertTrue(self.site.home.menu_carousel.is_displayed(),
                        msg='Sports Ribbon is not displayed for non-logged user')

        # Verify the presence of a sport in the Sports Ribbon and store its name
        self.__class__.sport_name = self.verify_the_presence_of_sport_in_sports_ribbon_FE(name=True)

    def test_003_verify_scrollability_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Scrollability of sports ribbon tab
        EXPECTED: Should be left and right scrollable and Image alignment should not be disturbed while scrolling .
        """
        # Get all items in the Sports Ribbon and convert them into a list of key-value pairs (name, item)
        all_items_in_sport_ribbon = list(self.site.home.menu_carousel.items_as_ordered_dict.items())
        # Extract the name and item for the first item in the ribbon
        first_item_name, first_item = all_items_in_sport_ribbon[0]
        # Extract the name and item for the last item in the ribbon
        last_item_name, last_item = all_items_in_sport_ribbon[-1]
        # Scroll to the first item in the Sports Ribbon
        first_item.scroll_to()
        self.assertTrue(first_item.is_displayed(scroll_to=False),
                        msg=f"The first item {first_item_name} is not displayed after scrolling to {first_item_name}")
        # Scroll to the last item in the Sports Ribbon
        last_item.scroll_to()
        self.assertTrue(last_item.is_displayed(scroll_to=False),
                        msg=f"The Last item {last_item_name} is not displayed after scrolling to {last_item_name}")

    def test_004_verify__untiedchampionship_sport_icon_is_displayed_and_clickable(self):
        """
        DESCRIPTION: Verify  Untied(Championship) sport icon is displayed and clickable
        EXPECTED: Untied(Championship) sport icon should be displayed and clickable
        """
        # Click on the sport item in the Sports Ribbon with the name stored in `self.sport_name`
        self.site.home.menu_carousel.click_item(self.sport_name)
        # Wait for the content state to change
        self.site.wait_content_state_changed()
        # Get the current URL after navigating to the sport's page
        actual_category_ulr = self.device.get_current_url()
        # Check if the current URL matches the expected URL
        self.assertIn(self.new_category_ulr,actual_category_ulr,
                      msg=f"User is not navigated to the expected page {self.sport_name}")

        # Check the brand and perform a back button click accordingly
        if self.brand == 'ladbrokes':
            self.site.back_button_click()
        else:
            self.site.sports_page.back_button_click()

    def test_005_verify_the_order_of_sport_by_using_drag_and_drop_in_cms(self):
        """
        DESCRIPTION: Verify the order of sport by using drag and drop in cms
        EXPECTED: Sport order should be changed after drag and drop in cms and same should be shown in Sport ribbon tab
        """
        #  covered in C65940577

    def test_006_verify__by_unchecking_show_in_sports_ribbon_tab_and_check_active_checkbox_in_cms(self):
        """
        DESCRIPTION: Verify  By unchecking "show in sports ribbon tab" and check "Active" checkbox in cms
        EXPECTED: Untied(Championship) sport should not display in Sports ribbon tab
        """
        # Update the sport category with the specified ID to not show in the home and not be a top sport
        self.cms_config.update_sport_category(sport_category_id=self.sport_category_id, showInHome=False,
                                              isTopSport=False, disabled=False)
        # Verify that the sport is not present in the Sports Ribbon (expected to be False)
        self.verify_the_presence_of_sport_in_sports_ribbon_FE(expected=False)
        # Update the sport category with the specified ID to show in the home
        self.cms_config.update_sport_category(sport_category_id=self.sport_category_id, showInHome=True,disabled=False)
        # Verify that the sport is present in the Sports Ribbon (expected to be True)
        self.verify_the_presence_of_sport_in_sports_ribbon_FE()

    def test_007_verify_by_uncheck_activecheckbox_and_check_show_in_sports_ribbon_tab_in_cms(self):
        """
        DESCRIPTION: Verify By uncheck "Active"checkbox and check "show in sports ribbon tab" in cms
        EXPECTED: Untied(Championship) sport should not display in Sports ribbon tab
        """
        # Update the sport category with the specified ID to be disabled
        self.cms_config.update_sport_category(sport_category_id=self.sport_category_id, disabled=True,showInHome=True)
        # Verify that the sport is not present in the Sports Ribbon (expected to be False)
        self.verify_the_presence_of_sport_in_sports_ribbon_FE(expected=False)
        # Update the sport category with the specified ID to be enabled (not disabled)
        self.cms_config.update_sport_category(sport_category_id=self.sport_category_id, disabled=False,showInHome=True)
        # Verify that the sport is present in the Sports Ribbon (expected to be True)
        self.verify_the_presence_of_sport_in_sports_ribbon_FE()

    def test_008_verify_by_click_on_untiedchampionship_icon_in_sport_ribbon_tab(self):
        """
        DESCRIPTION: Verify by Click on Untied(Championship) Icon in sport ribbon tab
        EXPECTED: Should redirect to Matches Tab of Untied(Championship) page.
        EXPECTED: By Default Matches tab should be opened as per CMS configuration
        """
    #     not applicable to untied sport category

    def test_009_verify_alignment_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Alignment of Sports ribbon tab
        EXPECTED: Alignment should be proper and below things need to veify:
        EXPECTED: Foreground Image
        EXPECTED: Backkground Image
        EXPECTED: Text Alignment.
        """
        # covered in C65900572

    def test_010_verify_sub_menu_tabs(self):
        """
        DESCRIPTION: Verify Sub menu tabs
        EXPECTED: All the configured sub menu tabs should be displayed as per cms
        EXPECTED: Inpay,Competitions,outrights and specials.
        """
        # not applicable to untied sport category
