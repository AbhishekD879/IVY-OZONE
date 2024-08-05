import pytest
import tests
from tests.base_test import vtest
from json import JSONDecodeError
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C60004650_Verify_that_BETBOOST_request_Removed_after_build_bet(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C60004650
    NAME: Verify that BETBOOST request Removed after build bet
    DESCRIPTION: This Test Сase verifies that there is no BETBOOST request after 'build bet' request.
    PRECONDITIONS: 1. Should be created a user with available odds boost.
    PRECONDITIONS: 2. How to add odds boost token https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+add+Odds+boost+token
    """
    keep_browser_open = True
    invalid_req = 'accountFreebets?freebetTokenType=BETBOOST'
    ss_url = 'accountFreebets?'
    eventID = []

    def get_response_url(self, url):
        """
        :param url: SS or Commentary url
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def check_request(self):
        """
        :return: Complete url
        """
        sleep(10)  # Need time for SS requests to load
        sp_url = self.get_response_url(url=self.ss_url)
        self.assertNotIn(self.invalid_req, sp_url, msg=f'Required "{self.invalid_req}" parameter found')

    def test_000_pre_conditions(self):
        """
        DESCRIPTION: Open App and login with user from preconditions.
        DESCRIPTION: Create events
        """
        event1 = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.eventID_1 = event1.event_id
        event2 = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.selection_id1 = list(event1.selection_ids.values())[0]
        self.__class__.selection_id2 = list(event2.selection_ids.values())[0]
        self.__class__.user_name = tests.settings.betplacement_user

    def test_001_open_app_and_login_with_user_from_preconditionsadd_selection_to_betslip(self):
        """
        DESCRIPTION: Open App and login with user from preconditions.
        DESCRIPTION: Add selection to betslip.
        EXPECTED: - Open devtool. There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        EXPECTED: - All valid freebets and odds boost should be available for user.
        EXPECTED: - Oxygen-UI should use missing freeBetOfferType from /Proxy/v1/buildBet response for filtering and sorting logic of odds boosts in betslip.
        """
        self.site.login(username=self.user_name)
        self.ob_config.grant_odds_boost_token(username=self.user_name, level='selection')

        self.open_betslip_with_selections(selection_ids=[self.selection_id1])
        self.check_request()

    def test_002_add_a_couple_of_additional_selections_to_betslip(self):
        """
        DESCRIPTION: Add a couple of additional selections to betslip.
        EXPECTED: - Open devtool. There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        EXPECTED: - All valid freebets and odds boost should be available for user.
        EXPECTED: - Oxygen-UI should use missing freeBetOfferType from /Proxy/v1/buildBet response for filtering and sorting logic of odds boosts in betslip.
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_id1, self.selection_id2])
        self.check_request()

    def test_003_remove_one_of_the_selections_from_the_betslip(self):
        """
        DESCRIPTION: Remove one of the selections from the betslip
        EXPECTED: - Open devtool. There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        EXPECTED: - All valid freebets and odds boost should be available for user.
        EXPECTED: - Oxygen-UI should use missing freeBetOfferType from /Proxy/v1/buildBet response for filtering and sorting logic of odds boosts in betslip.
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        self.stake = list(singles_section.values())[0]
        self.stake.remove_button.click()
        self.check_request()

    def test_004_remove_all_selections_from_the_betslip(self):
        """
        DESCRIPTION: Remove all selections from the betslip.
        EXPECTED:
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        self.stake = list(singles_section.values())[0]
        self.stake.remove_button.click()

    def test_005_for_mobileadd_selection_to_quick_bet(self):
        """
        DESCRIPTION: **For Mobile**
        DESCRIPTION: Add selection to 'Quick Bet'
        EXPECTED: - Open devtool. There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        EXPECTED: - All valid freebets and odds boost should be available for user.
        EXPECTED: - Oxygen-UI should use missing freeBetOfferType from /Proxy/v1/buildBet response for filtering and sorting logic of odds boosts in betslip.
        """
        if self.device_type == 'mobile':
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventIDss = event_params.event_id
            market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')

            self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)
            self.navigate_to_edp(event_id=self.eventIDss)
            self.add_selection_from_event_details_to_quick_bet(market_name='Match Result')
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.open_betslip()
            self.site.close_all_dialogs()
            singles_section = self.get_betslip_sections().Singles
            self.assertTrue(singles_section.items(), msg='*** No stakes found')
            self.stake = list(singles_section.values())[0]
            self.stake.remove_button.click()
            self.check_request()

    def test_006_for_mobilepress_x_and_remove_selection_to_quick_betopen_betslip(self):
        """
        DESCRIPTION: **For Mobile**
        DESCRIPTION: Press 'X' and remove selection to 'Quick Bet'.
        DESCRIPTION: Open Betslip.
        EXPECTED: - Selection from the 'Quick Bet' added to the betslip.
        EXPECTED: - Open devtool. There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        EXPECTED: - All valid freebets and odds boost should be available for user.
        EXPECTED: - Oxygen-UI should use missing freeBetOfferType from /Proxy/v1/buildBet response for filtering and sorting logic of odds boosts in betslip.
        """
        # Covered in step 5
