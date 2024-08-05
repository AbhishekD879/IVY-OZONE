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
class Test_C64663379_Verify_the_display_of_Markets_with_Handicap_WDW_template(Common):
    """
    TR_ID: C64663379
    NAME: Verify the display of Markets with Handicap WDW template
    DESCRIPTION: This test case verifies the display of Handicap WDW template
    PRECONDITIONS: 1: Handicap 3 Way Market should be available for the event
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_edp(self):
        """
        DESCRIPTION: Navigate to EDP
        EXPECTED: 
        """
        pass

    def test_003_expand_any_handicap_3_way_market(self):
        """
        DESCRIPTION: Expand any Handicap 3 Way Market
        EXPECTED: * Market Header should be displayed along with signposting if available
        EXPECTED: * Option 1 Label (Team Name) should be displayed
        EXPECTED: * Option 2 Label (Team Name) should be displayed
        EXPECTED: * Option 3 Label (Draw) should be displayed
        EXPECTED: * Handicap Value for Option 1 should be displayed within price button
        EXPECTED: * Handicap Value for Option 3 should be displayed within price button
        """
        pass

    def test_004_open_ti_and_change_the_handicap_valuevalidate_the_change_in_fe(self):
        """
        DESCRIPTION: Open TI and change the Handicap Value
        DESCRIPTION: Validate the change in FE
        EXPECTED: * Handicap values should be updated within the price button
        """
        pass

    def test_005_repeat_above_for_all_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Repeat above for all Tier 1 and Tier 2 sports
        EXPECTED: 
        """
        pass
