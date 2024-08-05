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
class Test_C64658653_Verify_Sort_Code_for_all_List_Templates(Common):
    """
    TR_ID: C64658653
    NAME: Verify Sort Code for all List Templates
    DESCRIPTION: Verify Sort Code for all List Templates
    PRECONDITIONS: Verify Sort Code in Net Work tab
    PRECONDITIONS: ![](index.php?/attachments/get/651db18b-d755-48d0-aedd-e7da70b3d8fb)
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
        EXPECTED: Any of the Below Sort codes should be present for List Market
        EXPECTED: ![](index.php?/attachments/get/8e06c8f1-40b5-4f9c-9188-57722de3ba1a)
        """
        pass
