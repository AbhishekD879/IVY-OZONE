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
class Test_C59985468_Verify_multiple_bet_option_in_expanded_Betslip(Common):
    """
    TR_ID: C59985468
    NAME: Verify multiple bet option in expanded Betslip
    DESCRIPTION: This test case verifies multiple bet options in expanded Betslip.
    PRECONDITIONS: * Application is installed and launched
    PRECONDITIONS: Designs:
    PRECONDITIONS: Coral https://app.zeplin.io/project/5dc1abe9fefe5d837a9b93cd/screen/5dc2ae6281baec82fe5bc953
    PRECONDITIONS: Ladbrokes https://app.zeplin.io/project/5dc1abb838e1dd72b89d1a21/screen/5ea989452d8bd3bda177b7c0
    """
    keep_browser_open = True

    def test_001_add_two_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add two selections from different events to the Betslip.
        EXPECTED: * Selections are added.
        """
        pass

    def test_002_expand_the_betslip(self):
        """
        DESCRIPTION: Expand the betslip
        EXPECTED: * Betslip is expanded.
        EXPECTED: * "Edit" and "Remove all" buttons are available at the right top of the Betslip.
        EXPECTED: * Selection Name is shown.
        EXPECTED: * Market Name is shown.
        EXPECTED: * Event Name is shown.
        EXPECTED: * "Est. Returns" is shown.
        """
        pass

    def test_003_observe_the_multiples_section(self):
        """
        DESCRIPTION: Observe the multiples section
        EXPECTED: * Multiples section is shown.
        EXPECTED: * Bet type name is shown (E.G Doubles).
        EXPECTED: * Odd (Fractional or Decimal depending on user preference)is shown.
        EXPECTED: * "Est. Returns" is shown.
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/120264499)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/120264500)
        """
        pass

    def test_004_tap_on_stake_box(self):
        """
        DESCRIPTION: Tap on "Stake" box.
        EXPECTED: * Stake box is clickable.
        """
        pass
