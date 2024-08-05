import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from voltron.utils.helpers import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot create events in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C9315085_Verify_that_Sorry_one_of_the_selections_cannot_be_boosted_please_remove_the_selection_and_try_again_error_message_is_shown_in_Betslip(BaseBetSlipTest):
    """
    TR_ID: C9315085
    NAME: Verify that "Sorry, one of the selections cannot be boosted, please remove the selection and try again." error message is shown in Betslip
    DESCRIPTION: This test case verifies that "Sorry, one of the selections cannot be boosted, please remove the selection and try again." error message is shown in Betslip in case if one of selections is not allowed for boost
    PRECONDITIONS: Load application and login by User with odds boost token ANY available
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token - instruction for generating tokens
    PRECONDITIONS: Back office https://backoffice-tst2.coral.co.uk/ti
    """
    keep_browser_open = True
    event_ids = []
    selection_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        """
        for _ in range(3):
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.event_ids.append(event_params.event_id)
            self.selection_ids.append(list(event_params.selection_ids.values())[0])

    def test_001_add_treble_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add Treble selections to the Betslip
        EXPECTED: Selections are added
        """
        username = tests.settings.betplacement_user
        self.ob_config.grant_odds_boost_token(username=username)
        self.site.login(username=username)
        self.open_betslip_with_selections(self.selection_ids)

    def test_002_add_stake_only_for_treble_selection__tap_boost_button(self):
        """
        DESCRIPTION: - Add stake only for Treble selection
        DESCRIPTION: - Tap 'Boost' button
        EXPECTED: Stake is added and boosted
        """
        sections = self.get_betslip_sections(multiples=True)
        multiples_section = sections.Multiples
        treble = multiples_section.get(vec.betslip.TBL)
        self.enter_stake_amount(stake=(treble.name, treble))
        odds_boost_header = self.site.betslip.odds_boost_header
        self.assertTrue(odds_boost_header.boost_button.is_displayed(), msg='Odds boost button is not displayed in betslip')
        odds_boost_header.boost_button.click()
        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

    def test_003_navigate_to_back_office_see_preconditions__open_event_for_the_first_selection_in_betslip__uncheck_enhanced_odds_available_check_box(self):
        """
        DESCRIPTION: - Navigate to Back Office (see preconditions)
        DESCRIPTION: - Open event for the first selection in Betslip
        DESCRIPTION: - Uncheck 'Enhanced Odds Available' check box
        EXPECTED: 'Enhanced Odds Available' is unchecked for the first selection in Betslip
        """
        self.ob_config.change_event_enhanced_odds_status(event_id=self.event_ids[0], enhanced_odds_available=False)

    def test_004_back_to_the_betslip_in_application__tap_bet_now_button_and_verify_that_error_message_is_displayed_on_the_betslip(self):
        """
        DESCRIPTION: - Back to the Betslip in application
        DESCRIPTION: - Tap 'Bet now' button and verify that error message is displayed on the betslip
        EXPECTED: Error message is displayed on the Betslip
        """
        self.site.betslip.bet_now_button.click()

    def test_005_verify_content_of_error_message(self):
        """
        DESCRIPTION: Verify content of error message
        EXPECTED: Text: "Sorry, one of the selections cannot be boosted, please remove the selection and try again."
        """
        wait_for_result(lambda: self.get_betslip_content().suspended_account_warning_message.is_displayed(),
                        name='Warning message not appeared', timeout=10)
        error_message = self.get_betslip_content().suspended_account_warning_message.text
        self.assertEqual(error_message, vec.quickbet.BET_PLACEMENT_ERRORS.odds_boost_not_allowed,
                         msg=f'Actual error message "{error_message}" is not same'
                             f'as Expected error message "{vec.quickbet.BET_PLACEMENT_ERRORS.odds_boost_not_allowed}"')
