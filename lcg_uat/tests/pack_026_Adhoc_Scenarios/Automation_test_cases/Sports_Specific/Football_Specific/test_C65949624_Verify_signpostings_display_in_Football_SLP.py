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
class Test_C65949624_Verify_signpostings_display_in_Football_SLP(Common):
    """
    TR_ID: C65949624
    NAME: Verify signposting's display in Football SLP
    DESCRIPTION: This Test case verifies  signposting's in Football SLP
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    """
    keep_browser_open = True

    def test_001_launch_application(self):
        """
        DESCRIPTION: Launch application
        EXPECTED: Application should be launched successfully
        """
        pass

    def test_002_navigate_to_football_sport(self):
        """
        DESCRIPTION: Navigate to Football sport
        EXPECTED: Matches tab will load by default with inplay widget
        """
        pass

    def test_003_verify_signpostings_in_football_slp(self):
        """
        DESCRIPTION: Verify signpostings in football SLP
        EXPECTED: All the signpostings should be displayed for all football events  SLP
        """
        pass

    def test_004_verify_signpostings_behavior(self):
        """
        DESCRIPTION: Verify Signpostings behavior
        EXPECTED: Desktop and mobile:
        EXPECTED: signpostings including Price boost, betinplay, cashout should be displayed and when clicked static information should be displayed
        """
        pass

    def test_005_verify_build_in_bet_signpostings(self):
        """
        DESCRIPTION: Verify build in bet signpostings
        EXPECTED: When clicked on BYB signposting user should be navigated to Football EDP page
        """
        pass

    def test_006_verify_price_boost_and_odds_booster_signposting(self):
        """
        DESCRIPTION: Verify Price boost and odds booster signposting
        EXPECTED: When clicked on Price boost signposting and odds boosting user should see a popup with information having more and OK buttons
        """
        pass
