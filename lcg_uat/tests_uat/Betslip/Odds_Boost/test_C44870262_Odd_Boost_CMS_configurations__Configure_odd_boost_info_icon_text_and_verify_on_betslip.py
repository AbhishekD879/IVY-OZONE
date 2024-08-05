import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.prod - This test case is limited to QA2 only because can't update odds boost CMS configuration on prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.betslip
@pytest.mark.odds_boost
@pytest.mark.cms
@pytest.mark.quick_bet
@pytest.mark.desktop
@vtest
class Test_C44870262_Odd_Boost_CMS_configurations__Configure_odd_boost_info_icon_text_and_verify_on_betslip(BaseBetSlipTest):
    """
    TR_ID: C44870262
    NAME: "Odd Boost CMS configurations - Configure odd boost info icon text and verify on betslip"
    """
    keep_browser_open = True
    new_logged_out_header_text = 'New_LoggedOutText'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create user and event
        """
        self.cms_config.update_odds_boost_config(enabled=True)
        self.__class__.odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')

        self.assertTrue(self.odds_boost, msg='Odds boost is not enabled in CMS')
        if self.odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)
            self.__class__.old_logged_in_header_text = self.odds_boost['loggedInHeaderText']
            self.__class__.old_logged_out_header_text = self.odds_boost['loggedOutHeaderText']
            self.__class__.old_terms_and_condition_text = self.odds_boost['termsAndConditionsText']
            self.cms_config.update_odds_boost_config(logged_in_header_text=self.old_logged_in_header_text,
                                                     logged_out_header_text=self.old_logged_out_header_text,
                                                     terms_and_conditions_text=self.old_terms_and_condition_text)
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event.event_id
        self.__class__.section_name = self.expected_market_sections.match_result
        self.__class__.team1 = list(event.selection_ids.keys())[0]
        self.__class__.team1 = self.team1.upper() if self.brand == 'ladbrokes' else self.team1
        self.__class__.username = tests.settings.betplacement_user
        self.__class__.is_mobile = False if self.device_type == 'desktop' else True

    def test_001_load_cms___odds_boost_menuverify_elements_on_odds_boost_page_in_cms(self):
        """
        DESCRIPTION: Load CMS -> "Odds Boost" Menu.
        DESCRIPTION: Verify elements on "Odds Boost" page in CMS.
        EXPECTED: The following elements are shown:
        EXPECTED: * Odds Boost Active checkbox
        EXPECTED: * Upload field for Image (svg)
        EXPECTED: * Text field for Logged Out Header Text
        EXPECTED: * Text field for Logged In Header Text
        EXPECTED: * Text field for Terms&Conditions
        """
        # Skipping this step as it requires verification of CMS UI

    def test_002_load_the_application_and_verify_that_odds_boost_data_is_shown_in_the_initial_request_network___mobile(self):
        """
        DESCRIPTION: Load the application and verify that odds boost data is shown in the initial request (Network -> "mobile")
        EXPECTED: Appropriate data from CMS is shown in oddsBoost section of request:
        EXPECTED: enabled: true
        EXPECTED: lang:
        EXPECTED: loggedInHeaderText:
        EXPECTED: loggedOutHeaderText:
        EXPECTED: svg:
        EXPECTED: svgFilename:
        EXPECTED: svgId:
        EXPECTED: termsAndConditionsText:
        """
        expected_values = ['enabled', 'lang', 'loggedInHeaderText', 'loggedOutHeaderText', 'svg',
                           'svgFilename', 'svgId', 'termsAndConditionsText']
        self.assertTrue(self.odds_boost['enabled'], msg='Odds boost is not enabled according to the network response')
        for value in expected_values:
            self.assertIn(value, self.odds_boost.keys(), msg=f'{value} value is not present in the response values {self.odds_boost.keys()}')

    def test_003_login_to_application_with_user_1navigate_to_odds_boost_page_and_verify_that_appropriate_odds_boost_elements_are_shown(self):
        """
        DESCRIPTION: Login to application with User 1.
        DESCRIPTION: Navigate to Odds Boost Page and verify that appropriate odds boost elements are shown.
        EXPECTED: The following elements configured in CMS are shown on Odds Boost page:
        EXPECTED: * Image
        EXPECTED: * Logged In Header Text
        EXPECTED: * Terms&Conditions Text
        """
        self.__class__.username = tests.settings.odds_boost_user
        self.ob_config.grant_odds_boost_token(username=self.username)
        self.site.login(username=self.username)
        self.navigate_to_page('/oddsboost')
        self.site.wait_content_state(state_name='oddsboost')
        self.ob_config.grant_odds_boost_token(username=self.username)
        sections = self.site.odds_boost_page.sections.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        today_odds_boost = sections.get(vec.odds_boost.PAGE.today_odds_boosts)
        terms = sections.get(vec.odds_boost.PAGE.terms_and_conditions_section_title)
        self.assertEqual(today_odds_boost.description, vec.odds_boost.PAGE.today_odds_boosts,
                         msg=f'Text for logged out user "{today_odds_boost.description}" on {vec.odds_boost.PAGE.today_odds_boosts}'
                             f' section is not the same as expected "{vec.odds_boost.PAGE.today_odds_boosts}')
        self.assertEqual(terms.description, vec.odds_boost.PAGE.terms_and_conditions_section_title,
                         msg=f'Text "{terms.description}" on "{vec.odds_boost.PAGE.terms_and_conditions_section_title}"" section '
                             f'is not the same as expected "{vec.odds_boost.PAGE.terms_and_conditions_section_title}"')
        # cannot automate changing image

    def test_004_load_cms___odds_boost_menuremove_configured_image_and_edit_header_text__termsconditions_textsave_changes(self):
        """
        DESCRIPTION: Load CMS -> "Odds Boost" Menu.
        DESCRIPTION: Remove configured Image and edit Header text / Terms&Conditions text.
        DESCRIPTION: Save changes.
        EXPECTED: Changes are saved in CMS
        """
        self.cms_config.update_odds_boost_config(logged_in_header_text=vec.odds_boost.PAGE.today_odds_boosts,
                                                 logged_out_header_text=self.new_logged_out_header_text,
                                                 terms_and_conditions_text=vec.odds_boost.PAGE.terms_and_conditions_section_title)
        # cannot automate changing image

    def test_005_navigate_back_to_application_logged_in_as_user_1___odds_boost_page(self):
        """
        DESCRIPTION: Navigate back to application (logged in as User 1) -> Odds Boost page
        EXPECTED: The following elements configured in CMS are shown on Odds Boost page:
        EXPECTED: * Default odds boost image
        EXPECTED: * Logged In Header Text (edited in Step 4)
        EXPECTED: * Terms&Conditions Text (edited in Step 4)
        """
        result = wait_for_result(lambda: self.cms_config.get_initial_data(cached=True).get('oddsBoost')['loggedInHeaderText'].strip('</p>') == vec.odds_boost.PAGE.today_odds_boosts,
                                 poll_interval=1,
                                 timeout=180)
        self.assertTrue(result, msg='New Oddsboost config was not activated')
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        sections = self.site.odds_boost_page.sections.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        today_odds_boost = sections.get(vec.odds_boost.PAGE.today_odds_boosts)
        terms = sections.get(vec.odds_boost.PAGE.terms_and_conditions_section_title)
        self.assertEqual(today_odds_boost.description, vec.odds_boost.PAGE.today_odds_boosts,
                         msg=f'Text for logged out user "{today_odds_boost.description}" on {vec.odds_boost.PAGE.today_odds_boosts}'
                             f' section is not the same as expected "{vec.odds_boost.PAGE.today_odds_boosts}"')
        self.assertEqual(terms.description, vec.odds_boost.PAGE.terms_and_conditions_section_title,
                         msg=f'Text "{terms.description}" on {vec.odds_boost.PAGE.terms_and_conditions_section_title} section '
                             f'is not the same as expected "{vec.odds_boost.PAGE.terms_and_conditions_section_title}"')

    def test_006_load_cms___odds_boost_menucheck_off_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Load CMS -> "Odds Boost" Menu
        DESCRIPTION: Check off Active checkbox and save changes
        EXPECTED: Changes are saved in CMS
        """
        self.site.logout()
        self.cms_config.update_odds_boost_config(enabled=False,
                                                 logged_in_header_text=vec.odds_boost.PAGE.today_odds_boosts,
                                                 logged_out_header_text=self.new_logged_out_header_text,
                                                 terms_and_conditions_text=vec.odds_boost.PAGE.terms_and_conditions_section_title)

    def test_007_load_the_application_and_verify_no_data_is_shown_for_odds_boost_in_the_initial_request(self):
        """
        DESCRIPTION: Load the application and verify no data is shown for odds boost in the initial request
        EXPECTED: oddsBoost: null is shown in Odds Boost section of request
        """
        # covered in 8 step

    def test_008_login_with_user_1(self):
        """
        DESCRIPTION: Login with User 1
        EXPECTED: Odds Boost token summary popup is not shown
        EXPECTED: Odds Boost is not shown in Right Menu
        EXPECTED: Odds boost page is unavailable
        EXPECTED: Odds Boost button is not shown in Betslip
        EXPECTED: Odds Boost button is not shown in Quick Bet
        """
        self.site.login(username=self.username, ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
        self.assertFalse(self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=10))
        self.navigate_to_page('/oddsboost')
        self.navigate_to_edp(event_id=self.eventID)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='No markets found')
        market = markets_list.get(self.section_name)
        self.assertTrue(market, msg='Can not find Match Result section')
        outcomes = market.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes are shown for Match Result market')
        self.assertIn(self.team1, outcomes, msg=f'"{self.team1}" is not in outcomes "{outcomes}"')
        outcomes.get(self.team1).click()
        self.device.refresh_page()
        if self.is_mobile:
            quick_bet = self.site.quick_bet_panel
            self.assertFalse(quick_bet.has_odds_boost_button(expected_result=False, timeout=2),
                             msg='"Odds boost button" is present on Quickbet panel')
            quick_bet.add_to_betslip_button.click()
        self.site.open_betslip()
        self.assertFalse(self.get_betslip_content().has_odds_boost_header, msg='"Odds boost header" is shown')
