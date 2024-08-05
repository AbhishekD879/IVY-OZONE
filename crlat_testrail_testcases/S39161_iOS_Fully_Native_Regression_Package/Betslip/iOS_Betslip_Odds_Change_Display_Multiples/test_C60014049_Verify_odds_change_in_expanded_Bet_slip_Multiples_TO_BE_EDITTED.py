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
class Test_C60014049_Verify_odds_change_in_expanded_Bet_slip_Multiples_TO_BE_EDITTED(Common):
    """
    TR_ID: C60014049
    NAME: Verify odds change in expanded Bet slip (Multiples) TO BE EDITTED
    DESCRIPTION: Test  case verifies Odds changes view when Bet slip expanded
    PRECONDITIONS: App installed and launched
    PRECONDITIONS: Bet slip contains 3 added selections
    PRECONDITIONS: Bet slip in collapsed sate
    PRECONDITIONS: Designs:
    PRECONDITIONS: Coral: https://zpl.io/beJxmol
    PRECONDITIONS: Ladbrokes: https://zpl.io/V4BXjeM
    """
    keep_browser_open = True

    def test_001__expand_bet_slip_with_added_selections(self):
        """
        DESCRIPTION: * Expand Bet slip with added selections
        EXPECTED: * Bet slip expanded
        EXPECTED: * Info about added selections correctly displays in Bet slip
        """
        pass

    def test_002_odds_on_one_of_the_selections_changesfyi_mock_data_will_be_used_to_trigger_odds_change_until_be_is_available(self):
        """
        DESCRIPTION: *Odds on one of the selections changes
        DESCRIPTION: (FYI: Mock Data will be used to trigger Odds change until BE is available)
        EXPECTED: * Bet slip remains collapsed
        EXPECTED: * Odds changes for one of selections
        EXPECTED: * Odds change must trigger update the colour of Odds shown according to UX guidelines
        """
        pass
