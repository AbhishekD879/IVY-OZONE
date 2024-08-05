import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result, wait_for_cms_reflection, wait_for_haul
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.desktop_specific
@pytest.mark.desktop_only
@pytest.mark.adhoc_suite
@vtest
class Test_C65949653_Right_side_widget_display_in_desktop_before_login(Common):
    """
    TR_ID: C65949653
    NAME: Right side widget display in desktop before login
    DESCRIPTION: This test case verifies right side widget in desktop before login
    PRECONDITIONS: 1. Login to CMS
    PRECONDITIONS: 2. Navigate to Widgets section
    PRECONDITIONS: 3. Modules should be enabled in widgets section
    PRECONDITIONS: 4. Desktop offers should be created in CMS
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def widget_order_change(self, widget_list: list):
        # Select the second item in the widget list to be moved.
        moving_item = widget_list[1]
        # Remove the selected item from the list.
        widget_list.remove(moving_item)
        # Insert the removed item at the second-to-last position in the list.
        widget_list.insert(-1, moving_item)
        # Set the new widget ordering in the CMS configuration with the specified moving item.
        self.cms_config.set_widget_ordering(new_order=widget_list, moving_item=moving_item)
        # Retrieve the expected widgets from the CMS configuration after the ordering change.
        expected_widget_lists = self.cms_config.get_widgets()
        # Create a list of expected widget IDs that are not disabled and should be shown on the desktop.
        expected_widget_name_list = [expected_widget_list.get('id') for expected_widget_list in
                                     expected_widget_lists if
                                     expected_widget_list.get('disabled') == False
                                     and expected_widget_list.get('showOnDesktop') == True]

        # Assert that the updated widget list matches the expected widget name list.
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

    def test_002_verify_betslip_section(self):
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

    def test_003_verify_mybets_section(self):
        """
        DESCRIPTION: Verify Mybets section
        EXPECTED: Coral:
        EXPECTED: Cashout, Open bets, settled bets tabs should be displayed with "Please log in to see your cash out bets. With a Login button should be displayed"
        EXPECTED: Ladbrokes:
        EXPECTED: Open bets, Settled bets tab should be displayed with " Your open bets will appear here,
        EXPECTED: Please log in to view." message
        """
        # Click on the 'MY BETS' tab in the betslip
        self.site.betslip.betslip_tabs.items_as_ordered_dict.get('MY BETS').click()
        # Retrieve the 'CASH OUT' tab in the betslip (no need to assign it to a variable)
        self.site.betslip.tabs_menu.items_as_ordered_dict.get('CASH OUT').click()
        # Check if the 'You have no Cash Out bets available' text is present
        cashout_no_selection_msg = self.site.cashout.tab_content.no_selections_message
        self.assertTrue(cashout_no_selection_msg, msg='"You have no Cash Out bets available" text is not present')
        # Click on the 'OPEN BETS' tab in the betslip
        self.site.betslip.tabs_menu.items_as_ordered_dict.get('OPEN').click()
        # Retrieve the 'Open bets' message (no need to assign it to a variable)
        open_bets = self.site.open_bets.tab_content.no_selections_message
        # Check if the 'You have no Open bets available' text is present
        self.assertTrue(open_bets, msg='"You have no Open bets available" text is not present')
        # Click on the 'SETTLED BETS' tab in the betslip
        self.site.betslip.tabs_menu.items_as_ordered_dict.get('SETTLED').click()
        # Retrieve the 'Settled bet' message (no need to assign it to a variable)
        settle_bet_message = self.site.settled_bets.tab_content.no_selections_message
        # Check if the 'Settled bet' message is displayed
        self.assertTrue(settle_bet_message, msg=f'settle bet msg {settle_bet_message} is not displayed')
        # Refresh the page using self.device.refresh_page()
        self.device.refresh_page()

    def test_004_verify_mini_games_section(self):
        """
        DESCRIPTION: Verify Mini games section
        EXPECTED: Mini games banner should be displayed. On clicking mini games banner, it will redirect to Login page
        """
        # Get the name of the Mini Games widget using the MINI_GAMES_TYPE_NAME constant from cms_config.
        name = self.get_filtered_widget_name(self.cms_config.constants.MINI_GAMES_TYPE_NAME)
        # Wait for the content state to be 'Homepage' on the site.
        self.site.wait_content_state(state_name='Homepage')
        # Retrieve the Mini Games widget from the right column items.
        mini_games = self.site.right_column.items_as_ordered_dict.get(name)
        # Check if the Mini Games widget is displayed.
        self.assertTrue(mini_games, msg='Mini Games widget is not displayed')
        # If the Mini Games widget is not expanded, expand it and wait for it to expand within a 10-second timeout.
        if not mini_games.is_expanded():
            wait_for_result(lambda: mini_games.expand(), timeout=10)
        # Check if the Mini Games widget is expanded.
        self.assertTrue(mini_games.is_expanded(), msg='"Mini Games" widget is not expanded')
        # Click on the Mini Games widget.
        mini_games.click()
        # Wait for the "DIALOG_MANAGER_LOG_IN" dialog to appear.
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        # Check if the dialog is displayed.
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        # Click the close button on the dialog's header.
        dialog.header_object.close_button.click()

    def test_005_coralverify_favourites_section(self):
        """
        DESCRIPTION: Coral:
        DESCRIPTION: Verify Favourites section
        EXPECTED: To view and add matches into your favourites,
        EXPECTED: please log in to your account message with a login button should be displayed
        """
        if self.brand == "bma":
            self.site.right_column.items_as_ordered_dict.get(vec.sb.FAVOURITES.upper()).click()
            favorites_widget = self.site.favourites
            favorites_widget.expand()
            self.assertTrue(favorites_widget.is_expanded(), msg='Favourites widget is not expanded')
            please_log_in_text = favorites_widget.widget_text_not_logged
            log_in_button = favorites_widget.login_button.name
            self.assertTrue(please_log_in_text,
                            msg=f'please log in to your account message {please_log_in_text} is not displayed')
            self.assertTrue(log_in_button, msg='log in button is not displayed')

    def test_006_verify_offer_modules_section(self):
        """
        DESCRIPTION: Verify Offer modules section
        EXPECTED: Offer module should be displayed as per CMS config
        """
        self.device.refresh_page()
        # this will give the offers created on front end
        module_name = 'PROMOTIONS' if self.brand != "bma" else 'OFFER MODULES'
        offer_module_items = self.site.right_column.items_as_ordered_dict.get(module_name).items_as_ordered_dict.keys()
        # Assertion to check that the offer_module_id is found in the offer module items ie in front end
        self.assertIn(self.offer_module.get('name').upper(), list(offer_module_items),
                      f"Offer module {self.offer_module} not found in right column items")

    def test_007_verify_next_races_section(self):
        """
        DESCRIPTION: Verify Next races section
        EXPECTED: Next races section should be displayed with all next
        EXPECTED: upcoming meetings.
        """
        section = self.site.right_column.items_as_ordered_dict.get(vec.racing.NEXT_RACES.upper())
        upcoming_meeting = section.items_as_ordered_dict
        self.assertTrue(upcoming_meeting, msg="No upcoming meeting found under next races section")

    def test_008_change_the_modules_order_in_cms(self):
        """
        DESCRIPTION: Change the modules order in CMS
        EXPECTED: Modules order should match with CMS order
        """
        # Retrieve the expected widgets from the CMS configuration.
        expected_widgets = self.cms_config.get_widgets()
        # Create a list of expected widget IDs that are not disabled and should be shown on the desktop.
        expected_widget_ids = [expected_widget.get('id') for expected_widget in expected_widgets if
                               expected_widget.get('disabled') == False
                               and expected_widget.get('showOnDesktop') == True]

        # Change the order of widgets using the widget_order_change method.
        self.widget_order_change(widget_list=expected_widget_ids)
        # Retrieve the expected widgets again after the order change.
        expected_widget_lists = self.cms_config.get_widgets()
        # Create a list of expected widget names that are not disabled and should be shown on the desktop.
        expected_widget_name_list = [expected_widget_list.get('title').upper() for expected_widget_list in
                                     expected_widget_lists if expected_widget_list.get('disabled') == False and
                                     expected_widget_list.get('showOnDesktop') == True and
                                     (expected_widget_list.get(
                                         'columns').upper() == "RIGHTCOLUMN" or expected_widget_list.get(
                                         'columns').upper() == "BOTH")]

        # Assert that the original and updated lists of expected widgets are not equal.
        self.assertNotEqual(expected_widgets, expected_widget_lists, "The lists are not equal")
        # Wait for the CMS reflection to ensure that the actual widget order matches the expected order.
        wait_for_cms_reflection(
            lambda: list(self.site.right_column.items_as_ordered_dict.keys()) == expected_widget_name_list,
            timeout=5, haul=5, ref=self)

        # Get the actual widget list from the site's right column.
        actual_widget_list = list(self.site.right_column.items_as_ordered_dict.keys())
        # Assert that the actual widget order matches the expected order with a custom message.
        self.assertEqual(actual_widget_list, expected_widget_name_list,
                         msg=f'expected widget order {expected_widget_name_list} not equals to actual widget order '
                             f'{actual_widget_list}')

    def test_009_disable_any_module_from_above_modules_in_cms(self):
        """
        DESCRIPTION: Disable any module from above modules in CMS
        EXPECTED: Respective module shouldn't be displayed in FE
        """
        expected_widgets = self.cms_config.get_widgets()[0]
        self.cms_config.update_widget(widget_id=expected_widgets.get('id'), disabled=True)
        self.assertNotIn(expected_widgets.get('title'), self.site.right_column.items_as_ordered_dict.keys())
        self.cms_config.update_widget(widget_id=expected_widgets.get('id'), disabled=False)
