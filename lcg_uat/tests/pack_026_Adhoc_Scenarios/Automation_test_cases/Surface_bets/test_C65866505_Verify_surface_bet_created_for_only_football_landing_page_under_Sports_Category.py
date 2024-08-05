import pytest
import tests
from datetime import datetime
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_haul, wait_for_result
from crlat_ob_client.utils.date_time import get_date_time_as_string
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.surface_bets
@vtest
class Test_C65866505_Verify_surface_bet_created_for_only_football_landing_page_under_Sports_Category(BaseBetSlipTest):
    """
    TR_ID: C65866505
    NAME: Verify surface bet created for only football landing page under Sports Category
    DESCRIPTION: This test case verifies surface bet is displayed specific to sports
    PRECONDITIONS: Surface bet Creation in CMS:
    PRECONDITIONS: 1.Login to Environment specific CMS
    PRECONDITIONS: 2.Click Sports from side navigation and select 'Football' option from sports category
    PRECONDITIONS: 3.Click 'Surface Bet Module' and click 'Create Surface bet'
    PRECONDITIONS: 4.Check the checkbox 'Enabled', 'Display on EDP' and 'Display in Desktop'
    PRECONDITIONS: 5.Enter All fields like
    PRECONDITIONS: Active Checkbox
    PRECONDITIONS: Title
    PRECONDITIONS: EventIds (Create with EventId)
    PRECONDITIONS: Show on Sports select 'Football'
    PRECONDITIONS: Content Header
    PRECONDITIONS: Content
    PRECONDITIONS: Was Price
    PRECONDITIONS: Selection ID
    PRECONDITIONS: Display From
    PRECONDITIONS: Display To
    PRECONDITIONS: SVG Icon
    PRECONDITIONS: SVG Background
    PRECONDITIONS: 6.Check segment as 'Universal'
    PRECONDITIONS: 7.Click Save Changes
    PRECONDITIONS: Check the Sort Order of Surface bet Module
    PRECONDITIONS: Navigate to Sports--&gt;Football--&gt;Surface bet Module--&gt; Select newly Created Surface bet--&gt;
                    Check the Surface bet order
    """
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        surface_bet_module = cms_config.get_sport_module(sport_id=16, module_type='SURFACE_BET')[0]
        cms_config.change_sport_module_state(sport_module=surface_bet_module, active=True)

    def get_status_of_surface_bet(self, surface_bet_name, time=1, expected_result=True):
        if time > 180:
            return [not expected_result, []]
        wait_for_haul(1)
        if not self.site.football.tab_content.has_surface_bets(expected_result=True):
            surface_bets_names = []
        else:
            try:
                surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
            except:
                surface_bets = {}
            surface_bets_names = []
            for name, sb_obj in surface_bets.items():
                sb_obj.scroll_to_we()
                surface_bets_names.append(sb_obj.name)
        alive = True
        if surface_bet_name not in [sb.upper() for sb in surface_bets_names]:
            alive = False
        if alive == expected_result:
            return alive, surface_bets_names
        else:
            return self.get_status_of_surface_bet(surface_bet_name=surface_bet_name, time=time + 1,
                                                  expected_result=expected_result)

    def get_status_of_surface_bet_module(self, time=1, expected_result=True):
        wait_for_haul(1)
        if time > 180:
            return not expected_result
        result = self.site.football.tab_content.has_surface_bets()
        if (result is not None and expected_result == True) or (result is None and expected_result == False):
            return expected_result
        else:
            return self.get_status_of_surface_bet_module(time=time + 1, expected_result=expected_result)

    def get_surface_bet_from_fe(self, timeout=None):
        if timeout:
            self.device.refresh_page()
            wait_for_haul(timeout)
        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        for name, sb_obj in surface_bets.items():
            sb_obj.scroll_to_we()
            if sb_obj.name == self.surface_bet['title'].upper():
                return sb_obj
        return None

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Sports pages > Sports category
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(event_selection.values())[0]
        else:
            event = self.ob_config.add_football_event_to_england_premier_league()
            selection_id = event.selection_ids[event.team1]
            self.__class__.eventID = event.event_id

        # self.cms_config.add_sport_module_to_event_hub(page_id= 16, module_type='SURFACE_BET')
        self.__class__.surface_bet = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                                     categoryIDs=[16, 0],
                                                                     eventIDs=[self.eventID],
                                                                     svg_icon='football',
                                                                     displayOnDesktop=True
                                                                     )
        self.__class__.surface_bet_title = self.surface_bet.get('title').upper()
        self.__class__.surface_bet_id = self.surface_bet.get('id')
        self.__class__.sb_cms_configurations = self.surface_bet
        # wait_for_haul(20)

    def test_001_login_to_ladscoral_ampltenvironmentampgtnavigate_to_football_slp(self):
        """
        DESCRIPTION: Login to Lads/Coral &amp;lt;Environment&amp;gt;
        DESCRIPTION: Navigate to Football SLP
        EXPECTED: User should be logged in
        """
        self.site.login()
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

    def test_002_validate_the_surface_bet_is_displayed_on_football_landing_page(self):
        """
        DESCRIPTION: Validate the surface bet is displayed on football landing page
        EXPECTED: Surface bet created should reflect only on football landing page as per CMS config
        """
        surface_bet_content = self.site.football.tab_content.has_surface_bets(expected_result=True)
        self.assertTrue(surface_bet_content, "Surface Bets Content is not Shown on foot ball")

    def test_003_validate_the_surface_bet_title(self):
        """
        DESCRIPTION: Validate the surface bet Title
        EXPECTED: Title Name should be displayed as per CMS config
        """
        self.__class__.surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(self.surface_bets, msg='No Surface Bets found')
        self.assertIn(self.surface_bet_title, list(self.surface_bets.keys()),
                      f'surface bet : "{self.surface_bet_title}" is not found in {list(self.surface_bets.keys())}')
        self.__class__.surface_bet_content = self.surface_bets.get(self.surface_bet_title)
        wait_for_haul(5)
        self.surface_bet_content.scroll_to()
        self.assertEqual(self.surface_bet_content.header.title.upper(), self.sb_cms_configurations['title'].upper(),
                         f'Actual title : "{self.surface_bet_content.header.title.upper()}" is not same as '
                         f'Expected title : "{self.sb_cms_configurations["title"].upper()}"')

    def test_004_validate_the_surface_bet_content_header_and_validate_the_svg_icon_and_svg_background(self):
        """
        DESCRIPTION: Validate the surface bet 'Content header' and Validate the SVG icon and SVG background
        EXPECTED: Content Header should be displayed as per CMS config
        EXPECTED: SVG icon and SVG background should be displayed as per CMS config
        """

        self.assertEqual(self.surface_bet_content.header.icontext,
                         '#football', f'Svg Icon is not same as configured in cms')
        self.assertEqual(self.surface_bet_content.content_header.upper(),
                         self.sb_cms_configurations['contentHeader'].upper(),
                         f'Actual Content Header :"{self.surface_bet_content.content_header.upper()}" is not same as'
                         f'Expected Content Header : "{self.sb_cms_configurations["contentHeader"].upper()}"')

    def test_005_validate_the_surface_bet_content(self):
        """
        DESCRIPTION: Validate the surface bet 'Content'
        EXPECTED: Content should be displayed as per CMS config
        """
        self.assertEqual(self.surface_bet_content.content.strip().upper(),
                         self.sb_cms_configurations['content'].strip().upper(),
                         f'Actual Content : "{self.surface_bet_content.content.strip().upper()}" is not same as '
                         f'Expected Content : "{self.sb_cms_configurations["content"].strip().upper()}"')

    def test_006_verify_the_surface_bet_display_from_and_to_date(self):
        """
        DESCRIPTION: Verify the Surface Bet Display From and To date
        EXPECTED: Surface bet should be displayed based on CMS config start date
        EXPECTED: Surface bet should be displayed based on CMS config end date
        """
        now = datetime.now()  # taking now time
        now = get_date_time_as_string(date_time_obj=now,
                                      time_format='%Y-%m-%dT%H:%M:%S.%f',
                                      url_encode=False)[:-3] + 'Z'  # formatting the now time as CMS time format
        display_from = self.surface_bet['displayFrom']
        display_to = self.surface_bet['displayTo']
        status = display_from < now < display_to
        self.assertTrue(status, f'Surface Bet is not displayed as per CMS configurations(in between start '
                                f'time and end time)')

    def test_007_verify_surface_bet_display_from_and_display_to_date_has_set_to_pastfuture_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' and 'Display to' date has set to past/future in CMS
        EXPECTED: Surface bet should not be displayed in FE
        """
        self.__class__.time_format = '%Y-%m-%dT%H:%M:%S.%f'
        start_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                             url_encode=False, hours=-22)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                           url_encode=False, hours=-20)[:-3] + 'Z'
        # display from : past
        # display to : past
        self.cms_config.update_surface_bet(self.surface_bet_id, displayFrom=start_time,
                                           displayTo=end_time)
        alive, surface_bets_names = self.get_status_of_surface_bet(self.surface_bet_title.upper(),
                                                                   expected_result=False)

        self.assertFalse(alive,
                         f'{self.surface_bet_title.upper()} still in Front end surface bets {surface_bets_names}')

        # display to : future
        end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                           url_encode=False, days=3)[:-3] + 'Z'
        self.cms_config.update_surface_bet(self.surface_bet_id,
                                           displayTo=end_time)
        alive, surface_bets_names = self.get_status_of_surface_bet(self.surface_bet_title.upper(),
                                                                   expected_result=True)
        self.assertTrue(alive,
                        f'{self.surface_bet_title.upper()} not in Front end surface bets {surface_bets_names}')

        # display from : future
        start_time = get_date_time_as_string(date_time_obj=datetime.now(),
                                             time_format=self.time_format,
                                             url_encode=False, days=2)[:-3] + 'Z'
        self.cms_config.update_surface_bet(self.surface_bet_id, displayFrom=start_time)
        alive, surface_bets_names = self.get_status_of_surface_bet(self.surface_bet_title.upper(),
                                                                   expected_result=False)

        self.assertFalse(alive,
                         f'{self.surface_bet_title.upper()} still in Front end surface bets {surface_bets_names}')

    def test_008_verify_surface_bet_display_from_has_set_to_past_and_display_to_in_a_few_mins_from_the_current_time(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to past and 'Display to' in a few mins from the current time.
        EXPECTED: Surface bet should disappear in FE
        """
        # Update of Surface bet start_time to present for the present time and end_time to Future

        # Calculate the start time by subtracting 10 hours and adding 2 minutes from the current UTC time
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-10)[:-3] + 'Z'
        # Calculate the end time by adding 10 hours from the current UTC time
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=10)[:-3] + 'Z'
        # Update the surface bet's display dates in the CMS configuration
        self.cms_config.update_surface_bet(self.surface_bet_id, displayFrom=start_time, displayTo=end_time)
        # Verify the surface bets on the front-end with the expectation of finding the bet
        self.device.refresh_page()
        alive, surface_bets_names = self.get_status_of_surface_bet(self.surface_bet_title.upper(),
                                                                   expected_result=True)
        self.assertTrue(alive,
                         f'{self.surface_bet_title.upper()} not in Front end surface bets {surface_bets_names}')

    def test_009_verify_surface_bet_display_from_has_set_to_few_mins_from_current_time_and_display_to_from_the_future(
            self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to few mins from current time and 'Display to' from the future
        EXPECTED: Surface bet should display as per 'Display from' time
        """
        # covered in above step

    def test_010_verify_surface_bets_display_if_there_are_more_no_of_surfaces_bets_created_in_football_landing_page(
            self):
        """
        DESCRIPTION: Verify Surface bets display if there are more no of surfaces bets created in Football landing page
        EXPECTED: Surface bet with Right or Left arrow should display
        """
        # when ever we create two SB this step will applicable

    def test_011_verify_surface_bets_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify Surface bets left and right scroll
        EXPECTED: User should be able to scroll from left to right &amp; from right to left
        """
        # when ever we create two SB this step will applicable

    def test_012_verify_user_is_able_to_select_the_selections_on_surface_bet(self):
        """
        DESCRIPTION: Verify user is able to select the selections on Surface bet
        EXPECTED: User should be able to select &amp; selections should be highlighted
        """
        surface_bet = self.site.sports_page.tab_content.surface_bets.items_as_ordered_dict.get(self.surface_bet_title)
        bet_button = surface_bet.bet_button
        bet_button.click()
        self.assertTrue(bet_button.is_selected(), msg='Bet Button is not selected')
        if self.device_type == 'mobile':
            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            quick_bet.place_bet.click()
            bet_receipt_displayed = wait_for_result(lambda: quick_bet.wait_for_bet_receipt_displayed())
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.bet_receipt.reuse_selection_button.click()
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.bet_receipt.footer.reuse_selection_button.click()
        wait_for_haul(5)
        bet_button.scroll_to()
        self.site.open_betslip()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_013_activatedeactivate_the_whole_surface_bet_module_on_football_slp(self):
        """
        DESCRIPTION: Activate/Deactivate the whole Surface bet module on Football-SLP
        EXPECTED: Surface bet should display on Home page if it is activated
        EXPECTED: Surface bet should not display on Home page if it is deactivated
        """
        surface_bet_module = self.cms_config.get_sport_module(sport_id=16, module_type='SURFACE_BET')[0]
        self.cms_config.change_sport_module_state(sport_module=surface_bet_module, active=False)

        surface_bet_visible_status = self.get_status_of_surface_bet_module(expected_result=False)
        self.assertFalse(surface_bet_visible_status, f'surface bet module still visible even though surface bet '
                                                     f'module deactivated')

        surface_bet_module = self.cms_config.get_sport_module(sport_id=16, module_type='SURFACE_BET')[0]
        self.cms_config.change_sport_module_state(sport_module=surface_bet_module, active=True)

        surface_bet_visible_status = self.get_status_of_surface_bet_module()
        self.assertTrue(surface_bet_visible_status, f'surface bet module is not visible even though surface bet '
                                                    f'module activated')

    def test_014_verify_edited_field_changes_are_reflecting_in_fe_for_surface_bet(self):
        """
        DESCRIPTION: Verify Edited field changes are reflecting in FE for Surface bet
        EXPECTED: Edited fields data should be updated for Surface bet
        """
        surface_bet_updated = self.cms_config.update_surface_bet(self.surface_bet_id, contentHeader="Automation",
                                                                 content="SB Automation in Football SLP")
        attempts = 12
        while attempts:
            attempts -= 1
            try:
                self.get_surface_bet_from_fe(timeout=10)
                surface_bets_contents = self.site.football.tab_content.surface_bets.items_as_ordered_dict.get(
                    self.surface_bet['title'].upper())
                surface_bets_contents.scroll_to_we()
                self.assertEqual(surface_bets_contents.content_header.upper(),
                                 surface_bet_updated['contentHeader'].upper(),
                                 f'Actual Content Header :"{surface_bets_contents.content_header.upper()}" is not same as'
                                 f'Expected Content Header : "{surface_bet_updated["contentHeader"].upper()}"')
                self.assertEqual(surface_bets_contents.content.upper(),
                                 surface_bet_updated['content'].upper(),
                                 f'Actual Content :"{surface_bets_contents.content.upper()}" is not same as'
                                 f'Expected Content : "{surface_bet_updated["content"].upper()}"')
            except Exception as e:
                if attempts:
                    continue
                else:
                    raise e

    def test_015_verify_surface_bet_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet disappears in FE upon deletion in CMS
        EXPECTED: Surface bet should disappear in FE
        """
        # ******** Removing Surface Bet *************************
        surface_bet_id = self.surface_bet.get('id')
        self.cms_config.delete_surface_bet(surface_bet_id)
        self.cms_config._created_surface_bets.remove(surface_bet_id)
        # ******** Verification of surface Bet *************************
        alive, surface_bets_names = self.get_status_of_surface_bet(self.surface_bet_title.upper(),
                                                                   expected_result=False)
        self.assertFalse(alive,
                         f'{self.surface_bet_title.upper()} still in Front end surface bets {surface_bets_names}')
