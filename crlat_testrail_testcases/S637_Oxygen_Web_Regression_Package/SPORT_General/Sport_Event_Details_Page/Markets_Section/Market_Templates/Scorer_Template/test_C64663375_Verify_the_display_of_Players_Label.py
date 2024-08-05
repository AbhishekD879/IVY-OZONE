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
class Test_C64663375_Verify_the_display_of_Players_Label(Common):
    """
    TR_ID: C64663375
    NAME: Verify the display of 'Players' Label
    DESCRIPTION: This test case verifies the display of players lable for scorer markets
    PRECONDITIONS: 1.Market which fall under scorer format should follow this templet
    PRECONDITIONS: ![](index.php?/attachments/get/d52855fc-ef03-4c98-9abc-b69f8db3d311)
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
        EXPECTED: * Market Header should be displayed for the scorer market
        """
        pass

    def test_004_validate_the_players_label_for_scorer_market(self):
        """
        DESCRIPTION: Validate the "PLAYERS" Label for scorer market
        EXPECTED: Player lable should be displayed for scorer market
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/ce635d22-702c-4e53-b729-648d6a4fa91b)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/2b422dae-6917-41c2-a441-5481f29262dc)
        """
        pass
