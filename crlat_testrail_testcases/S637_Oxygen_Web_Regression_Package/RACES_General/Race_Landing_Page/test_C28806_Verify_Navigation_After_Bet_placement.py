import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28806_Verify_Navigation_After_Bet_placement(Common):
    """
    TR_ID: C28806
    NAME: Verify Navigation After Bet placement
    DESCRIPTION: This test case verifies navigation after bet placement when user selects outcome from Race landing page.
    DESCRIPTION: Jira tickets: BMA-5233,BMA-11096
    PRECONDITIONS: User should be logged in to place a bet.
    PRECONDITIONS: User can place a bet from 'Next 4 Races' module only.
    """
    keep_browser_open = True

    def test_001_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: *   <Race> landing page is opened
        """
        pass

    def test_002_add_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        EXPECTED: *   Bet Slip page is open
        EXPECTED: *   Selection is present
        """
        pass

    def test_003_enter_stake_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and tap 'Bet Now' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Bet Receipt is present
        """
        pass

    def test_004_tap_done_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Tap 'Done' button on Bet Receipt page
        EXPECTED: *   Bet Receipt is not shown anymore and Bet Slip Slider closes
        EXPECTED: *   User stays on <Race> landing page
        """
        pass

    def test_005_for_greyhounds_chose_by_time_sorting_type(self):
        """
        DESCRIPTION: For GreyHounds chose 'By Time' sorting type
        EXPECTED: 'By Time' sorting type is chosen
        """
        pass

    def test_006_repeat_steps_2_4(self):
        """
        DESCRIPTION: Repeat steps 2-4
        EXPECTED: *   Bet Receipt is not shown anymore and Bet Slip Slider closes
        EXPECTED: *   User stays on same page
        EXPECTED: *   'By Time' sorting type is selected
        """
        pass
