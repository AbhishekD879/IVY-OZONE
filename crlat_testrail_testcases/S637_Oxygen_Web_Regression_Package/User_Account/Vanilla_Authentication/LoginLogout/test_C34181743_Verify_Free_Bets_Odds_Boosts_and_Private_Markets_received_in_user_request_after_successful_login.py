import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C34181743_Verify_Free_Bets_Odds_Boosts_and_Private_Markets_received_in_user_request_after_successful_login(Common):
    """
    TR_ID: C34181743
    NAME: Verify Free Bets, Odds Boosts and Private Markets received in 'user' request after successful login
    DESCRIPTION: This test case verifies receiving Free Bets, Odds Boosts and Private Markets in 'user' request after successful login via Login popup or "Login and Place Bet" button.
    PRECONDITIONS: - User should be logged out
    PRECONDITIONS: - Users shouldn't have any active Free Bets, Odd Boost tokens or Private Markets.
    PRECONDITIONS: Request to be checked:
    PRECONDITIONS: Devtools -> Network ->'user' request
    PRECONDITIONS: NOTE:
    PRECONDITIONS: Separate requests to retrieve Odds Boosts and Private markets after User login:
    PRECONDITIONS: https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=BETBOOST - Odds Boosts
    PRECONDITIONS: https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=ACCESS - Private markets
    PRECONDITIONS: are no longer used. Free Bets, Odds Boosts and Private Markets are received in one 'user' request(after implementation of ticket https://jira.egalacoral.com/browse/BMA-48103)
    """
    keep_browser_open = True

    def test_001_login_to_oxygen_application_using_ordinary_login_popup_or_login_and_place_bet_buttoncheck_user_request(self):
        """
        DESCRIPTION: Login to Oxygen application using Ordinary Login popup or "Login and Place Bet" button.
        DESCRIPTION: Check 'user' request.
        EXPECTED: - User is logged in successfuly.
        EXPECTED: - 'User' request contains empty attributes: "betBoosts", "freeBets" and "privateMarkets".
        EXPECTED: - Requests:
        EXPECTED: https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=BETBOOST, https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=ACCESS
        EXPECTED: are not present after User login.
        EXPECTED: - BETBOOST request is made in case of login using "Login and Place Bet" (BETBOOST request is made after buildbet request in case when odds boost popup is shown)
        """
        pass

    def test_002_log_out_from_oxygen_application(self):
        """
        DESCRIPTION: Log out from Oxygen application
        EXPECTED: 
        """
        pass

    def test_003_create_new_free_bet_for_the_user_from_preconditionslogin_to_oxygen_application_using_ordinary_login_popup_or_login_and_place_bet_button_and_check_user_request(self):
        """
        DESCRIPTION: Create new Free bet for the User from Preconditions.
        DESCRIPTION: Login to Oxygen application using Ordinary Login popup or "Login and Place Bet" button and check 'user' request.
        EXPECTED: - User is logged in successfuly.
        EXPECTED: - 'User' request contains configured Freebet in "freeBets" attribute data.
        EXPECTED: - 'User' request contains empty attributes: "betBoosts", "privateMarkets".
        EXPECTED: - Requests:https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=BETBOOST, https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=ACCESS
        EXPECTED: are not present after User login.
        EXPECTED: - BETBOOST request is made in case of login using "Login and Place Bet" (BETBOOST request is made after buildbet request in case when odds boost popup is shown)
        """
        pass

    def test_004_log_out_from_oxygen_application(self):
        """
        DESCRIPTION: Log out from Oxygen application
        EXPECTED: 
        """
        pass

    def test_005_configure_new_odds_boost_token_for_the_user_from_preconditionslogin_to_oxygen_application_using_ordinary_login_popup_or_login_and_place_bet_button_and_check_user_request(self):
        """
        DESCRIPTION: Configure new Odds Boost token for the User from Preconditions.
        DESCRIPTION: Login to Oxygen application using Ordinary Login popup or "Login and Place Bet" button and check 'user' request.
        EXPECTED: - User is logged in successfuly.
        EXPECTED: - 'User' request contains configured Freebet in "freeBets" attribute data.
        EXPECTED: - 'User' request contains configured Odds Boost token in "betBoosts" attribute data.
        EXPECTED: - 'User' request contains empty attribute: "privateMarkets".
        EXPECTED: - Requests:
        EXPECTED: https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=BETBOOST, https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=ACCESS
        EXPECTED: requests are not present after User login.
        EXPECTED: - BETBOOST request is made in case of login using "Login and Place Bet" (BETBOOST request is made after buildbet request in case when odds boost popup is shown)
        """
        pass

    def test_006_log_out_from_oxygen_application(self):
        """
        DESCRIPTION: Log out from Oxygen application
        EXPECTED: 
        """
        pass

    def test_007_configure_private_market_for_the_user_from_preconditions_trigger_this_private_market_by_placing_any_bet_on_trigger_event_for_this_private_market(self):
        """
        DESCRIPTION: Configure Private market for the User from Preconditions. Trigger this private market by placing any bet on trigger event for this Private market.
        EXPECTED: 
        """
        pass

    def test_008_login_to_oxygen_application_using_ordinary_login_popup_or_login_and_place_bet_button_and_check_user_request(self):
        """
        DESCRIPTION: Login to Oxygen application using Ordinary Login popup or "Login and Place Bet" button and check 'user' request.
        EXPECTED: - User is logged in successfuly.
        EXPECTED: - 'User' request contains configured Freebet in "freeBets" attribute data.
        EXPECTED: - 'User' request contains configured Odds Boost token in "betBoosts" attribute data.
        EXPECTED: - 'User' request contains configured Private Market in "privateMarkets" attribute data.
        EXPECTED: - Requests:
        EXPECTED: https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=BETBOOST, https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=ACCESS
        EXPECTED: are not present after User login.
        EXPECTED: - BETBOOST request is made in case of login using "Login and Place Bet" (BETBOOST request is made after buildbet request in case when odds boost popup is shown)
        """
        pass

    def test_009_user_all_free_bets_and_odds_boost_tokens_of_the_user_so_user_doesnt_have_any_free_bets_and_odds_boost_tokens_available_and_log_out_from_oxygen_application(self):
        """
        DESCRIPTION: User all Free Bets and Odds Boost tokens of the User so User doesn't have any Free Bets and Odds Boost tokens available and log out from Oxygen application.
        EXPECTED: 
        """
        pass

    def test_010_login_to_oxygen_application_using_ordinary_login_popup_or_login_and_place_bet_button_and_check_user_request(self):
        """
        DESCRIPTION: Login to Oxygen application using Ordinary Login popup or "Login and Place Bet" button and check 'user' request.
        EXPECTED: - User is logged in successfuly.
        EXPECTED: - 'User' request contains configured Private Market in "privateMarkets" attribute data.
        EXPECTED: - 'User' request contains empty attributes: "betBoosts", "freeBets".
        EXPECTED: - Requests:
        EXPECTED: https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=BETBOOST, https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=ACCESS
        EXPECTED: are not present after User login.
        EXPECTED: - BETBOOST request is made in case of login using "Login and Place Bet" (BETBOOST request is made after buildbet request in case when odds boost popup is shown)
        """
        pass

    def test_011_place_any_bet_on_the_private_market_available_for_the_user_and_log_out_from_oxygen_application(self):
        """
        DESCRIPTION: Place any bet on the private market available for the User and log out from Oxygen application.
        EXPECTED: 
        """
        pass

    def test_012_login_to_oxygen_application_using_ordinary_login_popup_or_login_and_place_bet_button_and_check_user_request(self):
        """
        DESCRIPTION: Login to Oxygen application using Ordinary Login popup or "Login and Place Bet" button and check 'user' request.
        EXPECTED: - User is logged in successfuly.
        EXPECTED: - 'User' request contains empty attributes: "betBoosts", "freeBets" and "privateMarkets".
        EXPECTED: - Requests:
        EXPECTED: https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=BETBOOST, https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?freebetTokenType=ACCESS
        EXPECTED: are not present after User login.
        EXPECTED: - BETBOOST request is made in case of login using "Login and Place Bet" (BETBOOST request is made after buildbet request in case when odds boost popup is shown)
        """
        pass
