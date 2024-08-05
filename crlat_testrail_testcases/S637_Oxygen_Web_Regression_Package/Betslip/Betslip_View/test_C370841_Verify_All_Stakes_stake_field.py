import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C370841_Verify_All_Stakes_stake_field(Common):
    """
    TR_ID: C370841
    NAME: Verify 'All Stakes' stake field
    DESCRIPTION: This test case verifies 'All Stakes' stake field in the betslip for Coral brand
    PRECONDITIONS: Note: 'All Stakes' functionality is the same for mobile/tablet/desktop views
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_add_one_selection_to_the_betslip_from_any_area_of_the_application___openobserve_betslip(self):
        """
        DESCRIPTION: Add ONE selection to the betslip from any area of the application -> Open/observe betslip
        EXPECTED: 1. Selection is added
        EXPECTED: 2. 'All Stakes' field is NOT present in the betslip
        """
        pass

    def test_003_add__more_selections_to_the_betslip___openobserve_betslip(self):
        """
        DESCRIPTION: Add  more selections to the betslip -> Open/observe betslip
        EXPECTED: 1. Selections are added
        EXPECTED: 2. 'All Stake' field is shown above all singles within 'Singles' section
        """
        pass

    def test_004_enter_stake_into_all_stakes_field(self):
        """
        DESCRIPTION: Enter stake into 'All Stakes' field
        EXPECTED: 1. Entered value is shown in 'All Stakes' field
        EXPECTED: 2. All singles stake boxes are auto-populated with value from 'All Stakes' field
        EXPECTED: 3. Multiples stake boxes are not affected if available
        """
        pass

    def test_005_go_to_separate_single_stake_box___edit_stake_value(self):
        """
        DESCRIPTION: Go to separate single stake box -> Edit stake value
        EXPECTED: 1. Stake value is changed for selected single selection
        EXPECTED: 2. 'All Stakes' field is not changed
        EXPECTED: 3. Stakes for other bets in the betslip are not changed
        """
        pass

    def test_006_enter_new_stake_value_into_all_stakes_field(self):
        """
        DESCRIPTION: Enter new stake value into 'All Stakes' field
        EXPECTED: 1. Entered value is shown in 'All Stakes' field
        EXPECTED: 2. All singles stake boxes are auto-populated with new value from 'All Stakes' field
        EXPECTED: 3. Every manipulation with 'All Stakes' field overrides all singles stake boxes with selected value
        """
        pass

    def test_007_delete_stake_value_from_all_stakes_field(self):
        """
        DESCRIPTION: Delete stake value from 'All Stakes' field
        EXPECTED: 1. Stake value is removed from 'All Stakes' field
        EXPECTED: 2. All singles stake boxes are cleared respectively
        EXPECTED: 3. Multiples stake boxes are not affected if available
        """
        pass

    def test_008_enter_stake_value_into_all_stakes_field_when_at_least_one_single_is_suspended(self):
        """
        DESCRIPTION: Enter stake value into 'All Stakes' field when at least one single is suspended
        EXPECTED: 1. Entered value is shown in 'All Stakes' field
        EXPECTED: 2. All active singles stake boxes are auto-populated with new value from 'All Stakes' field
        EXPECTED: 3. All suspended singles stake boxes are not affected by the change
        EXPECTED: 3. Multiples stake boxes are not affected if available
        """
        pass

    def test_009_unsuspend_previously_suspended_selection(self):
        """
        DESCRIPTION: Unsuspend previously suspended selection
        EXPECTED: 1. Selection is unsuspended
        EXPECTED: 2. Selection's stake box contains the same value as before suspension
        """
        pass
