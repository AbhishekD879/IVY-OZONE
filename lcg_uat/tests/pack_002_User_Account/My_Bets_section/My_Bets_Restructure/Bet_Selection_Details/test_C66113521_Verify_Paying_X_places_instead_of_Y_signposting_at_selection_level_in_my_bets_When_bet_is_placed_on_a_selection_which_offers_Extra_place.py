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
class Test_C66113521_Verify_Paying_X_places_instead_of_Y_signposting_at_selection_level_in_my_bets_When_bet_is_placed_on_a_selection_which_offers_Extra_place(Common):
    """
    TR_ID: C66113521
    NAME: Verify 'Paying X places instead of Y' signposting at selection level in my bets When bet is placed on a selection which offers Extra place
    DESCRIPTION: This testcase verifies 'Paying X places instead of Y' signposting at selection level in my bets When bet is placed on a selection which offers Extra place
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
        EXPECTED: Paying X places instead of Y' signposting should be displayed as per figma
        EXPECTED: ![](index.php?/attachments/get/c3357aaf-c7a8-436a-a783-b0c82a6872bc)
        """
        pass

    def test_004_click_on_cash_out(self):
        """
        DESCRIPTION: Click on cash out
        EXPECTED: Cash out tab is opened
        """
        pass

    def test_005_verify_horse_racing_bets_which_offers_extra_place_in_cash_out_tab(self):
        """
        DESCRIPTION: Verify Horse racing Bets which offers Extra place in Cash out tab
        EXPECTED: Paying X places instead of Y' signposting should be displayed as per figma
        EXPECTED: ![](index.php?/attachments/get/ae83a1b4-f5d4-4b6c-8421-2f13bc21bb7c)
        """
        pass

    def test_006_click_on_settled_tab(self):
        """
        DESCRIPTION: Click on settled tab
        EXPECTED: Settled tab is opened
        """
        pass

    def test_007_verify_horse_racing_bets_which_offers_extra_place_in_settled_tab(self):
        """
        DESCRIPTION: Verify Horse racing Bets which offers Extra place in Settled tab
        EXPECTED: Paying X places instead of Y' signposting should be displayed as per figma
        EXPECTED: ![](index.php?/attachments/get/6c0bd797-73e9-46c0-b1e1-d9cdedf87e87)
        """
        pass
