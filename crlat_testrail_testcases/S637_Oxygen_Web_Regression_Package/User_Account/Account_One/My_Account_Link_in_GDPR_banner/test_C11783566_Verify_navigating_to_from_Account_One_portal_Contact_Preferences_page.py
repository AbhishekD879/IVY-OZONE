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
class Test_C11783566_Verify_navigating_to_from_Account_One_portal_Contact_Preferences_page(Common):
    """
    TR_ID: C11783566
    NAME: Verify navigating to/from 'Account One' portal 'Contact Preferences ' page
    DESCRIPTION: This test case verifies navigating to/from 'Account One' portal 'Contact Preferences ' page and setting contact preferences
    PRECONDITIONS: User (with 'mrktpref_status' = "active", 'mrktpref_status_seen' = "no" tags in IMS) is logged in
    PRECONDITIONS: Instruction on how to set GDPR related user data in IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/IMS+configuration+for+GDPR IMS link
    PRECONDITIONS: To check Contact Preferences on IMS: navigate to Contact preferences section in a user account.
    PRECONDITIONS: CMS Static Block used: "GDPR Policy"
    PRECONDITIONS: ________________
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link & creds to Ladbrokes IMS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: * Account One redirection urls:
    PRECONDITIONS: * TST2: http://accountone-test.ladbrokes.com/contact-preferences?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * STG: https://accountone-stg.ladbrokes.com/contact-preferences?clientType=sportsbook&back_url=[url to an app]
    PRECONDITIONS: * PROD: http://accountone.ladbrokes.com/contact-preferences?clientType=sportsbook&back_url=[url to an app]
    """
    keep_browser_open = True

    def test_001_tap_my_account_link_updated_policies_banner(self):
        """
        DESCRIPTION: Tap 'My account' link 'Updated Policies' banner
        EXPECTED: * Account one contact-preferences page is open
        EXPECTED: * URL corresponds to URL from preconditions
        """
        pass

    def test_002_check_off_some_checkboxes___tap_close_button_x(self):
        """
        DESCRIPTION: Check off some checkboxes  > Tap 'Close' button ('X')
        EXPECTED: * User is landed on the page he came from
        EXPECTED: * User is logged in
        EXPECTED: * Contact Preferences on IMS for this user are set according to ticked checkboxes
        EXPECTED: * Tag value for 'mrktpref_status_seen' is set "yes" (in "openapi" "Set Player Tags" websocket request )
        """
        pass
