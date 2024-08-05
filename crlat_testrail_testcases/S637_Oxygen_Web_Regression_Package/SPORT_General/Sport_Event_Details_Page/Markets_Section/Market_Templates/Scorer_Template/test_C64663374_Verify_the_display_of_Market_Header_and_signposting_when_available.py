import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C64663374_Verify_the_display_of_Market_Header_and_signposting_when_available(Common):
    """
    TR_ID: C64663374
    NAME: Verify the display of Market Header and signposting when available
    DESCRIPTION: This test case verifies market header with signposting available
    PRECONDITIONS: 1.Market which fall under scorer format should follow this templet
    PRECONDITIONS: ![](index.php?/attachments/get/49fd3c7f-227e-4fbe-8ad3-113c267d0b8e)
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: * User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_sports__edp_page(self):
        """
        DESCRIPTION: Navigate to sports  EDP page
        EXPECTED: * EDP page should be displayed
        """
        pass

    def test_003_expand_the_markets_which_should_display_the_scorer_template(self):
        """
        DESCRIPTION: Expand the markets which should display the Scorer Template
        EXPECTED: * Market Header should be displayed with signposting if available
        """
        pass
