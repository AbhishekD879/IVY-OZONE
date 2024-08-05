import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.other
@vtest
class Test_C60709307_Euro_Loyalty__verify_messaging(Common):
    """
    TR_ID: C60709307
    NAME: Euro Loyalty - verify messaging
    DESCRIPTION: This test case is to verify different messages in Euro Loyalty page
    PRECONDITIONS: 1.  Matchday rewards configuration should done and enabled in CMS
    PRECONDITIONS: 2.  User should mapped to tier
    PRECONDITIONS: Note: free bet value in message Free Bets value either £5 or £10 or £20, which is based on the configuration setup in Open Bet and user customer tier segment.
    PRECONDITIONS: **Logic :**
    PRECONDITIONS: > For each 3 bet placement user will get free bet token
    PRECONDITIONS: > If user is not placed any bet "YOUR NEXT REWARD £X FREE BET Place 3 qualifying bets to receive your reward" should display
    PRECONDITIONS: > If user place one bet, the NUMBER showing in message should decrease to one "YOUR NEXT REWARD £X FREE BET Place 2 qualifying bets to receive your reward" should display. The above message shows until user place next qualifying bet
    PRECONDITIONS: > If user places all bets which is qualifying to get free bet token, then Message "CONGRATULATIONS You have earned £X Free Bet, make sure you come tomorrow" should display
    PRECONDITIONS: **Offer1 Configuration :**
    PRECONDITIONS: > with valid UK start and end time
    PRECONDITIONS: > Allow customer to track progress = Yes, Disable Cashout Checks= Yes
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
    PRECONDITIONS: for Euros trigget level should be Football > Football international > UEFA champion league > event > market. If we want to give badge on all events, add till type level
    PRECONDITIONS: Now user has to place bet as per above config to get respective badge
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application_and_navigate_to_euro_loyalty_page(self):
        """
        DESCRIPTION: Launch oxygen application and navigate to Euro Loyalty page
        EXPECTED: Euro Loyalty page should open
        EXPECTED: User should be able to see the badges and the free bet values in the match day rewards page
        """
        pass

    def test_002_login_to_oxygen_application_and_navigate_to_euro_loyalty_page(self):
        """
        DESCRIPTION: Login to oxygen application and navigate to Euro Loyalty page
        EXPECTED: Euro Loyalty page should open
        EXPECTED: 1.  If user is not participated yet in Euro program, first badge should display with yellow line
        EXPECTED: 2.  Mobile & Desktop: Below to first row message **"YOUR NEXT REWARD £X FREE BET Place 3 qualifying bets to receive your reward"** should display
        EXPECTED: *Free Bets value either £5 or £10 or £20, which is based on the configuration setup in Open Bet and user customer tier segment.*
        """
        pass

    def test_003_place_a_qualifying_bet_on_day1_and_verify_badge_display_and_message(self):
        """
        DESCRIPTION: Place a qualifying bet on day1 and verify badge display and message
        EXPECTED: 1. First badge should changed to green color
        EXPECTED: 2.  Message **"CONGRATULATIONS You've earned today's stamp, make sure you come tomorrow"** should display
        EXPECTED: 3. Next badge should display yellow line
        """
        pass

    def test_004_refresh_the_page_or_navigate_to_other_page_and_come_back_to_matchday_rewards_page(self):
        """
        DESCRIPTION: Refresh the page or navigate to other page and come back to matchday rewards page
        EXPECTED: 1.  First badge should display in green color
        EXPECTED: 2.  Message **"YOUR NEXT REWARD £X FREE BET Place 2 qualifying bets to receive your reward"** should display
        EXPECTED: 3.  Next badge should display yellow line
        EXPECTED: *Free Bets value either £5 or £10 or £20, which is based on the configuration setup in Open Bet and user customer tier segment.*
        """
        pass

    def test_005_place_a_qualifying_bet_on_day2_and_verify_badge_display_and_message(self):
        """
        DESCRIPTION: Place a qualifying bet on day2 and verify badge display and message
        EXPECTED: 1.  Second badge should changed to red color
        EXPECTED: 2.  Message **"CONGRATULATIONS You've earned today's stamp, make sure you come tomorrow"** should display
        EXPECTED: 3.  Next badge should display yellow line
        """
        pass

    def test_006_refresh_the_page_or_navigate_to_other_page_and_come_back_to_matchday_rewards_page(self):
        """
        DESCRIPTION: Refresh the page or navigate to other page and come back to matchday rewards page
        EXPECTED: 1.  Second badge should display in red color
        EXPECTED: 2.  Message **"YOUR NEXT REWARD £X FREE BET Place 1 qualifying bets to receive your reward"** should display
        EXPECTED: 3.  Next badge should display yellow line
        EXPECTED: *Free Bets value either £5 or £10 or £20, which is based on the configuration setup in Open Bet and user customer tier segment.*
        """
        pass

    def test_007_place_a_qualifying_bet_on_day3_and_verify_badge_display_and_message(self):
        """
        DESCRIPTION: Place a qualifying bet on day3 and verify badge display and message
        EXPECTED: 1.  Third badge should changed to yellow color
        EXPECTED: 2.  Message **"CONGRATULATIONS You've earned £X Free Bet, make sure you come tomorrow"** should display
        EXPECTED: 3.  Next badge should display yellow line
        EXPECTED: 4.  Awarded free bet token should show in user account - offers and free bets - sports free bet tokens
        EXPECTED: *Congratulation message should show as popup with white background and black font and **close** button. user is not allowed to perform any action until click on close button*
        """
        pass

    def test_008_refresh_the_page_or_navigate_to_other_page_and_come_back_to_matchday_rewards_page(self):
        """
        DESCRIPTION: Refresh the page or navigate to other page and come back to matchday rewards page
        EXPECTED: 1.  Third badge should display in yellow color
        EXPECTED: 2.  Below to second row, Message **"CONGRATULATIONS You've earned £X Free Bet, make sure you come tomorrow"** should display
        EXPECTED: 3.  Next badge (4th)should display yellow line
        EXPECTED: *Free Bets value either £5 or £10 or £20, which is based on the configuration setup in Open Bet and user customer tier segment.*
        """
        pass

    def test_009_place_qualifying_bets_till_the_end_of_program_and_verify_messages(self):
        """
        DESCRIPTION: Place qualifying bets till the end of program and verify messages
        EXPECTED: 1.  Respective message should display
        EXPECTED: 2.  Always message location should be below to the current stage
        EXPECTED: 3.  if user is in stage 2 message location should always below to stage 2 untill he comepleted stage2
        EXPECTED: 4.  Once after completion of stage2 message location should be below to stage3
        """
        pass

    def test_010_repeat_all_steps_with_user_with_different_tiers(self):
        """
        DESCRIPTION: repeat all steps with user with different tiers
        EXPECTED: Free bet value should display as per OB config for that user tier
        """
        pass
