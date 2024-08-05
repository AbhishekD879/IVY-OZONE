import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C60727640_Verify_badge_eligibility_if_user_is_not_placing_bets_on_each_day(Common):
    """
    TR_ID: C60727640
    NAME: Verify badge eligibility if user is not placing bets on each day
    DESCRIPTION: This test case verifies badge eligibility if user is not placing bets on each day
    DESCRIPTION: If user is placing qualifying bets on each day, he will get badges and free bets and he will complete all challenges
    DESCRIPTION: If user is not placing a qualifying bet at least any one day he will not complete all challenges
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  Euro Loyalty Page should created, activated and should be in valid date range in CMS special pages - Euro Loyalty page
    PRECONDITIONS: 3.  CMS->System Config->Structure->Euro Loyalty (Toggle-ON/OFF)
    PRECONDITIONS: **Offer1 Configuration :**
    PRECONDITIONS: > with valid UK start and end time
    PRECONDITIONS: > Allow customer to track progress = Yes, Disable Cashout Checks=Yes
    PRECONDITIONS: > Minimum Bet Trigger Interval = 1 to enable only one bet per day(for testing all badges in same day leave this field empty)
    PRECONDITIONS: > three generic bet triggers with ranks 1,2 and 3
    PRECONDITIONS: > Mim price value,EUR or GBP should define as per requirement
    PRECONDITIONS: > Trigger level for generic bet triggers should be "Football" if we want to restrict freebet only to football
    PRECONDITIONS: > One sports book token with redemption value
    PRECONDITIONS: **Offer2 configuration :**
    PRECONDITIONS: > With valid UK start and end time
    PRECONDITIONS: > Allow customer to track progress = Yes
    PRECONDITIONS: > Minimum Bet Trigger Interval = 1 to enable only one bet per day(for testing all badges in same day leave this field empty)
    PRECONDITIONS: > One offer trigger with rank 1 and offer trigger should linked to OFFER one
    PRECONDITIONS: > three generic bet triggers with ranks 2,3 and 4
    PRECONDITIONS: > Mim price value,EUR or GBP should define as per requirement
    PRECONDITIONS: > Trigger level for generic bet triggers should be "Football" if we want to restrict freebet only to football
    PRECONDITIONS: > One sports book token with redemption value
    PRECONDITIONS: *Offer 3 should be same as offer2 but should have offer trigger  with offer2 link.Like create 7 offers*
    PRECONDITIONS: **Dummy Offer 8 Configuration :**
    PRECONDITIONS: > With valid UK start and end time
    PRECONDITIONS: > Allow customer to track progress = Yes
    PRECONDITIONS: > Minimum Bet Trigger Interval = 1 to enable only one bet per day
    PRECONDITIONS: > One offer trigger with rank 1 and offer trigger should linked to OFFER 7
    PRECONDITIONS: > should not have generic bet triggers
    PRECONDITIONS: > One sports book token with redemption value
    PRECONDITIONS: ***to create dummy offer follow any one step from below***
    PRECONDITIONS: 1.  Add a bet trigger with a level that it's not possible to place a bet on
    PRECONDITIONS: 2.  Setup that pretty much disqualifies any customer. e.g an Acc20+ bet type with very big odds and very big stake
    PRECONDITIONS: 3.  Even if you leave an OFFER trigger with a token, the customer will not be able to get the token. Firing the OFFER trigger (with current code) doesn't grant you any tokens
    PRECONDITIONS: **What is qualifying bet?**
    PRECONDITIONS: In OB Euro offer configuration, we have to add generic bet triggers(Bet type,min price, EUR, GBP, stake and Is inplay ) and trigger level for each trigger based on requirement
    PRECONDITIONS: for Euros trigger level should be Football > Football international > UEFA champion league > event > market. If we want to give badge on all events, add till type level
    PRECONDITIONS: Now user has to place bet as per above config to get respective badge
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch oxygen application and login with valid credentials
        EXPECTED: User is logged into the application
        """
        pass

    def test_002_place_a_qualifying_bet_on_day1_and_verify(self):
        """
        DESCRIPTION: Place a qualifying bet on day1 and verify
        EXPECTED: User should awarded with a green badge
        EXPECTED: Second badge should display yellow line
        """
        pass

    def test_003_make_sure_user_didnt_placed_bet_on_day2(self):
        """
        DESCRIPTION: Make sure user didn't placed bet on day2
        EXPECTED: User should not awarded 2nd badge in stage1
        EXPECTED: Second badge should display yellow line
        """
        pass

    def test_004_place_a_qualifying_bet_on_day3_and_verify(self):
        """
        DESCRIPTION: Place a qualifying bet on day3 and verify
        EXPECTED: User should awarded 2nd badge[Red] in stage1
        EXPECTED: Third badge should display yellow line
        """
        pass

    def test_005_place_multiple_bets_on_day4_which_are_not_qualifying_to_euro_badge(self):
        """
        DESCRIPTION: Place multiple bets on day4 which are not qualifying to euro badge
        EXPECTED: User should not eligible to get any badge on day4
        EXPECTED: Still user should be stage1
        """
        pass

    def test_006_place_multiple_bets_on_day5_which_are_not_qualifying_to_euro_badge_andat_the_of_day_place_a_qualifying_bet_and_verify(self):
        """
        DESCRIPTION: Place multiple bets on day5 which are not qualifying to euro badge and
        DESCRIPTION: At the of day place a qualifying bet and verify
        EXPECTED: User should awarded with yellow badge and free bet token
        EXPECTED: Awarded free bet token should show in user account - offers and free bets - sports free bet tokens
        EXPECTED: Fourth badge should display yellow line
        """
        pass

    def test_007_repeat_this_for_different_user_levels(self):
        """
        DESCRIPTION: repeat this for different user levels
        EXPECTED: Should works as expected
        """
        pass
