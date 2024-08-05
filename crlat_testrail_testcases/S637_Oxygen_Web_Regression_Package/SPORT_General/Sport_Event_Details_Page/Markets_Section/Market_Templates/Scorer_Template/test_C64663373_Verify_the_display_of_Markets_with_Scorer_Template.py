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
class Test_C64663373_Verify_the_display_of_Markets_with_Scorer_Template(Common):
    """
    TR_ID: C64663373
    NAME: Verify the display of Markets with Scorer Template
    DESCRIPTION: This test case verifies market with scorer templet
    PRECONDITIONS: 1.Market which fall under scorer format should follow this templet
    PRECONDITIONS: ![](index.php?/attachments/get/a8d12134-ec2b-4f7d-80a4-7bd26eb18f33)
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: * User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_any_sports__edp_page(self):
        """
        DESCRIPTION: Navigate to any sports  EDP page
        EXPECTED: * EDP page should be displayed
        """
        pass

    def test_003_expand_the_markets_which_should_display_the_scorer_template(self):
        """
        DESCRIPTION: Expand the markets which should display the Scorer Template
        EXPECTED: * Market Header should be displayed with standard list templet available
        EXPECTED: * "PLAYERS" Label
        EXPECTED: * List of Options (each with Player Name, Team Name & Price Button)
        EXPECTED: * “SHOW MORE/“SHOW LESS…” Link should be available
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/b4a86a29-ab90-4144-bf98-bb6602a98aff)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/f880f12f-3a15-4325-b36d-589dab339b25)
        """
        pass
