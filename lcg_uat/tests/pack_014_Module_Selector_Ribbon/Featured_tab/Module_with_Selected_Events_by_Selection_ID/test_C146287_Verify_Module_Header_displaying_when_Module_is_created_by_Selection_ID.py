import pytest

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod  # cannot create featured modules on prod
@pytest.mark.featured
@pytest.mark.badges
@pytest.mark.cms
@pytest.mark.module_ribbon
@pytest.mark.medium
@pytest.mark.desktop
@vtest
class Test_C146287_Verify_Module_Header_displaying_when_Module_is_created_by_Selection_ID(BaseFeaturedTest):
    """
    TR_ID: C146287
    NAME: Verify Module Header displaying when Module is created by Selection ID
    """
    keep_browser_open = True
    badges = {'Specials': 'Special',
              'Enhanced': 'Enhanced'}
    featured_modules = {}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football events
        DESCRIPTION: Create in CMS featured modules
        EXPECTED: With 'Special' badge is displayed on the Header
        EXPECTED: With 'Enhanced' badge is displayed on the Header
        EXPECTED: With 'None' badge is not displayed on the Header
        """
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.football_config.category_id
            event = self.get_active_events_for_category(category_id=category_id)[0]
            self.__class__.eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            # outcomeMeaningMinorCode: A - away, H - home, D - draw
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1:
                raise SiteServeException('No Home team found')
            selection = self.selection_ids[self.team1]
        else:
            start_time = self.get_date_time_formatted_string(hours=3)
            event = self.ob_config.add_football_event_to_autotest_league2(start_time=start_time)
            selection = event.selection_ids[event.team1]

        for cms_badge, ui_badge in self.badges.items():
            module_name = self.cms_config.add_featured_tab_module(
                select_event_by='Selection', id=selection, badge=cms_badge)['title'].upper()

            self.__class__.featured_modules.update({cms_badge: module_name})

    def test_001_tap_featured_tab(self):
        """
        DESCRIPTION: Open Featured tab
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=list(self.featured_modules.values())[0])
        self.__class__.module = self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))

    def test_002_verify_badge_status(self):
        """
        DESCRIPTION: Select Featured Module by Selection ID with 'Badge' parameter value = 'Special', 'Enhanced', 'None
        DESCRIPTION: Verify Header displaying for the Module
        """
        for cms_badge, expected_ui_badge in self.badges.items():
            section_name = self.featured_modules.get(cms_badge)
            sections = self.module.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No section was found in module')
            section = sections.get(section_name)
            self.assertTrue(section, msg=f'Section "{section_name}" is not found on Featured tab')
            label = section.group_header.badge_label
            self.assertEqual(expected_ui_badge, label.title(),
                             msg=f'Section "{section_name}" expected badge "{expected_ui_badge}" don\'t match "{label.title()}"')
