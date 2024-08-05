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
class Test_C60727649_Euro_loyalty__Verify_user_is_getting_only_one_badge_per_day_and_only_for_the_current_day_events(Common):
    """
    TR_ID: C60727649
    NAME: Euro loyalty - Verify user is getting only one badge per day and only for the current day events
    DESCRIPTION: This test case is to verify user is getting only one badge per day and only for the current day events
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  Euro Loyalty Page should created, activated and should be in valid date range in CMS special pages - Euro Loyalty page
    PRECONDITIONS: 3.  CMS->System Config->Structure->Euro Loyalty (Toggle-ON/OFF)
    PRECONDITIONS: **Offer1 Configuration :**
    PRECONDITIONS: with valid UK start and end time
    PRECONDITIONS: Allow customer to track progress = Yes, Disable Cashout Checks=Yes
    PRECONDITIONS: Minimum Bet Trigger Interval = 1 to enable only one bet per day
    PRECONDITIONS: three generic bet triggers with ranks 1,2 and 3
    PRECONDITIONS: Mim price value,EUR or GBP should define as per requirement
    PRECONDITIONS: Trigger level for generic bet triggers should be "Football" if we want to restrict freebet only to football
    PRECONDITIONS: One sports book token with redemption value
    PRECONDITIONS: **Offer2 configuration :**
    PRECONDITIONS: With valid UK start and end time
    PRECONDITIONS: Allow customer to track progress = Yes
    PRECONDITIONS: Minimum Bet Trigger Interval = 1 to enable only one bet per day
    PRECONDITIONS: One offer trigger with rank 1 and offer trigger should linked to OFFER one
    PRECONDITIONS: three generic bet triggers with ranks 2,3 and 4
    PRECONDITIONS: Mim price value,EUR or GBP should define as per requirement
    PRECONDITIONS: Trigger level for generic bet triggers should be "Football" if we want to restrict freebet only to football
    PRECONDITIONS: One sports book token with redemption value
    PRECONDITIONS: Offer 3 should be same as offer2 but should have offer trigger with offer2 link.Like create 7 offers
    PRECONDITIONS: **Dummy Offer 8 Configuration :**
    PRECONDITIONS: With valid UK start and end time
    PRECONDITIONS: Allow customer to track progress = Yes
    PRECONDITIONS: Minimum Bet Trigger Interval = 1 to enable only one bet per day
    PRECONDITIONS: One offer trigger with rank 1 and offer trigger should linked to OFFER 7
    PRECONDITIONS: should not have generic bet triggers
    PRECONDITIONS: One sports book token with redemption value
    PRECONDITIONS: **to create dummy offer follow any one step from below**
    PRECONDITIONS: Add a bet trigger with a level that it's not possible to place a bet on
    PRECONDITIONS: Setup that pretty much disqualifies any customer. e.g an Acc20+ bet type with very big odds and very big stake
    PRECONDITIONS: Even if you leave an OFFER trigger with a token, the customer will not be able to get the token. Firing the OFFER trigger (with current code) doesn't grant you any tokens
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

    def test_002_navigate_to_euro_2020_big_competition_or_football_and_place_bet_on_future_day_event_which_will_get_badge(self):
        """
        DESCRIPTION: Navigate to Euro 2020 big competition or football and place bet on future day event which will get badge
        EXPECTED: User should not get badge
        """
        pass

    def test_003_navigate_to_euro_2020_big_competition_or_football_and_place_bet_on_future_day_event_which_will_not_get_badge(self):
        """
        DESCRIPTION: Navigate to Euro 2020 big competition or football and place bet on future day event which will not get badge
        EXPECTED: User should not get badge
        """
        pass

    def test_004_navigate_to_euro_2020_big_competition_or_football_and_place_bet_on_todays_event_which_will_not_get_badge(self):
        """
        DESCRIPTION: Navigate to Euro 2020 big competition or football and place bet on today's event which will not get badge
        EXPECTED: User should not get badge
        """
        pass

    def test_005_navigate_to_euro_2020_big_competition_or_football_and_place_bet_on_todays_pre_play_or_inplay_event_which_will__get_badge(self):
        """
        DESCRIPTION: Navigate to Euro 2020 big competition or football and place bet on today's pre play or inplay event which will  get badge
        EXPECTED: User should get badge
        """
        pass

    def test_006_navigate_to_euro_2020_big_competition_or_football_and_place_bet_on_todays_pre_play_or_inplay_event_which_will__get_badge(self):
        """
        DESCRIPTION: Navigate to Euro 2020 big competition or football and place bet on today's pre play or inplay event which will  get badge
        EXPECTED: User should not get badge
        """
        pass

    def test_007_place_qualifying_bet_from_below_areas_and_verify_user_is_getting_badge_or_notfeatured_tabsurface_bethc_or_event_hubdesktop_featured_tabinplay_mrtfootball_matches_tabfootball_inplay_tabdesktop_inplay_or_live_streammobile_live_stream(self):
        """
        DESCRIPTION: Place qualifying bet from below areas and verify user is getting badge or not
        DESCRIPTION: featured tab,
        DESCRIPTION: surface bet,
        DESCRIPTION: HC or event hub,
        DESCRIPTION: desktop featured tab
        DESCRIPTION: Inplay MRT
        DESCRIPTION: Football matches tab
        DESCRIPTION: Football inplay tab
        DESCRIPTION: Desktop inplay or Live stream
        DESCRIPTION: Mobile live stream
        EXPECTED: If user is eligible to get badge for the day, he should get the badge
        """
        pass
