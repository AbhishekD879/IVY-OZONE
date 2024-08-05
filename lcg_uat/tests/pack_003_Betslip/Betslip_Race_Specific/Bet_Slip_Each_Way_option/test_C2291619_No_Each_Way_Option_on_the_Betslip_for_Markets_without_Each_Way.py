import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.each_way
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2291619_No_Each_Way_Option_on_the_Betslip_for_Markets_without_Each_Way(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C2291619
    NAME: No Each Way Option on the Betslip for Markets without Each Way
    DESCRIPTION: This test case verifies Absence of Each Way Option on the Betslip for Markets without Each Way available
    PRECONDITIONS: **There is a race event with market without Each Way available**
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/Find racing event without each way terms
        """
        if tests.settings.backend_env == 'prod':
            ew_not_available_filter = simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_FALSE)
            selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                                          additional_filters=ew_not_available_filter)
            selection_ids = {name: selection_id for name, selection_id in selection_ids.items() if 'Unnamed' not in name}
            self._logger.info(f'*** Found Horse racing event with selection ids "{selection_ids}"')

        else:
            selection_ids = self.ob_config.add_UK_racing_event(ew_terms=False, number_of_runners=1).selection_ids

        self.__class__.selection_id = list(selection_ids.values())[0]

    def test_001_add_race_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add race selection to the Bet Slip
        EXPECTED: Race selection added to the Bet Slip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Selection is displayed on the Betslip
        EXPECTED: There is no Each Way checkbox
        """
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.assertFalse(stake.has_each_way_checkbox(expected_result=False),
                         msg=f'Stake "{stake_name}" have Each Way checkbox')
