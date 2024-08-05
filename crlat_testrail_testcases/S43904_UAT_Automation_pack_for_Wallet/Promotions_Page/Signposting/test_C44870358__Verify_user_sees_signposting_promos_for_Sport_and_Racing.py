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
class Test_C44870358__Verify_user_sees_signposting_promos_for_Sport_and_Racing(Common):
    """
    TR_ID: C44870358
    NAME: " Verify user sees signposting promos for Sport  and Racing
    DESCRIPTION: "This test case Verify  signposting promos on Sport and Racing pages, Betslip, Bet Receipt, My Bets
    DESCRIPTION: (Money back ,extra place,odds boost,smart boost ,cash out,#getaprice,cashout,price boost etc)
    DESCRIPTION: - Verify signposting labels should not be dispylaed from Competitions Tab page ( Build your bet  should not be visible )"
    PRECONDITIONS: UserName: goldenbuild1  Password: password1
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage opened
        """
        pass

    def test_002_verify_money_back_promo_icon_for_an_event_on_homepage(self):
        """
        DESCRIPTION: Verify Money back promo icon for an Event on HomePage
        EXPECTED: Promo icon is displayed on event
        """
        pass

    def test_003_navigate_to_edp_of_event_with_moneyback_flag_ticked_at_market_level(self):
        """
        DESCRIPTION: Navigate to EDP of event with MoneyBack flag ticked at market level
        EXPECTED: MoneyBack icon is displayed on the right side of market header (eg. on 'Match Result' market header)
        """
        pass

    def test_004_expandcollapse_market_header(self):
        """
        DESCRIPTION: Expand/Collapse market header
        EXPECTED: MoneyBack icon remains displayed on the right side of market header
        """
        pass

    def test_005_add_a_selection_and_money_back_icon_in__quickbetbetslip(self):
        """
        DESCRIPTION: Add a selection and Money back icon in  Quickbet/Betslip
        EXPECTED: Money back icon is displayed below the Event name in Quickbet/Betslip
        """
        pass

    def test_006_enter_stake_place_bet_and_verify_money_back_icon_in_bet_receipt(self):
        """
        DESCRIPTION: Enter stake, Place bet and verify Money back icon in Bet receipt
        EXPECTED: Money back icon is displayed in Bet receipt
        """
        pass

    def test_007_verify_money_back_icon_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Verify Money back icon in My bets, Open bets
        EXPECTED: Money back icon is displayed in Open bets
        """
        pass

    def test_008_verify_money_back_icon_in_my_bets_settle_bet(self):
        """
        DESCRIPTION: Verify Money back icon in My bets Settle bet
        EXPECTED: Money back icon is displayed for settle bets
        """
        pass

    def test_009_repeat_step_2_to_8__for_extra_placeodds_boostsmart_boost_cash_outgetapricecashoutprice_boost_etc_for_sports_and_racing(self):
        """
        DESCRIPTION: Repeat step #2 to #8  for extra place,odds boost,smart boost ,cash out,#getaprice,cashout,price boost etc for Sports and Racing
        EXPECTED: 
        """
        pass

    def test_010_verify_signposting_labels_should_not_be_displayed_from_competitions_tab_page__build_your_bet__should_not_be_visible_(self):
        """
        DESCRIPTION: Verify signposting labels should not be displayed from Competitions Tab page ( Build your bet  should not be visible )
        EXPECTED: Build your bet is not displayed
        """
        pass
