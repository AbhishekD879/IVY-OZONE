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
class Test_C64663377_Verify_the_display_of_Show_More_and_Show_Less_Link(Common):
    """
    TR_ID: C64663377
    NAME: Verify the display of Show More and Show Less Link
    DESCRIPTION: This test case verifies the display of show more/show less for scorer markets
    PRECONDITIONS: 1.Market which fall under scorer format should follow this templet
    PRECONDITIONS: ![](index.php?/attachments/get/9482daf9-86ff-4d61-82e2-941594018516)
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
        EXPECTED: * Market Header should be displayed market templet available
        EXPECTED: * "PLAYERS" Label should be available
        EXPECTED: * List of Options (each with Player Name, Team Name & Price Button)
        """
        pass

    def test_004_vaidate__show_moreshow_less_link(self):
        """
        DESCRIPTION: vaidate * “SHOW MORE/“SHOW LESS…” Link
        EXPECTED: * “SHOW MORE/“SHOW LESS…” Link should be available [when selects  show more remaining price options should be revealed to the user and "SHOW MORE..." link should be replaced with a "SHOW LESS..." Link]
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/b9d99184-ebb9-4501-bf5c-5b5394c3c7d7)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/95e532e1-c42e-46cd-b5d1-1bef4d4b6166)
        """
        pass
