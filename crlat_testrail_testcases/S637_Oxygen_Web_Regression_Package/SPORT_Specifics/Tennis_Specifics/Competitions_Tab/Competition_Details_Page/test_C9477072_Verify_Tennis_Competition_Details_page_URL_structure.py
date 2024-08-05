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
class Test_C9477072_Verify_Tennis_Competition_Details_page_URL_structure(Common):
    """
    TR_ID: C9477072
    NAME: Verify Tennis Competition Details page URL structure
    DESCRIPTION: This test case verifies URL structure for Tennis Competition Details pages
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Tennis landing page and choose 'Competition' tab
    """
    keep_browser_open = True

    def test_001_click_tap_any_type_accordion(self):
        """
        DESCRIPTION: Click/ tap any type accordion
        EXPECTED: Competition Details page is opened
        """
        pass

    def test_002_verify_url_structure(self):
        """
        DESCRIPTION: Verify URL structure
        EXPECTED: URL structure of Competition Details page is:
        EXPECTED: https://{domain}/competitions/tennis/class/type
        EXPECTED: where
        EXPECTED: class - OB class name
        EXPECTED: type - OB type name
        """
        pass

    def test_003_verify_url_structure_format(self):
        """
        DESCRIPTION: Verify URL structure format
        EXPECTED: * All text within URL is in lower case
        EXPECTED: * Space between worlds is replaced by "-" symbol
        EXPECTED: * The next specials characters "%", "-", ":" are replaced by "-" symbol
        """
        pass

    def test_004_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: Competitions landing page is opened
        """
        pass

    def test_005_repeat_steps_1_3_for_any_other_competition(self):
        """
        DESCRIPTION: Repeat steps #1-3 for any other Competition
        EXPECTED: 
        """
        pass
