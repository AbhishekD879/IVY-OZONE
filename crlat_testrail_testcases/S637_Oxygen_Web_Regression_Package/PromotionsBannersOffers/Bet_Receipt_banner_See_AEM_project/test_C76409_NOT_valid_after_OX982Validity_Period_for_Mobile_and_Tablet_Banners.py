import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C76409_NOT_valid_after_OX982Validity_Period_for_Mobile_and_Tablet_Banners(Common):
    """
    TR_ID: C76409
    NAME: [NOT valid after OX98.2]Validity Period for Mobile and Tablet Banners
    DESCRIPTION: This test case verifies Validity Period for Player Bets banners on Bet Receipt for Mobile and Tablet Banners
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   [BMA-16377 (CMS: Player Bets banner on Bet Receipt)][1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-16377
    PRECONDITIONS: At least one Mobile and Tablet banners are added
    PRECONDITIONS: User is logged in to Oxygen application.
    PRECONDITIONS: User has enough funds to place a bet
    """
    keep_browser_open = True

    def test_001_navigate_to_cms_page_with_mobile_player_bets_banners_for_bet_receipt_banners___bet_receipt_banners_mobile(self):
        """
        DESCRIPTION: Navigate to CMS page with Mobile Player Bets banners for bet receipt (Banners -> Bet Receipt Banners Mobile)
        EXPECTED: Page with list of banners is opened
        """
        pass

    def test_002_add_new_banner_for_some_of_supported_leagues(self):
        """
        DESCRIPTION: Add new banner for some of supported leagues
        EXPECTED: 
        """
        pass

    def test_003_verify_validity_period_start_date_and_time(self):
        """
        DESCRIPTION: Verify 'Validity Period Start' date and time
        EXPECTED: Date: YYYY-MM-DD
        EXPECTED: Time: HH:MM:SS
        EXPECTED: 'Now' button set up current time automatically
        """
        pass

    def test_004_verify_validity_period_end_date_and_time(self):
        """
        DESCRIPTION: Verify 'Validity Period End' date and time
        EXPECTED: Date: YYYY-MM-DD
        EXPECTED: Time: HH:MM:SS
        EXPECTED: 'Now' button set up current time automatically
        """
        pass

    def test_005_enter_valid_validity_period_start_and_validity_period_end_that_cover_current_time_and_click_on_create_button(self):
        """
        DESCRIPTION: Enter valid Validity Period Start and Validity Period End that cover current time and click on 'Create' button
        EXPECTED: Changes are saved
        """
        pass

    def test_006_in_oxygen_application_place_a_bet_on_event_from_league_for_which_banner_was_added(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from league for which banner was added
        EXPECTED: Bet Receipt is shown with Player bets clickable banner
        """
        pass

    def test_007_proceed_to_cms_and_set_validity_period_start_and_validity_period_end_date_and_time_as_time_range_from_the_past(self):
        """
        DESCRIPTION: Proceed to CMS and set 'Validity Period Start' and 'Validity Period End' date and time as time range from the past
        EXPECTED: Changes are saved
        """
        pass

    def test_008_in_oxygen_application_place_a_bet_on_event_from_league_for_which_banner_was_added(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from league for which banner was added
        EXPECTED: Bet Receipt is shown without Player bets clickable banner
        """
        pass

    def test_009_proceed_to_cms_and_set_validity_period_start_and_validity_period_end_date_and_time_as_time_range_from_the_future(self):
        """
        DESCRIPTION: Proceed to CMS and set 'Validity Period Start' and 'Validity Period End' date and time as time range from the future
        EXPECTED: Changes are saved
        """
        pass

    def test_010_in_oxygen_application_place_a_bet_on_event_from_league_for_which_banner_was_added(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from league for which banner was added
        EXPECTED: Bet Receipt is shown without Player bets clickable banner
        """
        pass

    def test_011_proceed_to_cms_and_set_validity_period_start_from_the_past_and_validity_period_end_in_a_few_mins_from_current_time(self):
        """
        DESCRIPTION: Proceed to CMS and set 'Validity Period Start' from the past and 'Validity Period End' in a few mins from current time
        EXPECTED: Changes are saved
        """
        pass

    def test_012_in_oxygen_application_place_a_bet_on_event_from_league_for_which_banner_was_addedwait_till_time_set_in_validity_period_end_is_passed(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from league for which banner was added.
        DESCRIPTION: Wait till time set in 'Validity Period End' is passed
        EXPECTED: After time set in 'Validity Period End' is passed Player Bets banner **is no more shown** on bet receipt
        """
        pass

    def test_013_proceed_to_cms_and_set_validity_period_start_in_a_few_mins_from_current_time_and_validity_period_end_from_the_future(self):
        """
        DESCRIPTION: Proceed to CMS and set 'Validity Period Start' in a few mins from current time and 'Validity Period End' from the future
        EXPECTED: Changes are saved
        """
        pass

    def test_014_in_oxygen_application_place_a_bet_on_event_from_league_for_which_banner_was_addedwait_till_time_set_in_validity_period_start_is_passed(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from league for which banner was added.
        DESCRIPTION: Wait till time set in 'Validity Period Start' is passed
        EXPECTED: After time set in 'Validity Period Start' is passed Player Bets banner **appears to be shown** on bet receipt
        """
        pass

    def test_015_proceed_to_cms_and_set_validity_period_start_from_the_future_and_validity_period_end_from_the_past(self):
        """
        DESCRIPTION: Proceed to CMS and set 'Validity Period Start' from the future and 'Validity Period End' from the past
        EXPECTED: Changes are saved
        """
        pass

    def test_016_in_oxygen_application_place_a_bet_on_event_from_league_for_which_banner_was_added(self):
        """
        DESCRIPTION: In Oxygen application place a bet on event from league for which banner was added.
        EXPECTED: Bet Receipt is shown without Player bets clickable banner
        """
        pass

    def test_017_navigate_to_cms_page_with_tablet_player_bets_banners_for_bet_receipt_banners___bet_receipt_banners_tablet(self):
        """
        DESCRIPTION: Navigate to CMS page with Tablet Player Bets banners for bet receipt (Banners -> Bet Receipt Banners Tablet)
        EXPECTED: Page with list of banners is opened
        """
        pass

    def test_018_front_end_part_is_not_implemented_yet_repeat_steps_2_17_for_tablet_banners(self):
        """
        DESCRIPTION: FRONT END PART IS NOT IMPLEMENTED YET: Repeat steps #2-17 for Tablet banners
        EXPECTED: 
        """
        pass
