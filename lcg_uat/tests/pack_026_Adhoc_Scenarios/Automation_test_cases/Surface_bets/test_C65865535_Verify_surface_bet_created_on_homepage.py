import pytest
import tests
import voltron.environments.constants as vec
from crlat_cms_client.utils.date_time import get_date_time_as_string
from voltron.utils.helpers import generate_name
from tests.base_test import vtest
from datetime import datetime
from tzlocal import get_localzone
from voltron.utils.waiters import wait_for_haul
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.surface_bets
@pytest.mark.homepage_featured
@vtest
class Test_C65865535_Verify_surface_bet_created_on_homepage(BaseBetSlipTest):
    """
    TR_ID: C65865535
    NAME: Verify surface bet created on homepage
    DESCRIPTION: This test case verifies surface bet created on homepage
    PRECONDITIONS: Create an event in OB
    PRECONDITIONS: Surface bet Creation in CMS:
    PRECONDITIONS: 1.Login to Environment specific CMS
    PRECONDITIONS: 2.Navigate to Home Page -->Surface bets
    PRECONDITIONS: 3.Click 'Create Surface bet'
    PRECONDITIONS: 4.Check the checkbox 'Enabled','Display on Highlights tab','Display on EDP' and 'Display in Desktop'
    PRECONDITIONS: 5.Enter All fields like
    PRECONDITIONS: Active Checkbox
    PRECONDITIONS: Title as 'Featured - Ladies Matches '
    PRECONDITIONS: EventIds (Create with EventId)
    PRECONDITIONS: Show on Sports
    PRECONDITIONS: Show on EventHub
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
    PRECONDITIONS: Navigate to Home Page-->Surface bet Module--> Select newly Created Surface bet--> Check the Surface bet order
    """
    keep_browser_open = True
    segment = vec.bma.CSP_CMS_SEGEMENT
    timezone = str(get_localzone())

    def wait_up_to_time_complete(self, end_time):
        now = get_date_time_as_string(date_time_obj=datetime.now(),
                                      time_format='%Y-%m-%dT%H:%M:%S.%f',
                                      url_encode=False)[:-3] + 'Z'
        time_formate = '%Y-%m-%dT%H:%M:%S.%fZ'
        end_time = datetime.strptime(end_time, time_formate)
        now_time = datetime.strptime(now, time_formate)
        time_difference_in_sec = (end_time - now_time).total_seconds()
        wait_for_haul(time_difference_in_sec)

    def verify_surface_bet(self, expected_result=True):
        """
        To Verify presence of surface
        """
        surface_bet = None
        for i in range(20):
            self.device.refresh_page()
            if self.device_type == 'mobile' and self.site.home.tab_content.has_surface_bets(expected_result=True,
                                                                                            timeout=2):
                self.__class__.surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
                self.__class__.surface_bets = {sb_name.upper(): sb for sb_name, sb in self.surface_bets.items()}
                surface_bet = self.surface_bets.get(self.surface_bet_title)

            if self.device_type != 'mobile' and self.site.home.get_module_content(
                    vec.SB.HOME_FEATURED_NAME).has_surface_bets(expected_result=True, timeout=2):
                self.__class__.surface_bets = self.site.home.get_module_content(
                    vec.SB.HOME_FEATURED_NAME).surface_bets.items_as_ordered_dict
                self.__class__.surface_bets = {sb_name.upper(): sb for sb_name, sb in self.surface_bets.items()}
                surface_bet = self.surface_bets.get(self.surface_bet_title)

            if expected_result == bool(surface_bet):
                break
            else:
                wait_for_haul(5)

        if expected_result:
            self.assertTrue(surface_bet, msg=f"surface bet : {self.surface_bet_title} is not displayed")
        else:
            self.assertFalse(surface_bet, msg=f"surface bet : {self.surface_bet_title} is displayed")

    def test_000_preconditions(self):
        """"
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Sports pages > Sports category
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)
            outcomes_1 = next(((market['market']['children']) for market in events[0]['event']['children'] if
                               market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_1}
            selection_id_1 = list(event_selection.values())[0]

            outcomes_2 = next(((market['market']['children']) for market in events[1]['event']['children'] if
                               market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_2}
            selection_id_2 = list(event_selection.values())[1]

        else:
            event = self.ob_config.add_football_event_to_england_premier_league()
            selection_id_1 = event.selection_ids[event.team1]
            selection_id_2 = event.selection_ids[event.team1]
        self.__class__.surface_bet = self.cms_config.add_surface_bet(selection_id=selection_id_1,
                                                                     title='Auto_' + generate_name(),
                                                                     highlightsTabOn=True,
                                                                     svg_icon='football',
                                                                     displayOnDesktop=True,
                                                                     on_homepage=True)

        self.cms_config.add_surface_bet(selection_id=selection_id_2,
                                        title="Autotest_5535_dummy",
                                        highlightsTabOn=True,
                                        svg_icon='football',
                                        displayOnDesktop=True,
                                        on_homepage=True)

        self.__class__.surface_bet_title = self.surface_bet.get('title').upper()
        self.__class__.surface_bet_id = self.surface_bet['id']

    def test_001_login_to_ladscoral_ltenvironmentgt(self):
        """
        DESCRIPTION: Login to Lads/Coral &lt;Environment&gt;
        EXPECTED: User should be logged in
        """
        self.site.login()

    def test_002_observe_the_surface_bet_created_on_homepage(self):
        """
        DESCRIPTION: Observe the surface bet created on homepage
        EXPECTED: Surface bet created in CMS should be reflected on homepage
        """
        self.verify_surface_bet()
        surface_bet = self.surface_bets.get(self.surface_bet_title)

        # verify Content Header
        surface_bet.scroll_to_we()
        header = surface_bet.content_header.upper()
        Header_from_cms = self.surface_bet['contentHeader'].upper()
        self.assertEqual(header, Header_from_cms,
                         msg=f'Actual header is {header}, But expected is {Header_from_cms}')

        # Verify Content
        content = surface_bet.content.strip().upper()
        content_from_cms = self.surface_bet['content'].strip().upper()
        self.assertEqual(content, content_from_cms,
                         msg=f'Actual Content is {content}, But expected is {content_from_cms}')

        # Verify svg icon
        svg_icon = surface_bet.header.icontext
        svg_cms = '#' + self.surface_bet['svgId']
        self.assertEqual(svg_icon, svg_cms,
                         msg=f'Actual svg icon is {svg_icon}, But expected is {svg_cms}')

    def test_003_validate_the_order_of_surface_bet_created_on_homepage(self):
        """
        DESCRIPTION: Validate the Order of surface bet created on homepage
        EXPECTED: Order of Surface bet created should be as per CMS config
        """
        # Covered in other test cases

    def test_004_change_the_order_of_surface_bet_created(self):
        """
        DESCRIPTION: Change the Order of surface bet created
        EXPECTED: Order of Surface bet created should be as per CMS config
        """
        # Covered in other test cases

    def test_005_validate_the_surface_bet_title(self):
        """
        DESCRIPTION: Validate the surface bet Title
        EXPECTED: Title Name should be displayed as per CMS config
        """
        # This step is covered in step 02

    def test_006_validate_the_surface_bet_is_displayed_on_all_sports(self):
        """
        DESCRIPTION: Validate the surface bet is displayed on 'All Sports'
        EXPECTED: Surface bet created should reflect on 'All Sports' pages as per CMS config
        """
        # Will not cover this step. Surface bet is reflected in All sports pages.

    def test_007_validate_the_surface_bet_is_displayed_in_the_event_hub_selected(self):
        """
        DESCRIPTION: Validate the surface bet is displayed in the event hub selected
        EXPECTED: Surface bet created should reflect in the 'eventhub' selected as per CMS config
        """
        # This step covered in other test cases

    def test_008_validate_the_surface_bet_content_header(self):
        """
        DESCRIPTION: Validate the surface bet 'Content header'
        EXPECTED: Content Header' should be displayed as per CMS config
        """
        # This step is covered in step 02

    def test_009_validate_the_surface_bet_content(self):
        """
        DESCRIPTION: Validate the surface bet 'Content'
        EXPECTED: Content' should be displayed as per CMS config
        """
        # This step is covered in step 02

    def test_010_validate_the_surface_bet_was_price(self):
        """
        DESCRIPTION: Validate the surface bet 'Was Price'
        EXPECTED: Was Price' should be displayed as per config in the OB
        """
        # NA

    def test_011_verify_the_surface_bet_display_from_and_to_date(self):
        """
        DESCRIPTION: Verify the Surface Bet Display From and To date
        EXPECTED: Surface bet should be displayed based on CMS config start date
        EXPECTED: Surface bet should be displayed based on CMS config end date
        """
        # This step is covered in step 13

    def test_012_validate_the_svg_icon_and_svg_background(self):
        """
        DESCRIPTION: Validate the SVG icon and SVG background
        EXPECTED: SVG icon and SVG background should be displayed as per CMS config
        """
        # This step is covered in step 02

    def test_013_verify_surface_bet_display_from_and_display_to_date_has_set_to_pastfuture_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' and 'Display to' date has set to past/future in CMS
        EXPECTED: Surface bet should not be displayed in FE
        """
        self.__class__.time_format = '%Y-%m-%dT%H:%M:%S.%f'
        future_date_from = self.get_date_time_formatted_string(time_format=self.time_format, days=2)[:-3] + 'Z'
        future_date_to = self.get_date_time_formatted_string(time_format=self.time_format, days=3)[:-3] + 'Z'
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           displayFrom=future_date_from,
                                           displayTo=future_date_to)
        self.verify_surface_bet(expected_result=False)

    def test_014_verify_surface_bet_display_from_has_set_to_past_and_display_to_in_a_few_mins_from_the_current_time(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to past and 'Display to' in a few mins from the current time.
        EXPECTED: Surface bet should disappear in FE
        """
        # display from : past
        # display to : 1 min from now
        start_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                             url_encode=False, hours=-20)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                           url_encode=False, minutes=1.5)[:-3] + 'Z'
        if self.timezone.upper() == "UTC":
            end_time_for_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                       url_encode=False, minutes=1)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            end_time_for_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                       url_encode=False, minutes=-59)[:-3] + 'Z'
        else:
            end_time_for_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                       url_encode=False, hours=-5.5, minutes=1)[:-3] + 'Z'
        self._logger.info(f'end_time_for_cms before update : {end_time_for_cms}')

        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           displayFrom=start_time,
                                           displayTo=end_time_for_cms)
        self.verify_surface_bet(expected_result=True)
        self.wait_up_to_time_complete(end_time)
        self.verify_surface_bet(expected_result=False)

    def test_015_verify_surface_bet_display_from_has_set_to_few_mins_from_current_time_and_display_to_from_the_future(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to few mins from current time and 'Display to' from the future
        EXPECTED: Surface bet should display as per 'Display from' time
        """
        # display from : 1.5 min from now
        # display to : tomorrow
        start_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                             url_encode=False, minutes=1.5)[:-3] + 'Z'
        if self.timezone.upper() == "UTC":
            start_time_for_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                         url_encode=False, minutes=1)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            start_time_for_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                         url_encode=False, minutes=-59)[:-3] + 'Z'
        else:
            start_time_for_cms = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                                         url_encode=False, hours=-5.5, minutes=1)[:-3] + 'Z'
        end_time = self.get_date_time_formatted_string(time_format=self.time_format, days=1)[:-3] + 'Z'
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           displayFrom=start_time_for_cms,
                                           displayTo=end_time)
        self.verify_surface_bet(expected_result=False)
        self.wait_up_to_time_complete(start_time)
        self.verify_surface_bet(expected_result=True)

    def test_016_verify_surface_bets_display_if_there_are_more_no_of_surfaces_bets_created_in_homepage(self):
        """
        DESCRIPTION: Verify Surface bets display if there are more no of surfaces bets created in homepage
        EXPECTED: Surface bet with Right or Left arrow should display
        """
        if self.device_type != 'mobile':
            surface_bets = self.site.home.get_module_content(
                vec.SB.HOME_FEATURED_NAME).surface_bets.items_as_ordered_dict

            if len(surface_bets) > 3:
                event1 = list(surface_bets.values())[0]
                event1.mouse_over()
                wait_for_haul(2)
                scroll_arrow = self.site.home.get_module_content(
                    vec.SB.HOME_FEATURED_NAME).surface_bets.has_scroll_button()
                self.assertTrue(scroll_arrow, msg="Slider button is not displayed even if there are more than 3 "
                                                  "surface bets")

    def test_017_verify_surface_bets_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify Surface bets left and right scroll
        EXPECTED: User should able to scroll from left to right &amp; from right to left
        """
        # This step is covered in C65865536

    def test_018_verify_user_is_able_to_select_the_selections_on_surface_bet(self):
        """
        DESCRIPTION: Verify user is able to select the selections on Surface bet
        EXPECTED: User should be able to select &amp; selections should be highlighted
        """
        if self.device_type == 'mobile':
            surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        else:
            surface_bets = self.site.home.get_module_content(
                vec.SB.HOME_FEATURED_NAME).surface_bets.items_as_ordered_dict

        surface_bets = {sb_name.upper(): sb for sb_name, sb in surface_bets.items()}
        surface_bet = surface_bets.get(self.surface_bet_title)
        surface_bet.scroll_to_we()
        bet_button = surface_bet.bet_button
        bet_button.click()
        self.assertTrue(bet_button.is_selected(), f'unable to select bet button')

        if self.device_type == 'mobile':
            wait_for_haul(2)
            quick_bet = self.site.quick_bet_panel
            wait_for_haul(3)
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            quick_bet.place_bet.click()
            bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.header.close_button.click()
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.bet_receipt.footer.reuse_selection_button.click()
            bet_button.scroll_to_we()
            self.assertTrue(bet_button.is_selected(), f'bet button is not selected after clicking on reuse selection')
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()

    def test_019_activatedeactivate_the_whole_surface_bet_module_on_homepage(self):
        """
        DESCRIPTION: Activate/Deactivate the whole Surface bet module on homepage
        EXPECTED: Surface bet should display on Home page if it is activated
        EXPECTED: Surface bet should not display on Home page if it is deactivated
        """
        # This step covered  another test cases

    def test_020_verify_surface_bet_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet disappears in FE upon deletion in CMS
        EXPECTED: Surface bet should disappear in FE
        """
        # This step is covered in tear Down

    def test_021_verify_edited_field_changes_are_reflecting_in_fe_for_surface_bet(self):
        """
        DESCRIPTION: Verify Edited field changes are reflecting in FE for Surface bet
        EXPECTED: Edited fields data should be updated for Surface bet
        """
        self.__class__.surface_bet_title = generate_name().upper()
        self.cms_config.update_surface_bet(self.surface_bet['id'], title=self.surface_bet_title)
        self.verify_surface_bet(expected_result=True)

    def test_022_verify_surface_bet_display_for_logged_in_amp_logged_out_users(self):
        """
        DESCRIPTION: Verify Surface bet display for Logged in &amp; Logged out users
        EXPECTED: Surface bet should display for all Logged in &amp; Logged out users
        """
        self.site.logout()
        self.verify_surface_bet(expected_result=True)
