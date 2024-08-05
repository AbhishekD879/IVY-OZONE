import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66119948_Verify_of_Paying_X_places_instead_of_Y_signposting_and_message_notification_at_selection_level_in_my_bets_When_Extra_place_offer_is_no_longer_available_due_to_lack_of_runners(Common):
    """
    TR_ID: C66119948
    NAME: Verify of 'Paying X places instead of Y' signposting and message notification at selection level in my bets When Extra place offer is no longer available due to lack of runners
    DESCRIPTION: Verify of 'Paying X places instead of Y' signposting and message notification at selection level in my bets When Extra place offer is no longer available due to lack of runners
    PRECONDITIONS: Horse racing Bets on selections which offers Extra place should be avilable in open,cash out,Settled tabs
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials_with_precondition1(self):
        """
        DESCRIPTION: Login to the application with valid credentials with precondition1
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_verify_horse_racing_bets_which_offers_extra_place_in_open_tab(self):
        """
        DESCRIPTION: Verify Horse racing Bets which offers Extra place in open tab
        EXPECTED: Paying X places instead of Y' signposting should be displayed at market level
        """
        pass

    def test_004_verify_the_same_bet_when_one_or_more_horses_becomes_non_runner(self):
        """
        DESCRIPTION: Verify the same bet when one or more horses becomes non runner
        EXPECTED: "We are no longer offering Extra places ont this race" Message should be displayed as pert figma which notifies the user about the offer is no longer available due to lack of runners
        EXPECTED: ![](index.php?/attachments/get/16fbea19-e1be-4bf4-9d6f-a442c6b128af)
        """
        pass

    def test_005_now_verify_paying_x_places_instead_of_y_signposting_for_the_same_bet(self):
        """
        DESCRIPTION: Now Verify 'Paying X places instead of Y' signposting for the same bet
        EXPECTED: 'Paying X places instead of Y' signposting should not be displayed at market level as the offer is no longer available due to lack of runners
        """
        pass

    def test_006_repeat_step_5_and_step_6_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat step 5 and step 6 in cash out tab
        EXPECTED: Result should be same
        """
        pass
