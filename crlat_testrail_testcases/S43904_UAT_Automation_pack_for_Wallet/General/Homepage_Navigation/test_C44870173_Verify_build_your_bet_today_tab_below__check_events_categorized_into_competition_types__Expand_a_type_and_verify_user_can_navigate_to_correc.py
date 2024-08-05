import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870173_Verify_build_your_bet_today_tab_below__check_events_categorized_into_competition_types__Expand_a_type_and_verify_user_can_navigate_to_correct_EDP__Not_Applicable_for_Roxanne(Common):
    """
    TR_ID: C44870173
    NAME: "Verify  'build your bet' today tab below, - check events categorized into competition types. - Expand a type and verify user can navigate to correct EDP " .. Not Applicable for Roxanne
    DESCRIPTION: "Verify  'build your bet' today tab below,
    DESCRIPTION: - check events categorized into competition types.
    DESCRIPTION: - Expand a type and verify user can navigate to correct EDP
    DESCRIPTION: "
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: https://beta-sports.coral.co.uk/
        EXPECTED: User is logged in and on the Homepage
        """
        pass

    def test_002_select_build_your_bet_from_module_ribbon_tab(self):
        """
        DESCRIPTION: Select 'Build your bet' from Module Ribbon Tab
        EXPECTED: User is on the Build Your Bet tab within a football event detail page
        """
        pass

    def test_003_add_any_selections_from_the_events(self):
        """
        DESCRIPTION: Add any selections from the events
        EXPECTED: Selections (Game Market or Player Bet) are added to the Build Your Bet dashboard
        """
        pass

    def test_004_verify_if_the_user_is_able_to_add_and_delete_selections(self):
        """
        DESCRIPTION: Verify if the user is able to add and delete selections.
        EXPECTED: User can add and delete selections.
        """
        pass

    def test_005_verify_if_the_user_is_able_to_place_bet_with_appropriate_selections(self):
        """
        DESCRIPTION: Verify if the user is able to place bet with appropriate selections
        EXPECTED: Bet placement successful.
        """
        pass

    def test_006_repeat_steps_by_selecting_several_byb_football_events(self):
        """
        DESCRIPTION: Repeat steps by selecting several BYB football events.
        EXPECTED: 
        """
        pass
