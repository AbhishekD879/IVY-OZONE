import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28610_Verify_CMS_configuration_of_Favourite_Matches_page(Common):
    """
    TR_ID: C28610
    NAME: Verify CMS configuration of 'Favourite Matches' page
    DESCRIPTION: This test case verifies CMS configuration of 'Favourite Matches' page for logged out users
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: *   BMA-12438 As a TA I want the duplicate calls to favourites-introductory-text & favourites-login-button-text reduced to a single call
    PRECONDITIONS: 1. User is logged out
    PRECONDITIONS: 2. User is on Football landing page
    PRECONDITIONS: 3. User has at least 1 event added to favourites
    PRECONDITIONS: 4. CMS endpoints can be found here https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed (CMS-API (Coral) section)
    PRECONDITIONS: 5. "favoritesText" config is created in System Configuration
    PRECONDITIONS: **NOTE**: Favourites always should be turned off for Ladbrokes
    """
    keep_browser_open = True

    def test_001_tap_the_favourite_matches_icon_and_verifyfavourite_matches_page_mobile_or_favourites_widget_desktop(self):
        """
        DESCRIPTION: Tap the 'Favourite Matches' icon and verify 'Favourite Matches' page (mobile) or Favourites widget (desktop)
        EXPECTED: Make sure data from 'favoritesText' CMS config is displayed on the page/widget:
        EXPECTED: 'introductoryText' and 'loginButtonText'
        """
        pass

    def test_002_in_cms_navigate_to_system_configuration__structure_section(self):
        """
        DESCRIPTION: In CMS navigate to System-configuration > Structure section
        EXPECTED: 'System-configuration' section is opened
        """
        pass

    def test_003_in_cms__system_configuration__structure_change_values_in_introductorytext_and_loginbuttontext_fieldsand_save(self):
        """
        DESCRIPTION: In CMS > System-configuration > Structure Change values in 'introductoryText' and 'loginButtonText' fields and save
        EXPECTED: 
        """
        pass

    def test_004_in_app_reload_page_and_verify_changes_received_in_initial_data_response_in_systemconfiguration__favoritestext_param(self):
        """
        DESCRIPTION: In app reload page and verify changes received in initial-data response in SystemConfiguration > favoritesText param
        EXPECTED: Changes made in CMS are received for 'introductoryText' and 'loginButtonText'
        """
        pass

    def test_005_verify_changes_made_in_cms_onfavourite_matches_pagewidget(self):
        """
        DESCRIPTION: Verify changes made in CMS on 'Favourite Matches' page/widget
        EXPECTED: Changes made in CMS are displayed successfully
        """
        pass
