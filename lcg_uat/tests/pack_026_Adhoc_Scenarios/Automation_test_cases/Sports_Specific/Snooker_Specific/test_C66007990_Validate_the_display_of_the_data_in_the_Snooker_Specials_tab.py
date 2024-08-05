from collections import OrderedDict
import pytest
from crlat_cms_client.utils.exceptions import CMSException
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.sports_specific
@pytest.mark.snooker_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C66007990_Validate_the_display_of_the_data_in_the_Snooker_Specials_tab(BaseBetSlipTest):
    """
    TR_ID: C66007990
    NAME: Validate the display of the data in the Snooker Specials tab.
    DESCRIPTION: This test case needs to verify Specials tab display for the Snooker sport.
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2.Specials tab can be configured from CMS-&gt;
    PRECONDITIONS: Sports menu -&gt; Sportscategory -&gt; Snooker -&gt; Specials tab -&gt; Enable/Disable.
    PRECONDITIONS: Note: In mobile when no events are available Snooker sport is not displayed in A-Z sports menu and on clicking Snooker  from Sports ribbon user is navigated back to the sports homepage.
    """
    keep_browser_open = True
    home_breadcrumb = vec.sb.HOME_FOOTER_ITEM.title()

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        cms_config.update_sports_tab_status(sport_tab_id=cls.sport_tab_id, enabled=cls.enable_status)

    def get_sport_tab_name(self, name: str, category_id: int):
        tabs_data = self.cms_config.get_sport_config(category_id=category_id).get('tabs')
        sport_tab = next((tab for tab in tabs_data if tab.get('name') == name), '')
        sport_tab_name = sport_tab.get('label').upper()
        return sport_tab_name

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: In CMS, Sport pages -> Sport Categories -> Basketball sport -> Matches tab -> Under  'Virtual Sports Entry Points Section: Matches'
        PRECONDITIONS: check 'Banner Enabled' check box and enter data in remaining fields
        """
        self.__class__.sport_id = self.ob_config.snooker_config.category_id
        self.__class__.sport_name = self.get_sport_title(self.sport_id)
        tab_name = 'specials'
        status = self.cms_config.get_sport_tab_status(tab_name=tab_name, sport_id=self.sport_id)
        if not status:
            raise CMSException('events are not available in specials tab')
        sports_tab_data = self.cms_config.get_sports_tab_data(sport_id=self.sport_id, tab_name=tab_name)
        self.__class__.enable_status = sports_tab_data.get('enabled')
        self.__class__.sport_tab_id = sports_tab_data.get('id')
        if not sports_tab_data.get('enabled'):
            self.cms_config.update_sports_tab_status(sport_tab_id=self.sport_tab_id, enabled=True)

    def test_001_launch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes/Coral application
        EXPECTED: Home page should loaded successfully
        """
        self.site.login()

    def test_002_click_on_snooker_sport(self):
        """
        DESCRIPTION: Click on Snooker sport
        EXPECTED: User should be able to navigate Snooker landing page.
        """
        self.navigate_to_page('sport/snooker')
        self.site.wait_content_state_changed()

    def test_003_verify_snooker_landing_page(self):
        """
        DESCRIPTION: Verify Snooker landing page.
        EXPECTED: Desktop
        EXPECTED: Tabs should be displayed with Matches tab selected by default with today events.
        EXPECTED: In play widget will display if any events are in live when it was enabled in sys config.
        EXPECTED: Mobile
        EXPECTED: Matches module loaded as default with inplay events in it
        """
        # covered in C66007984
        current_tab = self.site.sports_page.tabs_menu.current
        default_tab = self.get_sport_tab_name(name='matches', category_id=self.sport_id)
        self.assertEqual(current_tab.upper(), default_tab, msg=f'default tab is not {default_tab} tab')
        specials_tab = self.get_sport_tab_name(name='specials', category_id=self.sport_id)
        self.site.sports_page.tabs_menu.click_button(specials_tab)
        current_tab = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab.upper(), specials_tab, msg='Could not navigate to outright tab after '
                                                                'clicking on outright tab')

    def test_004_verify_specials_tab(self):
        """
        DESCRIPTION: Verify Specials tab
        EXPECTED: First Accordions should be in expanded mode by default rest need to be in collapsed mode if data present.
        EXPECTED: Special tab should not be visible to the user if no data present in it .
        """
        accordions = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(accordions, msg='accordions is not available are not available')
        accordion_name, accordion = list(accordions.items())[0]
        self.assertTrue(accordion.is_expanded(), msg=f'accordion {accordion_name} is not expanded by default')
        if len(accordions) > 1:
            for accordion_name, accordion in list(accordions.items())[1:]:
                self.assertFalse(accordion.is_expanded(), msg=f'accordion {accordion_name} is expanded by default')

    def test_005_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordions are collapsable and expandable
        EXPECTED: Accordions should be collapsable and expandable
        """
        accordions = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        for accordion_name, accordion in list(accordions.items()):
            if not accordion.is_expanded:
                accordion.expand()
                self.assertTrue(accordion.is_expanded(),
                                msg=f'accordion {accordion_name} is not expanded after expansion')

    def test_006_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should be navigated on the respective page on click
        """
        if self.device_type == 'desktop':
            current_tab = self.site.sports_page.tabs_menu.current
            page = self.site.sports_page
            breadcrumbs = OrderedDict((key.strip(), page.breadcrumbs.items_as_ordered_dict[key])
                                      for key in page.breadcrumbs.items_as_ordered_dict)
            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')
            self.assertEqual(list(breadcrumbs.keys()).index(self.home_breadcrumb), 0,
                             msg='Home page is not shown the first by default')
            self.assertTrue(breadcrumbs[self.home_breadcrumb].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.home_breadcrumb}" breadcrumb')
            self.assertEqual(list(breadcrumbs.keys()).index(self.sport_name), 1,
                             msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
            self.assertTrue(breadcrumbs[self.sport_name].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')
            self.assertEqual(list(breadcrumbs.keys()).index(current_tab.title()), 2,
                             msg=f'"{current_tab.title()} " item name is not shown after "{self.sport_name}"')
            self.assertTrue(int(breadcrumbs[current_tab.title()].link.css_property_value('font-weight')) == 700,
                            msg=f'" matches " hyperlink from breadcrumbs is not highlighted according to the selected page')

    def test_007_verify_by_clicking_on_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be navigated to homepage
        """
        if self.device_type == 'desktop':
            home_breadcrumb = self.site.sports_page.breadcrumbs.items_as_ordered_dict.get('Home')
            home_breadcrumb.click()
            self.site.wait_content_state(state_name='HomePage')

    def test_008_verify_by_clicking_on_backward_chevron_on_above__sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron on above  sport header
        EXPECTED: Mobile
        EXPECTED: User should be navigated to sport navigation page
        """
        if self.device_type == 'mobile':
            if self.brand == 'ladbrokes':
                self.site.header.back_button.click()
                self.site.wait_content_state_changed()
            else:
                self.site.sports_page.header_line.back_button.click()
                self.site.wait_content_state_changed()

    def test_009_verify_by_expanding_the_accordion_and_click_on_events(self):
        """
        DESCRIPTION: Verify by expanding the accordion and click on events
        EXPECTED: User should be navigated to respective page .
        """
        self.test_002_click_on_snooker_sport()
        self.test_003_verify_snooker_landing_page()
        accordions = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        accordion = list(accordions.values())[0]
        if not accordion.is_expanded():
            accordion.expand()
        events = accordion.items_as_ordered_dict
        self.assertTrue(events, msg='events are not available')
        event_name, event = list(events.items())[0]
        event.click()
        actual_event_name = wait_for_result(lambda: self.site.sport_event_details.default_title_bar.event_name_we.text,
                                            timeout=20)
        self.assertEqual(event_name.upper(), actual_event_name.upper(), msg=f'could not navigate to {event_name} page')

    def test_010_verify_by_clicking_on_backward_chevron_beside_specials__header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside Specials  header
        EXPECTED: Desktop
        EXPECTED: User should be naviagted to Specials page
        """
        if self.device_type == 'desktop':
            self.site.back_button_click()
            current_url = self.device.get_current_url()
            self.assertIn('snooker/specials', current_url, msg='could not navigate to specials page')

    def test_011_verify_by_clicking_on_backward_chevron_on_above__specials__header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron on above  Specials  header
        EXPECTED: Mobile
        EXPECTED: User should be naviagted to Specials page
        """
        if self.device_type == 'mobile':
            if self.brand == 'ladbrokes':
                self.site.header.back_button.click()
            else:
                self.site.sports_page.header_line.back_button.click()
            current_url = self.device.get_current_url()
            self.assertIn('snooker/specials', current_url, msg='could not navigate to specials page')

    def test_012_verify_bet_placements_for_single_multiple_complex(self):
        """
        DESCRIPTION: Verify bet placement
        EXPECTED: Bet placements should be successful
        """
        accordion = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        if not accordion.is_expanded():
            accordion.expand()
        event = list(accordion.items_as_ordered_dict.values())[0]
        event.template.bet_button.click()
        if self.device_type == 'mobile':
            self.site.quick_bet_panel.header.close_button.click()
            self.site.open_betslip()
            self.assertTrue(self.site.has_betslip_opened(), msg='Failed to open Betslip')
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
