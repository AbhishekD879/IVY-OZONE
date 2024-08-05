import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2644884_Verify_Odds_boost_configuration_in_CMS(Common):
    """
    TR_ID: C2644884
    NAME: Verify "Odds boost" configuration in CMS
    DESCRIPTION: This test case verifies the possibility to configure "Odds boost" in CMS
    DESCRIPTION: AUTOTEST C10581662
    PRECONDITIONS: Load CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Token is NOT expired
    """
    keep_browser_open = True

    def test_001_tap_odds_boost_menu_item_in_the_navigation_menu(self):
        """
        DESCRIPTION: Tap "Odds Boost" Menu item in the navigation menu
        EXPECTED: "Odds Boost" landing page opens
        """
        pass

    def test_002_verify_elements_on_odds_boost__page_in_cms(self):
        """
        DESCRIPTION: Verify elements on "Odds Boost"  page in CMS.
        EXPECTED: *Odds Boost ON/OFF Toggle button
        EXPECTED: *Custom field for Image (svg) (Image1)
        EXPECTED: *Custom rich text field for Logged Out Header Text ('HeaderText1')
        EXPECTED: *Custom rich text field  for Logged In Header Text ('HeaderText2')
        EXPECTED: *Custom Field for Terms&Conditions text ('T&CText1')
        """
        pass

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
        pass

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
        pass

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
        pass

    def test_006_load_cmsnavigate_to_odds_boost_menu_item_in_the_navigation_menuturn_off_odds_boost_toggle___save_changes(self):
        """
        DESCRIPTION: Load CMS
        DESCRIPTION: Navigate to "Odds Boost" Menu item in the navigation menu
        DESCRIPTION: Turn OFF "Odds Boost" Toggle -> Save changes
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_007_load_the_applicationverify_that_no_data_is_shown_for_odds_boost_in_the_initial_requestuse_mobile_filter_in_network_tab(self):
        """
        DESCRIPTION: Load the application
        DESCRIPTION: Verify that no data is shown for odds boost in the initial request
        DESCRIPTION: Use 'mobile' filter in Network tab.
        EXPECTED: *oddsBoost: null* is shown in odd Boost section of request
        """
        pass
