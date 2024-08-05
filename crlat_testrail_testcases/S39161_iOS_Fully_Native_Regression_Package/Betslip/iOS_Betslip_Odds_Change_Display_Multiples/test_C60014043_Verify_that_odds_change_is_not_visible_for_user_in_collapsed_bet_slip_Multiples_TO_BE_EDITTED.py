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
class Test_C60014043_Verify_that_odds_change_is_not_visible_for_user_in_collapsed_bet_slip_Multiples_TO_BE_EDITTED(Common):
    """
    TR_ID: C60014043
    NAME: Verify that odds change is not visible for user in collapsed bet slip (Multiples) TO BE EDITTED
    DESCRIPTION: Test case verifies that odds change for added in bet slip selections(more then 2) is not visible to user in collapse bet slip
    PRECONDITIONS: App installed and launched
    PRECONDITIONS: Bet slip is empty
    PRECONDITIONS: Designs:
    PRECONDITIONS: Coral: https://zpl.io/beJxmol
    PRECONDITIONS: Ladbrokes: https://zpl.io/V4BXjeM
    """
    keep_browser_open = True

    def test_001__add_several_selections_to_bet_slip_more_then_2_eg_3_selections(self):
        """
        DESCRIPTION: * Add several selections to Bet slip (more then 2, e.g.: 3 selections)
        EXPECTED: * Selected selections were added to Bet slip(e.g.: 3 selections)
        EXPECTED: * Bet slip collapsed
        """
        pass

    def test_002__trigger_odds_changefyi_mock_data_will_be_used_to_trigger_odds_change__until_be_is_available(self):
        """
        DESCRIPTION: * Trigger Odds change
        DESCRIPTION: (FYI: Mock Data will be used to trigger Odds change  until BE is available)
        EXPECTED: Odds change was triggered
        EXPECTED: * Bet slip remains collapsed
        EXPECTED: * No action should be taken to inform user of odds change
        """
        pass
