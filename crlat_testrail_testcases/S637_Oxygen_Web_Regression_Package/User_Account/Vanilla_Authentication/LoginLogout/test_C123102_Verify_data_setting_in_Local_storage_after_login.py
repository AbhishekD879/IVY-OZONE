import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C123102_Verify_data_setting_in_Local_storage_after_login(Common):
    """
    TR_ID: C123102
    NAME: Verify data setting in Local storage after login
    DESCRIPTION: This test case verify data setting in local storage after login
    DESCRIPTION: NOTE: not up to date due to old cashier steps
    PRECONDITIONS: 1. Open Developer tool
    PRECONDITIONS: NOTE: OX.USER data flags can be changed and appear new one's. Most important are present in this test case
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_in_developer_tool_open_application_tab___local_storage_section_and_check_oxuser_record(self):
        """
        DESCRIPTION: In Developer tool, open Application tab -> Local Storage section and check **'OX.USER'** record
        EXPECTED: **'OX.USER'** record contains the next default  data:
        EXPECTED: - bppToken: null,
        EXPECTED: - sessionToken: null,
        EXPECTED: - username: null,
        EXPECTED: - sportBalance: null,
        EXPECTED: - advertiser: null,
        EXPECTED: - countryCode: null,
        EXPECTED: - currencySymbol: '£',
        EXPECTED: - currency: 'GBP',
        EXPECTED: - email: null,
        EXPECTED: - firstname: null,
        EXPECTED: - firstNews: null,
        EXPECTED: - lastname: null,
        EXPECTED: - oddsFormat: 'frac',
        EXPECTED: - playerCode: null,
        EXPECTED: - playerDepositLimits: null,
        EXPECTED: - postCode: null,
        EXPECTED: - previousLoginTime: null,
        EXPECTED: - profileId: null,
        EXPECTED: - sessionLimit: 0,
        EXPECTED: - vipLevel: null,
        EXPECTED: - firstLogin: false,
        EXPECTED: - passwordResetLogin: false,
        EXPECTED: - showBalance: true,
        EXPECTED: - status: false,
        EXPECTED: - termsLogin: false
        """
        pass

    def test_003_login_with_valid_credentials_and_repeat_step_2(self):
        """
        DESCRIPTION: Login with valid credentials and repeat step #2
        EXPECTED: **'OX.USER'** record contains the next data:
        EXPECTED: - bppToken:
        EXPECTED: - sessionToken:
        EXPECTED: - username:
        EXPECTED: - sportBalance:
        EXPECTED: - advertiser:
        EXPECTED: - countryCode:
        EXPECTED: - currencySymbol:
        EXPECTED: - currency:
        EXPECTED: - email:
        EXPECTED: - firstname:
        EXPECTED: - firstNews:
        EXPECTED: - lastname:
        EXPECTED: - oddsFormat:
        EXPECTED: - playerCode:
        EXPECTED: - playerDepositLimits:
        EXPECTED: - postCode:
        EXPECTED: - previousLoginTime:
        EXPECTED: - profileId:
        EXPECTED: - sessionLimit:
        EXPECTED: - vipLevel:
        EXPECTED: - firstLogin:
        EXPECTED: - passwordResetLogin:
        EXPECTED: - showBalance:
        EXPECTED: - status:
        EXPECTED: - termsLogin:
        """
        pass

    def test_004_open_network_tab___xhr_filter___choose_second_user_request_and_verify_bpptoken_in_response(self):
        """
        DESCRIPTION: Open Network tab -> XHR filter -> choose second 'user' request and verify **bppToken** in response
        EXPECTED: - **bppToken** is present in response
        EXPECTED: - **bppToken** set in **'OX.USER'** record in local storage is equal to bppToken from response
        """
        pass

    def test_005_open_network_tab___ws_filter___choose_31002_response_and_verify_sessiontoken(self):
        """
        DESCRIPTION: Open Network tab -> WS filter -> choose 31002 response and verify **sessionToken**
        EXPECTED: - **sessionToken** is present in response
        EXPECTED: - **sessionToken** set in **'OX.USER'** record in local storage is equal to sessionToken from response
        """
        pass

    def test_006_verify_showbalance_parameter(self):
        """
        DESCRIPTION: Verify **showBalance** parameter
        EXPECTED: **showBalance = false** if user chooses 'Hide balance' option
        """
        pass

    def test_007_verify_status_parameter(self):
        """
        DESCRIPTION: Verify **status** parameter
        EXPECTED: **status=true** parameter after login or page refresh during active session
        """
        pass

    def test_008_open_network_tab___ws_filter___choose_32010_response_and_verify_sportbalance_parameter(self):
        """
        DESCRIPTION: Open Network tab -> WS filter -> choose 32010 response and verify **sportBalance** parameter
        EXPECTED: **SportBalance** parameter corresponds to **balances.balance.amount** value when **balanceType =
        EXPECTED: sportsbook_gaming_balance**
        """
        pass

    def test_009_verify_oddsformat_parameter(self):
        """
        DESCRIPTION: Verify **oddsFormat** parameter
        EXPECTED: - **oddsFormat = dec** if user chooses Decimal price format
        EXPECTED: - **oddsFormat' = frac** if user chooses Fractional price format
        """
        pass

    def test_010_open_network_tab___ws_filter___choose_31006_response_and_verify_username_advertiser_signupdate_countrycode_playercode_viplevel_profileid_firstname_lastname_email_postcode_currencysymbol_and_currency_parameters(self):
        """
        DESCRIPTION: Open Network tab -> WS filter -> choose 31006 response and verify **username**, **advertiser**, **signupDate**, **CountryCode**, **playerCode**, **viplevel**, **profileID**, **firstname**, **lastname**, **email**, **postCode**, **currencySymbol** and **currency** parameters
        EXPECTED: - All parameters are present in response
        EXPECTED: - **username**, **advertiser**, **signupDate**, **CountryCode**, **playerCode**, **viplevel**, **profileID**, **firstname**, **lastname**, **email**, **postCode**, **currencySymbol** and **currency** parameters set in 'OX.USER' record in local storage is equal to appropriate value from response
        EXPECTED: **NOTE** that currently we do not receive **profileID** from Playtech
        """
        pass

    def test_011_verify_firstlogin_parameter(self):
        """
        DESCRIPTION: Verify **firstLogin** parameter
        EXPECTED: **firstLogin = true** parameter is set after registraion of new user
        """
        pass

    def test_012_verify_termslogin_parameter(self):
        """
        DESCRIPTION: Verify **termsLogin** parameter
        EXPECTED: **TermsLogin = true** parameter when new Terms and Conditions are received
        """
        pass

    def test_013_verify_passwordresetlogin_parameter(self):
        """
        DESCRIPTION: Verify **passwordResetLogin** parameter
        EXPECTED: **PasswordResetLogin = true** when user logs in with temporary password received after resetting password functionality
        """
        pass

    def test_014_open_network_tab___ws_filter___choose_31133_notification_and_verify_sessionlimit_parameter(self):
        """
        DESCRIPTION: Open Network tab -> WS filter -> choose 31133 notification and verify **sessionLimit** parameter
        EXPECTED: - **SessionLimit** parameter corresponds to **action.actionShowSessionTimerInfo.sessionLimit** value from notification
        EXPECTED: - **SessionLimit = 0** if user has no limits set; note in this case 31133 notification is not received
        """
        pass

    def test_015_open_network_tab___ws_filter___choose_89905_response_and_verify_playerdepositlimits_parameter(self):
        """
        DESCRIPTION: Open Network tab -> WS filter -> choose 89905 response and verify **playerDepositLimits** parameter
        EXPECTED: **PlayerDepositLimits** parameter consists of array of current and waiting (if available) limits
        """
        pass

    def test_016_log_out_and_repeat_step_2(self):
        """
        DESCRIPTION: Log out and repeat step #2
        EXPECTED: 
        """
        pass
