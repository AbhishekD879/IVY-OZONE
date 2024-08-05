import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.p1
# @pytest.mark.prod      cannot script it on prod as price need to be changed
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44870325_Verify_each_in_play_event_price_update_by_live_push_and_bet_placement(BaseBetSlipTest):
    """
    TR_ID: C44870325
    NAME: Verify each in play event price update by live push and bet placement
    DESCRIPTION: this test case verify price updates on  inplay tab and bet placement
    """
    # This testcase might take more time sometimes, as it is related to inplay sports (depends on the
    # number of inplay sports present)
    keep_browser_open = True
    bet_amount = 1
    prices = '1/2'
    new_price_selection = '15/2'

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_go_to_in_play_tab(self):
        """
        DESCRIPTION: Go to In-Play tab
        EXPECTED: In-Play tab opened with all inplay sports
        """
        if self.device_type == 'desktop':
            self.site.header.sport_menu.items_as_ordered_dict.get(vec.inplay.BY_IN_PLAY.upper()).click()
        else:
            if self.brand == 'ladbrokes':
                self.site.home.menu_carousel.items_as_ordered_dict.get(vec.inplay.BY_IN_PLAY).click()
            else:
                self.site.home.menu_carousel.items_as_ordered_dict.get(vec.inplay.BY_IN_PLAY.upper()).click()
        self.site.wait_content_state(state_name='InPlay')
        self.__class__.inplay_sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(self.inplay_sports.keys(), msg=f'"IN-PLAY" sports are not displayed')

    def test_003_go_to_football_and_add_selections_to_the_betslip(self):
        """
        DESCRIPTION: Go to Football and Add selections to the Betslip
        EXPECTED: Selection added
        """
        # TODO: raised bug for ladbrokes for price updation issue
        self.inplay_tabs = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        for sport_name, sport in self.inplay_tabs.items():
            if sport_name in ['FOOTBALL', 'Football']:
                event = self.ob_config.add_autotest_premier_league_football_event(is_live=True, lp_prices=self.prices)
            elif sport_name in ['TENNIS', 'Tennis']:
                event = self.ob_config.add_tennis_event_to_autotest_trophy(is_live=True, lp_prices=self.prices)
            elif sport_name in ['HANDBALL', 'Handball']:
                event = self.ob_config.add_handball_event_to_croatian_premijer_liga(is_live=True, lp_prices=self.prices)
            elif sport_name in ['VOLLEYBALL', 'Volleyball']:
                event = self.ob_config.add_volleyball_event_to_austrian_league(is_live=True, lp_prices=self.prices)
            elif sport_name in ['BEACH VOLLEYBALL', 'Beach Volleyball']:
                event = self.ob_config.add_beach_volleyball_event_to_austrian_cup(is_live=True, lp_prices=self.prices)
            elif sport_name in ['BASEBALL', 'Baseball']:
                event = self.ob_config.add_baseball_event_to_autotest_league(is_live=True, lp_prices=self.prices)
            elif sport_name in ['BASKETBALL', 'Basketball']:
                event = self.ob_config.add_basketball_event_to_austrian_league(is_live=True, lp_prices=self.prices)
            elif sport_name in ['BADMINTON', 'Badminton']:
                event = self.ob_config.add_badminton_event_to_autotest_league(is_live=True, lp_prices=self.prices)
            elif sport_name in ['ICE HOCKEY', 'Ice Hockey']:
                event = self.ob_config.add_ice_hockey_event_to_ice_hockey_usa(is_live=True, lp_prices=self.prices)
            elif sport_name in ['HORSE RACING', 'Horse Racing']:
                event = self.ob_config.add_UK_racing_event(is_live=True, lp_prices=self.prices)
            elif sport_name in ['GREYHOUND RACING', 'Greyhound Racing']:
                event = self.ob_config.add_UK_greyhound_racing_event(lp_prices=self.prices)
            else:
                event = None
            if event is not None:
                eventID, selection_ids = event.event_id, event.selection_ids
                selection_id = list(selection_ids.values())[0]
                self.navigate_to_page('Homepage')
                if self.site.wait_logged_out(timeout=3):
                    self.site.login()
                self.__class__.expected_betslip_counter_value = 0
                self.open_betslip_with_selections(selection_ids=selection_id)
                singles_section = self.get_betslip_sections().Singles
                stake_name, stake = list(singles_section.items())[0]
                self.ob_config.change_price(selection_id=selection_id, price=self.new_price_selection)
                if self.brand == 'ladbrokes':    # TODO BMA-55571
                    self.device.refresh_page()
                    self.site.wait_splash_to_hide(5)
                    self.site.open_betslip()
                else:
                    price_update = self.wait_for_price_update_from_live_serv(selection_id=selection_id,
                                                                             price=self.new_price_selection)
                    self.assertTrue(price_update,
                                    msg=f'Price update for selection "{event.team1}" with id "{selection_id}" is not received')
                    wait_for_result(lambda: stake.error_message, timeout=10)
                    error = stake.error_message
                    expected_error = vec.betslip.STAKE_PRICE_CHANGE_MSG.format(old=self.prices,
                                                                               new=self.new_price_selection)
                    self.assertEqual(error, expected_error,
                                     msg=f' Received error "{error}" is not the same as expected "{expected_error}"')
                self.place_single_bet(number_of_stakes=1)
                self.check_bet_receipt_is_displayed()
                self.site.bet_receipt.footer.click_done()
                event_url = f'{tests.HOSTNAME}/event/{eventID}'
                self.device.navigate_to(event_url)
                event = list(self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.values())[0]
                sel = list(event.outcomes.items_as_ordered_dict.values())[0]
                outcome_val = sel.output_price
                self.assertEqual(outcome_val, self.new_price_selection,
                                 msg=f'current outcome price "{outcome_val}" is not same as "{self.new_price_selection}"')

    def test_004_verify_price_update_in_in_play_sport_and_betslip(self):
        """
        DESCRIPTION: Verify price update in In-Play sport and betslip
        EXPECTED: Message appear in betslip - Price is changed from XX to XX
        """
        # covered in step3

    def test_005_click_on_accept_and_place_bet_button(self):
        """
        DESCRIPTION: Click on 'Accept and Place bet' Button
        EXPECTED: Bet is placed successfully
        """
        # covered in step3

    def test_006_repeat_step_3_to_5_for_all_inplay_sports(self):
        """
        DESCRIPTION: Repeat step #3 to #5 for all inplay sports
        EXPECTED:
        """
        # covered in step3
