import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


#@pytest.mark.tst2
#@pytest.mark.stg2  TC is not automatable
# @pytest.mark.crl_prod
# @pytest.mark.hl
@pytest.mark.odds_boost
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.cms
@pytest.mark.mobile_only
@pytest.mark.slow
@pytest.mark.na
@vtest
class Test_C2644884_Verify_Odds_boost_configuration_in_CMS(BaseBetSlipTest):
    """
    TR_ID: C2644884
    VOL_ID: C10475183
    NAME: Verify "Odds boost" configuration in CMS
    DESCRIPTION: This test case verifies the possibility to configure "Odds boost" in CMS
    PRECONDITIONS: Load CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Token is NOT expired
    """
    keep_browser_open = True
    new_logged_in_header_text = 'New_LoggedInText'
    new_logged_out_header_text = 'New_LoggedOutText'
    new_terms_and_conditions_text = 'New_Terms'

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
        cms_config.update_odds_boost_config(logged_in_header_text=cls.old_logged_in_header_text,
                                            logged_out_header_text=cls.old_logged_out_header_text,
                                            terms_and_conditions_text=cls.old_terms_and_condition_text)

    def test_001_tap_odds_boost_menu_item_in_the_navigation_menu(self):
        """
        DESCRIPTION: Tap "Odds Boost" Menu item in the navigation menu
        EXPECTED: "Odds Boost" landing page opens
        """
        self.navigate_to_page('/oddsboost')
        self.site.wait_content_state(state_name='oddsboost')

    def test_002_verify_elements_on_odds_boost__page_in_cms(self):
        """
        DESCRIPTION: Verify elements on "Odds Boost"  page in CMS.
        EXPECTED: *Odds Boost ON/OFF Toggle button
        EXPECTED: *Custom field for Image (svg) (Image1)
        EXPECTED: *Custom rich text field for Logged Out Header Text ('HeaderText1')
        EXPECTED: *Custom rich text field  for Logged In Header Text ('HeaderText2')
        EXPECTED: *Custom Field for Terms&Conditions text ('T&CText1')
        """
        pass  # we do not automate CMS

    def test_003_load_the_applicationverify_that_odds_boost_data_is_shown_in_the_initial_requestuse_mobile_filter_in_network_tab(self):
        """
        DESCRIPTION: Load the application
        DESCRIPTION: Verify that odds boost data is shown in the initial request
        DESCRIPTION: Use 'mobile' filter in Network tab.
        EXPECTED: Appropriate data is shown in odds Boost section of request:
        EXPECTED: enabled: true
        EXPECTED: lang: "en"
        EXPECTED: loggedInHeaderText: "<p>HeaderText2 </p>"
        EXPECTED: loggedOutHeaderText: "<p>HeaderText1</p>"
        EXPECTED: svg: "<symbol id="..."
        EXPECTED: svgFilename: "Image1.svg"
        EXPECTED: svgId: "#..."
        EXPECTED: termsAndConditionsText: "<p>T&CText1</p>"
        """
        expected_values = ['enabled', 'lang', 'loggedInHeaderText', 'loggedOutHeaderText', 'svg',
                           'svgFilename', 'svgId', 'termsAndConditionsText']

        odds_boost = self.cms_config.get_initial_data().get('oddsBoost')

        self.assertTrue(odds_boost['enabled'], msg='Odds boost is not enabled in CMS')
        for value in expected_values:
            self.assertIn(value, odds_boost.keys(), msg=f'{value} value is not present '
                                                        f'in the response values {odds_boost.keys()}')

    def test_004_load_cmsnavigate_to_odds_boost_menu_item_in_the_navigation_menuremove_image1change_logged_out_header_text_to_headertext3change_logged_in_header_text_to_headertext4change_termsconditions_text_to_tc_text2save_changes(self):
        """
        DESCRIPTION: Load CMS
        DESCRIPTION: Navigate to "Odds Boost" Menu item in the navigation menu
        DESCRIPTION: Remove Image1
        DESCRIPTION: Change Logged Out Header Text to 'HeaderText3'
        DESCRIPTION: Change Logged In Header Text to 'HeaderText4'
        DESCRIPTION: Change Terms&Conditions Text to 'T&C_Text2'
        DESCRIPTION: Save changes
        EXPECTED: Changes are saved in CMS
        """
        self.cms_config.update_odds_boost_config(logged_in_header_text=self.new_logged_in_header_text,
                                                 logged_out_header_text=self.new_logged_out_header_text,
                                                 terms_and_conditions_text=self.new_terms_and_conditions_text)

    def test_005_load_the_applicationverify_that_updated_odds_boost_data_is_shown_in_the_initial_requestuse_mobile_filter_in_network_tab(self):
        """
        DESCRIPTION: Load the application
        DESCRIPTION: Verify that updated odds boost data is shown in the initial request
        DESCRIPTION: Use 'mobile' filter in Network tab.
        EXPECTED: Appropriate data is shown in odds Boost section of request:
        EXPECTED: enabled: true
        EXPECTED: lang: "en"
        EXPECTED: loggedInHeaderText: "<p>HeaderText4</p>"
        EXPECTED: loggedOutHeaderText: "<p>HeaderText3</p>"
        EXPECTED: svg: ""
        EXPECTED: svgFilename: null
        EXPECTED: svgId: "#..."
        EXPECTED: termsAndConditionsText: "<p>T&CText2</p>"
        """
        result = wait_for_result(lambda: self.cms_config.get_initial_data().get('oddsBoost')['loggedInHeaderText'] == self.new_logged_in_header_text,
                                 name=f'New Oddsboost config to become active. '
                                      f'Current logged in header is {self.cms_config.get_initial_data().get("oddsBoost")["loggedInHeaderText"]}',
                                 poll_interval=2,
                                 timeout=300)
        self.assertTrue(result, msg='New Oddsboost config was not activated')

        odds_boost = self.cms_config.get_initial_data().get('oddsBoost')

        logged_in_text = odds_boost['loggedInHeaderText']
        logged_out_text = odds_boost['loggedOutHeaderText']
        terms_text = odds_boost['termsAndConditionsText']

        self.assertEqual(logged_in_text, self.new_logged_in_header_text,
                         msg=f'Logged in header text "{logged_in_text}" '
                             f'is not the same as expected "{self.new_logged_in_header_text}"')
        self.assertEqual(logged_out_text, self.new_logged_out_header_text,
                         msg=f'Logged in header text "{logged_out_text}" '
                             f'is not the same as expected "{self.new_logged_out_header_text}"')
        self.assertEqual(terms_text, self.new_terms_and_conditions_text,
                         msg=f'Logged in header text "{terms_text}" '
                             f'is not the same as expected "{self.new_terms_and_conditions_text}"')

    def test_006_load_cmsnavigate_to_odds_boost_menu_item_in_the_navigation_menuturn_off_odds_boost_toggle___save_changes(self):
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

    def test_007_load_the_applicationverify_that_no_data_is_shown_for_odds_boost_in_the_initial_requestuse_mobile_filter_in_network_tab(self):
        """
        DESCRIPTION: Load the application
        DESCRIPTION: Verify that no data is shown for odds boost in the initial request
        DESCRIPTION: Use 'mobile' filter in Network tab.
        EXPECTED: *oddsBoost: null* is shown in odd Boost section of request
        """
        result = wait_for_result(
            lambda: self.cms_config.get_initial_data().get('oddsBoost') is None,
            name='Oddsboost config to become disabled',
            poll_interval=2,
            timeout=300)
        self.assertTrue(result, msg='Oddsboost config was not disabled')
