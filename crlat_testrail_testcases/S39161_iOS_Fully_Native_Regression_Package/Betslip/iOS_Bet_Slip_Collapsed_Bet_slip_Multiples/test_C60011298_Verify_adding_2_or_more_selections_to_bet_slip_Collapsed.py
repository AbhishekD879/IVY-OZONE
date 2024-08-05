import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C60011298_Verify_adding_2_or_more_selections_to_bet_slip_Collapsed(Common):
    """
    TR_ID: C60011298
    NAME: Verify adding 2 or more selections to bet slip (Collapsed)
    DESCRIPTION: Test cases verifies view of collapsed bet slip during adding 2 or more selections
    PRECONDITIONS: Light Theme is enabled on tested device (Setting -> Display & Brightness -> Select "Light" theme)
    PRECONDITIONS: App installed and opened
    PRECONDITIONS: Bet slip is empty
    PRECONDITIONS: *Designs*
    PRECONDITIONS: Ladbrokes - https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea98a80395ffa255f45d4db
    PRECONDITIONS: Coral - https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5eaa98a5c4cec8bf7b2aff32
    """
    keep_browser_open = True

    def test_001__add_2_selections_with_fractional_odds_to_bet_slip_verify_that_added_selections_in_collapsed_bet_slip_conforms_to_coralladbrokes_light_theme_designs(self):
        """
        DESCRIPTION: * Add 2 selections with fractional odds to bet slip
        DESCRIPTION: * Verify that added selections in collapsed bet slip conforms to Coral/Ladbrokes Light theme designs
        EXPECTED: * 2 selections were successfully added to bet slip
        EXPECTED: * bet slip in collapsed state
        EXPECTED: * bet slip displays with a notification icon that highlights number of selections added to bet slip
        EXPECTED: * bet slip displays the accumulative Odds for added selections including the bet type - E.G User adds 2 selections to bet slip and the accumulator price of those selections is 6.9 must display 'Double @ 7.0'
        EXPECTED: * added selections in collapsed bet slip conforms to Coral/Ladbrokes Light theme designs
        EXPECTED: Coral/Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/120925772) ![](index.php?/attachments/get/120925773)
        """
        pass

    def test_002__enable_dark_theme_on_devicesetting___display__brightness___select_light_theme(self):
        """
        DESCRIPTION: * Enable Dark theme on device
        DESCRIPTION: (Setting -> Display & Brightness -> Select "Light" theme)
        EXPECTED: * Dark theme was enabled on device
        """
        pass

    def test_003__verify_that_added_selections_in_collapsed_bet_slip_conforms_to_coralladbrokes_dark_theme_designs(self):
        """
        DESCRIPTION: * Verify that added selections in collapsed bet slip conforms to Coral/Ladbrokes Dark theme designs
        EXPECTED: * bet slip remains in collapsed state
        EXPECTED: * bet slip displays with a notification icon that highlights number of selections added to bet slip
        EXPECTED: * bet slip displays the accumulative Odds for added selections including the bet type ( E.G User adds 2 selections to bet slip and the accumulator price of those selections is 6.9 must display 'Double @ 7.0')
        EXPECTED: * added selections in collapsed bet slip conforms to Coral/Ladbrokes Dark theme designs
        EXPECTED: Coral/Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/120925774) ![](index.php?/attachments/get/120925775)
        """
        pass

    def test_004__repeat_1_3_steps_with_selections_that_have_decimal__odds(self):
        """
        DESCRIPTION: * Repeat 1-3 steps with selections that have decimal  odds
        EXPECTED: * Results from steps 1-3
        EXPECTED: * bet slip correctly  depicts decimal  odds for added selections in collapsed state
        """
        pass
