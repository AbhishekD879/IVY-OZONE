import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C2989397_Verify_handling_of_invalid_account_one_links_configurations_in_CMS(Common):
    """
    TR_ID: C2989397
    NAME: Verify handling of invalid account one links configurations in CMS
    DESCRIPTION: This test case verifies handling of invalid account one links configurations in CMS
    PRECONDITIONS: 1. CMS is loaded
    PRECONDITIONS: (Use link: https://confluence.egalacoral.com/display/SPI/Migration+CMS-API )
    PRECONDITIONS: where CMS_ENDPOINT e.g. DEV0 or DEV1 can be found using devlog
    PRECONDITIONS: 2. In CMS: Current brand 'Ladbrokes' is selected -> 'System Configuration' -> 'Structure' is opened
    PRECONDITIONS: 3. 'ExternalUrls' section with the following 'Field Name' fields related to AccountOne are present with appropriate links in 'Field Value':
    PRECONDITIONS: * change-password - https://accountone.ladbrokes.com/forgot-password
    PRECONDITIONS: * forgot-password - https://accountone.ladbrokes.com/forgot-password
    PRECONDITIONS: * forgot-username - https://accountone.ladbrokes.com/forgot-username
    PRECONDITIONS: * signup - https://accountone.ladbrokes.com/register
    PRECONDITIONS: * personal-details - https://accountone.ladbrokes.com/personal-details
    PRECONDITIONS: * deposit - https://accountone.ladbrokes.com/deposit
    PRECONDITIONS: * freebets - https://accountone.ladbrokes.com/free-bets
    PRECONDITIONS: * transfer - http://accountone.ladbrokes.com/transfer
    PRECONDITIONS: * withdraw - http://accountone.ladbrokes.com/withdraw
    PRECONDITIONS: * account-history - http://accountone.ladbrokes.com/gaming-and-account
    PRECONDITIONS: * transaction-history - http://accountone.ladbrokes.com/gaming-and-account
    PRECONDITIONS: * gaming-history - http://accountone.ladbrokes.com/gaming-and-account
    PRECONDITIONS: * view-balances - http://accountone.ladbrokes.com/view-balances
    PRECONDITIONS: * limits - https://accountone.ladbrokes.com/responsible-gambling
    PRECONDITIONS: * responsible-gambling - https://accountone.ladbrokes.com/responsible-gambling
    PRECONDITIONS: * marketing-preferences - https://accountone.ladbrokes.com/contact-preferences
    PRECONDITIONS: * kyc-entry-point - https://accountone.ladbrokes.com/entry-point
    """
    keep_browser_open = True

    def test_001_cms_change_the_accountone_domain_part_in_field_value_section_for_one_of_the_fields_eg___tap_save_changes_button(self):
        """
        DESCRIPTION: **CMS:** Change the 'accountone' domain part in 'Field Value' section for one of the fields e.g.' -> tap 'Save changes' button
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_002_in_applicationtap_log_in_button___tap_forgot_password_link(self):
        """
        DESCRIPTION: In application:
        DESCRIPTION: Tap 'Log in' button -> Tap 'Forgot Password?' link
        EXPECTED: The link e.g. 'Forgot Password?' is NOT clickable
        """
        pass

    def test_003_cms_change_the_path_in_field_values_for_one_of_the_fields_eg_forgot_password___tap_save_changes_button(self):
        """
        DESCRIPTION: **CMS:** Change the path in 'Field Values' for one of the fields e.g. 'Forgot password?' -> tap 'Save changes' button
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_004_repeat_steps_2(self):
        """
        DESCRIPTION: Repeat steps #2
        EXPECTED: User is navigated to default AccountOne page
        """
        pass

    def test_005_cms_system_configuration___config___externalurls___delete_any_config_item(self):
        """
        DESCRIPTION: **CMS:** 'System Configuration' -> 'Config' -> ExternalUrls -> Delete any config item
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_006_repeat_steps_2(self):
        """
        DESCRIPTION: Repeat steps #2
        EXPECTED: 
        """
        pass
