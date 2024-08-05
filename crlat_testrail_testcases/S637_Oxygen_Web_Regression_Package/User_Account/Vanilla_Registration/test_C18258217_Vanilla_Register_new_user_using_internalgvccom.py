import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C18258217_Vanilla_Register_new_user_using_internalgvccom(Common):
    """
    TR_ID: C18258217
    NAME: [Vanilla] Register new user using @internalgvc.com
    DESCRIPTION: This test case verifies possibility of new user registration using internal GVC mechanism to by-pass KYC verification.
    DESCRIPTION: It is a simplest happy path scenario for user registration
    PRECONDITIONS: Make sure you are logged out of the system.
    PRECONDITIONS: This test case should be tested on Desktop, Tablet and Mobile devices.
    """
    keep_browser_open = True

    def test_001_open_qa2_environment(self):
        """
        DESCRIPTION: Open qa2 environment;
        EXPECTED: 
        """
        pass

    def test_002_tap_on_join_button(self):
        """
        DESCRIPTION: Tap on 'Join' button
        EXPECTED: step 1 of registration form appears;
        """
        pass

    def test_003_insert_following_datacountry_of_residence_united_kingdomcurrency_gbpemail_internalgvccomusername_ukmigct_password_12345qwe(self):
        """
        DESCRIPTION: Insert following data:
        DESCRIPTION: Country of residence: United Kingdom
        DESCRIPTION: Currency: GBP
        DESCRIPTION: Email: *@internalgvc.com
        DESCRIPTION: Username: ukmigct-*
        DESCRIPTION: Password: 12345Qwe
        EXPECTED: All mandatory fields are filled
        EXPECTED: None of fields are highlighted in red
        """
        pass

    def test_004_click_continue(self):
        """
        DESCRIPTION: Click CONTINUE
        EXPECTED: step 2 of registration form appears
        """
        pass

    def test_005_insert_following_datamrfirst_name_firstlast_name_lastdate_of_birth_17_apr_1994(self):
        """
        DESCRIPTION: Insert following data:
        DESCRIPTION: Mr.
        DESCRIPTION: First name: first
        DESCRIPTION: Last name: last
        DESCRIPTION: Date of birth: 17-Apr-1994
        EXPECTED: All mandatory fields are filled
        EXPECTED: None of fields are highlighted in red
        """
        pass

    def test_006_click_continue(self):
        """
        DESCRIPTION: Click CONTINUE
        EXPECTED: next step of registration form appears
        """
        pass

    def test_007_insert_following_datahouse_number_house_numbercity_citypostcode_12345mobile_number_7788123456(self):
        """
        DESCRIPTION: Insert following data:
        DESCRIPTION: House number: house number
        DESCRIPTION: City: city
        DESCRIPTION: Postcode: 12345
        DESCRIPTION: Mobile number: 7788123456
        EXPECTED: All mandatory fields are filled
        EXPECTED: None of fields are highlighted in red
        """
        pass

    def test_008_click_create_my_account(self):
        """
        DESCRIPTION: Click CREATE MY ACCOUNT
        EXPECTED: Deposit limits page appears;
        """
        pass

    def test_009_click_no_limit(self):
        """
        DESCRIPTION: Click NO LIMIT
        EXPECTED: 
        """
        pass

    def test_010_check_acceptance_checkbox(self):
        """
        DESCRIPTION: Check Acceptance checkbox
        EXPECTED: 
        """
        pass

    def test_011_click_submit(self):
        """
        DESCRIPTION: Click SUBMIT
        EXPECTED: Deposit page appears with deposit options
        """
        pass

    def test_012_click_x(self):
        """
        DESCRIPTION: Click X
        EXPECTED: Sportsbook page appears with user logged in;
        """
        pass
