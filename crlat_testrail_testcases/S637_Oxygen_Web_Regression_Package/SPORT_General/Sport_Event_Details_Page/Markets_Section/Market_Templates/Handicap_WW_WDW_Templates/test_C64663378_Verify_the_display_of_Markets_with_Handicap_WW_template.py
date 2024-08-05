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
class Test_C64663378_Verify_the_display_of_Markets_with_Handicap_WW_template(Common):
    """
    TR_ID: C64663378
    NAME: Verify the display of Markets with Handicap WW template
    DESCRIPTION: This Test case verifies the display of Handicap WW template
    PRECONDITIONS: 1: Handicap Market should be available
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_edp_page(self):
        """
        DESCRIPTION: Navigate to EDP page
        EXPECTED: EDP page should be displayed
        """
        pass

    def test_003_expand_any_handicap_2_way_market_and_verify_the_limits_of_handicap_values(self):
        """
        DESCRIPTION: Expand any Handicap 2-Way Market and Verify the Limits of handicap values
        EXPECTED: * Market Header should be displayed along with signposting if available
        EXPECTED: * Option 1 Label (Team Name) should be displayed
        EXPECTED: * Option 2 Label (Team Name) should be displayed
        EXPECTED: * Handicap Value for Option 1 should be displayed within the price button (as per Zeplin CSS styles) up to "-100"
        EXPECTED: * Handicap Value for Option 2 should be displayed within the price button (as per Zeplin CSS styles) up to "+100"
        EXPECTED: ![](index.php?/attachments/get/0f641eb2-e831-4231-a35d-56b73f65e995)
        """
        pass

    def test_004_open_ti_and_change_the_handicap_valuevalidate_the_change_in_fe(self):
        """
        DESCRIPTION: Open TI and change the handicap value
        DESCRIPTION: Validate the change in FE
        EXPECTED: * Handicap Value within the price button should be updated
        """
        pass

    def test_005_repeat_the_above_steps_for_all_tier_1_and_tier_2_sports_where_handicap_markets_are_applicable(self):
        """
        DESCRIPTION: Repeat the above steps for all Tier 1 and Tier 2 sports where Handicap markets are applicable
        EXPECTED: 
        """
        pass
