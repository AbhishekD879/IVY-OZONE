import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C64569604_Verify_that_Market_Type_Market_Description_Popular_Market_checkbox_is_displayed_in_BYB_Markets_Page(Common):
    """
    TR_ID: C64569604
    NAME: Verify that Market Type, Market Description, Popular Market checkbox is displayed in BYB Markets Page
    DESCRIPTION: 
    PRECONDITIONS: 1: User should have access to CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin User
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_navigate_to_byb_gt_byb_markets(self):
        """
        DESCRIPTION: Navigate to BYB &gt; BYB Markets
        EXPECTED: Verify that User is able to view Create BuildYourMarket button
        EXPECTED: Table Headers
        EXPECTED: 1: Market Title
        EXPECTED: 2: Market Group Name
        EXPECTED: 3: Market Grouping
        EXPECTED: 4: Incident Grouping
        EXPECTED: 5: Market Type
        EXPECTED: 6: Popular Market
        EXPECTED: 7: Market Description
        EXPECTED: 8: Remove
        EXPECTED: 9: Edit
        """
        pass

    def test_003_navigate_to_any_of_the_market_created_and_check_the_market_type_market_description_popular_market_checkbox_is_displayed(self):
        """
        DESCRIPTION: Navigate to any of the market created and check the Market Type, Market Description, Popular Market checkbox is displayed
        EXPECTED: Market Type, Market Description, Popular Market checkbox is displayed
        """
        pass

    def test_004_validate_that_user_is_able_to_see__market_description(self):
        """
        DESCRIPTION: Validate that User is able to see  Market Description
        EXPECTED: * User should be able to enter Market description
        """
        pass

    def test_005_validate_market_type_dropdown_field(self):
        """
        DESCRIPTION: Validate Market Type Dropdown field
        EXPECTED: * User should be able to view the below options N/A, Player Bet, Team Bet
        EXPECTED: * Dropdown should be a single select and NOT multi select
        """
        pass

    def test_006_validate_the_popular_markets_checkbox(self):
        """
        DESCRIPTION: Validate the Popular Markets Checkbox
        EXPECTED: * User should be able to enable/disable the Popular Market check box
        """
        pass
