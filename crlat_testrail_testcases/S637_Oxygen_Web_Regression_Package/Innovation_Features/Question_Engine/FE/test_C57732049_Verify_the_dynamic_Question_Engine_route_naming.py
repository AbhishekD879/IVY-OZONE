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
class Test_C57732049_Verify_the_dynamic_Question_Engine_route_naming(Common):
    """
    TR_ID: C57732049
    NAME: Verify the dynamic Question Engine route naming
    DESCRIPTION: This test case verifies the dynamic Question Engine route naming.
    PRECONDITIONS: 1. The User is logged in.
    """
    keep_browser_open = True

    def test_001_click_on_the_play_now_for_free_button(self):
        """
        DESCRIPTION: Click on the 'Play Now For Free' button.
        EXPECTED: A Question page is opened.
        """
        pass

    def test_002_check_the_url(self):
        """
        DESCRIPTION: Check the URL.
        EXPECTED: The URL has '/qe/&lt;sample_name&gt;/questions' route.
        """
        pass
