import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports_specific
@pytest.mark.golf_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C65968972_Verify_details_on_the_Golf_sport_landing_page_display_as_per_CMS_config(Common):
    """
    TR_ID: C65968972
    NAME: Verify details on the Golf sport landing page display as per CMS config
    DESCRIPTION: This test case verifies Golf sports landing page display is as per the CMS configuration.
    """
    is_changed_the_order_of_tabs = False
    keep_browser_open = True
    mandatory_fields = {
        'disabled': False,
        'inApp': True,
        'showInPlay': True,
        'showInHome': True,  # show in sport ribbon
        'showInAZ': True,
        'showScoreboard': True,
        'outrightSport': True
    }
    list_of_tabs_response = []
    moving_item = None
    original_order = []

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if cls.is_changed_the_order_of_tabs:
            cms_config = cls.get_cms_config()
            cms_config.set_sport_tabs_ordering(moving_item=cls.moving_item, new_order=cls.original_order)

    def check_accordions_flexibility(self, accordion_list):
        accordions = accordion_list.n_items_as_ordered_dict(4)
        for accordion_name, accordion in list(accordions.items())[:3]:
            if accordion.is_expanded():
                accordion.collapse()
                self.assertFalse(accordion.is_expanded(), f'Unable Collapse the accordion : "{accordion_name}"')
            accordion.expand()
            self.assertTrue(accordion.is_expanded(), f'Unable to Expand the accordion : "{accordion_name}"')
            accordion.collapse()
            self.assertFalse(accordion.is_expanded(), f'Unable Collapse the accordion : "{accordion_name}"')

    def check_order_of_tabs_as_per_CMS(self, time=1, timeout=120, refresh=False):
        self.__class__.list_of_tabs_response = self.cms_config.get_sport_tabs(self.ob_config.golf_config.category_id)
        cms_tabs = [tab['displayName'].upper() for tab in self.list_of_tabs_response if
                not (not tab['enabled'] or (tab['checkEvents'] and not tab['hasEvents']))]

        while time <= timeout:
            try:
                fe_tabs = list(self.site.golf.tabs_menu.items_as_ordered_dict.keys())
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

        self.__class__.list_of_tabs_response = self.cms_config.get_sport_tabs(self.ob_config.golf_config.category_id)
        order_from_cms_after_changing = [tab['id'].upper() for tab in self.list_of_tabs_response if
                                         not (not tab['enabled'] or (tab['checkEvents'] and not tab['hasEvents']))]

        self.assertListEqual(cms_tabs, order_from_cms_after_changing, f'Order is not Changed in CMS')
        self.__class__.is_changed_the_order_of_tabs = True

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: 1. CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf
        PRECONDITIONS: 2. CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf-&gt; General Sport Configuration
        PRECONDITIONS: Active, In App, Show Inplay, Show in sports ribbon, show in AZ, Show scoreboard, Is Outright Sport checkboxes should be enabled
        PRECONDITIONS: 3.CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf-&gt; General Sport Configuration-&gt; Active/Inactive sport
        """
        sports = self.cms_config.get_sport_categories()
        for sport in sports:
            if sport['imageTitle'] == vec.olympics.GOLF:
                self.__class__.sport_id = sport['id']
                is_all_mandatory_fields_satisfied = next((False for field in self.mandatory_fields if self.mandatory_fields[field] != sport.get(field)), True)

                if not is_all_mandatory_fields_satisfied:
                    self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                                          **self.mandatory_fields)
                break
        else:
            raise VoltronException(f'{vec.olympics.GOLF} sport not found in sports categories')
        sys_config = self.get_initial_data_system_configuration()
        self.__class__.market_selector_status = sys_config.get('MarketSwitcher').get('golf')

    def test_001_launch_the_ladbrokes_and_coral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes and Coral application.
        EXPECTED: The application should be launched successfully.
        """
        self.site.go_to_home_page()
        self.site.wait_content_state('Home')

    def test_002_select_the_golf_sport_either_from_the_sports_ribbon_or_through_the_a_z_menu(self):
        """
        DESCRIPTION: Select the Golf Sport either from the sports ribbon or through the A-Z menu.
        EXPECTED: User should be redirected to the Golf sport landing page.
        EXPECTED: The various tabs which are configured in the CMS should be displayed in the front end.(Matches; Events; Competitions; Outright's; Coupons; Specials; In-Play)
        """
        self.site.open_sport('Golf')

    def test_003_change_the_sequence_on_the_order_of_display_of_tabs_by_altering_the_position_of_any_of_the_tabs_in_cmssport_categories__ampgt_golf__ampgt_tab_name_table__ampgt_drag_and_drop_any_of_the_options_from_the_tab_name_table(self):
        """
        DESCRIPTION: Change the sequence on the order of display of tabs by altering the position of any of the tabs in CMS.(Sport Categories -&amp;gt; Golf -&amp;gt; Tab Name table -&amp;gt; Drag and Drop any of the options from the Tab Name table.
        EXPECTED: The display of the various tabs should be updated in the front end based on the updated positions in the CMS.
        """
        self.check_order_of_tabs_as_per_CMS()
        self.change_order_of_tabs_in_CMS()
        self.check_order_of_tabs_as_per_CMS(refresh=True)

    def test_004_verify_that_user_is_able_to_switch_between_various_tabs_availableevents_competitions_outrights_specialsmatches(self):
        """
        DESCRIPTION: Verify that user is able to switch between various tabs available.
        DESCRIPTION: (Events; Competitions, Outright's; Specials;Matches)
        EXPECTED: The user should be able to switch between various tabs successfully.
        EXPECTED: The Data should get updated accordingly as per the selected tab.
        """
        competitions = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                self.ob_config.golf_config.category_id)

        tabs = self.site.golf.tabs_menu.items_as_ordered_dict
        for tab_name, tab in tabs.items():
            tab.click()
            if self.device_type == 'mobile' and tab_name.upper() == ['MATCHES', 'EVENTS']:
                wait_for_result(lambda: self.site.golf.tabs_menu.current.upper() in ['MATCHES', 'EVENTS'])
                self.assertIn(self.site.golf.tabs_menu.current.upper(), ['MATCHES', 'EVENTS'],
                                 f'Unable to Switch "{tab_name}"')
            else:
                wait_for_result(lambda: self.site.golf.tabs_menu.current == tab_name)
                self.assertEqual(tab_name, self.site.golf.tabs_menu.current,
                                 f'Unable to Switch "{tab_name}"')
            if tab_name.title() in [competitions.upper(), 'MATCHES'] and self.market_selector_status:
                market_obj = next((market for name, market in self.site.golf.tab_content.dropdown_market_selector.items_as_ordered_dict.items() if name.upper() in ['3 BALL BETTING', '2 BALL BETTING']), None)
                if not market_obj:
                    continue
                market_obj.click()
            accordion_list = self.site.golf.tab_content.competitions_categories_list if tab_name.title() == competitions.title() else self.site.golf.tab_content.accordions_list
            self.check_accordions_flexibility(accordion_list=accordion_list)

    def test_005_verify_that_user_is_able_to_expand_and_collapse_the_accordions(self):
        """
        DESCRIPTION: Verify that user is able to expand and collapse the accordions
        EXPECTED: User should be able to expand and collapse the accordions without errors.
        """
        # covered in above step
