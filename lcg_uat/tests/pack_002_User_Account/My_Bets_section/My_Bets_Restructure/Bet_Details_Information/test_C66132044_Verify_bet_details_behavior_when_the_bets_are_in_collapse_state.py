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
class Test_C66132044_Verify_bet_details_behavior_when_the_bets_are_in_collapse_state(Common):
    """
    TR_ID: C66132044
    NAME: Verify bet details behavior when the bets are in collapse state
    DESCRIPTION: This test case Verify bet details behavior when the bets are in collapse state
    PRECONDITIONS: Bets should be available in open/cashout and settle tab
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

    def test_000_place_singlemutiple_bets__from_sportsraces(self):
        """
        DESCRIPTION: Place single/Mutiple bets  from Sports/Races
        EXPECTED: Bets should be placed successfully
        """
        pass

    def test_000_tap_on_my_bets(self):
        """
        DESCRIPTION: Tap on 'My bets'
        EXPECTED: My bets page/Bet slip widget is opened
        """
        pass

    def test_000_click_on_open_tab(self):
        """
        DESCRIPTION: Click on Open tab
        EXPECTED: Open'  tab is selected by default
        EXPECTED: Placed bet is displayed
        """
        pass

    def test_000_check_new_section_with_bet_detail_area_available_with__chevron(self):
        """
        DESCRIPTION: Check new section with bet detail area available with  Chevron
        EXPECTED: Bet detail area is available with expand and collapse
        EXPECTED: **Ladbrokes**
        EXPECTED: ![](index.php?/attachments/get/a888fe62-d8cf-4dd3-a1f1-9ac91432ad7c)
        EXPECTED: **Coral**
        EXPECTED: ![](index.php?/attachments/get/aa1e247d-08e8-42cb-a3cd-54bfb9c42e12)
        """
        pass

    def test_000_collapse_the_bet_type_bet_type_and_check_the_bet_details_behavior(self):
        """
        DESCRIPTION: Collapse the bet type bet type and check the bet details behavior
        EXPECTED: Bet details should not show when the bet is collapsed
        EXPECTED: **Ladbrokes**
        EXPECTED: ![](index.php?/attachments/get/77d5e6c9-753b-4abf-9ad1-f60c1b90dfbb)
        EXPECTED: **Coral**
        EXPECTED: ![](index.php?/attachments/get/4619dcb5-ca66-4c39-955c-fb0c258f0881)
        """
        pass

    def test_000_repeat_the_above_steps_for_cashout_and_settle(self):
        """
        DESCRIPTION: Repeat the above steps for cashout and settle
        EXPECTED: 
        """
        pass
