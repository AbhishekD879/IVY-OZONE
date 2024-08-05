import pytest
import tests
import voltron.environments.constants as vec
from crlat_cms_client.cms_client import fake
from tests.base_test import vtest
from tests.Common import Common
from crlat_cms_client.utils.date_time import get_date_time_as_string
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_cms_reflection, wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.surface_bets
@pytest.mark.desktop
@vtest
@pytest.mark.timeout(900)
class Test_C65865539_Verify_surface_bet_created_for_In_Play_event(Common):
    """
    TR_ID: C65865539
    NAME: Verify surface bet created for In-Play event
    """
    keep_browser_open = True
    surface_bet_title = f"Autotest inplay C65865539 {fake.name_female()}".upper()
    surface_bet_header = "C65865539 surface bet header"
    surface_bet_content = "C65865539 surface bet content"
    surface_bet_svg_icon = "Football"

    def _fetch_and_assert_surface_bet(self, fetch_func, name, page_name, expected_result=True):

        surface_bet = wait_for_cms_reflection(
            fetch_func,
            timeout=10,
            refresh_count=5,
            expected_result=expected_result,
            ref=self,
            haul=10
        )
        if expected_result:
            self.assertTrue(surface_bet, msg=f"Surface bet: {name} not found on {page_name}")
            surface_bet.scroll_to()
        else:
            self.assertFalse(surface_bet, msg=f"Surface bet: {name} Found on {page_name}")
        return surface_bet

    def get_surface_bet_on_home(self, name, expected_result=True):
        def fetch_surface_bet_mobile():
            return self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(name)

        def fetch_surface_bet_others():
            return self.site.home.desktop_modules.items_as_ordered_dict.get(
                vec.SB.HOME_FEATURED_NAME).tab_content.surface_bets.items_as_ordered_dict.get(
                name)

        fetch_surface_bet_func = fetch_surface_bet_mobile if self.device_type == 'mobile' else fetch_surface_bet_others
        return self._fetch_and_assert_surface_bet(fetch_surface_bet_func, name, "Home page", expected_result)

    def get_surface_bet_on_SLP(self, name, expected_result=True):
        return self._fetch_and_assert_surface_bet(
            lambda: self.site.sports_page.tab_content.surface_bets.items_as_ordered_dict.get(name),
            name,
            "SLP page",
            expected_result
        )

    def get_surface_bet_on_EDP(self, name, expected_result=True):
        return self._fetch_and_assert_surface_bet(
            lambda: self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict.get(name),
            name,
            "EDP page",
            expected_result
        )

    def get_surface_bet_on_EVENTHUB(self, name, event_hub_name, expected_result=True):
        if self.device_type != 'mobile':
            raise VoltronException(
                "Event Hub is only available on mobile devices; cannot fetch surface bet on event hub")

        home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
        matched_event_hub_tab = next((tab for tab in home_page_tabs if tab.upper() == event_hub_name), None)
        self.assertTrue(matched_event_hub_tab, msg=f'Event Hub tab: {event_hub_name} not found in Home Page tabs')

        home_page_tabs[matched_event_hub_tab].click()
        self.assertEqual(self.site.home.tabs_menu.current, matched_event_hub_tab,
                         f'Tab did not switch after clicking the "{event_hub_name}" tab')

        return self._fetch_and_assert_surface_bet(
            lambda: self.site.sports_page.tab_content.surface_bets.items_as_ordered_dict.get(name),
            name,
            "SLP page",
            expected_result
        )

    def get_surface_bet(self, on="HOME", name="", **kwargs):
        fetch_methods = {
            "HOME": {
                "method": self.get_surface_bet_on_home,
                "args": ["name", "expected_result"]
            },
            "SLP": {
                "method": self.get_surface_bet_on_SLP,
                "args": ["name", "expected_result"]
            },
            "EDP": {
                "method": self.get_surface_bet_on_EDP,
                "args": ["name", "expected_result"]
            },
            "EVENTHUB": {
                "method": self.get_surface_bet_on_EVENTHUB,
                "args": ["name", "event_hub_name", "expected_result"]
            }
        }

        on_upper = on.upper()
        if on_upper not in fetch_methods:
            raise ValueError(f"Invalid surface bet location: {on}")

        method_info = fetch_methods[on_upper]
        method = method_info["method"]
        method_args = {arg: kwargs.get(arg) for arg in method_info["args"] if arg in kwargs}

        # The name argument is common to all methods
        method_args["name"] = name

        return method(**method_args)

    def get_event_hub(self) -> tuple:
        """Retrieve or create event hub and return its index number and name."""
        existing_event_hubs = self.cms_config.get_event_hubs()
        existing_event_hubs_index_numbers = [index['indexNumber'] for index in existing_event_hubs]

        # Find a suitable index number
        index_number = next(index for index in range(1, 20) if index not in existing_event_hubs_index_numbers)

        # Create event hub
        created_event_hub = self.cms_config.create_event_hub(index_number=index_number)
        event_hub_name = created_event_hub.get('title').upper()

        # Add event hub to module ribbon tab
        internal_id = f'tab-eventhub-{index_number}'
        module_ribbon_tab_name = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                               internal_id=internal_id,
                                                                               hub_index=index_number,
                                                                               display_date=True)

        return index_number, module_ribbon_tab_name.get('title').upper()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create a event in OB
        PRECONDITIONS: Surface bet Creation in CMS:
        PRECONDITIONS: 1.Login to Environment specific CMS
        PRECONDITIONS: 2.Navigate to Home Page -->Surface bets
        PRECONDITIONS: 3.Click 'Create Surface bet'
        PRECONDITIONS: 4.Check the checkbox 'Enabled','Display on Highlights tab','Display on EDP' and
        'Display in Desktop'
        PRECONDITIONS: 5.Enter All fields like
        PRECONDITIONS: Active Checkbox
        PRECONDITIONS: Title as 'Featured - Ladies Matches '
        PRECONDITIONS: EventId (Take an Inplay EventID )
        PRECONDITIONS: Show on Sports select 'All Sports'
        PRECONDITIONS: Show on EventHub: Select any eventhub
        PRECONDITIONS: Content Header
        PRECONDITIONS: Content
        PRECONDITIONS: Was Price
        PRECONDITIONS: Selection ID
        PRECONDITIONS: Display From
        PRECONDITIONS: Display To
        PRECONDITIONS: SVG Icon
        PRECONDITIONS: SVG Background
        PRECONDITIONS: 6.Check segment as 'Universal' or 'Segment'
        PRECONDITIONS: 7.Click Save Changes
        PRECONDITIONS: Check the Sort Order of Surface bet Module
        PRECONDITIONS: Navigate to Home Page-->Surface bet Module--> Select newly Created Surface bet-->
        Check the Surface bet order
        """
        # Extract event based on backend_env
        if tests.settings.backend_env == "prod":
            event = self.get_active_events_for_category(in_play_event=True, category_id=16)[0].get("event")
        else:
            event = self.ob_config.add_football_event_to_autotest_league2(is_live=True).ss_response['event']

        # Extract live_event_market and event_selection from the event
        live_event_market = next(
            (market['market'] for market in event['children'] if market['market'].get('children')),
            None
        )
        self.__class__.live_event_market_id = live_event_market['id']
        self.__class__.event_selection = live_event_market['children'][0]['outcome']
        index_number, self.__class__.event_hub_name = self.get_event_hub()

        sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(index_number)
        sb_module_cms = None
        for module in sports_module_event_hub:
            if module['moduleType'] == 'SURFACE_BET':
                sb_module_cms = module
                break
        if sb_module_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='SURFACE_BET',
                                                          page_id=index_number)
        else:
            surface_bet_module_status = next((module['disabled'] for module in sports_module_event_hub
                                              if module['moduleType'] == 'SURFACE_BET'), None)
            if surface_bet_module_status is True:
                self.cms_config.change_sport_module_state(sport_module=sb_module_cms, active=True)

        self.__class__.event_id = event['id']
        # Define surface_bet_config
        surface_bet_config = {
            "selection_id": self.event_selection['id'],
            "eventIDs": [self.event_id],
            "highlightsTabOn": True,
            "edp_on": True,
            "svg_icon": self.surface_bet_svg_icon,
            "eventHubsIndexes": [index_number],
            "on_homepage": True,
            "displayOnDesktop": True,
            "title": self.surface_bet_title,
            "contentHeader": self.surface_bet_header,
            "content": self.surface_bet_content,
            "categoryIDs": [16],
            "all_sports": True,
        }

        # Add surface bet
        self.__class__.created_surface_bet = self.cms_config.add_surface_bet(**surface_bet_config)

    def test_001_login_to_ladscoral_ampltenvironmentampgt(self):
        """
        DESCRIPTION: Login to Lads/Coral &amp;lt;Environment&amp;gt;
        EXPECTED: User should be logged in
        """
        self.site.login()

    def test_002_observe_the_surface_bet_created_on_homepage(self):
        """
        DESCRIPTION: Observe the surface bet created on homepage
        EXPECTED: Surface bet created in CMS should be reflected on homepage
        """
        self.__class__.surface_bet = self.get_surface_bet(on="HOME", name=self.surface_bet_title)
        self.assertTrue(self.surface_bet, msg=f"Surface bet with title '{self.surface_bet_title}' "
                                              f"not found on Homepage")

    def test_003_validate_the_surface_bet_title(self):
        """
        DESCRIPTION: Validate the surface bet Title
        EXPECTED: Title Name should be displayed as per CMS config
        """
        surface_bet_title = self.surface_bet.name
        self.assertEqual(surface_bet_title, self.surface_bet_title,
                         msg=f"Expected surface bet title '{self.surface_bet_title}' "
                             f"but found {surface_bet_title}")

    def test_004_validate_the_surface_bet_is_displayed_on_specific_sports(self):
        """
        DESCRIPTION: Validate the surface bet is displayed on Specific Sports
        EXPECTED: Surface bet created should reflect on specific sports pages as per CMS config
        """
        self.navigate_to_page('sport/football')
        surface_bet = self.get_surface_bet(on="SLP", name=self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f"Surface bet with title '{self.surface_bet_title}' "
                                         f"not found on SPORT PAGE")
        self.site.back_button_click()

    def test_005_validate_the_surface_bet_is_displayed_in_the_event_hubs(self):
        """
        DESCRIPTION: Validate the surface bet is displayed in the event hubs
        EXPECTED: Surface bet created should reflect in the 'eventhub' selected as per CMS config
        """
        if self.device_type == "mobile":
            self.__class__.surface_bet = self.get_surface_bet(on="EVENTHUB",
                                                              name=self.surface_bet_title,
                                                              event_hub_name=self.event_hub_name)
            self.assertTrue(self.surface_bet, msg=f"Surface bet with title '{self.surface_bet_title}' "
                                                  f"not found on Event hub: {self.event_hub_name}")

    def test_006_validate_the_surface_bet_content_header(self):
        """
        DESCRIPTION: Validate the surface bet 'Content header'
        EXPECTED: Content Header' should be displayed as per CMS config
        """
        self.__class__.surface_bet = self.get_surface_bet(on="HOME", name=self.surface_bet_title)
        self.assertTrue(self.surface_bet, msg=f"Surface bet with title '{self.surface_bet_title}' "
                                              f"not found on Homepage")
        self.surface_bet.scroll_to()
        surface_bet_header = wait_for_result(lambda: self.surface_bet.content_header, timeout=10, expected_result=True)
        self.assertEqual(surface_bet_header, self.surface_bet_header,
                         msg=f"Expected surface bet header {self.surface_bet_header} "
                             f"but found {surface_bet_header}")

    def test_007_validate_the_surface_bet_content(self):
        """
        DESCRIPTION: Validate the surface bet 'Content'
        EXPECTED: Content' should be displayed as per CMS config
        """
        surface_bet_content = self.surface_bet.content
        self.assertEqual(surface_bet_content, self.surface_bet_content,
                         msg=f"Expected surface bet content to be {self.surface_bet_content} "
                             f"but found {surface_bet_content}")

    def test_008_validate_the_svg_icon_and_svg_background(self):
        """
        DESCRIPTION: Validate the SVG icon and SVG background
        EXPECTED: SVG icon and SVG background should be displayed as per CMS config
        """
        svg_icon = self.surface_bet.header.icontext
        self.assertEqual(svg_icon, f"#{self.surface_bet_svg_icon}",
                         msg=f"Expected surface bet icon {self.surface_bet_svg_icon} "
                             f"but got surface bet icon {svg_icon}")

    def test_009_verify_user_is_able_to_select_the_selections_on_surface_bet(self):
        """
        DESCRIPTION: Verify user is able to select the selections on Surface bet
        EXPECTED: User should be able to select &amp; selections should be highlighted
        """
        self.surface_bet.scroll_to_we()
        bet_button = self.surface_bet.bet_button
        bet_button.click()
        if self.device_type == "mobile":
            self.site.wait_for_quick_bet_panel(expected_result=True)
            self.site.quick_bet_panel.close()
            self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        bet_button.scroll_to_we()
        self.assertTrue(bet_button.is_selected(), f'unable to select bet button')

    def test_010_verify_edited_field_changes_are_reflecting_in_fe_for_surface_bet(self):
        """
        DESCRIPTION: Verify Edited field changes are reflecting in FE for Surface bet
        EXPECTED: Edited fields data should be updated for Surface bet
        """
        self.navigate_to_page("/")
        update_surface_bet_config = {
            "surface_bet_id": self.created_surface_bet['id'],
            "contentHeader": self.surface_bet_header + " Updated",
            "content": self.surface_bet_content + " Updated",
            "title": self.surface_bet_title + " Updated".upper()
        }
        self.cms_config.update_surface_bet(**update_surface_bet_config)
        wait_for_haul(5)
        updated_surface_bet = self.get_surface_bet(on="HOME", name=update_surface_bet_config.get("title"))

        # content Header verification
        surface_bet_header = updated_surface_bet.content_header
        self.assertEqual(surface_bet_header, update_surface_bet_config['contentHeader'],
                         msg=f"Expected surface bet header {update_surface_bet_config['contentHeader']} "
                             f"but found {surface_bet_header}")

        # content verification
        surface_bet_content = updated_surface_bet.content
        self.assertEqual(surface_bet_content, update_surface_bet_config['content'],
                         msg=f"Expected surface bet content to be {update_surface_bet_config['content']} "
                             f"but found {surface_bet_content}")

    def test_011_verify_surface_bet_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet disappears in FE upon deletion in CMS
        EXPECTED: Surface bet should disappear in FE
        """
        self.cms_config.delete_surface_bet(self.created_surface_bet['id'])
        self.cms_config._created_surface_bets.remove(self.created_surface_bet['id'])
        surface_bet = self.get_surface_bet(on="HOME", name=self.surface_bet_title, expected_result=False)
        self.assertFalse(surface_bet, msg=f"Surface bet {self.surface_bet_title} is Still Displayed "
                                          f"Even though surface bet is Deleted")
