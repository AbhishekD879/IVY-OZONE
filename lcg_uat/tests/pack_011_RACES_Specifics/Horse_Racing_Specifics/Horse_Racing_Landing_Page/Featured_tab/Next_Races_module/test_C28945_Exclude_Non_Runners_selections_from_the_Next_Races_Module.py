import pytest

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.next_races
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C28945_Exclude_Non_Runners_selections_from_the_Next_Races_Module(BaseRacing):
    """
    TR_ID: C28945
    NAME: Exclude Non-Runners selections from the 'Next Races' Module
    DESCRIPTION: This test case verifies that 'Non-Runners' will be excluded from the 'Next Races' module.
    PRECONDITIONS: There is <Race> event with 'Non-Runners' (e.g. event which contains 3 or less selection and one of those selections is 'non-runner')
    PRECONDITIONS: 'Non-Runners' is a selection which contains 'N/R' text next to it's name
    """
    keep_browser_open = True
    number_of_runners = 3

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event with Non-Runners
        """
        # This cms switcher added to display all events, not only with LP prices
        self.cms_config.next_races_price_switcher(show_priced_only=False)
        self.setup_cms_next_races_number_of_events()
        type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
        self.check_and_setup_cms_next_races_for_type(type_id=type_id)

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=self.number_of_runners, time_to_start=3)
        event_id = event_params.event_id
        event_off_time = event_params.event_off_time
        name = self.horseracing_autotest_uk_name_pattern if self.brand == 'bma' and self.device_type == 'desktop' else self.horseracing_autotest_uk_name_pattern.upper()
        self.__class__.created_event_name = f'{event_off_time} {name}'
        win_or_each_way_market_id = event_params.market_id

        self.__class__.selection_name, selection_id = list(event_params.selection_ids.items())[0]
        new_selection_name = f'{self.selection_name} N/R'

        self.ob_config.change_selection_name(selection_id=selection_id, new_selection_name=new_selection_name)
        self.ob_config.result_selection(selection_id=selection_id, market_id=win_or_each_way_market_id,
                                        event_id=event_id, result='V')
        self.ob_config.confirm_result(selection_id=selection_id, market_id=win_or_each_way_market_id,
                                      event_id=event_id, result='V')

    def test_001_navigate_to_next_races_module(self):
        """
        DESCRIPTION: Navigate to 'Next Races' module
        EXPECTED: 'Non-Runners' won't appear in the 'Next Races' module
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

        event = self.get_event_from_next_races_module(event_name=self.created_event_name)
        self.assertTrue(event, msg=f'Event "{self.created_event_name}" is not present in Next Races module')
        selections = event.items_as_ordered_dict
        self.assertTrue(selections, msg=f'No selections found for {self.created_event_name}')
        non_runner = next((selection_name for selection_name, selection in selections.items()
                           if self.selection_name in selection_name), None)
        self.assertFalse(non_runner, msg=f'Non-Runner "{non_runner}" still shown in "{self.created_event_name}"')
