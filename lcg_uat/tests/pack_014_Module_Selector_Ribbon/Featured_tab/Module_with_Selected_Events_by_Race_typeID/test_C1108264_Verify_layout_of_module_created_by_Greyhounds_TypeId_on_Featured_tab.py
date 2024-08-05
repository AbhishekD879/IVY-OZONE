import re

import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.featured
@pytest.mark.racing
@pytest.mark.module_ribbon
@pytest.mark.greyhounds
@pytest.mark.next_races
@pytest.mark.cms
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-52668')
@vtest
class Test_C1108264_Verify_layout_of_module_created_by_Greyhounds_TypeId_on_Featured_tab(BaseGreyhound, BaseFeaturedTest):
    """
    TR_ID: C1108264
    NAME: Verify layout of module created by Greyhounds Type Id on Featured tab
    """
    keep_browser_open = True
    type_id = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Greyhound event
        """
        self.__class__.featured_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured) if self.device_type == 'mobile' \
            else vec.sb_desktop.FEATURED_MODULE_NAME
        if tests.settings.cms_env != 'prd0':
            self.setup_cms_next_races_number_of_events()
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.backend.ti.greyhound_racing.category_id)[0]
            search = re.search(r'(?:\d{2}:\d{2})(?:\s\+\d{1,2}d)?\s([\w\s\']+)', event['event']['name'])  # Shepp' Dogs or +1d Fonner Park for example
            name_pattern = search.groups()[0]
            self.__class__.name_pattern = name_pattern.upper() if self.brand == 'ladbrokes' else name_pattern
            self.__class__.eventID = event['event']['id']
            self.__class__.type_id = event['event']['typeId']
        else:
            event_params = self.ob_config.add_UK_greyhound_racing_event(time_to_start=10, ew_terms=self.ew_terms,
                                                                        cashout=True)
            self.__class__.type_id = self.ob_config.backend.ti.greyhound_racing.greyhounds_live.autotest.type_id
            self.__class__.eventID = event_params.event_id
            self.__class__.name_pattern = self.greyhound_autotest_name_pattern.upper() if self.brand == 'ladbrokes' \
                else self.greyhound_autotest_name_pattern

    def test_001_add_event_to_featured_tab(self):
        """
        DESCRIPTION: Add Greyhound type to featured tab
        """
        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='RaceTypeId', id=self.type_id, show_expanded=True)['title'].upper()

    def test_002_check_layout_of_created_greyhound_module(self):
        """
        DESCRIPTION: Observe the layout of created Greyhounds module
        EXPECTED: Module 'Title'
        EXPECTED: Below title there should be present a box for each event with following components present:
        EXPECTED: Time, Venue
        EXPECTED: Each Way: x odds - places 1,2 - only for mobile/tablet;
        EXPECTED: Below there should be present greyhound selections with following components:
        EXPECTED: Color square box with number of greyhound, name of greyhound and price
        EXPECTED: In the footer of box there should be present hyperlink named "View Full Race Card"
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)
        featured_content = self.site.home.get_module_content(module_name=self.featured_name).accordions_list.items_as_ordered_dict
        self.assertTrue(featured_content, msg='"Featured" module does not contain any accordions')
        featured_modules = featured_content.keys()
        self.assertIn(self.module_name, featured_modules,
                      msg=f'Module "{self.module_name}" is not displayed. '
                          f'Please check list of all displayed modules:\n"{featured_modules}"')

        self.__class__.module = featured_content[self.module_name]
        self.assertTrue(self.module, msg='No accordions displayed in "Featured" section on Home page')
        events = self.module.items_as_ordered_dict
        self.assertTrue(events, msg=f'No event found in module "{self.module_name}"')
        for event_name, event in events.items():
            event.scroll_to()
            self.assertRegex(event_name, r'\d{2}:\d{2} %s' % self.name_pattern,
                             msg=f'Event name: "{event_name}" doesn\'t match expected pattern: <HH:MM {self.name_pattern}>')
            if self.brand == 'ladbrokes' or self.device_type == 'mobile':
                self.assertTrue(event.has_each_way_terms(), msg=f'Event "{self.event_name}" does not have Each Way Terms')
            self.assertTrue(event.has_view_full_race_card(),
                            msg=f'Event "{self.event_name}" does not View Full Race Card Link')
            outcomes = event.items_as_ordered_dict
            self.assertTrue(outcomes, msg=f'No outcomes found for event "{self.event_name}"')
            for outcome_name, outcome in outcomes.items():
                outcome.bet_button.scroll_to()
                self.assertTrue(outcome.runner_info.has_silks, msg=f'Outcome "{outcome_name}" does not have silk')
                self.assertTrue(outcome.bet_button.outcome_price_text,
                                msg=f'Outcome "{outcome_name}" does not have price')
