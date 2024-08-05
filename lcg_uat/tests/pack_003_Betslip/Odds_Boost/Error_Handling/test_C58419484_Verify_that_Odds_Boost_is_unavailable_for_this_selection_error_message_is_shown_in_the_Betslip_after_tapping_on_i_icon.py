import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't grant odds boost on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C58419484_Verify_that_Odds_Boost_is_unavailable_for_this_selection_error_message_is_shown_in_the_Betslip_after_tapping_on_i_icon(BaseBetSlipTest):
    """
    TR_ID: C58419484
    NAME: Verify that "Odds Boost is unavailable for this selection' error message is shown in the Betslip after tapping on 'i' icon"
    DESCRIPTION: This test case verifies that "Odds Boost is unavailable for this selection' error message is shown in the Betslip after tapping on 'i' icon"
    PRECONDITIONS: Load application and login with User with odds boost token ANY available
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token - instruction for generating tokens
    PRECONDITIONS: OpenBet Systems: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    """
    keep_browser_open = True
    prices = {0: '4/12', 1: '5/14'}
    bet_amount = 0.11
    username = tests.settings.betplacement_user

    def test_000_precondition(self):
        """
        DESCRIPTION: "Odds Boost" Feature Toggle is enabled in CMS
        DESCRIPTION: CREATE Odds Boost token with ANY Bet Type
        DESCRIPTION: Login with USER1
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')
        self.ob_config.grant_odds_boost_token(username=self.username)

        event_params1 = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1,
                                                           lp_prices=self.prices)
        event_params2 = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1,
                                                           lp_prices=self.prices)
        self.__class__.selection_id1 = (list(event_params1.selection_ids.values())[0])
        self.__class__.selection_id2 = (list(event_params2.selection_ids.values())[0])
        event_params3 = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1)
        self.__class__.selection_id3 = (list(event_params3.selection_ids.values())[0])
        self.navigate_to_page('Homepage')
        self.site.login(username=self.username)
        self.site.wait_content_state('HomePage')

    def test_001_add_three_selections_to_the_betslip__add_selection_hr_with_sp_only_available_selection_1__add_selection_hr_with_lp_and_sp_available_selection_2_and_lp_price_is_selected__add_selection_hr_with_lp_and_sp_available_selection_3_and_lp_price_is_selected(self):
        """
        DESCRIPTION: Add three selections to the Betslip:
        DESCRIPTION: - Add selection (HR) with SP only available (Selection_1)
        DESCRIPTION: - Add selection (HR) with LP and SP available (Selection_2) and LP price is selected
        DESCRIPTION: - Add selection (HR) with LP and SP available (Selection_3) and LP price is selected
        EXPECTED: Selections are added
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id1, self.selection_id2, self.selection_id3))

    def test_002_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        EXPECTED: Selections are added and not boosted
        """
        sections = self.get_betslip_sections()
        self.__class__.singles_section = sections.Singles

    def test_003_add_stake_for_the_selection_1_and_tap_a_boost_button(self):
        """
        DESCRIPTION: Add Stake for the Selection_1 and tap a 'BOOST' button
        EXPECTED: 'i' icon appears next to Selection_1
        """
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections.keys(), msg=f'"{selections}" is not added to the betslip')
        stake_name, self.__class__.stake = list(selections.items())[0]
        self.enter_stake_amount(stake=(stake_name, self.stake))

        odds_boost_header = self.get_betslip_content().odds_boost_header
        odds_boost_header.boost_button.click()
        for stake_name, stake in self.singles_section.items():
            if stake.odds == 'SP':
                self.assertTrue(stake.odds_boost_info_icon.is_displayed(), msg='i icon is not shown')
                stake.odds_boost_info_icon.click()
                self.assertTrue(stake.has_odds_boost_tooltip(), msg='Odds Boost is unavailable for this selection')
            else:
                self.assertTrue(stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')

    def test_004_tap_i_icon_for_selection_1(self):
        """
        DESCRIPTION: Tap 'i' icon for Selection_1
        EXPECTED: 'Odds Boost is unavailable for this selection' is shown in the Betslip after tapping on 'i' icon
        EXPECTED: ![](index.php?/attachments/get/101624594)
        """
        # covered in above step
