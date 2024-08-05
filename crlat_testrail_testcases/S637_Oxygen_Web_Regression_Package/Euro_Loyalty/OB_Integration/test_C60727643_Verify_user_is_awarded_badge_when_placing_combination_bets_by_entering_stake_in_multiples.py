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
class Test_C60727643_Verify_user_is_awarded_badge_when_placing_combination_bets_by_entering_stake_in_multiples(Common):
    """
    TR_ID: C60727643
    NAME: Verify user is  awarded badge when placing combination bets by entering stake in multiples
    DESCRIPTION: This test case verifies user is  awarded badge when placing combination bets by entering stake in multiples
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

    def test_002_select_2_or_3_selections_from_multiple_events_in_which_at_least_one_should_qualify__to_get_euro_badgeenter_stake_in_multiplesdouble_or_triple_and_place_bet(self):
        """
        DESCRIPTION: Select 2 or 3 selections from multiple events in which at least one should qualify  to get euro badge
        DESCRIPTION: Enter stake in multiples(Double or triple) and place bet
        EXPECTED: User should be awarded badge since TBD
        """
        pass
