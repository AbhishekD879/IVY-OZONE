import pytest
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
import tests
from voltron.utils.helpers import normalize_name


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod # For Prod users, acca offer has to be granted from OB
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.acca
@pytest.mark.mobile_only
@pytest.mark.login
@vtest
class Test_C16367455_Verify_ACCA_Insurance_when_user_is_qualified_for_the_offer(BaseCashOutTest, BaseSportTest):
    """
    TR_ID: C16367455
    VOL_ID: C23657383
    NAME: Verify ACCA Insurance when user is qualified for the offer
    DESCRIPTION: Test case verifies ACCA Insurance presence when logged in user is qualified for the offer.
    PRECONDITIONS: * ACCA Insurance offer is configured through Openbet TI.
    PRECONDITIONS: * There are events with selections applicable for ACCA Offers(events from category "Football" and market "Match Result")
    PRECONDITIONS: * For configuration ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: * To verify ACCA Offer details please check requests in dev tools requests: BuildBet -> betOfferRef -> betTypeRef
    PRECONDITIONS: * 'superAcca' checkbox is checked in CMS -> System Configuration -> Structure -> 'Betslip' section
    PRECONDITIONS: * Oxygen app is opened and user is logged in.
    PRECONDITIONS: In this current case, TI offer was configured for 'eligible' response when 5 applicable selections were added into Betslip. (number is set through the trigger within the offer).
    """
    keep_browser_open = True

    def open_betslip_with_selections(self, selection_ids, timeout: int = 0):  # to avoid all the waits
        expected_betslip_counter_value = 1 if isinstance(selection_ids, str) else len(selection_ids)
        selections = selection_ids if expected_betslip_counter_value == 1 else ','.join(selection_ids)
        url = f'{tests.HOSTNAME}/betslip/add/{selections}'
        self.device.navigate_to(url=url)

        self.verify_betslip_counter_change(expected_value=expected_betslip_counter_value)

    def verify_acca_insurance_offer(self, acca_type):
        betslip_content = self.site.betslip
        actual_message = betslip_content.top_notification.error
        if actual_message == '':
            betslip_content.close_button.click()
            self.site.header.bet_slip_counter.click()
            actual_message = betslip_content.top_notification.error

        expected_message = vec.betslip.ACCA_INSURANCE_QUALIFY_MSG
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual: "{actual_message}" and expected: "{expected_message}" messages does not match')
        self.assertFalse(betslip_content.top_notification.wait_for_error(expected_result=False, timeout=6),
                         msg='Acca Insurance Qualify message is not disappeared')
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(acca_type, sections.keys(),
                      msg=f'No "{acca_type}" stake was found in "{sections.keys()}"')
        stake = list(sections.values())[0]
        self.assertTrue(stake.has_acca_insurance_icon(), msg='Acca Insurance Icon is not displayed')
        self.assertEqual(stake.market_name, vec.betslip.ACCA_INSURANCE,
                         msg=f'Actual Bet summary info "{stake.market_name}" does not match expected "{vec.betslip.ACCA_INSURANCE}"')
        self.assertTrue(stake.information_button.is_displayed(), msg='"Info" icon/button is not shown')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify ACCA Insurance when the user is not qualified yet for the offer for logged in user (Ladbrokes)
        PRECONDITIONS: 'superAcca' checkbox is checked in CMS -> System Configuration -> Structure -> 'Betslip' section
        PRECONDITIONS: Oxygen app is opened and user is logged in
        PRECONDITIONS: Create test events
        """
        betslip_config = self.get_initial_data_system_configuration().get('Betslip', {})
        if not betslip_config:
            betslip_config = self.cms_config.get_system_configuration_item('Betslip')
        if not betslip_config.get('superAcca'):
            self.cms_config.set_super_acca_toggle_component_status(super_acca_component_status=True)
        event_params = self.create_several_autotest_premier_league_football_events(number_of_events=5)
        self.__class__.selection_ids = [list(event.selection_ids.values())[0] for event in event_params]
        self.__class__.race_event = self.ob_config.add_UK_racing_event().selection_ids
        self.__class__.football_event = self.ob_config.add_autotest_premier_league_football_event()
        market_name = normalize_name(self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
        self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)
        self.site.login(async_close_dialogs=False)

    def test_001_add_5_selections_applicable_for_acca_insurance_offer_from_football_match_result_market(self):
        """
        DESCRIPTION: Add certain number of selections applicable for ACCA Insurance offer from Football - Match Result market into the Betslip (in our case it will be 5)
        EXPECTED: Betslip counter is increased by a number of added selections
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_open_betslip_and_view_xhr_requests_responses_for_it(self):
        """
        DESCRIPTION: Open Betslip and view XHR requests/responses for it
        EXPECTED: * Selections are present to betslip
        EXPECTED: * **'offerType:elligible'** is shown in 'buildBet' response in Dev Tools
        EXPECTED: * '5 Fold ACCA' bet is present within 'Multiple' section
        EXPECTED: * '5 Fold ACCA' row contains:
        EXPECTED: - (5+) icon;
        EXPECTED: - 'Acca Insurance' label;
        EXPECTED: - 'i' icon
        EXPECTED: * Signposting message is shown at the header of betslip for 5 seconds and disappears - text of the message is: "Your selections qualify for Acca Insurance"
        """
        self.verify_acca_insurance_offer(acca_type=vec.betslip.ACC5)

    def test_003_add_1_more_selection_which_is_not_applicable_for_acca_insurance_offer_into_the_betslip(self):
        """
        DESCRIPTION: Add 1 more selection which is not applicable for ACCA Insurance offer into the Betslip
        DESCRIPTION: (Not applicable selections are: HR/GR selections; Selections from Live events; Selections from same event that is applicable, but one selection is already used from it).
        EXPECTED: * Betslip counter is increased by 1
        EXPECTED: * Selection is added to betslip
        """
        self.selection_ids.append(list(self.race_event.values())[0])
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_004_open_betslip_and_view_xhr_requests_responses_for_it(self):
        """
        DESCRIPTION: Open Betslip and view XHR requests/responses for it
        EXPECTED: * No 'betOfferRef' is received in 'buildBet' response in Dev Tools
        EXPECTED: * Signposting message is not shown at the header of betslip
        EXPECTED: * Labels within row are: '# Fold ACCA' and 'Accumulator Bet'
        """
        self.assertFalse(self.site.betslip.top_notification.wait_for_error(expected_result=False),
                         msg='Acca Insurance Qualify signposting message is displayed')
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.ACC6, sections.keys(),
                      msg=f'No "{vec.betslip.ACC6}" stake was found in "{sections.keys()}"')
        multiple_stake = sections.get(vec.betslip.ACC6)
        self.assertEqual(multiple_stake.market_name, vec.betslip.ACC_INFO,
                         msg=f'Actual Bet summary info "{multiple_stake.market_name}" '
                             f'does not match expected "{vec.betslip.ACC_INFO}"')

    def test_005_remove_the_not_applicable_selection_from_betslip(self):
        """
        DESCRIPTION: Remove the *not applicable* selection from Betslip
        EXPECTED: * Betslip counter is decreased by 1
        EXPECTED: * The expected result matches the ER from step #2
        """
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[5]
        stake.remove_button.click()
        self.assertEquals(self.get_betslip_content().selections_count, '5',
                          msg=f'Selections count "{self.get_betslip_content().selections_count}" '
                          f'is not the same as expected "5"')
        self.verify_acca_insurance_offer(acca_type=vec.betslip.ACC5)

    def test_006_add_1_more_selection_applicable_for_acca_insurance_offer_from_football_match_result_market_into_the_betslip(self):
        """
        DESCRIPTION: Add 1 more selection *applicable* for ACCA Insurance offer from Football - Match Result market into the Betslip
        EXPECTED: Betslip counter is increased by 1
        """
        self.navigate_to_edp(event_id=self.football_event.event_id)
        bet_button = self.get_selection_bet_button(market_name=self.expected_market)
        bet_button.click()
        self.site.header.bet_slip_counter.click()
        self.assertEqual(self.get_betslip_content().selections_count, '6',
                         msg=f'Selections count "{self.get_betslip_content().selections_count}" '
                         f'is not the same as expected "6"')

    def test_007_open_betslip_and_view_xhr_requests_responses_for_it(self):
        """
        DESCRIPTION: Open Betslip and view XHR requests/responses for it
        EXPECTED: * Expected result matches ER from step #2
        EXPECTED: * Label within row is shown as: '6 Fold ACCA'
        """
        self.verify_acca_insurance_offer(acca_type=vec.betslip.ACC6)

    def test_008_enter_value_into_the_stake_field_of_6_fold_acca_row_and_place_bet(self):
        """
        DESCRIPTION: Enter value that doesn't exceed your user's current balance into the 'Stake' field of '6 Fold ACCA' row and 'Place Bet'
        EXPECTED: * Bet Receipt modal is shown
        EXPECTED: * Bet is successfully placed.
        """
        self.place_multiple_bet(stake_name=vec.betslip.ACC6)
        self.check_bet_receipt_is_displayed()
