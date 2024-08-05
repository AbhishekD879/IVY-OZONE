import voltron.environments.constants as vec
import pytest

import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_beta2
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.cms
@pytest.mark.desktop
@pytest.mark.next_races
@pytest.mark.high
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C28943_Exclude_Unnamed_Favourite_Selections_from_the_Next_Races_Module(BaseRacing):
    """
    TR_ID: C28943
    NAME: Exclude Unnamed Favourite Selections from the 'Next Races' Module
    DESCRIPTION: This test case verifies that 'Unnamed Favourite' and 'Unnamed 2nd Favourite'
    DESCRIPTION: selection shouldn't be displayed in the 'Next Races' Module module
    PRECONDITIONS: There is <Race> event with 'Unnamed Favourite' and 'Unnamed 2nd Favourite'
    PRECONDITIONS:  (e.g. two normal selections, 'Unnamed Favourite' and 'Unnamed 2nd Favourite)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Next4 race event with 'Unnamed Favourite' and 'Unnamed 2nd Favourite' selections
        EXPECTED: Next4 event is created
        """
        next_races_toggle = self.get_initial_data_system_configuration().get('NextRacesToggle', {})
        if not next_races_toggle:
            next_races_toggle = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle.get('nextRacesComponentEnabled'):
            raise CmsClientException('Next Races component disabled in CMS')
        if tests.settings.cms_env != 'prd0':
            self.setup_cms_next_races_number_of_events()
        self.__class__.next_races_selections_number = self.get_next_races_selections_number_from_cms()
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=10, unnamed_favorites=True)

    def test_001_navigate_to_next_races_module(self):
        """
        DESCRIPTION: Navigate to 'Next Races' module
        EXPECTED: 'Unnamed Favourite' and 'Unnamed 2nd Favourite' won't appear in the list of selection on the 'Next Races' module
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')
        next_races_section = self.get_next_races_section()
        events = next_races_section.items_as_ordered_dict
        self.assertTrue(events, msg='No events were found in Next races section')
        for race_name, race in events.items():
            events = self.get_next_races_section().items_as_ordered_dict
            self.assertTrue(events, msg='No events were found in Next races section')
            if race_name not in events:
                # handling case when expired/finished next racing event is removed from UI
                continue
            race = events.get(race_name)
            race.scroll_to()
            selections = race.items_as_ordered_dict
            self.assertTrue(selections, msg=f'No one selection found for race: "{race_name}"')
            self.assertNotIn(vec.racing.UNNAMED_FAVORITE, list(selections.keys()),
                             msg=f'Selection: "{vec.racing.UNNAMED_FAVORITE}" for: '
                                 f'"{self.next_races_title}" module event: "{race_name}"')
            self.assertNotIn(vec.racing.UNNAMED_FAVORITE_2ND, list(selections.keys()),
                             msg=f'Selection: "{vec.racing.UNNAMED_FAVORITE_2ND}" for: '
                                 f'"{self.next_races_title}" module event: "{race_name}"')
