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
class Test_C64658650_Verify_Your_Call_Template(Common):
    """
    TR_ID: C64658650
    NAME: Verify Your Call Template
    DESCRIPTION: Verify Your Call Template
    PRECONDITIONS: Verify Sort Code in Net Work tab
    PRECONDITIONS: ![](index.php?/attachments/get/32a75bbe-2bf6-4f52-8a50-dc2e30fd649a)
    PRECONDITIONS: ![](index.php?/attachments/get/b58da730-3a0a-4cc2-ae37-59de20582f30)![](index.php?/attachments/get/6d0e8734-b2dc-464d-a1ae-102890baccff)
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
        EXPECTED: Your call(Get a Price) is List (regardless of number of selections)
        EXPECTED: Any of the below can be present for List template
        EXPECTED: ![](index.php?/attachments/get/9b3a3701-bf15-4080-9de6-e3ead6877cb7)
        """
        pass
