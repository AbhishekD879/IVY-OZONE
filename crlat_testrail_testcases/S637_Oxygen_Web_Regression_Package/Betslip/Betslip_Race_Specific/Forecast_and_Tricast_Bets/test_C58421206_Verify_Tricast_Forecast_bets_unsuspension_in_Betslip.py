import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C58421206_Verify_Tricast_Forecast_bets_unsuspension_in_Betslip(Common):
    """
    TR_ID: C58421206
    NAME: Verify Tricast/Forecast bets unsuspension in Betslip
    DESCRIPTION: This test case verifies unsuspension notifications for Tricast/Forecast bets in Betslip.
    PRECONDITIONS: The related OCC ticket: https://jira.egalacoral.com/browse/BMA-51664
    PRECONDITIONS: Defect video from the OCC ticket available here: https://jira.egalacoral.com/secure/attachment/1380838/RPReplay-Final1583227399.MP4
    PRECONDITIONS: - Tricast/Forecast ckeck boxes are selected on Market level for the event in OB TI.
    PRECONDITIONS: - User is on HR EDP with Tricast/Forecast markets available.
    PRECONDITIONS: For manipulations with bet statuses use OB TI system according to brand needed:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True

    def test_001_add_2_different_forecast_bets_to_betslip_eg_1st2nd_runner_anyany_runners_bets(self):
        """
        DESCRIPTION: Add 2 different Forecast bets to betslip (eg. 1st/2nd runner, Any/Any runners bets)
        EXPECTED: Bets are added to Betslip
        """
        pass

    def test_002_open_betslip_and_meanwhile_suspend_the_entire_event_in_ti_backoffice_event_level(self):
        """
        DESCRIPTION: Open Betslip and meanwhile suspend the entire event in TI backoffice (event level)
        EXPECTED: - Bets become suspended immediately (greyed out with 'suspended' labels across the bets)
        EXPECTED: - Notification on blue background about suspension appears at the top of Betslip
        EXPECTED: ![](index.php?/attachments/get/101694100)
        """
        pass

    def test_003_refresh_the_pagekill_the_app_and_load_again(self):
        """
        DESCRIPTION: Refresh the page/kill the app and load again
        EXPECTED: Page is refreshed/App is up
        """
        pass

    def test_004_open_betslip_and_meanwhile_unsuspend_the_event_in_ti(self):
        """
        DESCRIPTION: Open Betslip and meanwhile unsuspend the event in TI
        EXPECTED: - Bets become active
        EXPECTED: - None of notifications about suspension are displayed to the user
        EXPECTED: ![](index.php?/attachments/get/101694099)
        """
        pass

    def test_005_repeat_steps_above_for_the_forecast_bets_and_suspension_on_market_level(self):
        """
        DESCRIPTION: Repeat steps above for the Forecast bets and suspension on Market level
        EXPECTED: Results are the same
        """
        pass

    def test_006_repeat_steps_above_for_the_tricast_bet(self):
        """
        DESCRIPTION: Repeat steps above for the Tricast bet.
        EXPECTED: Results are the same
        """
        pass
