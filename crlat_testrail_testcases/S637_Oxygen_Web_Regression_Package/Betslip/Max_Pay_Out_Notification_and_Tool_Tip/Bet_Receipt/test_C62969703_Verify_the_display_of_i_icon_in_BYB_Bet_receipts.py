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
class Test_C62969703_Verify_the_display_of_i_icon_in_BYB_Bet_receipts(Common):
    """
    TR_ID: C62969703
    NAME: Verify the display of 'i' icon in BYB Bet receipts
    DESCRIPTION: This test  Case verifies the display of 'i' icon on BYB or Bet Builder Bet Receipt
    PRECONDITIONS: 1: Maximum Payout should be configured in Open bet
    PRECONDITIONS: 2: Potential/Estimated returns should be greater than Maximum Payout configured in OB
    PRECONDITIONS: 3: Max Pay Out banner should be enabled in CMS
    PRECONDITIONS: Max Payout is already returned to us by OpenBet via the max_payout value as part of the reqBetBuild request.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_sport_landing_page_and_click_on_any_event_which_byb_or_bet_builder_markets_available(self):
        """
        DESCRIPTION: Navigate to Football Sport Landing Page and Click on any event which BYB or Bet Builder markets available
        EXPECTED: 
        """
        pass

    def test_003_add_selections_from_byb_or_bet_builder_markets___enter_stakeentered_stake_should_trigger_the_estimated_potential_returns_higher_than_maximum_payout_configured(self):
        """
        DESCRIPTION: Add Selections from BYB or Bet Builder Markets - Enter Stake
        DESCRIPTION: (Entered Stake should trigger the estimated /potential returns higher than Maximum Payout configured)
        EXPECTED: * Max Pay out banner should be displayed
        EXPECTED: * Text displayed should be same as configured in CMS
        EXPECTED: * T&C'S link should be displayed
        EXPECTED: * 'i' icon should be displayed
        """
        pass

    def test_004_click_on_place_bet(self):
        """
        DESCRIPTION: Click on Place Bet
        EXPECTED: * User should be able to Place bet successfully
        EXPECTED: * Bet receipt should be generated
        EXPECTED: * 'i' icon should be displayed after Estimated/Potential Returns text
        """
        pass
