import pytest

import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't change selection state on prod/hl
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.deeplink
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C29096_Verify_Adding_Suspended_Selections_via_Direct_Link(BaseBetSlipTest):
    """
    TR_ID: C29096
    TR_ID: C18636108
    NAME: Verify Adding Suspended Selections via Direct Link
    DESCRIPTION: This test case verifies how suspended selections can be added to the Bet slip via direct link
    """
    keep_browser_open = True
    selection_ids_2 = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Creating test event
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.team1, self.__class__.selection_ids = event.team1, event.selection_ids
        self.ob_config.change_selection_state(selection_id=self.selection_ids['Draw'], displayed=True, active=False)
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], displayed=True, active=False)

        self.__class__.selection_ids_2 = self.ob_config.add_UK_racing_event(number_of_runners=2).selection_ids
        for selection in self.selection_ids_2.values():
            self.ob_config.change_selection_state(selection_id=selection, displayed=True, active=False)

    def test_001_login(self):
        """
        DESCRIPTION: Login to application
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_open_betslip_via_deep_link(self):
        """
        DESCRIPTION: Open betslip via deeplink
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids['Draw'], self.selection_ids[self.team1]))

    def test_003_check_betslip(self):
        """
        DESCRIPTION: It is impossible to place bet on any suspended selection
        """
        self.check_suspended_selections_in_betslip(number_of_selections=2,
                                                   expected_message=vec.betslip.MULTIPLE_DISABLED)

    def test_004_open_betslip_via_deep_link(self):
        """
        DESCRIPTION: Open betslip via deeplink
        """
        self.open_betslip_with_selections(selection_ids=(list(self.selection_ids_2.values())[0], list(self.selection_ids_2.values())[1]))

    def test_005_check_betslip(self):
        """
        DESCRIPTION: It is impossible to place bet on any suspended selection
        """
        self.check_suspended_selections_in_betslip(number_of_selections=2,
                                                   expected_message=vec.betslip.MULTIPLE_DISABLED)

    def test_006_repeat_steps_for_just_one_outcome_id_in_direct_url(self):
        """
        DESCRIPTION: Repeat steps # 1-5 for just **ONE outcome id** in direct URL
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])
        self.check_suspended_selections_in_betslip(number_of_selections=1,
                                                   expected_message=vec.betslip.SINGLE_DISABLED)

        self.open_betslip_with_selections(selection_ids=list(self.selection_ids_2.values())[0])
        self.check_suspended_selections_in_betslip(number_of_selections=1,
                                                   expected_message=vec.betslip.SINGLE_DISABLED)
