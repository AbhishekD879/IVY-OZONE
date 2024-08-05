import pytest
from tests.base_test import vtest
from copy import copy
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # we can not change the countrypanel order in cms for prod/beta
@pytest.mark.races
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C60094845_Verify_the_display_of_Ladbrokes_Legends_panel_CMS_configured(Common):
    """
    TR_ID: C60094845
    NAME: Verify the display of Ladbrokes Legends panel-CMS configured
    DESCRIPTION: Verify that meetings in Ladbrokes Legends panel are positioned as configured in CMS
    PRECONDITIONS: 1: Ladbrokes/Coral Legends should have meetings displayed in FE
    PRECONDITIONS: 2: Admin access for CMS
    """
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        # reverting country panels ordering
        if cls.initial_markets_id_order:
            cms_config.set_county_panel_ordering_for_horse_racing(new_order=cls.initial_markets_id_order, moving_item=cls.drag_panel_id)

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.ob_config.add_virtual_racing_event(number_of_runners=3)
        self.site.wait_content_state('Homepage')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        if self.device_type == 'desktop':
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn(vec.sb.HORSERACING.upper(), sports.keys(),
                          msg=f'"{vec.sb.HORSERACING.upper()}" is not found in the header sport menu')
            sports.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.navigate_to_page('horse-racing')
        self.site.wait_content_state(state_name='Horseracing')

    def test_003_verify_the_display_of_ladbrokescoral_legends(self):
        """
        DESCRIPTION: Verify the display of Ladbrokes/Coral Legends
        """
        self.site.wait_splash_to_hide(timeout=5)
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        if self.brand == 'bma':
            if self.device_type == 'mobile':
                self.assertIn(vec.racing.VIRTUAL_SECTION_LIST[0], sections, msg='Virtual Racing is not displayed')
            else:
                self.assertIn(vec.racing.VIRTUAL_SECTION_LIST[0].title(), sections, msg='Virtual Racing is not displayed')
        else:
            self.assertIn(vec.racing.LEGENDS_TYPE_NAME, sections, msg='Ladbrokes Legends is not displayed')

    def test_004_log_in_to_cms_and_change_the_order_for_ladbrokescoral_legends(self):
        """
        DESCRIPTION: Log in to CMS and change the order for Ladbrokes/Coral Legends
        """
        horse_racing_sports = self.cms_config.get_sport_module(self.ob_config.horseracing_config.category_id, module_type=None)
        self.__class__.initial_markets_id_order = [country_panel['id'] for country_panel in horse_racing_sports]
        self.__class__.initial_markets_order_names = [country_panel['title'] for country_panel in horse_racing_sports]

        for country_panel in self.initial_markets_order_names:
            if country_panel in ['Virtual Racing', 'Ladbrokes Legends']:
                self.__class__.drag_panel_name = country_panel

        self.__class__.drag_panel_id = next(
            (panel['id'] for panel in horse_racing_sports if panel['title'] == self.drag_panel_name), '')
        if not self.drag_panel_id:
            raise VoltronException(f'Cannot find market id for {self.drag_panel_name}')
        new_order = copy(self.initial_markets_id_order)
        new_order.remove(self.drag_panel_id)
        for item in horse_racing_sports:
            if item['title'] == 'UK and Irish Races':
                position = horse_racing_sports.index(item)
                new_order.insert(position + 1, self.drag_panel_id)
                break
        self.cms_config.set_county_panel_ordering_for_horse_racing(new_order=new_order, moving_item=self.drag_panel_id)

    def test_005_verify_in_fe_the_order_displayed_is_as_configured_in_cms(self):
        """
        DESCRIPTION: Verify in FE the order displayed is as configured in CMS
        EXPECTED: User should be able to see the display order as per CMS configuration
        """
        sections = list(self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict.keys())
        self.assertTrue(sections, msg='No sections found on page')
        for item in sections:
            if item.upper() == 'UK AND IRISH RACES':
                position = sections.index(item)
                if self.brand == 'bma':
                    self.assertEqual(sections[position + 1].upper(), 'VIRTUAL RACING', msg='Virtual Racing position is not changed')
                else:
                    self.assertEqual(sections[position + 1].upper(), 'LADBROKES LEGENDS', msg='Ladbrokes legends position is not changed')
