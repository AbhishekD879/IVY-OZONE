import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod  # cannot create CMS modules on prod
@pytest.mark.featured
@pytest.mark.ob_smoke
@pytest.mark.module_ribbon
@pytest.mark.homepage
@pytest.mark.cms
@pytest.mark.bet_placement
@pytest.mark.login
@vtest
class Test_at_verifying_bets_from_featured_tab(BaseFeaturedTest, BaseBetSlipTest):
    """
    VOL_ID: C9697833
    NAME: Verifying bets from Featured tab
    """
    keep_browser_open = True
    output_prices = None
    module_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event and add it to Featured Module
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.event_name = events['event']['name']
            type_id = events['event']['typeId']
            self.__class__.team1, self.__class__.team2 = (events['event']['name']).split(' v ')
            match_result_market = next((market['market'] for market in events['event']['children']
                                        if market['market'].get('children')), None)
            if not match_result_market:
                raise SiteServeException('No available markets')
            outcomes = match_result_market.get('children')
            if not outcomes:
                raise SiteServeException('No available outcomes')
            self.__class__.selection_ids = {normalize_name(i['outcome']['name']): i['outcome']['id'] for i in outcomes}
        else:
            type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id
            start_time = self.get_date_time_formatted_string(hours=3)
            event_params = self.ob_config.add_football_event_to_featured_autotest_league(start_time=start_time)
            self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2
            self.__class__.event_name = f'{self.team1} v {self.team2}'
            self.__class__.selection_ids = event_params.selection_ids

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            show_all_events=True, select_event_by='Type', id=type_id)['title'].upper()

    def test_001_login(self):
        """
        DESCRIPTION: Login
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False, timeout_close_dialogs=10)

    def test_002_tap_featured_tab(self):
        """
        DESCRIPTION: Tap '<Featured> tab'
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)

    def test_003_make_selection(self):
        """
        DESCRIPTION: Make Multi selections. Verify that Betslip counter == 2
        """
        module_content = self.site.home.get_module_content(
            module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))

        sections = module_content.accordions_list.items_as_ordered_dict

        self.assertIn(self.module_name, sections, msg=f'"{self.module_name}" module is not in sections')
        self.__class__.section = sections[self.module_name]

        bet_button = self.section.get_bet_button_by_selection_id(selection_id=self.selection_ids[self.team1])

        self.assertTrue(bet_button,
                        msg=f'"{self.team1}" selection bet button is not found within module "{self.module_name}"')
        bet_button.click()

        self.site.add_first_selection_from_quick_bet_to_betslip()

        self.verify_betslip_counter_change(expected_value=1)

        bet_button2 = self.section.get_bet_button_by_selection_id(selection_id=self.selection_ids[self.team2])
        self.assertTrue(bet_button2,
                        msg=f'"{self.team2}" selection bet button is not found within module "{self.module_name}"')
        bet_button2.click()

        self.verify_betslip_counter_change(expected_value=2)

    def test_004_deselect_all_selections(self):
        """
        DESCRIPTION: Remove all selections. Verify that Betslip counter == 0
        """
        bet_button = self.section.get_bet_button_by_selection_id(selection_id=self.selection_ids[self.team1])
        bet_button2 = self.section.get_bet_button_by_selection_id(selection_id=self.selection_ids[self.team2])
        self.assertTrue(bet_button,
                        msg=f'"{self.team1}" selection bet button is not found within module "{self.module_name}"')
        self.assertTrue(bet_button2,
                        msg=f'"{self.team2}" selection bet button is not found within module "{self.module_name}"')
        bet_button.click()
        self.assertFalse(bet_button.is_selected(expected_result=False),
                         msg=f'"{self.team1}" selection bet button is still selected')
        bet_button2.click()
        self.assertFalse(bet_button2.is_selected(expected_result=False),
                         msg=f'"{self.team2}" selection bet button is still selected')

        self.verify_betslip_counter_change(expected_value=0)

    def test_005_make_single_selection(self):
        """
        DESCRIPTION: Make single selection. Verify that Betslip counter == 1
        """
        bet_button = self.section.get_bet_button_by_selection_id(selection_id=self.selection_ids[self.team1])
        self.assertTrue(bet_button,
                        msg=f'"{self.team1}" selection bet button is not found within module "{self.module_name}"')
        bet_button.click()
        self.site.add_first_selection_from_quick_bet_to_betslip()

        self.verify_betslip_counter_change(expected_value=1)

    def test_006_go_to_betslip(self):
        """
        DESCRIPTION: Go to the BetSlip and place bet. Verify that Betslip counter decrease to 0
        """
        self.site.header.bet_slip_counter.click()
        self.place_single_bet()

        self.site.bet_receipt.footer.click_done()

        self.device.navigate_to(url=f'https://{tests.HOSTNAME}/')
        self.site.wait_splash_to_hide()
        self.site.close_all_dialogs(async_close=False, timeout=0.5)

        self.verify_betslip_counter_change(expected_value=0)
