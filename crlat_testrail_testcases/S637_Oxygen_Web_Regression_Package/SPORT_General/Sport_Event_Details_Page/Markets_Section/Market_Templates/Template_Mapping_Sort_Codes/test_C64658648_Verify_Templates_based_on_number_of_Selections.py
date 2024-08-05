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
class Test_C64658648_Verify_Templates_based_on_number_of_Selections(Common):
    """
    TR_ID: C64658648
    NAME: Verify Templates based on number of Selections
    DESCRIPTION: This test cases verifies the market templates based on the number of selections
    PRECONDITIONS: In-&gt;network tab
    PRECONDITIONS: ![](index.php?/attachments/get/e13ae9f8-48e2-44db-8118-585f742caef1)
    PRECONDITIONS: ![](index.php?/attachments/get/bd3b3daa-f425-4ea7-a181-80f7ba93f902)
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
        EXPECTED: Sort codes should be displayed as per below markets
        EXPECTED: ![](index.php?/attachments/get/be82994b-7d11-4e26-96f9-1c92180b4f75)
        """
        pass

    def test_004_verify_market_templates_based_on_selections(self):
        """
        DESCRIPTION: Verify Market Templates based on Selections
        EXPECTED: Templates should be as per below
        EXPECTED: =================================
        EXPECTED: No. of Selections	Template
        EXPECTED: 1	List
        EXPECTED: 2	WW
        EXPECTED: 3	WDW
        EXPECTED: 4 or more	List
        EXPECTED: Price Boost	List (regardless of number of selections)
        EXPECTED: Your Call (Get a Price)	List (regardless of number of selections)
        """
        pass
