import pytest
from faker import Faker

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


#@pytest.mark.tst2
#@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.login
@pytest.mark.na
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-3404')
class Test_C2594359_Verify_displaying_Odds_Boost_info_page_Header(BaseBetSlipTest):
    """
    TR_ID: C2594359
    NAME: Verify displaying Odds Boost info page Header
    DESCRIPTION: This test case verifies displaying Odds Boost info page Header
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: CMS Define in Odds Boost details page:
    PRECONDITIONS: - Image_1 (png or svg)????
    PRECONDITIONS: - 'HeaderText_1' for logged out user
    PRECONDITIONS: - 'HeaderText_2' for logged in user
    PRECONDITIONS: - 'T&C_1' in Terms and Conditions text field
    PRECONDITIONS: Load application
    PRECONDITIONS: Do NOT login
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: User1:
    PRECONDITIONS: There are 'X1' AVAILABLE NOW odds boost (where X1 - number of *active* Odds Boost tokens generated for the user)
    PRECONDITIONS: There are 'X2' UPCOMING odds boost (where X2 - number of *upcoming* Odds Boost tokens generated for the user)
    """
    keep_browser_open = True
    faker = Faker()
    new_logged_in_header_text = f'New_LoggedInText_{faker.city()}'
    new_logged_out_header_text = f'New_LoggedOutText_{faker.city()}'
    new_terms_and_conditions_text = f'New_Terms_{faker.city()}'
    old_logged_in_header_text = None
    old_logged_out_header_text = None
    old_terms_and_condition_text = None

    @classmethod
    def custom_setUp(cls):
        cms_config = cls.get_cms_config()
        odds_boost = cms_config.get_initial_data().get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost section is disabled in CMS')
        cls.old_logged_in_header_text = odds_boost['loggedInHeaderText']
        cls.old_logged_out_header_text = odds_boost['loggedOutHeaderText']
        cls.old_terms_and_condition_text = odds_boost['termsAndConditionsText']

    @classmethod
    def custom_tearDown(cls):
        cms_config = cls.get_cms_config()
        odds_boost = cms_config.get_initial_data().get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost section is disabled in CMS')
        if any([cls.old_logged_in_header_text, cls.old_logged_out_header_text, cls.old_terms_and_condition_text]):
            cms_config.update_odds_boost_config(logged_in_header_text=cls.old_logged_in_header_text,
                                                logged_out_header_text=cls.old_logged_out_header_text,
                                                terms_and_conditions_text=cls.old_terms_and_condition_text)

    def get_today_odds_and_terms(self):
        sections = self.site.odds_boost_page.sections.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')

        today_odds_boost = sections.get(vec.odds_boost.PAGE.today_odds_boosts)
        terms = sections.get(vec.odds_boost.PAGE.terms_and_conditions_section_title)

        self.assertTrue(today_odds_boost, msg=f'"{vec.odds_boost.PAGE.today_odds_boosts}" section is not found')
        self.assertTrue(terms, msg=f'"{vec.odds_boost.PAGE.terms_and_conditions_section_title}" section is not found')

        return today_odds_boost, terms

    def get_available_now_and_upcoming_boosts(self):
        sections = self.site.odds_boost_page.sections.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')

        available_now = sections.get(vec.odds_boost.PAGE.available_now_section_title)
        upcoming = sections.get(vec.odds_boost.PAGE.upcoming_boosts)

        self.assertTrue(available_now, msg=f'"{vec.odds_boost.PAGE.available_now_section_title}" section is not found')
        self.assertTrue(upcoming, msg=f'"{vec.odds_boost.PAGE.upcoming_boosts}" section is not found')

        return available_now, upcoming

    def test_000_preconditions(self):
        """
        DESCRIPTION: "Odds Boost" Feature Toggle is enabled in CMS
        DESCRIPTION: CMS Define in Odds Boost details page:
        DESCRIPTION: - Image_1 (png or svg)????
        DESCRIPTION: - 'HeaderText_1'  for logged out user
        DESCRIPTION: -  'HeaderText_2'  for logged in user
        DESCRIPTION: - 'T&C_1' in Terms and Conditions text field
        DESCRIPTION: Load application
        DESCRIPTION: Do NOT login
        DESCRIPTION: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
        DESCRIPTION: User1:
        DESCRIPTION: There are 'X1' AVAILABLE NOW odds boost (where X1 - number of *active* Odds Boost tokens generated for the user)
        DESCRIPTION: There are 'X2' UPCOMING odds boost (where X2 - number of *upcoming* Odds Boost tokens generated for the user)
        """
        self.__class__.username = tests.settings.betplacement_user

        self.cms_config.update_odds_boost_config(logged_in_header_text=self.new_logged_in_header_text,
                                                 logged_out_header_text=self.new_logged_out_header_text,
                                                 terms_and_conditions_text=self.new_terms_and_conditions_text)
        result = wait_for_result(
            lambda: self.cms_config.get_initial_data().get('oddsBoost')['loggedInHeaderText'] == self.new_logged_in_header_text,
            name='New Oddsboost config to become active. '
            f'Current logged in header is {self.cms_config.get_initial_data().get("oddsBoost")["loggedInHeaderText"]}',
            poll_interval=2,
            timeout=300)

        self.assertTrue(result, msg='New Oddsboost config was not activated')

        self.ob_config.grant_odds_boost_token(username=self.username)

    def test_001_navigate_to_the_odds_boost_info_pageverify_odds_boost_page_displaying_for_logged_out_user(self):
        """
        DESCRIPTION: Navigate to the Odds boost info page.
        DESCRIPTION: Verify Odds Boost page displaying for logged out user.
        EXPECTED: Odds Boost page is displayed with following elements:
        EXPECTED: - Image1
        EXPECTED: - 'HeaderText_1'
        EXPECTED: - 'AVAILABLE NOW' value is displayed as 0
        EXPECTED: - 'UPCOMING BOOSTS' value is displayed as 0
        EXPECTED: - 'Log in' button is displayed
        EXPECTED: - 'T&C_1' in Terms&Coditions' section
        """
        self.navigate_to_page('oddsboost')
        self.site.wait_content_state(state_name='oddsboost')

        today_odds_boost, terms = self.get_today_odds_and_terms()

        # We're not able to verify image from automation prospective

        actual_description = today_odds_boost.description
        self.assertEqual(actual_description, self.new_logged_out_header_text,
                         msg=f'Text for logged out user "{actual_description}" on "{vec.odds_boost.PAGE.today_odds_boosts}"'
                         f' section is not the same as expected "{self.new_logged_out_header_text}"')
        available_now_amount = today_odds_boost.available_now.value
        expected_amount = "0"
        self.assertEqual(expected_amount, available_now_amount,
                         msg=f'"AVAILABLE NOW" value" is "{available_now_amount}" but was expected to be '
                         f'"{expected_amount}"')

        upcoming_boosts_amount = today_odds_boost.upcoming_boosts.value
        self.assertEqual(expected_amount, upcoming_boosts_amount,
                         msg=f'"UPCOMING BOOSTS" value" is "{upcoming_boosts_amount}" but was expected to be '
                         f'"{expected_amount}"')
        self.assertTrue(today_odds_boost.login_button.is_displayed(), msg=f'"Log in" button is not displayed')
        self.assertEqual(terms.description, self.new_terms_and_conditions_text,
                         msg=f'Text "{terms.description}" on "{vec.odds_boost.PAGE.terms_and_conditions_section_title}" section '
                         f'is not the same as expected "{self.new_terms_and_conditions_text}"')

    def test_002_login_with_user1_from_preconditions_and_verify_odds_boost_page_displaying_for_logged_in_user(self):
        """
        DESCRIPTION: Login with User1 from preconditions.
        DESCRIPTION: Verify Odds Boost page displaying for logged in user
        EXPECTED: Odds Boost page is displayed with following elements::
        EXPECTED: - Image1
        EXPECTED: - 'HeaderText_2'
        EXPECTED: - 'AVAILABLE NOW' value is displayed as 'X1'
        EXPECTED: - 'UPCOMING BOOSTS' value is displayed as 'X2'
        EXPECTED: -  List of available Odds Boosts for the user  (active and upcoming boosts sections?)
        EXPECTED: - 'T&C_1' in Terms&Coditions' section
        """
        self.site.login(username=self.username)
        self.site.wait_content_state(state_name='oddsboost')

        today_odds_boost, terms = self.get_today_odds_and_terms()

        # We're not able to verify image from automation prospective

        actual_description = today_odds_boost.description
        self.assertEqual(actual_description, self.new_logged_in_header_text,
                         msg=f'Text for logged out user "{actual_description}" on "{vec.odds_boost.PAGE.today_odds_boosts}"'
                         f' section is not the same as expected "{self.new_logged_in_header_text}"')
        self.assertEqual(terms.description, self.new_terms_and_conditions_text,
                         msg=f'Text "{terms.description}" on "{vec.odds_boost.PAGE.terms_and_conditions_section_title}" section '
                         f'is not the same as expected "{self.new_terms_and_conditions_text}"')

        expected_available_now_boost = int(today_odds_boost.available_now.value) + 1

        self.ob_config.grant_odds_boost_token(username=self.username)

        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        self.site.wait_content_state(state_name='oddsboost')

        today_odds_boost, terms = self.get_today_odds_and_terms()

        actual_available_now_boost = int(today_odds_boost.available_now.value)
        self.assertEqual(expected_available_now_boost, actual_available_now_boost,
                         msg=f'"AVAILABLE NOW" value is "{actual_available_now_boost}" but was expected to be '
                         f'"{expected_available_now_boost}"')

        upcoming_boosts_amount = int(today_odds_boost.upcoming_boosts.value)
        self.assertTrue(upcoming_boosts_amount >= 0,
                        msg=f'"UPCOMING BOOSTS" value "{upcoming_boosts_amount}" is not bigger or equal to "0"')

        available_now_boosts, upcoming_boosts = self.get_available_now_and_upcoming_boosts()
        available_count = len(available_now_boosts.items_as_ordered_dict)
        self.assertEqual(available_count, expected_available_now_boost,
                         msg=f'"{vec.odds_boost.PAGE.available_now_section_title}" boosts counter was expected to be '
                         f'"{expected_available_now_boost}" but it is "{available_count}"')

        # We cannot increase 'UPCOMING BOOSTS' value from automation prospective

    def test_003_log_out_and_verify_user_is_navigated_to_the_homepage(self):
        """
        DESCRIPTION: Log out and verify user is navigated to the Homepage
        EXPECTED: User is navigated to the Homepage
        """
        self.site.logout()
        self.site.wait_content_state('Homepage')
