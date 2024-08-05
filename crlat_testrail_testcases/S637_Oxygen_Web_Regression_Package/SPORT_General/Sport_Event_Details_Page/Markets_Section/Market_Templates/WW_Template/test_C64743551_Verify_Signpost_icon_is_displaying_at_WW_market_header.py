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
class Test_C64743551_Verify_Signpost_icon_is_displaying_at_WW_market_header(Common):
    """
    TR_ID: C64743551
    NAME: Verify Signpost icon is displaying  at WW market header
    DESCRIPTION: Verify Signpost icon is displaying of WW market template
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes__coral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes / Coral application
        EXPECTED: Launch Ladbrokes / Coral application
        """
        pass

    def test_002_navigate_to_football_edp(self):
        """
        DESCRIPTION: Navigate to Football EDP
        EXPECTED: User should be able to navigate to EDP page
        """
        pass

    def test_003_configure_few_signposts_to_particular_market_and_verify_those_are_displaying_in_frontend(self):
        """
        DESCRIPTION: Configure few Signposts to Particular market and verify those are displaying in Frontend
        EXPECTED: Signpost icons should be displayed at Market header
        """
        pass

    def test_004_validate_the_market_header_and_the_optionslabelsprice_button(self):
        """
        DESCRIPTION: Validate the Market Header and the options(Labels,Price Button)
        EXPECTED: Market for ww should be as below in Both Brands
        EXPECTED: 1.Option 1 Label and Option 1 Price Button
        EXPECTED: 2.Option 2 Label and Option 2 Price Button
        EXPECTED: ![](index.php?/attachments/get/da07b647-7df7-4a9c-bdec-a7ff8cdd2854)
        EXPECTED: ![](index.php?/attachments/get/4ae29293-e2f1-498e-9b70-3d207eb7e523)
        """
        pass

    def test_005_add_one_selection_to_betslip_or_quickbet_from_ww_market(self):
        """
        DESCRIPTION: Add one selection to Betslip or Quickbet from WW market
        EXPECTED: 1.Selection should be added to Bet slip/Quickbet Slip
        EXPECTED: 2.Signpost Icon/Text should be displayed like below
        EXPECTED: ![](index.php?/attachments/get/a5661b75-f701-4d89-a15d-71e407500470)
        """
        pass

    def test_006_now_pplace_bet(self):
        """
        DESCRIPTION: Now PPLACE BET
        EXPECTED: Bet Should be placed successfully along with Signposts icons/text
        """
        pass
