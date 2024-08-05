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
class Test_C13081436_Verify_the_user_is_able_to_delete_stakes_from_the_betslip_for_mobile(Common):
    """
    TR_ID: C13081436
    NAME: Verify the user is able to delete stakes from the betslip for mobile
    DESCRIPTION: This test case verifies that the user is able to delete stakes from the betslip for mobile (iPhone and android phones)
    DESCRIPTION: Cannot automate it on real devices
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_add_4_or_more_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add 4 or more selections to the Betslip
        EXPECTED: Selections are added
        """
        pass

    def test_002_add_stake_for_any_accumulator_or_other_fields(self):
        """
        DESCRIPTION: Add stake for any accumulator or other fields
        EXPECTED: Stake is added
        """
        pass

    def test_003_tap_on_selected_stake_field(self):
        """
        DESCRIPTION: Tap on selected stake field
        EXPECTED: 00 should be added after the '.' (dot) e.g.: '2.00'
        """
        pass

    def test_004_wait_about_2_3_min_do_not_lock_the_device(self):
        """
        DESCRIPTION: Wait about 2-3 min (do not lock the device)
        EXPECTED: Stakes are displayed well
        """
        pass

    def test_005_delete_stake_from_field(self):
        """
        DESCRIPTION: Delete stake from field
        EXPECTED: Stake is deleted
        """
        pass
