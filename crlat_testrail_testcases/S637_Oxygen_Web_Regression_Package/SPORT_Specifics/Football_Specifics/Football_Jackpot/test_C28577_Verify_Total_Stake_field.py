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
class Test_C28577_Verify_Total_Stake_field(Common):
    """
    TR_ID: C28577
    NAME: Verify 'Total Stake' field
    DESCRIPTION: This test case verifies 'Total Stake:' label and field
    DESCRIPTION: AUTOTEST [C9726421]
    PRECONDITIONS: 1) Make sure there is at least one active pool available to be displayed on front-end
    PRECONDITIONS: 2) The user may be logged in or logged out for the functionality to work
    """
    keep_browser_open = True

    def test_001_open_jackpot_tab(self):
        """
        DESCRIPTION: Open 'Jackpot' tab
        EXPECTED: Football Jackpot Page is opened
        """
        pass

    def test_002_go_tobet_placement_section(self):
        """
        DESCRIPTION: Go to  Bet Placement section
        EXPECTED: 'Total Stake:' label and field are displayed
        """
        pass

    def test_003_verify_default_value_which_is_shown_in_the_total_stake_field(self):
        """
        DESCRIPTION: Verify default value which is shown in the 'Total Stake' field
        EXPECTED: Default value '£0.00' is shown in the 'Total Stake' field (while no lines are chosen)
        """
        pass

    def test_004_select_one_or_more_lines(self):
        """
        DESCRIPTION: Select one or more lines
        EXPECTED: *   Selections that were made are highlighted
        EXPECTED: *   Number of lines is shown in the 'Total Lines' field
        EXPECTED: *   'Total Stake' = <total lines>*<stake per line > and is shown in format: **£YY.YY**
        """
        pass

    def test_005_verify_total_stake_field_view(self):
        """
        DESCRIPTION: Verify 'Total Stake' field view
        EXPECTED: 'Total Stake' field is able to handle at least 4 digits as standard – for more than 4 digits number can overflow field boundary on screen but must not truncate
        """
        pass

    def test_006_verify_total_stake_value_updating(self):
        """
        DESCRIPTION: Verify 'Total Stake' value updating
        EXPECTED: Shown value is automatically updated as the user updates the 'Total Lines' or 'Stake Per Line' values
        """
        pass
