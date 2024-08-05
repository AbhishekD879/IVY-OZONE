import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't change selection state on prod/hl
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.deeplink
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C29100_Verify_Adding_Different_Selections_via_Direct_Link_Several_times(BaseBetSlipTest):
    """
    TR_ID: C29100
    TR_ID: C18636112
    NAME: Verify Adding Different Selections via Direct Link Several times
    """
    keep_browser_open = True
    expected_outcome_names = []
    selection_ids_2 = None

    def check_betslip(self, number_of_selections):
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(len(singles_section.items()) == number_of_selections,
                        msg='Should be %s stakes found but present %s'
                            % (number_of_selections, len(singles_section.items())))
        self.assertTrue(set(self.expected_outcome_names) == set(list(singles_section.keys())),
                        msg='Expected stakes is "%s" but present "%s"'
                            % (self.expected_outcome_names, singles_section.keys()))

        self.__class__.expected_betslip_counter_value = 0

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
            event_params.team1, event_params.team2, event_params.selection_ids
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team2], displayed=True, active=False)
        self.__class__.expected_outcome_names = [self.team1, self.team2]

    def test_001_login(self):
        """
        DESCRIPTION: Login to application
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_open_betslip_via_deep_link(self):
        """
        DESCRIPTION: Enter direct URL with valid outcome id('s) in address bar -> press Enter key
        EXPECTED: Bet Slip with bet details is opened automatically
        EXPECTED: Entered selection(s) are added to the Bet Slip
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.team2], self.selection_ids[self.team1]))
        self.check_betslip(number_of_selections=2)

    def test_003_go_back_to_the_homepage(self):
        """
        DESCRIPTION: Go back to the homepage
        """
        self.site.close_betslip()

    def test_004_repeat_step_2(self):
        """
        DESCRIPTION: Open betslip via deeplink
        """
        self.__class__.expected_outcome_names.append('Draw')
        self.__class__.expected_betslip_counter_value = 2
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'], timeout=5)
        self.check_betslip(number_of_selections=3)

    def test_005_place_bets_on_active_selections(self):
        """
        DESCRIPTION: Bet(s) are placed successfully
        """
        self.place_single_bet(number_of_stakes=2)
        self.check_bet_receipt_is_displayed()
        self.__class__.expected_betslip_counter_value = 0

    def test_006_repeat_steps_for_several_sports_races(self):
        """
        DESCRIPTION: Repeat steps # 2 - 4 for several <Sports>/<Races>
        """
        event_params2 = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices={0: '1/2', 1: '3/2'})
        self.__class__.selection_ids_2 = event_params2.selection_ids
        self.ob_config.change_selection_state(selection_id=list(self.selection_ids_2.values())[0],
                                              displayed=True, active=False)
        self.__class__.expected_outcome_names = list(self.selection_ids_2.keys())

        self.open_betslip_with_selections(selection_ids=self.selection_ids_2.values())
        self.check_betslip(number_of_selections=2)

        self.site.close_betslip()

        self.__class__.expected_outcome_names.append('Draw')
        self.__class__.expected_betslip_counter_value = 2
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'], timeout=5)
        self.check_betslip(number_of_selections=3)

        self.place_single_bet(number_of_stakes=2)
        self.check_bet_receipt_is_displayed()
        self.__class__.expected_betslip_counter_value = 0

    def test_007_repeat_steps_for_just_one_outcome_id(self):
        """
        DESCRIPTION: Repeat steps # 2 - 4 for for just **ONE outcome id** in direct URL
        """
        self.__class__.expected_outcome_names = ['Draw']
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])
        self.check_betslip(number_of_selections=1)

        self.site.close_betslip()

        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'], timeout=5)
        self.check_betslip(number_of_selections=1)
        self.place_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
