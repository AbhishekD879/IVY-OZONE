import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.lad_prod
@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.other
@vtest
class Test_C16408286_Verify_my_Bets_counter_displaying_when_Bets_counter_is_turned_on_in_CMS(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C16408286
    NAME: Verify my Bets counter displaying when Bets counter is turned on in CMS
    DESCRIPTION: This test case verifies enabling Bet counter toggle in CMS
    PRECONDITIONS: 1. CMS-API Endpoints:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: 2. Make sure that development tool is opened once loading Oxygen/Ladbrokes app
    PRECONDITIONS: 3. Make sure to have a user with placed bets (open bets)
    """
    keep_browser_open = True

    def test_001__go_to_cms_and_navigate_to_system_configuration__structure__bet_counter_and_enable_toggle_save_changes(self):
        """
        DESCRIPTION: * Go to CMS and navigate to System configuration > Structure > Bet counter and enable toggle
        DESCRIPTION: * Save changes
        EXPECTED: - Changes are submitted successfully
        EXPECTED: - 'Bets counter' is enabled in CMS
        """
        if tests.settings.backend_env != 'prod':
            bets_counter = self.get_initial_data_system_configuration().get('BetsCounter')
            if not bets_counter:
                bets_counter = self.cms_config.get_system_configuration_item('BetsCounter')
            if not bets_counter.get('enabled'):
                self.cms_config.update_system_configuration_structure(config_item='BetsCounter',
                                                                      field_name='enabled',
                                                                      field_value=True)
        self.check_my_bets_counter_enabled_in_cms()

        if tests.settings.backend_env == 'prod':
            selections = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
            self.__class__.selection_ids = list(selections.values())[0]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_ids = event.selection_ids[event.team1]

    def test_002__load_coralladbrokes_app_and_login_with_user_from_preconditions_verify_that_my_bets_counter_is_displayed_on_footer(self):
        """
        DESCRIPTION: * Load Coral/Ladbrokes app and login with user from preconditions
        DESCRIPTION: * Verify that 'My Bets' counter is displayed on Footer
        EXPECTED: 'Bet counter' is displayed on the right top corner of 'My Bets' Footer Menu
        """
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_single_bet(number_of_stakes=1)
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state_changed()
        bets = self.site.navigation_menu.items_as_ordered_dict.get(vec.bet_history.TAB_TITLE)
        self.assertTrue(bets.has_indicator(expected_result=True),
                        msg=' "Bet Counter" is not displayed')