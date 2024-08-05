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
class Test_C17406322_Vanilla_Mini_Games_iFrame_Error_Handling(Common):
    """
    TR_ID: C17406322
    NAME: [Vanilla] Mini Games: iFrame Error Handling
    DESCRIPTION: This test case verifies handle the request/response between iFrame and Games content (Error scenario)
    PRECONDITIONS: 1. Desktop Mini games widget is created and configured in CMS > Widgets
    PRECONDITIONS: 2. Desktop Mini games widget is active in CMS
    PRECONDITIONS: 3. Developer Tools is opened - "Verbose" mode is ON, postMessages debugger is installed (https://chrome.google.com/webstore/detail/postmessage-debugger/ibnkhbkkelpcgofjlfnlanbigclpldad?hl=en);
    PRECONDITIONS: 4. User is logged out
    """
    keep_browser_open = True

    def test_001_load_desktop_appverify_desktop_mini_games_iframe(self):
        """
        DESCRIPTION: Load Desktop App
        DESCRIPTION: Verify Desktop Mini Games iFrame
        EXPECTED: Desktop Mini Games iFrame is displayed in Right Column right under Betslip widget
        EXPECTED: PostMessage { type: 'LOBBY_LOADED', data: { value: true } notification is visible in Console
        """
        pass

    def test_002_trigger_lobby_feed_error_post_message_and_verify_changes_on_feonly_someone_from_cashier_team_can_trigger_error_post_message_eg_prashantkivycomptechcom1_perform_inspect_element_on_mini_games_iframe2_search_url_sent_by_app_tp_iframe3_double_click_on_it_and_paste_this_onehttpstr_casino_clrouterivycomptechcoinhtmllobbyminilobbyindexhtmlbrandcorallobbytypeinstantminiinvokerproductbettingfrontendcluserip10130128252currencygbpchannelnamewcsessionkeyb38496ea3fb8426590129874d7c3a5belangen_ushosturlhttps2f2fbeta_sportscoralcouk2fenplangenaccountnametestgvccl_is016devicetypedesktopsportsminigametruelobby_feed_errortrue_where1_sessionkey_is_your_session_key_from_local_storage_oxuser2_accountname_is_your_login_name3_userip_is_your_ip_should_be_changed_only_if_session_and_login_name_changes_do_not_helped4_press_enter_to_resent_edited_url_to_iframeindexphpattachmentsget25038042(self):
        """
        DESCRIPTION: Trigger 'LOBBY_FEED_ERROR' post message and Verify changes on FE
        DESCRIPTION: (only someone from cashier team can trigger error post message e.g. prashantk@ivycomptech.com)
        DESCRIPTION: 1. Perform inspect element on mini-Games iFrame;
        DESCRIPTION: 2. Search URL sent by App tp iFrame;
        DESCRIPTION: 3. Double click on it and paste this one:
        DESCRIPTION: https://tr-casino-clrouter.ivycomptech.co.in/htmllobby/minilobby/index.html?brand=CORAL&lobbyType=instantMini&invokerProduct=BETTING&frontend=cl&userIp=10.130.128.252&currency=GBP&channelName=WC&sessionKey=b38496ea3fb8426590129874d7c3a5be&lang=en_US&HOSTURL=https:%2F%2Fbeta-sports.coral.co.uk%2Fen&pLang=en&accountName=testgvccl-is016&deviceType=DESKTOP&sportsminigame=true&LOBBY_FEED_ERROR=true
        DESCRIPTION: !!! WHERE:
        DESCRIPTION: 1) sessionKey is your session key from local storage OX.USER;
        DESCRIPTION: 2) accountName is your login name
        DESCRIPTION: 3) userIp is your ip, should be changed only if session and login name changes do not helped;
        DESCRIPTION: 4. Press Enter to resent edited URL to iFrame;
        DESCRIPTION: ![](index.php?/attachments/get/25038042)
        EXPECTED: Desktop Mini Games iFrame is not displayed on FE.
        EXPECTED: Post Message { type: 'LOBBY_FEED_ERROR'} notification is visible in Console
        EXPECTED: ![](index.php?/attachments/get/25038044)
        """
        pass

    def test_003_check_the_error_message_which_appears_inside_of_mini_games_iframe(self):
        """
        DESCRIPTION: Check the error message which appears inside of Mini Games iFrame
        EXPECTED: Error message 'Mini Games currently unavailable, please try again later' appears
        """
        pass
