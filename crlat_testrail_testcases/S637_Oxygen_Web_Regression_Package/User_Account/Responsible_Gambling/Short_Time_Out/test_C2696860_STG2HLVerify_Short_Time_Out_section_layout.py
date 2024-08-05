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
class Test_C2696860_STG2HLVerify_Short_Time_Out_section_layout(Common):
    """
    TR_ID: C2696860
    NAME: [STG2][HL]Verify 'Short Time Out' section layout
    DESCRIPTION: This test case verifies 'Short Time Out' section layout
    PRECONDITIONS: * Oxygen app is loaded and the user is logged in
    PRECONDITIONS: * Navigate to 'Right Menu' -> 'My Account' -> 'Responsible Gambling'
    PRECONDITIONS: * 'Responsible Gambling' page is opened and 'Short Time Out' section is displayed
    PRECONDITIONS: *Note:*
    PRECONDITIONS: * 'Responsible Gambling' page with all sections are CMS configurable. Please, take a look at https://ladbrokescoral.testrail.com/index.php?/cases/view/28369 to get acquainted with the instruction how to create or update content on 'Responsible Gambling' page.
    PRECONDITIONS: * 'Take a short break' link should be set in Static Block for 'Short Time-Out' section.
    """
    keep_browser_open = True

    def test_001_verify_short_time_out_section_layout(self):
        """
        DESCRIPTION: Verify 'Short Time Out' section layout
        EXPECTED: All content of the section is taken from 'Responsible Gambling EN' static block created in CMS and consists of:
        EXPECTED: * Header with left aligned 'Short Time Out' title
        EXPECTED: * Text
        EXPECTED: * 'Take a short break' link
        """
        pass

    def test_002_verify_take_a_short_break_link(self):
        """
        DESCRIPTION: Verify 'Take a short break' link
        EXPECTED: 'Take a short break' link is clickable
        """
        pass

    def test_003_clicktap_on_take_a_short_break_link(self):
        """
        DESCRIPTION: Click/Tap on 'Take a short break' link
        EXPECTED: * 'Take a short break' text is underlined
        EXPECTED: * User is redirected to 'Time Out' page
        """
        pass
