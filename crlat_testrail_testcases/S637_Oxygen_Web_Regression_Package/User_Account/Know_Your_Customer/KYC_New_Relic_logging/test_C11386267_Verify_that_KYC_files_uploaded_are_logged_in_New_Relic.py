import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C11386267_Verify_that_KYC_files_uploaded_are_logged_in_New_Relic(Common):
    """
    TR_ID: C11386267
    NAME: Verify that KYC files uploaded are logged in New Relic
    DESCRIPTION: This test case verifies ability of business user to access KYC files uploaded (KYC Jumio success popup) analytics in New Relic environment
    DESCRIPTION: Note: Cannot automate as we are not automating NewRelic app
    PRECONDITIONS: 1. Login to New Relic environment at https://insights.newrelic.com (ask your team lead for credentials)
    PRECONDITIONS: 2. In order to see all KYC related events run NRQL query, eg.: "SELECT * FROM PageAction where actionName = ‘KYC’ where appId = ‘54469423’ since last week"
    PRECONDITIONS: =======
    PRECONDITIONS: - In NRQL query 'appId' attribute defines environment (dev, stage, prod, etc.) on which you're requesting analytics. In order to see needed 'appId' for you environment: Open Oxygen app > Devtools > Console > type "newrelic" > press Enter > in returned values expand 'info' section > applicationID: "xxxxxxxx" (e.g. applicationID: "54469423")
    PRECONDITIONS: - Playtech IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001_in_oxygen_applogin_user_with_age_verification_status__active_grace_period_and_player_tag_agp_success_upload__5(self):
        """
        DESCRIPTION: In Oxygen app:
        DESCRIPTION: Login user with Age Verification Status = 'Active Grace Period' AND player tag: 'AGP_Success_Upload < 5'
        EXPECTED: - Verification Failed overlay displayed
        """
        pass

    def test_002_click_on_verify_meverify_my_address_button_and(self):
        """
        DESCRIPTION: Click on 'Verify Me'/'Verify My Address' button and
        EXPECTED: User redirected to Netverify document upload
        """
        pass

    def test_003_complete_netverify_document_upload_jumio(self):
        """
        DESCRIPTION: Complete Netverify document upload (Jumio)
        EXPECTED: - User successfully uploaded document(s)
        EXPECTED: - KYC Jumio success popup displayed
        """
        pass

    def test_004_in_new_relic_app__run_nrql_query__in_returned_data_find_username_youve_logged_in_with(self):
        """
        DESCRIPTION: In New Relic app:
        DESCRIPTION: - Run NRQL query
        DESCRIPTION: - In returned data find Username you've logged in with
        EXPECTED: - Corresponding record with your username is present ('username' attribute)
        EXPECTED: - 'kycUploadFiles' attribute should display added AGP_Success_Upload tag value after successful Netverify upload flow
        """
        pass
