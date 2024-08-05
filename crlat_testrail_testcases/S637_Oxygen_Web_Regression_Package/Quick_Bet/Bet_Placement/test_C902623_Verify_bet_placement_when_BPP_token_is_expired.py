import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.quick_bet
@vtest
class Test_C902623_Verify_bet_placement_when_BPP_token_is_expired(Common):
    """
    TR_ID: C902623
    NAME: Verify bet placement when BPP token is expired
    DESCRIPTION: This test case verifies bet placement when BPP token is expired
    DESCRIPTION: By default, token is expired in 1 hour after login. Also token is refreshed on each call to BPP, so that user can execute requests to BPP for an hour since last action. So, every request to BPP will return new token in response.
    DESCRIPTION: In order to test this you need to invalidate BPP session. To do so:
    DESCRIPTION: 1. Import to the Postman as plain text:
    DESCRIPTION: curl -X PUT -H 'token: AS6uyc0Ch-ED4Hi6jHTJfrgg9XiH5DsshgjArpVjNfTxTAe12u9mD2FdnWEG934jShv6WBrRSu6usACWSANUtRzm5Pujts6_sRHxEa9EHUTJrxQEyoHlcfFQzooszAjNPmQTOWqkmjEI0w9YNXp2qM5UlNnxDBvlk2j2mpBUAjb-Jt3pjXBfx115IiTmHlu0nH1s715UfVX70eBweT5BRjB80nwFjeVwKl_ev2BDoyWXsdymCcQs9H5NzxMJs1CBb35qEe52ZJKaU-_IwB2J1fcK_TTPGWfZyFW6LVaHM4ORqcb6XK2lEcJ_TYTRpEWKeSe9veDnkHvLOYdomuhMaKBM9X3KkkTDOD7ZPnCMjkcpu_QXG5kvYzC2SuKtr8_Yza0R2odKjhbwUgak5ZkpV9wHQxMPmkPrU7DhEujXCtKKCKaT78uAW4UMchab1qoQhC5Wgooo8YMItd8BTvV0SV778w3nWE3ZeGxDvUVgZmuqb582RNGKyxkQhvHN757EiwvJ5A==' https://bpp-dev1.coralsports.dev.cloud.ladbrokescoral.com/Proxy/debug/expire?expiresInMinutes=N --compressed
    DESCRIPTION: 2.In "expiresInMinutes=N" , instead of "N" type in needed time (in min.)
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * Dev Tools should be opened
    """
    keep_browser_open = True

    def test_001_load_app(self):
        """
        DESCRIPTION: Load app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_in_console___network___user___preview___take_jwt_bpp_token(self):
        """
        DESCRIPTION: In Console -> Network -> user -> preview -> take JWT (bpp token)
        EXPECTED: ![](index.php?/attachments/get/105776462)
        """
        pass

    def test_003__in_postman___headers___paste_current_jwt_bpp_token_click_send(self):
        """
        DESCRIPTION: * In Postman -> Headers -> paste current JWT (bpp token)
        DESCRIPTION: * Click Send
        EXPECTED: Token with expiration time "N" is configured
        """
        pass

    def test_004__wait_till_token_is_expired_in_console___application___local_storage___oxuser_change_current_jwt_to_the_expired_jwt_better_do_it_in_some_file_redactor_reload_app(self):
        """
        DESCRIPTION: * Wait till Token is expired
        DESCRIPTION: * In Console -> Application -> Local Storage -> OX.USER
        DESCRIPTION: * Change current JWT to the expired JWT (better do it in some file redactor)
        DESCRIPTION: * Reload App
        EXPECTED: * App is reloaded
        EXPECTED: * Valid token is changed to the Expired one
        """
        pass

    def test_005_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_006_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: 'Stake' field is populated with entered value
        """
        pass

    def test_007_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: App tries to place bet with old token,
        EXPECTED: * Bpp response with status code 401 is received
        EXPECTED: * Right after this new JWT is received
        EXPECTED: ![](index.php?/attachments/get/111161049)
        """
        pass

    def test_008_verify_quick_bet(self):
        """
        DESCRIPTION: Verify Quick bet
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        EXPECTED: * User balance is decreased by entered stake
        """
        pass

    def test_009_tap_x_button(self):
        """
        DESCRIPTION: Tap 'X' button
        EXPECTED: Bet Receipt is closed
        """
        pass
