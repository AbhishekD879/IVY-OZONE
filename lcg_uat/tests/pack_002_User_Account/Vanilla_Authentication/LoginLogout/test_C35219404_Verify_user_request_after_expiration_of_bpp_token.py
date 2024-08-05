import pytest
from crlat_ob_client.offer import Offer
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_014_Module_Selector_Ribbon.Private_Markets.BasePrivateMarketsTest import BasePrivateMarketsTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # we can not create private markets, grant freebets, odds boost in prod
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@vtest
class Test_C35219404_Verify_user_request_after_expiration_of_bpp_token(BasePrivateMarketsTest, BaseUserAccountTest):
    """
    TR_ID: C35219404
    NAME: Verify 'user' request after expiration of bpp token
    DESCRIPTION: This test case verifies 'user' request after expiration of bpp token.
    PRECONDITIONS: 1. User should have Free bets, Odds Boost tokens and Private markets available.
    PRECONDITIONS: 2. User should be logged in.
    PRECONDITIONS: In order to expire bpp token:
    PRECONDITIONS: Go to Devtools -> Application -> Local storage -> delete OX.User
    """
    keep_browser_open = True
    cookie_name = 'OX.USER'
    cookie_parameter = 'bppToken'
    free_bet_value = 1.03

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. User should have Free bets, Odds Boost tokens and Private markets available.
        PRECONDITIONS: 2. User is logged in to application
        """
        event = self.ob_config.add_autotest_premier_league_football_event(price_boost=True,
                                                                          market_price_boost=True,
                                                                          cashout=True)
        selection_id = event.selection_ids[vec.sb.DRAW.title()]
        self.__class__.username = tests.settings.betplacement_user
        self.ob_config.grant_freebet(username=self.username, freebet_value=self.free_bet_value, level='selection',
                                     id=selection_id)
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=selection_id)
        self.site.login(username=self.username, async_close_dialogs=False)
        offer_id = self.ob_config.backend.ob.private_market_offer.offer_id
        offer = Offer(env=tests.settings.backend_env, brand=self.brand)
        self.trigger_private_market_appearance(user=self.username, expected_market_name=self.private_market_name)
        offer.give_offer(username=self.username, offer_id=offer_id)

    def test_001_expire_bpp_token_refresh_the_page_and_check_network_for_user_request(self):
        """
        DESCRIPTION: Expire bpp token, refresh the page and check Network for 'user' request
        EXPECTED:
        """
        bpp_token = self.get_local_storage_cookie_value_as_dict(self.cookie_name).get(self.cookie_parameter)
        self.assertTrue(bpp_token, msg='BPP token is not received')
        self.delete_local_storage_cookie(self.cookie_name)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

    def test_002_check_user_request(self):
        """
        DESCRIPTION: Check 'user' request
        EXPECTED: Free bets, Odds Boost tokens and Private markets that are available for the user are received in 'user' request after page refresh.
        EXPECTED: * https://{env}.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountFreebets?channel=MI&returnOffers=Y
        """
        bpp_token = self.get_local_storage_cookie_value_as_dict(self.cookie_name).get(self.cookie_parameter)
        self.assertTrue(bpp_token, msg='BPP token is not received')
