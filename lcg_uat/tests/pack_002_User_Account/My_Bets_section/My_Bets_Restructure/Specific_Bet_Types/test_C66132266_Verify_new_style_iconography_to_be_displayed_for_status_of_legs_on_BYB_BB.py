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
class Test_C66132266_Verify_new_style_iconography_to_be_displayed_for_status_of_legs_on_BYB_BB(Common):
    """
    TR_ID: C66132266
    NAME: Verify new style iconography to be displayed  for status of legs on BYB/BB
    DESCRIPTION: This test case Verify new style iconography to be displayed  for status of legs on BYB/BB
    DESCRIPTION: This test case Verify new style iconography to be displayed  for status of legs on BYB/BB
    PRECONDITIONS: BYB/BB event should be available
    PRECONDITIONS: Bets should be available in  open/cashout(if available),settle  tabs for BYB/BB
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

    def test_000_check_bybbb__bet_available_in_open_tab(self):
        """
        DESCRIPTION: Check BYB/BB  bet available in open tab
        EXPECTED: 5-A-Side bet available in open tab
        """
        pass

    def test_000_check_the_legs__for_the_event_which__goes_to_in_play(self):
        """
        DESCRIPTION: Check the legs  for the event which  goes to in play
        EXPECTED: Status legs should be with new  iconography style it should be as per figma
        """
        pass

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

    def test_000_check_5_a_side_bet_available_in_open_tab(self):
        """
        DESCRIPTION: Check 5-A-Side bet available in open tab
        EXPECTED: 5-A-Side bet available in open tab
        """
        pass

    def test_000_check_bybbb_bets_after_its_got_settle_in_settle_tab(self):
        """
        DESCRIPTION: Check BYB/BB bets after its got settle in settle tab
        EXPECTED: BYB/BB settle bets should be displayed with signposting (for winning / losing)
        """
        pass
