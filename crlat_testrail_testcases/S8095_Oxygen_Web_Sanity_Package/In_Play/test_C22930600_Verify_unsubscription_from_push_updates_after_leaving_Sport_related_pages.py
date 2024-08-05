import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C22930600_Verify_unsubscription_from_push_updates_after_leaving_Sport_related_pages(Common):
    """
    TR_ID: C22930600
    NAME: Verify unsubscription from push updates after leaving Sport-related pages
    DESCRIPTION: This test case verifies unsubscription from live updates after leaving Sport-related pages
    PRECONDITIONS: * Load Oxygen app and log in
    PRECONDITIONS: * Open In Play tab on Homepage
    PRECONDITIONS: * Turn on slow 3G mode
    PRECONDITIONS: * To check updates open Dev Tools -> Network tab -> XHR option for push notification
    """
    keep_browser_open = True

    def test_001_go_to_next_race_tab_on_the_homepage(self):
        """
        DESCRIPTION: Go to 'Next Race' tab on the Homepage
        EXPECTED: * 'Next Race' tab starts loading
        """
        pass

    def test_002_clicktap_the_back_button_when_events_are_about_to_load_and_check_push_notification_subscription(self):
        """
        DESCRIPTION: Click/Tap the 'Back' button when events are about to load and check push notification subscription
        EXPECTED: * Subscription to event/markets/selections that are on 'Next Race' tab is NOT present in 'Request payload' section in push notification
        EXPECTED: * Only one connection may be opened without any subscription
        EXPECTED: ![](index.php?/attachments/get/36608)
        """
        pass

    def test_003_update_any_update_for_an_event_from_next_race_tab_eg_price_change_eventmarket_suspension(self):
        """
        DESCRIPTION: Update any update for an event from 'Next Race' tab e.g. price change, event/market suspension
        EXPECTED: Push notification with an update is NOT received in app
        """
        pass

    def test_004_go_back_to_next_race_tab_and_trigger_any_update_for_the_event(self):
        """
        DESCRIPTION: Go back to 'Next Race' tab and trigger any update for the event
        EXPECTED: * Push notification with the update is received in app
        EXPECTED: * Update is reflected in app for the event from 'Next Race' tab
        """
        pass

    def test_005_go_to_sport_landing_page_and_repeat_steps_2_4_for_specials_tab(self):
        """
        DESCRIPTION: Go to <Sport> landing page and repeat steps #2-4 for 'Specials' tab
        EXPECTED: 
        """
        pass

    def test_006_go_to_sport_landing_page___coupons_tab___select_any_coupons_detailed_page_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Go to <Sport> landing page -> 'Coupons' tab -> select any Coupons detailed page and repeat steps #2-4
        EXPECTED: 
        """
        pass

    def test_007_go_to_sport_landing_page___competitions_tab___select_any_competition_detailed_page_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Go to <Sport> landing page -> 'Competitions' tab -> select any Competition detailed page and repeat steps #2-4
        EXPECTED: 
        """
        pass

    def test_008_go_to_the_football_landing_page___add_a_few_selections_to_favorites___go_to_favorites_page_and_repeat_steps_2_4note_this_step_is_applicable_for_coral_mobile_only(self):
        """
        DESCRIPTION: Go to the 'Football landing page' -> add a few selections to Favorites -> go to 'Favorites' page and repeat steps #2-4
        DESCRIPTION: **NOTE** this step is applicable for **Coral mobile only**
        EXPECTED: 
        """
        pass

    def test_009_go_to_az_sports_page___go_to_race_landing_page_and_repeat_steps_1_4(self):
        """
        DESCRIPTION: Go to 'AZ Sports' page -> go to <Race> landing page and repeat steps #1-4
        EXPECTED: 
        """
        pass
