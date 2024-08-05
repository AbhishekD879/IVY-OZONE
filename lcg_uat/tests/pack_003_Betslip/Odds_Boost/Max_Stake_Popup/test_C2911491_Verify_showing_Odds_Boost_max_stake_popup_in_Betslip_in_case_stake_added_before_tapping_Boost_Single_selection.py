import pytest
import tests
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Cannot grant odds boost and free bets.
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C2911491_Verify_showing_Odds_Boost_max_stake_popup_in_Betslip_in_case_stake_added_before_tapping_Boost_Single_selection(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C2911491
    NAME: Verify showing Odds Boost max stake popup in Betslip in case stake added before tapping Boost (Single selection)
    DESCRIPTION: This test case verifies that odds boost max stake popup is showing when stake is added and then BOOST button is tapped
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: CREATE and ADD Odds Boost tokens for USER1, where max redemption value = 50, use instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add selection with appropriate odds boost available to Betslip
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: User should have odds boost and add sp selection to bet slip
        EXPECTED: - Odds boost and selections are added.
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')

        username = tests.settings.default_username
        self.ob_config.grant_odds_boost_token(username=username, token_value=50)

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '4/1'}, sp=False)
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.eventID = event_params.event_id
        self.site.login(username)

    def test_001_navigate_to_betslipadd_a_stake_value_higher_then_max_redemption_value_stake_value__51verify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Add a Stake value higher then max redemption value (Stake value = 51)
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: BOOST button  is shown
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = 51
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(self.odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
        self.assertEqual(self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled,
                         msg='Button text label "%s" is not the same as expected "%s"' %
                             (self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled))

    def test_002_tap_boost_buttonverify_that_max_stake_popup_is_shown(self):
        """
        DESCRIPTION: Tap BOOST button
        DESCRIPTION: Verify that max stake popup is shown
        EXPECTED: Popup is shown with appropriate elements:
        EXPECTED: -  the hardcoded text:'The current total stake exceeds the Odds Boost max stake. Please adjust your total stake.' You can boost up to 50 (the max redemption value defined in the token in TI by default) of your total stake
        EXPECTED: - OK button
        """
        self.odds_boost_header.boost_button.click()
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_MAX_STAKE_EXCEEDED,
                                                          timeout=20)
        self.assertTrue(self.dialog, msg="Odss boost max stake dialog not appeared")
        message = self.dialog.description.replace('\n', " ")
        self.assertEqual(message, vec.odds_boost.MAX_STAKE_EXCEEDED.text,
                         msg=f'Actual message:"{message}" is not same as'
                             f'Expected message: "{vec.odds_boost.MAX_STAKE_EXCEEDED.text}".')
        self.assertTrue(self.dialog.has_ok_button(), msg='"Ok" button is not displayed.')

    def test_003_tap_ok_buttonverify_that_popup_is_closed_and_odds_is_not_boosted(self):
        """
        DESCRIPTION: Tap OK button
        DESCRIPTION: Verify that popup is closed and odds is NOT boosted
        EXPECTED: - Popup is closed
        EXPECTED: - BOOST button is shown
        EXPECTED: - Odds is NOT boosted
        """
        self.dialog.ok_button.click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP,
                                           timeout=20)
        self.assertFalse(dialog, msg="Odss boost max stake dialog  appeared")
        odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
                                 name=' "BOOST" button is shown',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button is not shown.')

        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake = list(singles_section.values())[0]
        self.assertFalse(self.stake.has_boosted_odds, msg='Boosted odds are shown')

    def test_004_edit_stake__and_set_it_equal_to_the_max_redemption_value_stake_value__50verify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Edit Stake  and set it equal to the max redemption value. (Stake value = 50)
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: BOOST button is shown
        """
        self.stake.amount_form.input.value = 50
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: self.odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
                                 name=' "BOOST" button is shown',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button is not shown.')

    def test_005_tap_boost_buttonverify_that_max_stake_popup_is_not_shown(self):
        """
        DESCRIPTION: Tap BOOST button
        DESCRIPTION: Verify that max stake popup is NOT shown
        EXPECTED: - Popup is NOT shown
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is shown as cross out
        """
        self.odds_boost_header.boost_button.click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_MAX_STAKE_EXCEEDED,
                                           timeout=20)
        self.assertFalse(dialog, msg="Odss boost max stake dialog not appeared")
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        self.assertTrue(stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
        self.assertTrue(stake.is_original_odds_crossed, msg='Original odds are not crossed out')
