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
class Test_C62681948_Verify_whether_the_contest_entry_button_is_shown_in_betslip_when_the_contest_is_full(Common):
    """
    TR_ID: C62681948
    NAME: Verify whether the contest entry button is shown in betslip when the contest is full
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
    PRECONDITIONS: 3. Make one of  the contest full by placing maximum bets which is mentioned in SIZE
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_002_hit_the_standard_leaderboard_url_and_verify_that_user_able_to_optin_into_that_contest_and_place_bets_as_per_cms_config(self):
        """
        DESCRIPTION: Hit the standard Leaderboard URL and verify that user able to optin into that contest and place bets as per CMS config
        EXPECTED: User should be optin to that contest and contest should be added to the lobby and placed bets should enter into the contest
        """
        pass

    def test_003_navigate_to_the_5_a_side_event_for_which_the_contest_is_created_and_fullas_mentioned_in_pre_condition(self):
        """
        DESCRIPTION: Navigate to the 5-A-Side event for which the contest is created and full(as mentioned in pre condition)
        EXPECTED: User should choose an event for which the contest is full
        """
        pass

    def test_004_verify_build_team_button_is_clickable_or_not(self):
        """
        DESCRIPTION: verify Build Team button is clickable or not
        EXPECTED: Build Team button is should not clickable
        """
        pass

    def test_005_check_if_the_contest_entry_button_which_is_filled_is_shown_in_betslip(self):
        """
        DESCRIPTION: check if the contest entry button which is filled is shown in betslip
        EXPECTED: Contest entry button which is full shouldn't be shown on betslip
        """
        pass
