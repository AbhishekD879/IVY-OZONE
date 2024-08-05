import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.desktop
@pytest.mark.liveserv_updates
@pytest.mark.betslip
@pytest.mark.medium
@vtest
class Test_C29024_Undisplayed_selections_not_removed_from_the_Betslip(BaseBetSlipTest):
    """
    TR_ID: C29024
    NAME: Undisplayed selections not removed from the Betslip
    DESCRIPTION: This test case verifies that undisplayed selections are not removed from the bet slip.
    """
    keep_browser_open = True

    def test_000_preconditions_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        event_2 = self.ob_config.add_autotest_premier_league_football_event()

        self.__class__.selection, self.__class__.selection_ids = event.team1, event.selection_ids
        self.__class__.selection_2, self.__class__.selection_ids_2 = event_2.team1, event_2.selection_ids

        self.site.wait_content_state('Home')

    def test_001_add_two_active_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add two active selections to the Betslip
        EXPECTED: Betslip counter increases accordingly
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.selection],
                                                         self.selection_ids_2[self.selection_2]))

    def test_002_trigger_the_situation_when_data_of_one_selected_outcome_is_undisplayed_in_ss(self):
        """
        DESCRIPTION: Trigger the situation when data **of one selected outcome** is undisplayed in SS
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids_2[self.selection_2],
                                              displayed=False, active=True)

    def test_003_go_to_betslip_page(self):
        """
        DESCRIPTION: Go to Betslip page
        EXPECTED: Unchanged content of Betslip is shown, both selections are still present
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertEqual(len(singles_section.items()), self.expected_betslip_counter_value,
                         msg='Both selections should be present in betslip')

        self.verify_betslip_counter_change(expected_value=2)

        stake_name_1, _ = list(singles_section.items())[0]
        stake_name_2, _ = list(singles_section.items())[1]
        self.assertEqual(stake_name_1, self.selection,
                         msg=f'Selection {self.selection} should be present in betslip')
        self.assertEqual(stake_name_2, self.selection_2,
                         msg=f'Selection {self.selection_2} should be present in betslip')

    def test_004_refresh_the_page_and_open_betslip(self):
        """
        DESCRIPTION: Refresh the page/add one more active selection to the Betslip > Open Betslip
        EXPECTED: *   Undisplayed Selection remains present in the Betslip
        EXPECTED: *   Active selection remains visible
        EXPECTED: *   Betslip counter still shows "2"
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.open_betslip()

        singles_section = self.get_betslip_sections().Singles
        number_of_selections = len(singles_section.items())
        self.assertEqual(number_of_selections, self.expected_betslip_counter_value,
                         msg=f'Number of selections in betslip "{number_of_selections}" is not the same as'
                             f' expected "{self.expected_betslip_counter_value}"')

        self.verify_betslip_counter_change(expected_value=2)

        stake_name, _ = list(singles_section.items())[0]
        self.assertEqual(stake_name, self.selection, msg=f'Selection {self.selection} should be present in betslip')
        stake_name2, _ = list(singles_section.items())[1]
        self.assertEqual(stake_name2, self.selection_2, msg=f'Selection {self.selection} should be present in betslip')
