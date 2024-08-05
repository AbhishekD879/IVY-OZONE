import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul, wait_for_result, wait_for_cms_reflection


@pytest.mark.lad_prod
@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.super_button
@pytest.mark.mobile_only
@vtest
class Test_C65934239_Verify_Special_super_button_functionality_when_super_button_is_configured_for_same_time(Common):
    """
    TR_ID: C65934239
    NAME: Verify Special super button functionality when super button is configured for same time
    DESCRIPTION: This test case is to validate Special super button functionality when super button available at same time in FE as per CMS configuration
    """
    keep_browser_open = True
    description = "Autotest_SP_C65934239_Description"
    title = "Autotest_C65934239"

    def check_super_button(self, home_page: bool, sport_page: bool, name, expected_result: bool = True):
        if home_page:
            super_button = wait_for_cms_reflection(
                lambda: self.site.home.super_button_section.super_button.button.name == name.upper(),
                expected_result=expected_result,
                timeout=3,
                refresh_count=5, ref=self,
            )
            if expected_result:
                self.assertTrue(super_button, msg=f'Super button is not present in home page')
            else:
                self.assertFalse(super_button, msg=f'Super button is still present in home page')

        elif sport_page:
            super_button = wait_for_cms_reflection(
                lambda: self.site.sports_page.super_button_section.super_button.button.name == name.upper(),
                expected_result=expected_result,
                timeout=3,
                refresh_count=5, ref=self
            )
            if expected_result:
                self.assertTrue(super_button, msg=f'Super button is not present in home page')
            else:
                self.assertFalse(super_button, msg=f'Super button is still present in home page')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User should have oxygen CMS access
        PRECONDITIONS: 2) Navigate to Homepage -&gt; Special Super button -&gt; Click on Create Special super button link
        PRECONDITIONS: 3) Check on the Active check box
        PRECONDITIONS: 4) Enter the valid data for following fields
        PRECONDITIONS: a. Give proper Title
        PRECONDITIONS: b. Enter valid Destination URL
        PRECONDITIONS: c. Give proper Short Description
        PRECONDITIONS: d. Select home tabs from drop down to Show Special super button on Home Tabs (ex: Highlights in Ladbrokes, Featured in Coral)
        PRECONDITIONS: e. Select sport pages from drop down to  Show special super button on Sports (ex: Esports)
        PRECONDITIONS: f. Select big competition hub from drop down to Show special super button on Big Competitions (ex: World cup)
        PRECONDITIONS: g. Set Validity period start date
        PRECONDITIONS: h. Set Validity period end date
        PRECONDITIONS: i. Type "1-2 Free" in the Feature tag field
        PRECONDITIONS: j. Click on Create
        PRECONDITIONS: Note: Special super button is applicable for Ladbrokes only
        PRECONDITIONS: 5) Navigate to Homepage -&gt; Super button -&gt; Click on Create super button link
        PRECONDITIONS: 6) Check on the Active check box
        PRECONDITIONS: 7) Enter the valid data for following fields
        PRECONDITIONS: a. Enter proper destination URL
        PRECONDITIONS: b. Give valid title for Center Aligned CTA Title
        PRECONDITIONS: c. Give valid description for Center Aligned Description
        PRECONDITIONS: d. Give valid url for Destination URL
        PRECONDITIONS: e. Select tabs from drop down for Show on Home Tabs (ex: Highlights)
        PRECONDITIONS: f. Select sports from drop down for Show on Sports
        PRECONDITIONS: g. Select Big competitions from drop down for Show on Big Competitions
        PRECONDITIONS: h. Set same Validity Period Start Date and time of above Special super button for super button also
        PRECONDITIONS: i. Set same Validity Period End date and time of above special super button for Super button
        PRECONDITIONS: j. Select Themes from Drop down
        PRECONDITIONS: k. Select Universal radio button
        PRECONDITIONS: l.Click on Create link
        PRECONDITIONS: Note:
        PRECONDITIONS: 1. Set newly created super button should  be on top order in the list of all super buttons.
        PRECONDITIONS: 2. Special super button is applicable for Ladbrokes only
        PRECONDITIONS: 3. Both super button and Special super buttons should be active and running
        """
        target_uri = f'https://{tests.HOSTNAME}/1-2-free'
        home_tabs = []
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        next_races_tab = next((tab for tab in module_ribbon_tabs if tab['title'].upper() == "BET BUILDER"), None)
        home_tabs.append(next_races_tab.get('url'))
        self.__class__.super_button = self.cms_config.add_mobile_super_button(name=self.title,
                                                                              category_id=[148],
                                                                              competition_id=[],
                                                                              home_tabs=home_tabs,
                                                                              target_uri=target_uri,
                                                                              description=self.description)
        self.__class__.special_super_button = self.cms_config.add_mobile_special_super_button(
            name=self.title + 'special',
            category_id=[148],
            competition_id=[],
            home_tabs=['/home/betbuilder'],
            target_uri='/1-2-free',
            description=self.description)

    def test_001_hit_the_test_environment_url_to_launch_application(self):
        """
        DESCRIPTION: Hit the test environment URL to launch application
        EXPECTED: Front end of Application should launch without any issues.
        EXPECTED: By default home/featured tab should be loaded
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_verify_newly_created_super_button_on_home_page_fe(self):
        """
        DESCRIPTION: Verify newly created Super button on Home page (FE).
        EXPECTED: Newly created super button should be displayed on Home tab as per CMS config.
        EXPECTED: Super button will not be displayed If current date and time is before the configured start date and time.
        EXPECTED: Special super button should not displayed.
        """
        url = f'https://{tests.HOSTNAME}/home/betbuilder'
        self.device.navigate_to(url=url, testautomation=True)
        current_tab = self.site.home.module_selection_ribbon.tab_menu.current.upper()
        expected_tab = "bet builder".upper()
        self.assertEqual(current_tab, expected_tab, msg=f'Current active tab: {current_tab} is not equal to '
                                                        f'expected: "{expected_tab}"')
        self.assertTrue(self.site.home.has_super_button_section(),
                        msg=f'Quick Link section is not found on "{expected_tab}" page')
        has_button = wait_for_cms_reflection(lambda: self.site.home.super_button_section.super_button.has_button(),
                                             expected_result=True,
                                             timeout=10,
                                             ref=self)
        self.assertTrue(has_button, msg=f'Mobile Super Button was not found on "{expected_tab}" page')
        super_button_section = self.site.home.super_button_section
        super_button_alignment = super_button_section.cta_alignment
        self.assertEqual(super_button_alignment, "center", msg=f'{super_button_alignment} is not equal to "center"')
        super_button_description = self.site.home.super_button_section.super_button.description
        self.assertEqual(super_button_description.upper(), self.description.upper(),
                         msg=f'{super_button_description.upper()} is not '
                             f'equal to {self.description.upper()}')
        super_button = self.site.home.super_button_section.super_button.button.name
        self.assertEqual(super_button.upper(), self.title.upper(), msg=f'{super_button.upper()} is not '
                                                                       f'equal to {self.title.upper()}')

    def test_003_login_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login the application with valid credentials
        EXPECTED: Should be able to login application without any issues
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_004_verify_special_super_button_displaying_in_fe(self):
        """
        DESCRIPTION: Verify Special super button displaying in FE
        EXPECTED: Only Special super button should be displayed by default post login.
        EXPECTED: Super button should not be displayed now .
        """
        url = f'https://{tests.HOSTNAME}/home/betbuilder'
        self.device.navigate_to(url=url, testautomation=True)
        current_tab = self.site.home.module_selection_ribbon.tab_menu.current.upper()
        expected_tab = "bet builder".upper()
        self.assertEqual(current_tab, expected_tab, msg=f'Current active tab: "{current_tab}" not equal to '
                                                        f'expected: "{expected_tab}"')
        self.assertTrue(self.site.home.has_super_button_section(),
                        msg=f'Quick Link section is not found on "{expected_tab}" page')
        self.check_super_button(home_page=True, sport_page=False, name=self.title + 'special')
        self.assertTrue(self.site.home.super_button_section.super_button.has_button(),
                        msg=f'Mobile Super Button was not found on "{expected_tab}" page')
        super_button = self.site.home.super_button_section.super_button.button.name
        self.assertEqual(super_button.upper(), (self.title + "special").upper(), msg=f'{super_button.upper()} is not '
                                                                                     f'equal to {(self.title + "special").upper()}')

    def test_005_verify_special_super_button_displaying_on__home_tabs(self):
        """
        DESCRIPTION: Verify Special super button displaying on  Home tabs
        EXPECTED: Special super button should be displayed on Home tabs as per CMS config
        """
        # Covered In Above Step

    def test_006_verify_special_super_button_displaying_on_configured_home_sport_pages(self):
        """
        DESCRIPTION: Verify Special super button displaying on configured home/ Sport pages
        EXPECTED: Only Special super button should be displayed on Sport pages as per CMS config
        """
        url = f'https://{tests.HOSTNAME}/home/betbuilder'
        self.device.navigate_to(url=url, testautomation=True)
        expected_tab = "esport".upper()
        self.assertTrue(self.site.sports_page.has_super_button_section(),
                        msg=f'Quick Link section is not found on "{expected_tab}" page')
        self.assertTrue(self.site.sports_page.super_button_section.super_button.has_button(),
                        msg=f'Mobile Super Button was not found on "{expected_tab}" page')
        super_button = self.site.sports_page.super_button_section.super_button.button.name
        self.assertEqual(super_button.upper(), (self.title + "special").upper(), msg=f'{super_button.upper()} is not '
                                                                                     f'equal to {(self.title + "special").upper()}')

    def test_007_verify_the_navigating__url_of_special_super_button_after_clicking_on_it(self):
        """
        DESCRIPTION: Verify the navigating  URL of Special super button after clicking on it
        EXPECTED: Special super button should navigate to the url which is configured in CMS as Destination url
        """
        super_button = self.site.sports_page.super_button_section.super_button.button
        super_button.click()
        wait_for_haul(5)
        self.device.refresh_page()
        self.assertIn('/1-2-free', self.device.get_current_url(),
                      msg=f'expected url "/1-2-free" not in {self.device.get_current_url()}')

    def test_008_verify_1_2_free_game_page_as_per_cms_config(self):
        """
        DESCRIPTION: Verify 1-2-Free game page as per CMS config
        EXPECTED: 1-2-Free game page should be navigate and can see teams to add prediction of scores
        """

        one_two_free = self.site.one_two_free
        wait_for_result(lambda: one_two_free.one_two_free_welcome_screen.play_button.is_displayed())
        one_two_free.one_two_free_welcome_screen.play_button.click()
        submit_button = wait_for_result(lambda:
                                        one_two_free.one_two_free_current_screen.submit_button.is_enabled(
                                            expected_result=True),
                                        timeout=15)
        self.assertTrue(submit_button, msg='"Submit Button" is not active')
        self.assertTrue(one_two_free.one_two_free_current_screen.close.is_displayed(),
                        msg='Close button not displayed on one two free')
        matches = list(one_two_free.one_two_free_current_screen.items_as_ordered_dict.values())
        for match in matches:
            self.assertTrue(match.match_start_date,
                            msg=f'match start time is not displayed for "{match.name}".')
            for shirt in list(match.items_as_ordered_dict.values()):
                self.assertTrue(shirt.silk_icon.is_displayed(),
                                msg=f' Teams t-shirts not displayed for "{match.name}".')
                self.assertTrue(shirt.name,
                                msg=f'Team names not displayed for "{match.name}".')

    def test_009_verify_prediction_is_happening_in_1_2_free_game_page(self):
        """
        DESCRIPTION: Verify Prediction is happening in 1-2-Free game page
        EXPECTED: Should be able to submit the predictions in the 1-2-Free game page
        """
        self.__class__.one_two_free = self.site.one_two_free
        wait_for_result(lambda:
                        self.one_two_free.one_two_free_current_screen.submit_button.is_enabled(
                            expected_result=True),
                        timeout=15)
        submit_button = self.one_two_free.one_two_free_current_screen.submit_button
        self.assertTrue(submit_button, msg='"Submit Button" is not active')
        submit_button.click()

    def test_010_verify_the_close_link_by_clicking_on_x_mark_on_top_right_after_submitting_score_predictions(self):
        """
        DESCRIPTION: Verify the close link by clicking on "X" mark on top right after submitting score predictions
        EXPECTED: Should be able to exit from 1-2-Free game page and should be navigate to home page of Application
        """
        one_two_free_you_are_in = self.site.one_two_free.one_two_free_you_are_in
        self.assertTrue(one_two_free_you_are_in, msg=f'"1-2 free you are in" is not displayed')
        self.assertTrue(one_two_free_you_are_in.close, msg='"Close Button" is not active')
        wait_for_haul(3)
        one_two_free_you_are_in.close.click()
        self.site.wait_content_state('homepage')

    def test_011_verify_special_super_button_display_on_home_page(self):
        """
        DESCRIPTION: Verify Special super button display on home page
        EXPECTED: Special super button should not display once predictions are submitted
        """
        url = f'https://{tests.HOSTNAME}/home/betbuilder'
        self.device.navigate_to(url=url, testautomation=True)
        current_tab = self.site.home.module_selection_ribbon.tab_menu.current.upper()
        expected_tab = "bet builder".upper()
        self.assertEqual(current_tab, expected_tab, msg=f'Current active tab: "{current_tab}" is not equal to '
                                                        f'expected: "{expected_tab}"')
        self.check_super_button(home_page=True, sport_page=False, name=self.title + 'special', expected_result=False)

    def test_012_verify_super_button_displaying_home_page(self):
        """
        DESCRIPTION: Verify Super button displaying home page
        EXPECTED: Super button should be displayed if the setted Validity period of end date, time of super button is not expired
        """
        url = f'https://{tests.HOSTNAME}/home/betbuilder'
        self.device.navigate_to(url=url, testautomation=True)
        current_tab = self.site.home.module_selection_ribbon.tab_menu.current.upper()
        expected_tab = "bet builder".upper()
        self.assertEqual(current_tab, expected_tab, msg=f'Current active tab: "{current_tab}" is not equal to '
                                                        f'expected: "{expected_tab}"')
        self.check_super_button(home_page=True, sport_page=False, name=self.title)

    def test_013_verify_logout_from_avatar_menu(self):
        """
        DESCRIPTION: Verify logout From Avatar menu
        EXPECTED: Logout should be performed without any issues
        """
        self.site.logout()

    def test_014_verify_super_button_post_logout(self):
        """
        DESCRIPTION: Verify Super button post logout
        EXPECTED: Super button should be displayed as per CMS config
        """
        url = f'https://{tests.HOSTNAME}/home/betbuilder'
        self.device.navigate_to(url=url, testautomation=True)
        current_tab = self.site.home.module_selection_ribbon.tab_menu.current.upper()
        expected_tab = "bet builder".upper()
        self.assertEqual(current_tab, expected_tab, msg=f'Current active tab: "{current_tab}", '
                                                        f'expected: "{expected_tab}"')
        self.check_super_button(home_page=True, sport_page=False, name=self.title)
