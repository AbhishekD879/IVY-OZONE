import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66132265_Verify_no_background_iconography_at_the_selection_for_BYB_BB(Common):
    """
    TR_ID: C66132265
    NAME: Verify no background iconography at the selection for BYB/BB
    DESCRIPTION: This test case verify no background iconography at the selection for BYB/BB
    PRECONDITIONS: BYB/BB event should be available
    PRECONDITIONS: Bets should be available in  open/cashout(if available),settle  tabs for BYB/BB
    """
    keep_browser_open = True

    def test_000_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        pass

    def test_000_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        pass

    def test_000_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to football page
        EXPECTED: Football landing page  should opened
        """
        pass

    def test_000_navigate_to_any_event_which_has_byb_markets_gt_edp(self):
        """
        DESCRIPTION: Navigate to ANY event which has BYB markets &gt; EDP
        EXPECTED: User should be able to navigate to Football Event Details page
        """
        pass

    def test_000_click_on_build_your_bet_or_bet_builder(self):
        """
        DESCRIPTION: Click on Build Your Bet or Bet Builder
        EXPECTED: Bet Builder/Build Your Bet tab should be opened
        """
        pass

    def test_000_add_few_combinable_selections_to_build_your_bet_coral__bet_builder_ladbrokes_dashboard_from_different_markets_accordions(self):
        """
        DESCRIPTION: Add few combinable selections to Build Your Bet CORAL / Bet Builder LADBROKES Dashboard from different markets accordions
        EXPECTED: Selections are added to bet slip
        """
        pass

    def test_000_fill_some_value_in_the_stake_field_and_clicktap_place_bet_button(self):
        """
        DESCRIPTION: Fill some value in the 'Stake' field and click/tap 'Place bet' button
        EXPECTED: Bet receipt is displayed
        """
        pass

    def test_000_check_the_balance_is_updated(self):
        """
        DESCRIPTION: Check the balance is updated
        EXPECTED: User Balance is updated
        """
        pass

    def test_000_navigate_to_my_bets_gtopen(self):
        """
        DESCRIPTION: Navigate to My Bets-&gt;Open
        EXPECTED: Bets  should be available in open tab
        """
        pass

    def test_000_check_bbbyb__bet_available_in_open_tab(self):
        """
        DESCRIPTION: Check BB/BYB  bet available in open tab
        EXPECTED: BB/BYB  bet available in open tab
        """
        pass

    def test_000_check_the_background_image_display_for_selection_level(self):
        """
        DESCRIPTION: Check the background image display for selection level
        EXPECTED: No  background  iconography at selection level denoting BYB/BB Bet so that it is no longer visible
        """
        pass

    def test_000_go_to_settle_tab_and_check_after_the_above_bet_got_settled(self):
        """
        DESCRIPTION: Go to settle tab and check after the above bet got settled
        EXPECTED: BYB/BB settle bets should be available
        """
        pass

    def test_000_check_the_background_image_display_for_selection_level(self):
        """
        DESCRIPTION: Check the background image display for selection level
        EXPECTED: No  background  iconography at selection level denoting 5-A-Side Bet should be removed
        """
        pass
