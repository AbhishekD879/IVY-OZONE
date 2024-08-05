import pytest

from tests.base_test import vtest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.uk_tote
@pytest.mark.horseracing
@pytest.mark.liveserv_updates
@pytest.mark.races
@vtest
class Test_C2323040_Verify_Live_Updates_suspension_for_ExactaTrifecta_BetBuilder_on_HR_EDP(BaseUKTote):
    """
    TR_ID: C2323040
    NAME: Verify Live Updates (suspension) for Exacta/Trifecta BetBuilder on HR EDP
    DESCRIPTION: This test case verifies Live Updates (suspension) for Exacta/Trifecta BetBuilder on HR EDP
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [BMA-28915 UK Tote: Tote Bet Builder for Exacta Pool Type] [1]
    DESCRIPTION: [BMA-28445 UK Tote: Implement HR Trifecta pool type] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-28915
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-28445
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Exacta/Trifecta pool types is available for HR Event
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab) -> Exacta pool type
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True
    selection_id = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        ob_config = cls.get_ob_config()
        if cls.eventID:
            ob_config.change_event_state(event_id=cls.eventID, displayed=True, active=True)
        if cls.marketID:
            ob_config.change_market_state(event_id=cls.eventID, market_id=cls.marketID, displayed=True, active=True)
        if cls.selection_id:
            ob_config.change_selection_state(selection_id=cls.selection_id, displayed=True, active=True)

    def make_selection(self, tab_name, outcomes):
        counter = None
        selected_checkboxes = []

        if tab_name == vec.uk_tote.UK_TOTE_TABS.exacta:
            counter = 2
        elif tab_name == vec.uk_tote.UK_TOTE_TABS.trifecta:
            counter = 3

        for index, (outcome_name, outcome) in enumerate(outcomes[:counter]):
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            checkbox_name, checkbox = list(checkboxes.items())[index]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                        % (checkbox_name, outcome_name))
            selected_checkboxes.append(checkbox)
        return selected_checkboxes

    def get_selection_id(self, tab_name, event_id):
        counter = None
        if tab_name == vec.uk_tote.UK_TOTE_TABS.exacta:
            counter = 2
        elif tab_name == vec.uk_tote.UK_TOTE_TABS.trifecta:
            counter = 3

        ss_uk_tote_pool_outcomes = self.ss_req.ss_event_to_outcome_for_event(
            event_id=event_id)[0]['event']['children'][0]['market']['children']

        for index, (outcome_name, outcome) in enumerate(self.outcomes[:counter]):
            for element in ss_uk_tote_pool_outcomes:
                if element['outcome']['name'].strip('|') == outcome_name:
                    return element['outcome']['id']

    def wait_checkbox_to_become_active(self):
        outcome_name, outcome = self.outcomes[0]
        checkboxes = outcome.items_as_ordered_dict
        self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
        checkbox_name, checkbox = list(checkboxes.items())[0]

        return wait_for_result(lambda: checkbox.is_enabled() is True,
                               name='Checkbox to become enabled', timeout=15)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Navigate to EDP
        """
        event = self.get_uk_tote_event(uk_tote_exacta=True)
        self.__class__.eventID = event.event_id
        self.__class__.marketID = event.market_id

    def test_001_selecta_1_exacta_bet(self, tab_name=vec.uk_tote.UK_TOTE_TABS.exacta):
        """
        DESCRIPTION: Selecta 1 Exacta Bet
        EXPECTED: * Tote Bet Builder is appear
        EXPECTED: * 'ADD TO BETSLIP' button is an active
        """
        self.__class__.outcomes = self.get_single_leg_outcomes(tab_name=tab_name, event_id=self.eventID)
        self.__class__.checkboxes = self.make_selection(tab_name=tab_name, outcomes=self.outcomes)
        self.__class__.selection_id = self.get_selection_id(tab_name=tab_name, event_id=self.eventID)

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, self.__class__.section = list(sections.items())[0]

        result = wait_for_result(lambda: self.section.bet_builder.is_present(timeout=0) is True,
                                 name='Bet builder has not been shown', timeout=15)
        self.assertTrue(result, msg='Bet builder was not shown')

        self.assertTrue(self.section.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='"Add to betslip" button is not enabled')

    def test_002_suspend_one_selected_selection(self, tab_name=vec.uk_tote.UK_TOTE_TABS.exacta):
        """
        DESCRIPTION: Suspend one selected selection
        EXPECTED: * Suspended selection is unselected
        EXPECTED: * Active selection remains selected
        EXPECTED: * Tote Bet Builder is shown (with disabled 'ADD TO BETSLIP' button)
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, active=False, displayed=True)

        self.assertFalse(self.checkboxes[0].is_enabled(expected_result=False, timeout=50),
                         msg='Suspended selection checkbox was not suspended')
        self.assertFalse(self.checkboxes[0].is_selected(expected_result=False),
                         msg='Suspended selection checkbox was not unselected')
        self.assertTrue(self.checkboxes[1].is_selected(), msg='Not suspended selection checkbox was unselected')

        self.assertTrue(self.section.bet_builder.is_present(), msg='Bet builder is not present')
        self.assertFalse(self.section.bet_builder.summary.add_to_betslip_button.is_enabled(expected_result=False),
                         msg='"Add to betslip" button is enabled')

        self.checkboxes[1].click()
        if tab_name == vec.uk_tote.UK_TOTE_TABS.trifecta:
            self.checkboxes[2].click()
        self.ob_config.change_selection_state(selection_id=self.selection_id, active=True, displayed=True)

    def test_003_selecta_1_exacta_bet(self, tab_name=vec.uk_tote.UK_TOTE_TABS.exacta):
        """
        DESCRIPTION: Selecta 1 Exacta Bet
        EXPECTED: * 'ADD TO BETSLIP' button becomes enabled on Tote Bet Builder
        """
        self.__class__.checkboxes = self.make_selection(tab_name=tab_name, outcomes=self.outcomes)
        self.assertTrue(self.section.bet_builder.is_present(), msg='Bet builder is not present')
        self.assertTrue(self.section.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='"Add to betslip" button is not enabled')

    def test_004_suspend_current_market(self):
        """
        DESCRIPTION: Suspend current market
        EXPECTED: * All suspended selections are unselected
        EXPECTED: * Tote Bet Builder is disappeared
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=False)

        result = wait_for_result(lambda: self.section.bet_builder.is_present(timeout=0, expected_result=False) is False,
                                 name='Bet builder to become hidden', timeout=15)

        self.assertTrue(result, msg='Bet builder is still present')

        self.assertFalse(self.checkboxes[0].is_selected(expected_result=False),
                         msg='Suspended first selection checkbox was not unselected')
        self.assertFalse(self.checkboxes[1].is_selected(expected_result=False),
                         msg='Suspended second selection checkbox was not unselected')

    def test_005_make_the_market_active_again_and_select_1_exacta_bet(self, tab_name=vec.uk_tote.UK_TOTE_TABS.exacta):
        """
        DESCRIPTION: Make the market active again and Select 1 Exacta Bet
        EXPECTED: * Tote Bet Builder is appear
        EXPECTED: * 'ADD TO BETSLIP' button is an active
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)

        result = self.wait_checkbox_to_become_active()
        self.assertTrue(result, msg='Selections checkbox was not enabled')

        self.__class__.checkboxes = self.make_selection(tab_name=tab_name, outcomes=self.outcomes)

        result = wait_for_result(lambda: self.section.bet_builder.is_present(timeout=0) is True,
                                 name='Bet builder to become displayed', timeout=15)
        self.assertTrue(result, msg='Bet builder was not shown')
        self.assertTrue(self.section.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='"Add to betslip" button is not enabled')

    def test_006_suspend_current_event(self):
        """
        DESCRIPTION: Suspend current event
        EXPECTED: * All suspended selections are unselected
        EXPECTED: * Tote Bet Builder is disappeared
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)

        result = wait_for_result(lambda: self.section.bet_builder.is_present(timeout=0, expected_result=False),
                                 expected_result=False,
                                 name='Bet builder to become displayed', timeout=15)
        self.assertFalse(result, msg='Bet builder has not disappeared')

        self.assertFalse(self.checkboxes[0].is_selected(expected_result=False, timeout=4),
                         msg='First suspended selection checkbox was not unselected')
        self.assertFalse(self.checkboxes[1].is_selected(expected_result=False),
                         msg='Second suspended selection checkbox was not unselected')

    def test_007_make_the_event_active_again_and_select_1_exacta_bet(self, tab_name=vec.uk_tote.UK_TOTE_TABS.exacta):
        """
        DESCRIPTION: Make the event active again and Select 1 Exacta Bet
        EXPECTED: * Tote Bet Builder is appear
        EXPECTED: * 'ADD TO BETSLIP' button is an active
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

        result = self.wait_checkbox_to_become_active()
        self.assertTrue(result, msg='Selections checkbox was not enabled')

        self.__class__.checkboxes = self.make_selection(tab_name=tab_name, outcomes=self.outcomes)

        result = wait_for_result(lambda: self.section.bet_builder.is_present(timeout=0) is True,
                                 name='Bet builder to become displayed', timeout=15)
        self.assertTrue(result, msg='Bet builder was not shown')

    def test_008_suspend_current_exacta_pool(self):
        """
        DESCRIPTION: Suspend current Exacta pool
        EXPECTED: * All suspended selections are unselected
        EXPECTED: * Tote Bet Builder is disappeared
        """
        pass  # cannot automate

    def test_009_repeat_steps_1_9_for_1_trifecta_bet(self):
        """
        DESCRIPTION: Repeat steps 1-9 for 1 Trifecta Bet
        EXPECTED:
        """
        self.custom_tearDown()

        event = self.get_uk_tote_event(uk_tote_trifecta=True)
        self.__class__.eventID = event.event_id
        self.__class__.marketID = event.market_id

        self.test_001_selecta_1_exacta_bet(tab_name=vec.uk_tote.UK_TOTE_TABS.trifecta)
        self.test_002_suspend_one_selected_selection(tab_name=vec.uk_tote.UK_TOTE_TABS.trifecta)
        self.test_003_selecta_1_exacta_bet(tab_name=vec.uk_tote.UK_TOTE_TABS.trifecta)
        self.test_004_suspend_current_market()
        self.test_005_make_the_market_active_again_and_select_1_exacta_bet(tab_name=vec.uk_tote.UK_TOTE_TABS.trifecta)
        self.test_006_suspend_current_event()
        self.test_007_make_the_event_active_again_and_select_1_exacta_bet(tab_name=vec.uk_tote.UK_TOTE_TABS.trifecta)
