import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C12834654_Odds_Boost_configuration_in_CMS(Common):
    """
    TR_ID: C12834654
    NAME: Odds Boost configuration in CMS
    DESCRIPTION: This test case verifies possibility to configure Odds Boost in CMS.
    PRECONDITIONS: Generate Odds boost token in http://backoffice-tst2.coral.co.uk/office for User 1.
    PRECONDITIONS: How to add OB token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: CMS configuration for Odds Boost is added. Odds Boost is Active.
    """
    keep_browser_open = True

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
        pass

    def test_002_load_the_application_and_verify_that_odds_boost_data_is_shown_in_the_initial_request_network___mobile(self):
        """
        DESCRIPTION: Load the application and verify that odds boost data is shown in the initial request (Network -> "mobile")
        EXPECTED: Appropriate data from CMS is shown in _oddsBoost_ section of request:
        EXPECTED: enabled: true
        EXPECTED: lang:
        EXPECTED: loggedInHeaderText:
        EXPECTED: loggedOutHeaderText:
        EXPECTED: **from OX100** moreLink:
        EXPECTED: svg:
        EXPECTED: svgFilename:
        EXPECTED: svgId:
        EXPECTED: termsAndConditionsText:
        """
        pass

    def test_003_login_to_application_with_user_1navigate_to_odds_boost_page_and_verify_that_appropriate_odds_boost_elements_are_shown(self):
        """
        DESCRIPTION: Login to application with User 1.
        DESCRIPTION: Navigate to Odds Boost Page and verify that appropriate odds boost elements are shown.
        EXPECTED: The following elements configured in CMS are shown on Odds Boost page:
        EXPECTED: * Image
        EXPECTED: * Logged In Header Text
        EXPECTED: * Terms&Conditions Text
        """
        pass

    def test_004_load_cms___odds_boost_menuremove_configured_image_and_edit_header_text__termsconditions_textsave_changes(self):
        """
        DESCRIPTION: Load CMS -> "Odds Boost" Menu.
        DESCRIPTION: Remove configured Image and edit Header text / Terms&Conditions text.
        DESCRIPTION: Save changes.
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_005_navigate_back_to_application_logged_in_as_user_1___odds_boost_page(self):
        """
        DESCRIPTION: Navigate back to application (logged in as User 1) -> Odds Boost page
        EXPECTED: The following elements configured in CMS are shown on Odds Boost page:
        EXPECTED: * Default odds boost image
        EXPECTED: * Logged In Header Text (edited in Step 4)
        EXPECTED: * Terms&Conditions Text (edited in Step 4)
        """
        pass

    def test_006_load_cms___odds_boost_menucheck_off_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Load CMS -> "Odds Boost" Menu
        DESCRIPTION: Check off Active checkbox and save changes
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_007_load_the_application_and_verify_no_data_is_shown_for_odds_boost_in_the_initial_request(self):
        """
        DESCRIPTION: Load the application and verify no data is shown for odds boost in the initial request
        EXPECTED: _oddsBoost: null_ is shown in Odds Boost section of request
        """
        pass

    def test_008_login_with_user_1(self):
        """
        DESCRIPTION: Login with User 1
        EXPECTED: * Odds Boost token summary popup is not shown
        EXPECTED: * Odds Boost is not shown in Right Menu
        EXPECTED: * Odds boost page is unavailable
        EXPECTED: * Odds Boost button is not shown in Betslip
        EXPECTED: * Odds Boost button is not shown in Quick Bet
        """
        pass
