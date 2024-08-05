import pytest

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod  # We cannot create modules on prod
@pytest.mark.football
@pytest.mark.evergage
@pytest.mark.module_ribbon
@pytest.mark.racing
@pytest.mark.featured
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@vtest
class Test_C119840_Verify_eventID_attribute_in_DOM_on_Featured_Tab(BaseFeaturedTest):
    """
    TR_ID: C119840
    NAME: Verify 'eventid' attribute in the DOM/HTML on Featured Tab
    DESCRIPTION: This Test Case verified 'eventid' attribute in the DOM/HTML on Featured tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add test events to be sure Featured module will be shown on Featured Tab
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id)[0]
            self.__class__.race_type_id = event['event']['typeId']
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.football_type_id = event['event']['typeId']
        else:
            self.ob_config.add_football_event_to_featured_autotest_league()
            self.ob_config.add_UK_racing_event(number_of_runners=1)
            self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1)
            self.__class__.race_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id
            self.__class__.football_type_id = \
                self.ob_config.football_config.autotest_class.featured_autotest_league.type_id

    def test_001_add_featured_tab_modules(self):
        """
        DESCRIPTION: Add Featured Tab modules on CMS
        """
        self.__class__.module_football_type = self.cms_config.add_featured_tab_module(
            select_event_by='Type', id=self.football_type_id)['title'].upper()

        self.__class__.module_race_type = self.cms_config.add_featured_tab_module(
            select_event_by='RaceTypeId', id=self.race_type_id)['title'].upper()

    def test_002_check_eventid_for_module_with_football_type_events(self):
        """
        DESCRIPTION: Check eventid for module with football type events on Featured Tab
        EXPECTED: Event ids attributes are present for all events on Module
        """
        self.site.wait_content_state('Homepage')
        self.wait_for_featured_module(name=self.module_football_type)
        featured_module = self.site.home.get_module_content(
            module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
        featured_module.scroll_to()

        if self.device_type == 'mobile':
            section = self.get_section(self.module_football_type)
        else:
            section = featured_module.accordions_list.items_as_ordered_dict.get(self.module_football_type)

        self.assertTrue(section, msg=f'Section "{self.module_football_type}" was not found')
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No one event was found in "{self.module_football_type}" module')

        for event_name, event in list(events.items())[:self.max_number_of_events]:
            self._logger.info(f'*** Event id of event "{event_name}" is "{event.event_id}"')
            self.assertTrue(event.event_id, msg='Eventid attribute is empty in DOM')

    def test_003_check_eventid_for_module_with_race_type_events(self):
        """
        DESCRIPTION: Check eventid for module with Race Type events on Featured Tab
        EXPECTED: Event ids attributes are present for all events on Module
        """
        self.wait_for_featured_module(name=self.module_race_type)
        featured_module = self.site.home.get_module_content(
            module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
        featured_module.scroll_to()

        if self.device_type == 'mobile':
            section = self.get_section(self.module_race_type)
        else:
            section = featured_module.accordions_list.items_as_ordered_dict.get(self.module_race_type)
        self.assertTrue(section, msg=f'Section "{self.module_race_type}" is not found on Featured tab')

        cards = section.items_as_ordered_dict
        self.assertTrue(cards, msg=f'No Cards found on {self.module_race_type} module')
        for event_name, event in cards.items():
            self._logger.info(f'*** Event id of event "{event_name}" is "{event.event_id}"')
            self.assertTrue(event.event_id, msg='Eventid attribute is empty in DOM')
