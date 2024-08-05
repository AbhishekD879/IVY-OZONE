import pytest
from faker import Faker

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec

from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


#@pytest.mark.tst2
#@pytest.mark.stg2 Removed tst2, stg2 markers for NA test case
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.odds_boost
@pytest.mark.cms
@pytest.mark.quick_bet
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.login
@pytest.mark.na
@vtest
class Test_C2555607_Verify_that_CMS_configuration_for_Odds_Boost_is_shown_in_application(BaseBetSlipTest):
    """
    TR_ID: C2555607
    NAME: Verify that CMS configuration for Odds Boost is shown in application
    DESCRIPTION: This test case verifies that configurations for "Odds boost" in CMS are shown on application
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Token is NOT expired
    PRECONDITIONS: CMS configuration for Odds Boost are added:
    PRECONDITIONS: Odds Boost is Active
    PRECONDITIONS: *Image1* is added in Custom field for Image (svg)
    PRECONDITIONS: *'Header_Text_1'* text is added in Custom rich text field for Logged Out Header Text
    PRECONDITIONS: *'Header_Text_2' text is added in Custom rich text field for Logged In Header Text
    PRECONDITIONS: *'T&C_Text_1'* text is added in Custom Field for Terms&Conditions text
    """
    keep_browser_open = True
    faker = Faker()
    new_logged_in_header_text = f'New_LoggedInText_{faker.city()}'
    new_logged_out_header_text = f'New_LoggedOutText_{faker.city()}'
    new_terms_and_conditions_text = f'New_Terms_{faker.city()}'

    @classmethod
    def custom_setUp(cls):
        cms_config = cls.get_cms_config()
        odds_boost = cms_config.get_initial_data().get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost section is disabled in CMS')
        cls.old_logged_in_header_text = odds_boost['loggedInHeaderText'].strip('</p>')
        cls.old_logged_out_header_text = odds_boost['loggedOutHeaderText'].strip('</p>')
        cls.old_terms_and_condition_text = odds_boost['termsAndConditionsText'].strip('</p>')

    @classmethod
    def custom_tearDown(cls):
        cms_config = cls.get_cms_config()
        cms_config.update_odds_boost_config(enabled=True,
                                            logged_in_header_text=cls.old_logged_in_header_text,
                                            logged_out_header_text=cls.old_logged_out_header_text,
                                            terms_and_conditions_text=cls.old_terms_and_condition_text)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create user and event
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event.event_id
        self.__class__.section_name = self.expected_market_sections.match_result
        self.__class__.team1 = list(event.selection_ids.keys())[0]
        self.__class__.team1 = self.team1.upper() if self.brand == 'ladbrokes' else self.team1

        self.__class__.username = tests.settings.betplacement_user

        self.__class__.is_mobile = False if self.device_type == 'desktop' else True

    def test_001_load_application_and_navigate_to_odds_boost_page(self):
        """
        DESCRIPTION: Load application
        DESCRIPTION: Do NOT login
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that appropriate odds boost elements are shown on Odds Boost Header
        EXPECTED: The following elements are shown on Odds Boost page:
        EXPECTED: - Image_1
        EXPECTED: - 'Header_Text_1'
        EXPECTED: - 'T&C_Text_1'
        """
        self.navigate_to_page('/oddsboost')
        self.site.wait_content_state(state_name='oddsboost')
        sections = self.site.odds_boost_page.sections.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')

        today_odds_boost = sections.get(vec.odds_boost.PAGE.today_odds_boosts)
        terms = sections.get(vec.odds_boost.PAGE.terms_and_conditions_section_title)

        self.assertEqual(today_odds_boost.description, self.old_logged_out_header_text,
                         msg=f'Text for logged out user "{today_odds_boost.description}" on {vec.odds_boost.PAGE.today_odds_boosts}'
                             f' section is not the same as expected "{self.old_logged_out_header_text}"')
        self.assertEqual(terms.description, self.old_terms_and_condition_text,
                         msg=f'Text "{terms.description}" on {vec.odds_boost.PAGE.terms_and_conditions_section_title} section '
                             f'is not the same as expected "{self.old_terms_and_condition_text}"')

        # cannot automate changing image

    def test_002_login_with_user1_from_preconditions(self):
        """
        DESCRIPTION: Tap Log In button (login with User1 from precondition)
        DESCRIPTION: Verify that  appropriate odds boost elements are shown on Odds Boost Header after login
        EXPECTED: The following elements are shown on Odds Boost page:
        EXPECTED: - Image_1
        EXPECTED: - 'Header_Text_2'
        EXPECTED: - 'T&C_Text_1'
        """
        self.site.login(username=self.username)
        self.site.wait_content_state(state_name='oddsboost')

        self.ob_config.grant_odds_boost_token(username=self.username)

        sections = self.site.odds_boost_page.sections.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')

        today_odds_boost = sections.get(vec.odds_boost.PAGE.today_odds_boosts)
        terms = sections.get(vec.odds_boost.PAGE.terms_and_conditions_section_title)

        self.assertEqual(today_odds_boost.description, self.old_logged_in_header_text,
                         msg=f'Text for logged out user "{today_odds_boost.description}" on {vec.odds_boost.PAGE.today_odds_boosts}'
                             f' section is not the same as expected "{self.old_logged_in_header_text}"')
        self.assertEqual(terms.description, self.old_terms_and_condition_text,
                         msg=f'Text "{terms.description}" on {vec.odds_boost.PAGE.terms_and_conditions_section_title} section '
                             f'is not the same as expected "{self.old_terms_and_condition_text}"')

        # cannot automate changing image

    def test_003_load_cms_navigate_to_odds_boost_menu_item_made_changes_and_save_them(self):
        """
        DESCRIPTION: Load CMS
        DESCRIPTION: Navigate to "Odds Boost" Menu item in the navigation menu
        DESCRIPTION: Remove Image_1
        DESCRIPTION: Change Logged Out Header Text to 'Header_Text_3'
        DESCRIPTION: Change Logged In Header Text to 'Header_Text_4'
        DESCRIPTION: Change Terms&Conditions Text to 'T&C_Text_2'
        DESCRIPTION: Save changes
        EXPECTED: Changes are saved in CMS
        """
        self.cms_config.update_odds_boost_config(logged_in_header_text=self.new_logged_in_header_text,
                                                 logged_out_header_text=self.new_logged_out_header_text,
                                                 terms_and_conditions_text=self.new_terms_and_conditions_text)

        # cannot automate changing image

    def test_004_navigate_back_to_the_application_and_refresh_odds_boost_page(self):
        """
        DESCRIPTION: Navigate back to the application
        DESCRIPTION: Refresh Odds Boost page
        DESCRIPTION: Verify that appropriate updated on Odds Boost Header according to CMS changes
        EXPECTED: The following elements are shown on Odds Boost page:
        EXPECTED: - Default odds boost image
        EXPECTED: - 'Header_Text_4'
        EXPECTED: - 'T&C_Text_1'
        """
        result = wait_for_result(lambda: self.cms_config.get_initial_data().get('oddsBoost').get('loggedInHeaderText') is not None and self.cms_config.get_initial_data().get('oddsBoost').get('loggedInHeaderText', '').strip('</p>') == self.new_logged_in_header_text,
                                 name=f'New Oddsboost config to become active. Current logged in header is '
                                      f'{self.cms_config.get_initial_data().get("oddsBoost").get("loggedInHeaderText")}',
                                 poll_interval=1,
                                 timeout=180)
        self.assertTrue(result, msg='New Oddsboost config was not activated')

        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        sections = self.site.odds_boost_page.sections.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')

        today_odds_boost = sections.get(vec.odds_boost.PAGE.today_odds_boosts)
        terms = sections.get(vec.odds_boost.PAGE.terms_and_conditions_section_title)

        self.assertEqual(today_odds_boost.description, self.new_logged_in_header_text,
                         msg=f'Text for logged out user "{today_odds_boost.description}" on {vec.odds_boost.PAGE.today_odds_boosts}'
                             f' section is not the same as expected "{self.new_logged_in_header_text}"')
        self.assertEqual(terms.description, self.new_terms_and_conditions_text,
                         msg=f'Text "{terms.description}" on {vec.odds_boost.PAGE.terms_and_conditions_section_title} section '
                             f'is not the same as expected "{self.new_terms_and_conditions_text}"')

    def test_005_log_out_from_application_and_navigate_to_odds_boost_page(self):
        """
        DESCRIPTION: Log out from application
        DESCRIPTION: Navigate to Odds Boost page
        DESCRIPTION: Verify that appropriate updated on Odds Boost Header according to CMS changes
        EXPECTED: The following elements are shown on Odds Boost page:
        EXPECTED: - Default odds boost image
        EXPECTED: - 'Header_Text_3'
        EXPECTED: - 'T&C_Text_1'
        """
        self.site.logout()
        self.navigate_to_page('/oddsboost')
        self.site.wait_content_state(state_name='oddsboost')

        sections = self.site.odds_boost_page.sections.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')

        today_odds_boost = sections.get(vec.odds_boost.PAGE.today_odds_boosts)
        terms = sections.get(vec.odds_boost.PAGE.terms_and_conditions_section_title)

        self.assertEqual(today_odds_boost.description, self.new_logged_out_header_text,
                         msg=f'Text for logged out user "{today_odds_boost.description}" on {vec.odds_boost.PAGE.today_odds_boosts}'
                             f' section is not the same as expected "{self.new_logged_out_header_text}"')
        self.assertEqual(terms.description, self.new_terms_and_conditions_text,
                         msg=f'Text "{terms.description}" on {vec.odds_boost.PAGE.terms_and_conditions_section_title} section '
                             f'is not the same as expected "{self.new_terms_and_conditions_text}"')

    def test_006_in_cms_turn_off_odds_boost_toggle_save_changes(self):
        """
        DESCRIPTION: Load CMS
        DESCRIPTION: Navigate to "Odds Boost" Menu item in the navigation menu
        DESCRIPTION: Turn OFF "Odds Boost" Toggle -> Save changes
        EXPECTED: Changes are saved in CMS
        """
        self.cms_config.update_odds_boost_config(enabled=False,
                                                 logged_in_header_text=self.new_logged_in_header_text,
                                                 logged_out_header_text=self.new_logged_out_header_text,
                                                 terms_and_conditions_text=self.new_terms_and_conditions_text)

    def test_007_load_application_and_login_with_user1(self):
        """
        DESCRIPTION: Load application and Login with User1
        DESCRIPTION: Verify that Odds Boost functionality is not shown in the application
        EXPECTED: - Odds Boost token summary popup is not shown
        EXPECTED: - Odds Boost is not shown in (Menu)?
        EXPECTED: - Odds boost page is anavailable
        EXPECTED: - Odds Boost button is not shown in Betslip
        EXPECTED: - Odds Boost button is not shown in Quick Bet
        """
        result = wait_for_result(
            lambda: self.cms_config.get_initial_data().get('oddsBoost') is None,
            name='Oddsboost config to become disabled', timeout=240, poll_interval=1)
        self.assertTrue(result, msg='Oddsboost config was not disabled')

        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        self.site.login(username=self.username, ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
        self.assertFalse(self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=10))

        self.navigate_to_page('/oddsboost')
        self.site.wait_content_state('Homepage')

        self.navigate_to_edp(event_id=self.eventID)

        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='No markets found')

        market = markets_list.get(self.section_name)
        self.assertTrue(market, msg='Can not find Match Result section')

        outcomes = market.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes are shown for Match Result market')
        self.assertIn(self.team1, outcomes, msg=f'"{self.team1}" is not in outcomes "{outcomes}"')

        outcomes.get(self.team1).click()

        if self.is_mobile:
            quick_bet = self.site.quick_bet_panel
            self.assertFalse(quick_bet.has_odds_boost_button(expected_result=False, timeout=2),
                             msg='Odds boost button is present on Quickbet panel')
            quick_bet.add_to_betslip_button.click()
        self.site.open_betslip()

        self.assertFalse(self.get_betslip_content().has_odds_boost_header, msg='Odds boost header is shown')
        if self.is_mobile:
            self.site.close_betslip()
        else:
            self.site.header.right_menu_button.click()
            self.assertNotIn(vec.odds_boost.BETSLIP_HEADER.title.upper(), self.site.right_menu.items_as_ordered_dict.keys(),
                             msg=f'{vec.odds_boost.BETSLIP_HEADER.title.upper()} is still '
                                 f'in menu items {self.site.right_menu.items_as_ordered_dict.keys()}')
