from datetime import datetime
import random
import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from crlat_cms_client.utils.waiters import wait_for_result
from tzlocal import get_localzone
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.super_button
@pytest.mark.mobile_only
@vtest
class Test_C65934238_Verify_the_displaying_of_special_super_button_for_logged_in_user(Common):
    """
    TR_ID: C65934238
    NAME: Verify the displaying of special super button for logged in user
    DESCRIPTION: This test case is to verify the displaying of special super button for loged in user without any existing super button
    PRECONDITIONS: User should have cms access.
    PRECONDITIONS: 1-2 Free active game must be available.
    PRECONDITIONS: User should not predict 1-2 Free game.
    PRECONDITIONS: No active super button should be available.
    PRECONDITIONS: Navigate to homepage&gt;special super button
    PRECONDITIONS: Click on create special super button
    PRECONDITIONS: Enter the title.
    PRECONDITIONS: Enter the destination URL of 1-2 Free game page.
    PRECONDITIONS: Enter the description.
    PRECONDITIONS: Select any of the tab displayed in the  show on home tabs drop down (ex: Next races).
    PRECONDITIONS: Select any of the sport displayed on the show on sports drop down (ex: American football).
    PRECONDITIONS: Select any of the big competitions displayed on the show on big competitions drop down (ex: World cup).
    PRECONDITIONS: Enter start date and end date.
    PRECONDITIONS: Enter Feature Tag as 1-2 Free.
    PRECONDITIONS: click on create button.
    PRECONDITIONS: Note: Special super button is applicable for Ladbrokes only
    """
    keep_browser_open = True
    name = "special_SButton_C65934238"
    target_uri = '/1-2-free'
    description = 'Auto Test Special Super Button'
    disabled_super_buttons = []
    timezone = str(get_localzone())
    disabled_special_super_buttons = []

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        for sb_name in cls.disabled_super_buttons:
            cms_config.update_mobile_super_button(name=sb_name, enabled=True)
        for sb_name in cls.disabled_special_super_buttons:
            cms_config.update_mobile_special_super_button(name=sb_name, enabled=True)

    def disable_all_other_super_buttons(self, category_id=1, home_tab=""):
        all_super_buttons = self.cms_config.get_mobile_super_buttons()
        all_special_super_buttons = self.cms_config.get_mobile_special_super_buttons()
        for super_button in all_special_super_buttons:
            all_super_buttons.append(super_button)
        for supper_button in all_super_buttons:
            if supper_button.get('enabled') and (category_id in supper_button.get('categoryId') or home_tab in supper_button.get('homeTabs')):
                if self.timezone.upper() == "UTC":
                    now = get_date_time_as_string(date_time_obj=datetime.now(),
                                                  time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                  url_encode=False)[:-3] + 'Z'
                elif self.timezone.upper() == 'EUROPE/LONDON':
                    now = get_date_time_as_string(date_time_obj=datetime.now(),
                                                  time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                  url_encode=False, hours=-1)[:-3] + 'Z'
                else:
                    now = get_date_time_as_string(date_time_obj=datetime.now(),
                                                  time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                  url_encode=False, hours=-5.5)[:-3] + 'Z'
                if not (supper_button.get('validityPeriodStart') <= now <= supper_button.get('validityPeriodEnd')):
                    continue
                if supper_button.get('featureTag'):
                    self.cms_config.update_mobile_special_super_button(name=supper_button.get('title'), enabled=False)
                    self.disabled_special_super_buttons.append(supper_button.get('title'))
                else:
                    self.cms_config.update_mobile_super_button(name=supper_button.get('title'), enabled=False)
                    self.disabled_super_buttons.append(supper_button.get('title'))

    def verify_super_button_fe(self, title=None, description=None, page_type=None):
        page = self.site.sports_page if page_type == 'sport' else self.site.home
        self.assertTrue(page.super_button_section.super_button.has_button,
                        msg=f'{title} special super button is not displayed')
        fe_super_button_name = page.super_button_section.super_button.button.name
        fe_super_button_description = page.super_button_section.super_button.description

        # verifying special super button name as per CMS
        self.assertEqual(fe_super_button_name.upper(), title.upper(),
                         msg=f'Actual button name "{fe_super_button_name.upper()}" is not same as '
                             f'Expected button name {title.upper()}')

        # verifying special super button description as per CMs
        self.assertEqual(fe_super_button_description.upper(), description.upper(),
                         msg=f'Actual button description "{fe_super_button_description.upper()}" is not same as '
                             f'Expected button description {description.upper()}')

    def test_000_preconditions(self):
        """
        Description : Creating 1-2 free game in cms
        Description : Creating new special super button in cms
        """
        # getting next races home tab from cms
        home_tabs = []
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        next_races_tab = next((tab for tab in module_ribbon_tabs if tab['title'].upper() == "NEXT RACES"), None)
        self.assertIsNotNone(next_races_tab, msg=f'next races tab is not found in cms')
        home_tabs.append(next_races_tab.get('url'))
        # disabling special super buttons and special super buttons
        self.disable_all_other_super_buttons(home_tab=home_tabs[0])
        # creating new special super button in cms
        self.__class__.special_super_button = self.cms_config.add_mobile_special_super_button(name=self.name,
                                                                                              category_id=[1],
                                                                                              competition_id=[],
                                                                                              target_uri=self.target_uri,
                                                                                              description=self.description,
                                                                                              home_tabs=home_tabs,
                                                                                              enabled=True,
                                                                                              )

    def test_001_launch_the_oxygen_application(self):
        """
        DESCRIPTION: Launch the oxygen application.
        EXPECTED: Application should be loaded successfully home tab should be loaded by default.
        """
        self.site.wait_content_state(state_name="Homepage")

    def test_002_validate_the_super_button_available_in_home_page(self):
        """
        DESCRIPTION: validate the super button available in home page.
        EXPECTED: No super button should be displayed on home page
        """
        # checking next races tab is available in home tabs and navigating to next races tab
        home_page_tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        next_races_tab_name, next_races_tab = next(([tab_name, tab] for tab_name, tab in list(home_page_tabs.items()) if tab_name.upper() == 'NEXT RACES'), [None, None])
        self.assertIsNotNone(next_races_tab, f'Next Races tab is not present in home page tabs , home page tabs : {list(home_page_tabs.keys())}')
        next_races_tab.click()
        wait_for_haul(2)

        # getting current tab on home page
        current_tab = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(current_tab.upper(), next_races_tab_name.upper(), f'current tab {current_tab.upper()} is not equal to expected tab {next_races_tab_name.upper()}')

        # verifying special super button is visible on homepage without login
        super_button = self.site.home.super_button_section.has_super_button()
        self.assertFalse(super_button, msg=f'special supper button {self.name} is available in home page')

    def test_003_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application.
        EXPECTED: Logged in successfully .
        """
        # creating new user to predict 1-2-Free game
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_004_validate_the_special_super_button_on_home_page(self):
        """
        DESCRIPTION: Validate the special super button on home page.
        EXPECTED: Special super button should be displayed on homepage.
        """
        # verifying special super button according to cms on home page
        self.verify_super_button_fe(page_type="Home", title=self.name, description=self.description)

    def test_005_validate_the_title_is_displaying_as_per_cms(self):
        """
        DESCRIPTION: Validate the title is displaying as per cms.
        EXPECTED: The title should be same as per cms.
        """
        # Covered in  test_004_validate_the_special_super_button_on_home_page

    def test_006_validate_the_description_is_displaying_as_per_cms(self):
        """
        DESCRIPTION: Validate the description is displaying as per cms.
        EXPECTED: Description should be same as per cms.
        """
        # Covered in test_004_validate_the_special_super_button_on_home_page

    def test_007_navigate_to_configured_home_tabs_and_validate_the_displaying_of_super_button(self):
        """
        DESCRIPTION: Navigate to configured home tabs and validate the displaying of super button.
        EXPECTED: Special Super button should be displayed on home tabs.
        """
        # Covered in test_004_validate_the_special_super_button_on_home_page

    def test_008_navigate_to_configured_sports_tabs_and_validate_the_displaying_of_special_super_button(self):
        """
        DESCRIPTION: Navigate to configured sports tabs and validate the displaying of special super button.
        EXPECTED: Special Super button should be displayed on sports tab
        """
        self.navigate_to_page(name='sport/american-football')
        self.site.wait_content_state('american-football', timeout=5)
        # verifying special super button data according to cms in sport page
        self.verify_super_button_fe(page_type="sport", title=self.name, description=self.description)

    def test_009_navigate_to_big_competitions_and_validate_the_displaying_of_special_super_button(self):
        """
        DESCRIPTION: Navigate to big competitions and validate the displaying of special super button.
        EXPECTED: Special Super button should be displayed on big competition tab
        """
        # covered in test case : C65934240

    def test_010_click_on_special_super_button(self):
        """
        DESCRIPTION: Click on special super button.
        EXPECTED: User is navigated to 1-2 free game page
        """
        # click on special super button
        self.site.sports_page.super_button_section.super_button.button.click()
        wait_for_haul(5)
        special_super_button_url = self.device.get_current_url()
        expected_special_super_button_url = f'https://{tests.HOSTNAME}'+self.target_uri
        self.assertEqual(special_super_button_url, expected_special_super_button_url,
                         msg=f'Current url: "{special_super_button_url}" is not the same as expected: "{expected_special_super_button_url}"')

    def test_011_predict_1_2_free_game(self):
        """
        DESCRIPTION: Predict 1-2 free game.
        EXPECTED: The predicted scores should be displayed along with badges.
        """
        # Predicting 1-2-Free game
        one_two_free = self.site.one_two_free
        if self.device_type == 'mobile':
            one_two_free = self.site.one_two_free
            wait_for_result(lambda: one_two_free.one_two_free_welcome_screen.play_button.is_displayed())
            one_two_free.one_two_free_welcome_screen.play_button.click()
            wait_for_result(lambda:
                            one_two_free.one_two_free_current_screen.submit_button.is_enabled(
                                expected_result=True),
                            timeout=15)
            match = list(one_two_free.one_two_free_current_screen.items_as_ordered_dict.values())
            for score in match:
                score_switchers = score.score_selector_container.items
                for score_switcher in score_switchers:
                    self.assertTrue(score_switcher.increase_score_up_arrow.is_displayed(),
                                    msg=f'Upper arrow not displayed for "{score.name}".')
                    score_switcher.increase_score_up_arrow.click()
                    wait_for_haul(1)
                    actual_score = score_switcher.score
                    self.assertEqual(actual_score, '1',
                                     msg=f'Actual Score "{actual_score}" is not the same as expected "1"')
                    break
            submit_button = one_two_free.one_two_free_current_screen.submit_button
            self.assertTrue(submit_button, msg='"Submit Button" is not active')
            submit_button.click()
        # verifying '1-2 free you are in' after predicting 1-2-Free game
        one_two_free_you_are_in = one_two_free.one_two_free_you_are_in
        self.assertTrue(one_two_free_you_are_in, msg=f'"1-2 free you are in" is not displayed')
        self.assertTrue(one_two_free_you_are_in.close, msg='"Close Button" is not active')
        one_two_free_you_are_in.close.click()
        self.site.wait_content_state('american-football')

    def test_012_navigate_to_home_page(self):
        """
        DESCRIPTION: Navigate to home page
        EXPECTED: No special super  button should be visible
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        # verifying whether special super button is still existing after playing 1-2-Free game on homepage tab.
        self.test_002_validate_the_super_button_available_in_home_page()

    def test_013_log_out_from_application(self):
        """
        DESCRIPTION: Log out from application.
        EXPECTED: No special super  button should be visible
        """
        # verifying special super button is visible after logout
        self.site.logout()
        self.test_002_validate_the_super_button_available_in_home_page()



