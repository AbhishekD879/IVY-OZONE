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
class Test_C64658649_Verify_Price_Boost_Template(Common):
    """
    TR_ID: C64658649
    NAME: Verify Price Boost Template
    DESCRIPTION: This test case verifies the price boost market templet
    PRECONDITIONS: In-&gt;Network tab -&gt;Verify the market templet sort code
    PRECONDITIONS: ex:
    PRECONDITIONS: ![](index.php?/attachments/get/bb53ce15-6044-499a-bac4-afbc9132f201)
    PRECONDITIONS: ![](index.php?/attachments/get/f1736e0e-f0a8-4a09-80c8-c36117ce126a)
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes__coral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes / Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_edpopen_the_network_tab_as_mentioned_in_pre_conditionsopen_the_first_market_in_the_network_tab_and_look_for_the_market_meaning_minor_code(self):
        """
        DESCRIPTION: Navigate to Football EDP
        DESCRIPTION: Open the network tab as mentioned in pre-conditions
        DESCRIPTION: Open the first market in the network tab and look for the market meaning minor code
        EXPECTED: User should be able to navigate to EDP page
        EXPECTED: User should be able to see the network call
        EXPECTED: Market Meaning Minor code should be displayed
        """
        pass

    def test_003_validate_the_market_template_based_on_the_market_meaning_minor_code_sort_code(self):
        """
        DESCRIPTION: Validate the Market template based on the Market Meaning Minor Code (Sort Code)
        EXPECTED: * Sort code should be based on market templet
        """
        pass

    def test_004_verify_market_templates_based_on_selections_for_price_boost(self):
        """
        DESCRIPTION: Verify Market Templates based on Selections for price boost
        EXPECTED: Price Boost fallows List Template hence
        EXPECTED: Any of the Below sort code should be present
        EXPECTED: ![](index.php?/attachments/get/79bd8df8-be10-4e61-9bf7-a6dc53c64c52)
        """
        pass
