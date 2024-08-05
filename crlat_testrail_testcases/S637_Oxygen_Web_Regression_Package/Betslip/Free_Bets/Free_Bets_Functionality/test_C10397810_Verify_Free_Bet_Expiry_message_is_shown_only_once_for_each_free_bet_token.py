import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C10397810_Verify_Free_Bet_Expiry_message_is_shown_only_once_for_each_free_bet_token(Common):
    """
    TR_ID: C10397810
    NAME: Verify Free Bet Expiry message is shown only once for each free bet token
    DESCRIPTION: This test case verifies, that if User has Free Bet expiring within 24 hours, when they logs into the app - Free Bet Expiry message is shown AND this message is shown only once for each Free Bet Token.
    DESCRIPTION: Note: Per comment in https://jira.egalacoral.com/browse/BMA-50888, Free Bet Expiry message should NOT be shown on Ladbrokes brand at all on all platforms from OX 102 (vanilla).
    PRECONDITIONS: 1. User has few Free Bets expiring within 24 hours available on their account.
    PRECONDITIONS: 2. User is logged in and Free Bet Expiry message is shown for the Free Bet with the closest expiry date.
    """
    keep_browser_open = True

    def test_001_press_close_button_on_free_bet_expiry_message(self):
        """
        DESCRIPTION: Press close button on Free Bet Expiry message.
        EXPECTED: Free Bet Expiry message is closed.
        """
        pass

    def test_002_go_to_developer_tools___application___local_storageverify_that_oxhidefreebetsids_username_key_is_updated_with_appropriate_value(self):
        """
        DESCRIPTION: Go to Developer Tools -> Application -> Local Storage
        DESCRIPTION: Verify, that *OX.hideFreeBetsIDs-[username]* key is updated with appropriate value
        EXPECTED: freebetTokenId Value is saved in *OX.hideFreeBetsIDs-[username]* key
        EXPECTED: (freebetTokenId can be checked in _accountFreebets?freebetTokenType=SPORTS&channel=M&returnOffers=Y_ request in Network)
        """
        pass

    def test_003_perform_some_actions__tab_switching_across_app(self):
        """
        DESCRIPTION: Perform some actions / tab switching across App.
        EXPECTED: Free Bet Expiry message isn't shown again in current login session.
        """
        pass

    def test_004_log_out_and_log_in_again(self):
        """
        DESCRIPTION: Log out and log in again.
        EXPECTED: The same Free Bet Expiry message for Free Bet Token from previous steps isn't shown again.
        EXPECTED: Free Bet Expiry message is shown for the next Free Bet with the closest expiry date.
        EXPECTED: Note 2: Free Bet expiry message should not be shown on Ladbrokes brand on all platforms.
        """
        pass

    def test_005_repeat_steps_1_2(self):
        """
        DESCRIPTION: Repeat steps 1-2.
        EXPECTED: *OX.hideFreeBetsIDs-[username]* key is updated with freebetTokenId Value for Step 4 free bet token
        """
        pass
