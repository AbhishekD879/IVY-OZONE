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
class Test_C2322261_Verify_Live_Updates_suspension_for_ExactaTrifecta_pool_types_on_HR_EDP(BaseUKTote):
    """
    TR_ID: C2322261
    NAME: Verify Live Updates (suspension) for Exacta/Trifecta pool types on HR EDP
    DESCRIPTION: This test case verifies Live Updates (suspension) for Exacta/Trifecta pool types on HR EDP
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [UK Tote: Implement HR Exacta pool type] [1]
    DESCRIPTION: [UK Tote: Implement HR Trifecta pool type] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-28444
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-28445
    PRECONDITIONS: * The HR event should have Exacta and Trifecta pool types available
    PRECONDITIONS: * User should have a HR EDP with Exacta pool type open ("Tote" tab)
    """
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls, **kwargs):
        ob_config = cls.get_ob_config()
        if cls.eventID:
            ob_config.change_event_state(event_id=cls.eventID, displayed=True, active=True)
        if cls.marketID:
            ob_config.change_market_state(event_id=cls.eventID, market_id=cls.marketID, displayed=True, active=True)
        if cls.selection_id:
            ob_config.change_selection_state(selection_id=cls.selection_id, displayed=True, active=True)

    def get_selection_id(self, event_id, outcomes):

        ss_uk_tote_pool_outcomes = self.ss_req.ss_event_to_outcome_for_event(
            event_id=event_id)[0]['event']['children'][0]['market']['children']

        for index, (outcome_name, outcome) in enumerate(outcomes):
            for element in ss_uk_tote_pool_outcomes:
                if element['outcome']['name'].strip('|') == outcome_name:
                    return element['outcome']['id']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event id
        """
        event = self.get_uk_tote_event(uk_tote_exacta=True)
        self.__class__.eventID = event.event_id
        self.__class__.marketID = event.market_id
        self.__class__.outcomes = self.get_single_leg_outcomes(event_id=self.eventID,
                                                               tab_name=vec.uk_tote.UK_TOTE_TABS.exacta)
        self.__class__.selection_id = self.get_selection_id(event_id=self.eventID, outcomes=self.outcomes)

    def test_001_suspend_current_event_in_ti(self):
        """
        DESCRIPTION: Suspend current event in TI
        EXPECTED: All Exacta check boxes become disabled in real time
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)

        self.__class__.outcome_name, self.__class__.outcome = self.outcomes[0]
        self.__class__.checkbox_name, self.__class__.checkbox = list(self.outcome.items_as_ordered_dict.items())[0]

        result = wait_for_result(lambda: self.checkbox.is_enabled(expected_result=False, timeout=0),
                                 expected_result=False,
                                 name='Checkbox to become disabled', timeout=30)

        self.assertFalse(result, msg=f'{self.checkbox_name} checkbox of {self.outcome_name} outcome was not disabled')

        for outcome_name, outcome in self.outcomes:
            for checkbox_name, checkbox in outcome.items_as_ordered_dict.items():
                self.assertFalse(checkbox.is_enabled(expected_result=False, timeout=4),
                                 msg=f'{checkbox_name} checkbox of {outcome_name} outcome was not disabled')

    def test_002_make_the_event_active_again_in_ti(self):
        """
        DESCRIPTION: Make the event active again in TI
        EXPECTED: All Exacta check boxes become active in real time
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

        result = wait_for_result(lambda: self.checkbox.is_enabled(timeout=0),
                                 name='Checkbox to become enabled', timeout=30)

        self.assertTrue(result, msg=f'{self.checkbox_name} checkbox of {self.outcome_name} outcome was not disabled')

        for outcome_name, outcome in self.outcomes:
            for checkbox_name, checkbox in outcome.items_as_ordered_dict.items():
                self.assertTrue(checkbox.is_enabled(),
                                msg=f'{checkbox_name} checkbox of {outcome_name} outcome was not enabled')

    def test_003_suspend_market_from_current_event_in_ti(self):
        """
        DESCRIPTION: Suspend market from current event in TI
        EXPECTED: All Exacta check boxes become disabled in real time
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=False)
        result = wait_for_result(lambda: self.checkbox.is_enabled(expected_result=False, timeout=0),
                                 expected_result=False,
                                 name='Checkbox to become disabled', timeout=30)

        self.assertFalse(result, msg=f'{self.checkbox_name} checkbox of {self.outcome_name} outcome was not disabled')

        for outcome_name, outcome in self.outcomes:
            for checkbox_name, checkbox in outcome.items_as_ordered_dict.items():
                self.assertFalse(checkbox.is_enabled(expected_result=False),
                                 msg=f'{checkbox_name} checkbox of {outcome_name} outcome was not disabled')

    def test_004_make_the_market_active_again_in_ti(self):
        """
        DESCRIPTION: Make the market active again in TI
        EXPECTED: All Exacta check boxes become active in real time
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        result = wait_for_result(lambda: self.checkbox.is_enabled(timeout=0),
                                 name='Checkbox to become enabled', timeout=30)

        self.assertTrue(result, msg=f'{self.checkbox_name} checkbox of {self.outcome_name} outcome was not disabled')

        for outcome_name, outcome in self.outcomes:
            for checkbox_name, checkbox in outcome.items_as_ordered_dict.items():
                self.assertTrue(checkbox.is_enabled(),
                                msg=f'{checkbox_name} checkbox of {outcome_name} outcome was not enabled')

    def test_005_suspend_one_or_more_selections_from_current_event_in_ti(self):
        """
        DESCRIPTION: Suspend one or more selections from current event in TI
        EXPECTED: Particular suspended Exacta check boxes become disabled in real time
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, active=False, displayed=True)

        result = wait_for_result(lambda: self.checkbox.is_enabled(expected_result=False, timeout=0),
                                 expected_result=False,
                                 name='Checkbox to become disabled', timeout=30)

        self.assertFalse(result, msg=f'{self.checkbox_name} checkbox of {self.outcome_name} outcome was not disabled')

        for checkbox_name, checkbox in self.outcome.items_as_ordered_dict.items():
            self.assertFalse(checkbox.is_enabled(expected_result=False),
                             msg=f'{checkbox_name} checkbox of {self.outcome_name} outcome was not disabled')

    def test_006_make_the_selections_active_again_in_ti(self):
        """
        DESCRIPTION: Make the selection(s) active again in TI
        EXPECTED: Particular suspended Exacta check boxes become active again in real time
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, active=True, displayed=True)
        result = wait_for_result(lambda: self.checkbox.is_enabled(timeout=0),
                                 name='Checkbox to become enabled', timeout=30)

        self.assertTrue(result, msg=f'{self.checkbox_name} checkbox of {self.outcome_name} outcome was not enabled')

        for checkbox_name, checkbox in self.outcome.items_as_ordered_dict.items():
            self.assertTrue(checkbox.is_enabled(),
                            msg=f'{checkbox_name} checkbox of {self.outcome_name} outcome was not enabled')

    def test_007_repeat_steps_1_6_for_trifecta_pool_type(self):
        """
        DESCRIPTION: Repeat steps 1-6 for Trifecta pool type
        """
        event = self.get_uk_tote_event(uk_tote_exacta=True)
        self.__class__.eventID = event.event_id
        self.__class__.marketID = event.market_id
        self.__class__.outcomes = self.get_single_leg_outcomes(event_id=self.eventID,
                                                               tab_name=vec.uk_tote.UK_TOTE_TABS.trifecta)
        self.__class__.selection_id = self.get_selection_id(event_id=self.eventID, outcomes=self.outcomes)

        self.test_001_suspend_current_event_in_ti()
        self.test_002_make_the_event_active_again_in_ti()
        self.test_003_suspend_market_from_current_event_in_ti()
        self.test_004_make_the_market_active_again_in_ti()
        self.test_005_suspend_one_or_more_selections_from_current_event_in_ti()
        self.test_006_make_the_selections_active_again_in_ti()
