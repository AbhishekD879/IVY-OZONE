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
class Test_C11780007_Actual_from_OX_99_Verify_displaying_price_change_notification_where_user_has_entered_a_stake(Common):
    """
    TR_ID: C11780007
    NAME: **[Actual from OX 99]** Verify displaying price change notification where user has entered a stake
    DESCRIPTION: This test case verifies displaying price change notification where user has entered a stake
    PRECONDITIONS: Login into App
    PRECONDITIONS: Add selection to the Betslip
    PRECONDITIONS: Enter Stake into 'Stake' field
    """
    keep_browser_open = True

    def test_001_trigger_price_change_for_added_selection(self):
        """
        DESCRIPTION: Trigger price change for added selection
        EXPECTED: The selection price change is displayed via push with text:
        EXPECTED: 'Price change from x to y '
        """
        pass

    def test_002_verify_that_notification_box_is_displayed_at_the_bottom_of_the_betslip(self):
        """
        DESCRIPTION: Verify that notification box is displayed at the bottom of the betslip
        EXPECTED: Info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        """
        pass

    def test_003_for_ladbrokes_only_verify_that_notification_box_is_displayed_at_the_top_of_the_betslip_with_animations_and_is_removed_after_5_seconds(self):
        """
        DESCRIPTION: **FOR LADBROKES ONLY** Verify that notification box is displayed at the top of the betslip with animations and is removed after 5 seconds
        EXPECTED: **FOR LADBROKES ONLY** Info message is displayed at the top of the betslip with animations and is removed after 5 seconds
        EXPECTED: 'Some of the prices have changed'
        """
        pass

    def test_004_verify_that_place_bet_button_text_is_updated(self):
        """
        DESCRIPTION: Verify that 'Place bet' button text is updated
        EXPECTED: The Place bet button text is updated to:
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        EXPECTED: Ladbrokes: 'ACCEPT AND PLACE BET'
        """
        pass
