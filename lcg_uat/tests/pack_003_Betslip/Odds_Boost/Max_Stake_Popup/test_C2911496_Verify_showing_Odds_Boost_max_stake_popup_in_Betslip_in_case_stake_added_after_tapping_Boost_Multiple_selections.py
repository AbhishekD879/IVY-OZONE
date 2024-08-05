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
# @pytest.mark.prod #Cannot grant odds boost
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C2911496_Verify_showing_Odds_Boost_max_stake_popup_in_Betslip_in_case_stake_added_after_tapping_Boost_Multiple_selections(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C2911496
    NAME: Verify showing Odds Boost max stake popup in Betslip in case stake added after tapping Boost (Multiple selections)
    DESCRIPTION: This test case verifies that odds boost max stake popup is showing when BOOST button is tapped and then stake is added for multiple selections
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: CREATE and ADD Odds Boost tokens for USER1, where max redemption value = 50, use instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add TWO selections with appropriate odds boost available to Betslip
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
        event_params_2 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '3/1'}, sp=False)
        event_params_3 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '5/1'}, sp=False)
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.selection_id_2 = list(event_params_2.selection_ids.values())[0]
        self.__class__.selection_id_3 = list(event_params_3.selection_ids.values())[0]
        self.site.login(username)

    def test_001_navigate_to_betslipverify_that_odds_boost_section_is_shown(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that odds boost section is shown
        EXPECTED: BOOST button is shown
        """
        self.open_betslip_with_selections(selection_ids=[self.selection_id, self.selection_id_2])
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(self.odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
        self.assertEqual(self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled,
                         msg='Button text label "%s" is not the same as expected "%s"' %
                             (self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled))

    def test_002_tap_boost_buttonverify_that_odds_are_boosted(self):
        """
        DESCRIPTION: Tap BOOST button
        DESCRIPTION: Verify that odds are boosted
        EXPECTED: - Boosted odds is shown for SINGLES and DOUBLE
        EXPECTED: - Original odds is shown as cross out for SINGLES and DOUBLE
        """
        self.odds_boost_header.boost_button.click()
        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiple_sections = sections.Singles, sections.Multiples
        self.assertTrue(singles_section.items(), msg='No Single stakes found')
        self.assertTrue(multiple_sections.items(), msg='No multiple stakes found')
        self.__class__.single_1 = list(singles_section.values())[0]
        self.__class__.single_2 = list(singles_section.values())[1]
        self.__class__.double = list(multiple_sections.values())[0]
        self.assertTrue(self.single_1.boosted_odds_container.is_displayed(),
                        msg='Boosted odds are not shown for single_1')
        self.assertTrue(self.single_1.is_original_odds_crossed,
                        msg='Original odds are not crossed out shown for single_1')
        self.assertTrue(self.single_2.boosted_odds_container.is_displayed(),
                        msg='Boosted odds are not shown for single_2')
        self.assertTrue(self.single_2.is_original_odds_crossed, msg='Original odds are not crossed out for single_2')
        self.assertTrue(self.double.boosted_odds_container.is_displayed(),
                        msg='Boosted odds are not shown for double')
        self.assertTrue(self.double.is_original_odds_crossed, msg='Original odds are not crossed out for double')

    def test_003_add_a_stakes__for_selections_that_will_be_lower_or_equal_to_max_redemption_value__50__50single1__12single2__18double__20verify_that_max_stake_popup_is_not_shown(self):
        """
        DESCRIPTION: Add a Stakes  for selections that will be lower or equal to max redemption value ( 50 = 50):
        DESCRIPTION: Single1 = 12
        DESCRIPTION: Single2 = 18
        DESCRIPTION: Double = 20
        DESCRIPTION: Verify that max stake popup is NOT shown
        EXPECTED: - Popup is NOT shown
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is shown as cross out
        """
        self.single_1.amount_form.input.value = 12
        self.single_2.amount_form.input.value = 18
        self.double.amount_form.input.value = 20
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP,
                                           timeout=20)
        self.assertFalse(dialog, msg="Odss boost max stake dialog  appeared")
        self.assertTrue(self.single_1.boosted_odds_container.is_displayed(),
                        msg='Boosted odds are not shown for single_1')
        self.assertTrue(self.single_1.is_original_odds_crossed,
                        msg='Original odds are not crossed out shown for single_1')
        self.assertTrue(self.single_2.boosted_odds_container.is_displayed(),
                        msg='Boosted odds are not shown for single_2')
        self.assertTrue(self.single_2.is_original_odds_crossed, msg='Original odds are not crossed out for single_2')
        self.assertTrue(self.double.boosted_odds_container.is_displayed(),
                        msg='Boosted odds are not shown for double')
        self.assertTrue(self.double.is_original_odds_crossed, msg='Original odds are not crossed out for double')

    def test_004_add_one_more_selection_with_appropriate_odds_boost_availableenter_stake_value_for_the_selection_stake__1_and_treble__21verify_that_max_stake_popup_is_shown(self):
        """
        DESCRIPTION: Add one more selection with appropriate odds boost available
        DESCRIPTION: Enter stake value for the selection (Stake = 1 and TREBLE = 21)
        DESCRIPTION: Verify that max stake popup is shown
        EXPECTED: Popup is shown with appropriate elements:
        EXPECTED: - the hardcoded text:'The current total stake exceeds the Odds Boost max stake.
                    Please adjust your total stake.' You can boost up to 50 (the max redemption value defined in the
                    token in TI by default) of your total stake
        EXPECTED: - OK button
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id_3)
        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiple_sections = sections.Singles, sections.Multiples
        self.assertTrue(singles_section.items(), msg='No Single stakes found')
        self.assertTrue(multiple_sections.items(), msg='No multiple stakes found')
        single_3 = list(singles_section.values())[2]
        treble = list(multiple_sections.values())[0]
        single_3.amount_form.input.value = 1
        treble.amount_form.input.value = 21

        self.__class__.dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_MAX_STAKE_EXCEEDED,
            timeout=20)
        self.assertTrue(self.dialog, msg="Odss boost max stake dialog not appeared")
        message = self.dialog.description.replace('\n', " ")
        self.assertEqual(message, vec.odds_boost.MAX_STAKE_EXCEEDED.text,
                         msg=f'Actual message:"{message}" is not same as'
                             f'Expected message: "{vec.odds_boost.MAX_STAKE_EXCEEDED.text}".')
        self.assertTrue(self.dialog.has_ok_button(), msg='"Ok" button is not displayed.')

    def test_005_tap_ok_buttonverify_that_popup_is_closed_and_odds_boost_is_deselected(self):
        """
        DESCRIPTION: Tap OK button
        DESCRIPTION: Verify that popup is closed and odds boost is deselected
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

        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiple_sections = sections.Singles, sections.Multiples
        self.assertTrue(singles_section.items(), msg='No Single stakes found')
        self.assertTrue(multiple_sections.items(), msg='No multiple stakes found')
        single_1 = list(singles_section.values())[0]
        single_2 = list(singles_section.values())[1]
        single_3 = list(singles_section.values())[2]
        treble = list(multiple_sections.values())[0]
        self.assertFalse(single_1.has_boosted_odds, msg='Boosted odds are shown for selection1')
        self.assertFalse(single_2.has_boosted_odds, msg='Boosted odds are shown for selection2')
        self.assertFalse(single_3.has_boosted_odds, msg='Boosted odds are shown for selection3')
        self.assertFalse(treble.has_boosted_odds, msg='Boosted odds are shown for treble')
