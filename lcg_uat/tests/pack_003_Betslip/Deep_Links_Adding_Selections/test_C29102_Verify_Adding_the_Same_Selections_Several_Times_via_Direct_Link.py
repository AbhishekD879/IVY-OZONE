import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.deeplink
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C29102_Verify_Adding_the_Same_Selections_Several_Times_via_Direct_Link(BaseBetSlipTest):
    """
    TR_ID: C29102
    TR_ID: C18636114
    NAME: Verify Adding the Same Selections Several Times via Direct Link
    """
    keep_browser_open = True
    expected_outcome_names = []
    selection_ids_2 = None
    all_selection_ids = []

    def check_betslip(self, number_of_selections):
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(len(singles_section) > 0, msg='No stakes found in betslip Singles section')
        self.assertEqual(len(singles_section.keys()), number_of_selections,
                         msg=f'Should be "{number_of_selections}" stakes found but present "{len(singles_section.keys())}"')
        self.assertListEqual(self.expected_outcome_names, singles_section.keys(),
                             msg=f'Expected stakes are "{self.expected_outcome_names}" but present "{singles_section.keys()}"')
        self.__class__.expected_betslip_counter_value = 0

    def test_000_preconditions(self):
        """
        DESCRIPTION: Creating test events
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
            self.__class__.team1 = list(self.selection_ids.keys())[0]
            self._logger.info(f'*** Found Football event with selections "{self.selection_ids}"')

            # Races
            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                        expected_template_market='Win or Each Way')[0]

            for market in event['event']['children']:
                if market['market']['templateMarketName'] == 'Win or Each Way' and market['market'].get('children'):
                    outcomes = market['market']['children']
            self.__class__.selection_ids_2 = {i['outcome']['name'].replace('(','').replace(')',''): i['outcome']['id'] for i in outcomes}

        else:
            event_params1 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.selection_ids = event_params1.team1, event_params1.selection_ids

            self.__class__.selection_ids_2 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '1/2'}).selection_ids

        self.__class__.expected_outcome_names.append(self.team1.replace('(','').replace(')',''))
        self.__class__.all_selection_ids.append(self.selection_ids[self.team1])

        self.__class__.expected_outcome_names.append(list(self.selection_ids_2.keys())[0])
        self.__class__.all_selection_ids.append(list(self.selection_ids_2.values())[0])

    def test_001_login(self):
        """
        DESCRIPTION: Login to application
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)

    def test_002_open_betslip_via_deep_link(self):
        """
        DESCRIPTION: Enter direct URL with valid outcome id('s) in address bar -> press Enter key
        EXPECTED: Bet Slip with bet details is opened automatically
        EXPECTED: Entered selection(s) are added to the Bet Slip
        """
        self.open_betslip_with_selections(selection_ids=self.all_selection_ids)
        self.check_betslip(number_of_selections=2)

    def test_003_add_the_same_selections_to_the_bet_slip_via_direct_link(self):
        """
        DESCRIPTION: Open betslip via deeplink
        """
        self.open_betslip_with_selections(selection_ids=self.all_selection_ids)
        self.check_betslip(number_of_selections=2)

    def test_004_reload_bet_slip(self):
        """
        DESCRIPTION: Reload Bet Slip page
        EXPECTED: Same added selection(s) are present in the Bet Slip
        """
        self.reload_betslip()
        self.check_betslip(number_of_selections=2)

    def test_005_try_to_add_the_same_selections_several_times_via_direct_link(self):
        """
        DESCRIPTION: Try to add the same selection(s) several times via direct link
        EXPECTED: No matter how many times the same selection(s) are added to the Bet Slip -> Same added the first time selection(s) are present in the Bet Slip
        """
        selections = ''.join(['%s,' % selection for selection in self.all_selection_ids * 3])
        selections = selections.rstrip(',')
        url = f'https://{tests.HOSTNAME}/betslip/add/{selections}'
        self.device.navigate_to(url=url)
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_BETSLIP_FULL, timeout=2)
        if dialog:
            dialog.close_dialog()
            dialog.wait_dialog_closed()
        self.check_betslip(number_of_selections=2)

    def test_006_place_a_bet_for_added_selections(self):
        """
        DESCRIPTION: Place a bet for added selection(s)
        EXPECTED: Bet is placed successfully
        """
        self.place_single_bet(number_of_stakes=2)
        self.check_bet_receipt_is_displayed()

    def test_007_repeat_steps_for_just_one_outcome_id_in_direct_url(self):
        """
        DESCRIPTION: Repeat steps # 1-5 for just **ONE outcome id** in direct URL
        """
        self.__class__.expected_outcome_names = [self.team1]
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])
        self.check_betslip(number_of_selections=1)

        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])
        self.check_betslip(number_of_selections=1)

        self.reload_betslip()
        self.check_betslip(number_of_selections=1)

        selections = (self.selection_ids[self.team1] + ',') * 4
        self.device.navigate_to(url=f'https://{tests.HOSTNAME}/betslip/add/{selections}')
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_BETSLIP_FULL, timeout=2)
        if dialog:
            dialog.close_dialog()
            dialog.wait_dialog_closed()
        self.check_betslip(number_of_selections=1)

        self.place_single_bet(number_of_stakes=2)
        self.check_bet_receipt_is_displayed()
