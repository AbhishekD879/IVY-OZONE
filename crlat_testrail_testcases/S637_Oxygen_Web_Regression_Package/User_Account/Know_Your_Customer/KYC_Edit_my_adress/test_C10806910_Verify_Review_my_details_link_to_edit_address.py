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
class Test_C10806910_Verify_Review_my_details_link_to_edit_address(Common):
    """
    TR_ID: C10806910
    NAME: Verify "Review my details" link to edit address
    DESCRIPTION: This test case verifies that user who has failed the verification is able to update the address
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: **Playtech IMS**:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: **To find & edit user details in IMS** go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: **User Age Verification Result status** is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: - User with IMS **Age verification status** = Active grace period AND **Player tag** = “AGP_Success_Upload < 5” OR POA_Required & AGP_Success_Upload < 5 ( i.e failed 1+1 verification for ID and address) has edited his address inside Review my details pop up
    PRECONDITIONS: - The number of edits for the address is less than 3 ('Review my details' link is available)
    PRECONDITIONS: - **User is displayed the pop-up 'Verification failed'**
    """
    keep_browser_open = True

    def test_001_click_on_the_review_my_details_link(self):
        """
        DESCRIPTION: Click on the 'Review my details' link
        EXPECTED: The pop up "Review details" with their existing detail is shown:
        EXPECTED: - Name(Not editable)
        EXPECTED: - DOB (Not editable)
        EXPECTED: - Address(Editable)
        EXPECTED: - 'Update address' button (green)
        EXPECTED: - 'Live Chat' button (yellow) surrounded by text "To update your date of birth or name please contact customer support"
        """
        pass

    def test_002_update_the_editable_fields_address(self):
        """
        DESCRIPTION: Update the editable fields (address)
        EXPECTED: Fields with Address are edited
        """
        pass

    def test_003_click_on_the_update_address_button(self):
        """
        DESCRIPTION: Click on the 'Update address' button
        EXPECTED: - Timer overlay for '<x>' seconds (<x> is configurable in CMS) is displayed
        EXPECTED: - 'OX.reviewDetailsCounter' counter is incremented by 1 (Dev tool ->Application ->Local Storage)
        """
        pass
