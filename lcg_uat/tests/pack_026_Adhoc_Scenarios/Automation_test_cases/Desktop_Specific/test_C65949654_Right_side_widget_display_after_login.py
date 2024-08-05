import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_cms_reflection, wait_for_result, wait_for_haul
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.desktop_specific
@pytest.mark.adhoc_suite
@pytest.mark.reg165_fix
@vtest
class Test_C65949654_Right_side_widget_display_after_login(Common):
    """
    TR_ID: C65949654
    NAME: Right side widget display after login
    DESCRIPTION: This test case verifies right side widget in desktop after login
    PRECONDITIONS: 1. Login to CMS
    PRECONDITIONS: 2. Navigate to Widgets section
    PRECONDITIONS: 3. Modules should be enabled in widgets section
    PRECONDITIONS: 4. Desktop offers should be created in CMS
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def widget_order_change(self, widget_list: list):
        moving_item = widget_list[1]
        widget_list.remove(moving_item)
        widget_list.insert(-1, moving_item)
        self.cms_config.set_widget_ordering(new_order=widget_list, moving_item=moving_item)
        expected_widget_lists = self.cms_config.get_widgets()
        expected_widget_name_list = [expected_widget_list.get('id') for expected_widget_list in
                                     expected_widget_lists if
                                     expected_widget_list.get('disabled') == False
                                     and expected_widget_list.get('showOnDesktop') == True
                                     and expected_widget_list.get('columns') in ['both', 'rightColumn']]
        self.assertEqual(widget_list, expected_widget_name_list,
                         msg="Widget list does not match the expected widget name list")

    def test_000_precondition(self):
        """
        TR_ID: C65949653
        NAME: Right side widget display in desktop before login
        DESCRIPTION: This test case verifies right side widget in desktop before login
        PRECONDITIONS: 1. Login to CMS
        PRECONDITIONS: 2. Navigate to Widgets section
        PRECONDITIONS: 3. Modules should be enabled in widgets section
        PRECONDITIONS: 4. Desktop offers should be created in CMS
        """
        events = self.get_active_events_for_category(
            category_id=self.ob_config.football_config.category_id, number_of_events=1)
        self.__class__.eventID = events[0]['event']['id']
        all_cms_offer_modules = self.cms_config.get_offer_modules()
        active_module = [module for module in all_cms_offer_modules if not module.get('disabled')]
        self.assertTrue(active_module, "Active offers not found")
        cms_widgets = self.cms_config.get_widgets()
        active_widgets = [module for module in cms_widgets if not module.get('disabled')]
        self.assertTrue(active_widgets, "Active widgets not found")
        offer_name = 'Auto_offer_C65949654'
        self.__class__.offer_module = self.cms_config.create_offer_module(name=offer_name)
        offer_module_id = self.offer_module.get('id')
        self.cms_config.add_offer(offer_module_id=offer_module_id)

    def test_001_launch_application(self):
        """
        DESCRIPTION: Launch application
        EXPECTED: application launched successfully
        """
        self.site.wait_content_state(state_name="Homepage")

    def test_002_login_to_application(self):
        """
        DESCRIPTION: Login to application
        EXPECTED: user logged into application succesfully
        """
        self.site.login()

    def test_003_verify_betslip_section(self):
        """
        DESCRIPTION: Verify Betslip section
        EXPECTED: Your betslip is empty Please add one or more selections to place a bet message should be displayed.
        """
        right_column_items = self.site.right_column.items_as_ordered_dict
        self.assertIn("BETSLIP", right_column_items.keys(), msg="Betslip section Not Found In Right Column")
        bet_slip = right_column_items.get('BETSLIP')
        bet_slip.click()
        message = self.site.betslip.no_selections_title
        massage2 = self.site.betslip.no_selections_message
        self.assertEqual(message, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'"{message}" is not same as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')
        self.assertEqual(massage2, vec.betslip.NO_SELECTIONS_MSG,
                         msg=f'"{massage2}" is not same as expected "{vec.betslip.NO_SELECTIONS_MSG}"')

    def test_004_verify_mybets_section(self):
        """
        DESCRIPTION: Verify Mybets section
        EXPECTED: Coral:
        EXPECTED: Cashout, Open bets, settled bets tabs should load with respective bets
        EXPECTED: Ladbrokes
        EXPECTED: Open bets, Settled bets tab should load with respective bets
        """
        self.site.betslip.betslip_tabs.items_as_ordered_dict.get('MY BETS').click()

        self.site.betslip.tabs_menu.items_as_ordered_dict.get('OPEN')
        open_bets_data = wait_for_result(lambda:self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict,timeout=2)
        if not open_bets_data:
            open_bets = self.site.open_bets.tab_content.no_selections_message
            self.assertTrue(open_bets.strip(), msg='"You have no Open bets available" text is not present')


        self.site.betslip.tabs_menu.items_as_ordered_dict.get('CASH OUT').click()
        cashout_data = wait_for_result(lambda:self.site.cashout.tab_content.accordions_list.items_as_ordered_dict,timeout=2)
        # Check if cashout data is present
        if not cashout_data:
            # If no data is present, perform the assertion
            cashout_no_selection_msg = self.site.cashout.tab_content.no_selections_message
            self.assertTrue(cashout_no_selection_msg.strip(),
                            msg='"You have no Cash Out bets available" text is not present')

        self.site.betslip.tabs_menu.items_as_ordered_dict.get('SETTLED').click()
        settled_bets_data = wait_for_result(lambda:self.site.settled_bets.tab_content.accordions_list.items_as_ordered_dict, timeout=2)
        if not settled_bets_data:
            settle_bet_message = self.site.settled_bets.tab_content.no_selections_message
            self.assertFalse(settle_bet_message.strip(), msg=f'settle bet msg {settle_bet_message} is not displayed')

    def test_005_verify_mini_games_section(self):
        """
        DESCRIPTION: Verify Mini games section
        EXPECTED: Mini games section should load with available games. On clicking any game, respective game should be played
        """
        name = self.get_filtered_widget_name(self.cms_config.constants.MINI_GAMES_TYPE_NAME)
        self.site.wait_content_state(state_name='Homepage')
        # Added a refresh to ensure scrolling works for both the "My bets" frame and the main site frame.
        self.device.refresh_page()
        mini_games = self.site.right_column.items_as_ordered_dict.get(name)
        self.assertTrue(mini_games, msg='Mini Games widget is not displayed')
        if not mini_games.is_expanded():
            wait_for_result(lambda: mini_games.expand(), timeout=10)
        self.assertTrue(mini_games.is_expanded(), msg='"Mini Games" widget is not expanded')
        mini_games.click()

    def test_006_coralverify_favourites_section(self):
        """
        DESCRIPTION: Coral:
        DESCRIPTION: Verify Favourites section
        EXPECTED: Events added to favourite section should be displayed
        """
        if self.brand == "bma":
            self.navigate_to_edp(event_id=self.eventID)

            self.assertTrue(self.site.sport_event_details.has_favourite_icon(),
                        msg='Favourite icon is not displayed on Football Event Details page')
            favourite_icon = self.site.sport_event_details.favourite_icon
            favourite_icon.click()
            self.assertTrue(favourite_icon.is_selected(), msg=f'Favourite icon is not selected')
            self.site.go_to_home_page()
            favorites_widget = self.site.favourites
            favorites_widget.expand()
            self.assertTrue(favorites_widget.is_expanded(), msg='Favourites widget is not expanded')
            all_favourites_events = self.site.favourites.items_as_ordered_dict
            self.assertTrue(all_favourites_events, msg='favorites events not found even after adding to favourites')

    def test_007_verify_offer_modules_section(self):
        """
        DESCRIPTION: Verify Offer modules section
        EXPECTED: Offer module should be displayed as per CMS config
        """
        # this will give the offers created on front end
        if self.brand == 'bma':
            offer_module_items =self.site.right_column.items_as_ordered_dict.get('OFFER MODULES').items_as_ordered_dict.keys()
            self.assertIn(self.offer_module.get('name').upper(), list(offer_module_items),
                          f"Offer module {self.offer_module.get('name')} not found in offer items: {list(offer_module_items)}")
        else :
            offer_module_items =self.site.right_column.items_as_ordered_dict.get('PROMOTIONS').items_as_ordered_dict.keys()
            # Assertion to check that the offer_module_id is found in the offer module items ie in front end
            self.assertIn(self.offer_module.get('name').upper(), list(offer_module_items),
                          f"Offer module {self.offer_module.get('name')} not found in offer items: {list(offer_module_items)}")

    def test_008_verify_next_races_section(self):
        """
        DESCRIPTION: Verify Next races section
        EXPECTED: Next races section should be displayed with all next
        EXPECTED: upcoming meetings.
        """
        section = self.site.right_column.items_as_ordered_dict.get('NEXT RACES')
        upcoming_meeting = section.items_as_ordered_dict
        self.assertTrue(upcoming_meeting, msg="No upcoming meeting found under next races section")

    def test_009_change_the_modules_order_in_cms(self):
        """
        DESCRIPTION: Change the modules order in CMS
        EXPECTED: Modules order should match with CMS order
        """
        expected_widgets = self.cms_config.get_widgets()
        expected_widget_ids = [expected_widget.get('id') for expected_widget in expected_widgets if
                               expected_widget.get('disabled') == False
                               and expected_widget.get('showOnDesktop') == True
                               and expected_widget.get('columns') in ['both', 'rightColumn']]
        self.widget_order_change(widget_list=expected_widget_ids)
        expected_widget_lists = self.cms_config.get_widgets()
        expected_widget_name_list = [expected_widget_list.get('title').upper() for expected_widget_list in
                                     expected_widget_lists if
                                     expected_widget_list.get('disabled') == False
                                     and expected_widget_list.get('showOnDesktop') == True
                                     and expected_widget_list.get('columns') in ['both', 'rightColumn']]
        self.assertNotEqual(expected_widgets, expected_widget_lists, "The lists are not equal")
        wait_for_cms_reflection(
            lambda: list(self.site.right_column.items_as_ordered_dict.keys()) == expected_widget_name_list,
            timeout=5, haul=5, ref=self)
        actual_widget_list = list(self.site.right_column.items_as_ordered_dict.keys())
        self.assertEqual(actual_widget_list, expected_widget_name_list,
                         msg=f'expected widget order {expected_widget_name_list} not equals to actual widget order '
                             f'{actual_widget_list}')

    def test_010_disable_any_module_from_above_modules_in_cms(self):
        """
        DESCRIPTION: Disable any module from above modules in CMS
        EXPECTED: Respective module shouldn't be displayed in FE
        """
        expected_widgets = self.cms_config.get_widgets()[0]
        self.cms_config.update_widget(widget_id=expected_widgets.get('id'), disabled=True)
        self.assertNotIn(expected_widgets.get('title'), self.site.right_column.items_as_ordered_dict.keys())
        self.cms_config.update_widget(widget_id=expected_widgets.get('id'), disabled=False)
