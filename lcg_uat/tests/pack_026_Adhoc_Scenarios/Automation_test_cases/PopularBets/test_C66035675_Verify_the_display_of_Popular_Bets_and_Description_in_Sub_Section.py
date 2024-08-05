import pytest
from crlat_cms_client.utils.exceptions import CMSException
from lxml.html import fromstring
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.popular_bets
@pytest.mark.adhoc_suite
@pytest.mark.football
@pytest.mark.other
@pytest.mark.reg167_fix
@vtest
class Test_C66035675_Verify_the_display_of_Popular_Bets_and_Description_in_Sub_Section(Common):
    """
    TR_ID: C66035675
    NAME: Verify the display of Popular Bets and Description in Sub Section
    DESCRIPTION: This test case verifies the display of Popular Bets and Description in Sub Section
    """
    keep_browser_open = True
    is_changed_the_order_of_tabs = False
    list_of_tabs_response = []
    moving_item = None
    original_order = []

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if cls.is_changed_the_order_of_tabs:
            cms_config = cls.get_cms_config()
            cms_config.set_sport_tabs_ordering(moving_item=cls.moving_item, new_order=cls.original_order)

    def check_order_of_tabs_as_per_CMS(self, time=1, timeout=120, refresh=False):
        self.__class__.list_of_tabs_response = self.cms_config.get_sport_tabs(self.ob_config.football_config.category_id)
        cms_tabs = [tab['displayName'].upper() for tab in self.list_of_tabs_response if
                not (not tab['enabled'] or (tab['checkEvents'] and not tab['hasEvents']))]

        while time <= timeout:
            try:
                fe_tabs = list(self.site.football.tabs_menu.items_as_ordered_dict.keys())
                self.assertListEqual(cms_tabs, fe_tabs, f'tabs are  not as per cms config.\n Actual Order : "{fe_tabs}"'
                                                        f'\nExpected Order : "{cms_tabs}"')
                break
            except Exception as e:
                if time <= timeout:
                    wait_for_haul(2)
                    if refresh and time % 10 == 5:
                        self.device.refresh_page()
                    time += 2
                    continue
                else:
                    raise e

    def change_order_of_tabs_in_CMS(self):
        cms_tabs = [tab['id'].upper() for tab in self.list_of_tabs_response if
                    not (not tab['enabled'] or (tab['checkEvents'] and not tab['hasEvents']))]

        self.__class__.original_order.extend(cms_tabs)
        self.__class__.moving_item = cms_tabs[0]

        moving_item = cms_tabs.pop(0)
        cms_tabs.append(moving_item)
        self.cms_config.set_sport_tabs_ordering(moving_item=moving_item, new_order=cms_tabs)

        self.__class__.list_of_tabs_response = self.cms_config.get_sport_tabs(self.ob_config.football_config.category_id)
        order_from_cms_after_changing = [tab['id'].upper() for tab in self.list_of_tabs_response if
                                         not (not tab['enabled'] or (tab['checkEvents'] and not tab['hasEvents']))]

        self.assertListEqual(cms_tabs, order_from_cms_after_changing, f'Order is not Changed in CMS')
        self.__class__.is_changed_the_order_of_tabs = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
        """
        all_sub_tabs_for_football = self.cms_config.get_sport_tabs(sport_id=self.ob_config.football_config.category_id)
        self.__class__.tab_name = next((tab['displayName'].upper() for tab in all_sub_tabs_for_football if tab['enabled'] == True and tab['name'] == 'popularbets'), None)
        if not self.tab_name:
            raise CMSException('Popular Bet tab is not enabled in CMS!!')
        tab_id = self.cms_config.get_sport_tab_id(sport_id=self.ob_config.football_config.category_id,
                                                  tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.popularbets)
        popular_bets_tab_resp = self.cms_config.get_sport_tab_data_by_tab_id(sport_tab_id=tab_id)
        tab_names = self.cms_config.get_sport_tab_data_by_tab_id(sport_tab_id=tab_id).get('trendingTabs')
        for tab_name in tab_names:
            if tab_name.get('headerDisplayName') == 'Popular_bets':
                self.__class__.popular_tab_name = tab_name.get('trendingTabName')
                popular_bets_desc = tab_name.get('popularTabs')[0].get('informationTextDesc')
        self.__class__.desc_text = fromstring(popular_bets_desc).text_content().strip('\n').strip()
        if not popular_bets_tab_resp.get('showNewFlag'):
            self.cms_config.update_sports_tab_status(sport_tab_id=tab_id, showNewFlag=True)

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application is launched Successfully
        """
        self.site.open_sport('football')

    def test_002_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        # covered in above step

    def test_003_verify_the_display_of_popular_bets_section(self):
        """
        DESCRIPTION: Verify the display of Popular Bets section
        EXPECTED: User can able to see the Popular Bets section Tab
        """
        actual_sports_tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        self.assertTrue(actual_sports_tabs, f'tabs are not available for football')
        tab = next((tab for tab_name, tab in actual_sports_tabs.items() if tab_name.upper() == self.tab_name), None)
        self.assertTrue(tab, f'{self.tab_name} is not displayed in FE')
        tab.click()
        self.assertTrue(tab.has_new_icon, msg=f' {tab} has no new icon')

    def test_004_verify_the_display_of_new_flag_on_top_right_of_the_popular_bets_section(self):
        """
        DESCRIPTION: Verify the display of New Flag on top right of the Popular Bets section
        EXPECTED: User can able to see the New Flag on the top right of Popular Bets section Tab
        """
        # covered in above step

    def test_005_change_the_sorting_order_in_cms_amp_verify_in_front_end(self):
        """
        DESCRIPTION: Change the Sorting Order in CMS & verify in Front End
        EXPECTED: Able to see the Sorting Order as per the CMS in Front End
        """
        self.check_order_of_tabs_as_per_CMS()

    def test_006_cms__gtsports__gtfootball_change_the_position_of_popular_bets_by_drag_amp_drop_to_desired_position(self):
        """
        DESCRIPTION: CMS-->Sports-->Football change the position of popular bets by drag & drop to desired position.
        EXPECTED:
        """
        self.change_order_of_tabs_in_CMS()
        self.check_order_of_tabs_as_per_CMS(refresh=True)

    def test_007_click_on_popular_bets_tab(self):
        """
        DESCRIPTION: Click on Popular bets Tab
        EXPECTED: Popular bets tab is loaded.
        """
        # covered in above step

    def test_008_verify_the_display_of_popular_bets_description_and_info_icon_in_the_sub_section(self):
        """
        DESCRIPTION: Verify the display of popular bets description and Info Icon in the sub section
        EXPECTED: Able to see the Info icon and Description
        """
        current_tab = self.site.football.tab_content.grouping_buttons.current
        if current_tab != self.popular_tab_name.upper():
            self.site.football.tab_content.grouping_buttons.click_button(self.popular_tab_name.upper())
            self.site.wait_content_state_changed()
            current_tab = self.site.football.tab_content.grouping_buttons.current.upper()
            self.assertEqual(current_tab, self.popular_tab_name.upper(),
                         f'Actual Tab : "{current_tab}" is not same as' f'Expected Tab : "{self.popular_tab_name}"')
        description_visible_status = self.site.football.tab_content.has_description_container()
        self.assertTrue(description_visible_status, msg=f' popular bets tab has no description')

        desc_container = self.site.football.tab_content.description_container

        description_text = desc_container.description.strip()
        self.assertEqual(description_text, self.desc_text, msg=f'message configured in cms "{self.desc_text}" is not equal to message displayed in frontend "{description_text}"')
        desc_icon = desc_container.has_info_icon
        self.assertTrue(desc_icon, msg=f' popular bets tab has no description info icon')

        desc_close_btn = desc_container.close
        self.assertTrue(desc_close_btn,
                        msg=f' popular bets tab has no description close button for description tab')
        desc_close_btn.click()

        description_visible_status = self.site.football.tab_content.has_description_container()
        self.assertFalse(description_visible_status,
                         msg=f'popular bets tab has description after clicking on close button')

    def test_009_verify_the_display_of_x_button_and_its_functionality_when_user_clicks_on_close_x_of_popular_bets_description(self):
        """
        DESCRIPTION: Verify the display of "X" Button and its functionality when user clicks on close "X" of Popular bets description
        EXPECTED: Able to see the "X" Button , when user clicks  the description should be closed
        """
        # covered in above step

    def test_010_switch_the_tabpage_and_re_visits_popular_bets_pageto_check_the_description(self):
        """
        DESCRIPTION: Switch the tab/page and re-visits popular bets page(To check the description)
        EXPECTED: Description should be displayed again
        """
        actual_sports_tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        tab = next((tab for tab_name, tab in actual_sports_tabs.items() if tab_name != self.tab_name), None)
        tab.click()

        pop_tab = next((tab for tab_name, tab in actual_sports_tabs.items() if tab_name == self.tab_name), None)
        pop_tab.click()
        self.site.wait_content_state_changed()
        description_visible_status = self.site.football.tab_content.has_description_container()
        self.assertTrue(description_visible_status, msg=f' popular bets tab has no description')

    def test_011_verify_display_of_popular_bets_sub_section_below_the_description(self):
        """
        DESCRIPTION: Verify display of Popular Bets Sub section below the description
        EXPECTED: Able to see the Popular Bets Sub section under Popular Bets tab.
        """
        # covered in above step