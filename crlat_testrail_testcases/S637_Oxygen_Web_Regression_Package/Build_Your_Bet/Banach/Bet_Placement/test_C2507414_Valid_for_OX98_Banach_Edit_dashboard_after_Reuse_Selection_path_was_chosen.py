import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C2507414_Valid_for_OX98_Banach_Edit_dashboard_after_Reuse_Selection_path_was_chosen(Common):
    """
    TR_ID: C2507414
    NAME: [Valid for OX98] Banach. Edit dashboard after Reuse Selection path was chosen
    DESCRIPTION: Test case verifies Banach selection dashboard display and possibility to edit it after Reuse Selection option was used
    DESCRIPTION: NOTE: 'Reuse selection' button seems to be removed in OX100 redesign
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check odds: open Dev tools > Network > **price** request
    PRECONDITIONS: **User has placed Banach bet and sees Bet receipt on UI**
    """
    keep_browser_open = True

    def test_001_tap_reuse_selection_button(self):
        """
        DESCRIPTION: Tap "Reuse selection" button
        EXPECTED: - Selections dashboard is displayed in collapsed state
        EXPECTED: - Odds area contains value from **price** request
        """
        pass

    def test_002_expand_the_dashboard(self):
        """
        DESCRIPTION: Expand the dashboard
        EXPECTED: The dashboard has initial selections
        """
        pass

    def test_003_add_1_more_selection_to_dashboard(self):
        """
        DESCRIPTION: Add 1 more selection to dashboard
        EXPECTED: - Selection is added to dashboard
        EXPECTED: - Odds are updated (with value from **price** request)
        """
        pass
