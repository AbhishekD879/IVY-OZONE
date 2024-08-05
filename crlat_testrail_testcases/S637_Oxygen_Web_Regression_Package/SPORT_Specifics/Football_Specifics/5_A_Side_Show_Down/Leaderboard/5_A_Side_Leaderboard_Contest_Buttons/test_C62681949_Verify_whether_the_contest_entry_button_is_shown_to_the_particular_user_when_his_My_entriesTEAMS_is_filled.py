import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C62681949_Verify_whether_the_contest_entry_button_is_shown_to_the_particular_user_when_his_My_entriesTEAMS_is_filled(Common):
    """
    TR_ID: C62681949
    NAME: Verify whether the contest entry button is shown to the particular user when his My entries(TEAMS) is filled
    DESCRIPTION: 
    PRECONDITIONS: 1. User should have admin access to CMS
    PRECONDITIONS: 2. 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --> Create Menu Item
    PRECONDITIONS: Item Label. 5-A-Side Showdown
    PRECONDITIONS: Path. /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1. Create multiple contests for different events
    PRECONDITIONS: 2. Contest should be created for future events
    PRECONDITIONS: 3. Create one of the contest with TEAMS size = 5
    PRECONDITIONS: 3. Place 5 bets with a customer for the same contest so that the customer will see MAX ENTRIES REACHED in pre leaderboard
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application_with_customer_mentioned_in_pre_conditions(self):
        """
        DESCRIPTION: Login to ladbrokes application with customer mentioned in pre conditions
        EXPECTED: User mentioned in preconditions should be logged in successfully
        """
        pass

    def test_002_hit_the_standard_leaderboard_url_and_verify_that_user_able_to_optin_into_that_contest_and_place_bets_as_per_cms_config(self):
        """
        DESCRIPTION: Hit the standard Leaderboard URL and verify that user able to optin into that contest and place bets as per CMS config
        EXPECTED: User should be optin to that contest and contest should be added to the lobby and placed bets should enter into the contest
        """
        pass

    def test_003_navigate_to_5_a_side_event_for_which_the_max_entries_is_reached_for_the_contestas_mentioned_in_pre_condition(self):
        """
        DESCRIPTION: Navigate to 5-A-Side event for which the max entries is reached for the contest(as mentioned in pre condition)
        EXPECTED: User should choose an event for which the Max entries are reached
        """
        pass

    def test_004_verify_build_team_button_is_clickable_or_not(self):
        """
        DESCRIPTION: verify Build Team button is clickable or not
        EXPECTED: Build Team button is should not clickable
        """
        pass

    def test_005_check_if_that_particular_contest_entry_button_for_which_the__max_entries_are_reached_is_shown_in_betslip(self):
        """
        DESCRIPTION: Check if that particular contest entry button for which the  max entries are reached is shown in betslip
        EXPECTED: Contest entry button for which the max entries are reached shouldn't be shown on betslip
        """
        pass
