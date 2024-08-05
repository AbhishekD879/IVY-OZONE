import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from datetime import datetime
from faker import Faker
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.surface_bets
@vtest
class Test_C65866504_Verify_surface_bet_created_for_cricket_landing_pages_under_Sports_Category(BaseBetSlipTest):
    """
    TR_ID: C65866504
    NAME: Verify surface bet created for cricket landing pages under Sports Category
    DESCRIPTION: This test case verifies surface bet is displayed specific to sports
    PRECONDITIONS: Surface bet Creation in CMS:
    PRECONDITIONS: 1.Login to Environment specific CMS
    PRECONDITIONS: 2.Click Sports from side navigation and select 'cricket' option
    PRECONDITIONS: 3.Click 'Surface Bet Module' and click 'Create Surface bet'
    PRECONDITIONS: 4.Check the checkbox 'Enabled', 'Display on Highlights tab', 'Display on EDP' and 'Display in Desktop'
    PRECONDITIONS: 5.Enter All fields like
    PRECONDITIONS: Active Checkbox
    PRECONDITIONS: Title
    PRECONDITIONS: EventIds (Create with EventId)
    PRECONDITIONS: Show on Sports select 'All Sports'
    PRECONDITIONS: Show on EventHub
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
    PRECONDITIONS: Navigate to Sports--&gt;All Sports--&gt;Surface bet Module--&gt; Select newly Created Surface bet--&gt; Check the Surface bet order
    """
    keep_browser_open = True
    svg_bg_id = "BelgiumFlag-Euro2020"
    svgBg = None
    sb_bg_img_path = None
    svg_icon="cricket"
    surface_bet_header = "BIG BASH"
    surface_bet_content = "Build Your Bet"
    surface_bet_title = ("AUTO SB 504 "+ Faker().city()).upper()
    bet_amount = 0.1

    def wait_up_to_time_complete(self, end_time):
        now = datetime.now()  # taking now time
        now = get_date_time_as_string(date_time_obj=now,
                                      time_format='%Y-%m-%dT%H:%M:%S.%f',
                                      url_encode=False)[:-3] + 'Z'
        if now > end_time:
            return
        else:
            wait_for_haul(20)
            return self.wait_up_to_time_complete(end_time)

    def verify_surface_bets_on_fe(self, expected_result=True):
        import time
        wait_time = 5  # Wait time in seconds
        max_polling_time = 140  # Maximum polling time in seconds

        if expected_result:
            start_time = time.time()

            while time.time() - start_time < max_polling_time:
                has_surface_bet = self.site.sports_page.tab_content.has_surface_bets(
                    expected_result=expected_result)

                if has_surface_bet:
                    # Reading the surface bets in cricket slp
                    surface_bets = self.site.sports_page.tab_content.surface_bets.items_as_ordered_dict
                    if surface_bets.get(self.surface_bet_title):
                        break  # Break the loop if the condition is meet

                wait_for_haul(wait_time)

            self.assertTrue(has_surface_bet, "Surface Bets Content is not Shown on Cricket SLP")

            # Checking if the expected title is in the list of surface bets
            self.assertIn(self.surface_bet_title, list(surface_bets.keys()),
                          f'surface bet : "{self.surface_bet_title}" is not found in {list(surface_bets.keys())}')

            return surface_bets.get(self.surface_bet_title)
        else:
            start_time = time.time()

            while time.time() - start_time < max_polling_time:
                has_surface_bet = self.site.sports_page.tab_content.has_surface_bets(
                    expected_result=expected_result)
                if not has_surface_bet:
                    break  # Break the loop if the condition is met
                time.sleep(wait_time)
            self.assertFalse(has_surface_bet,
                             msg=f'surface bet : "{self.surface_bet_title}" which is not meant to present is found in on Cricket SLP')
    def test_000_preconditions(self):
        """"
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.cricket_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(event_selection.values())[0]

        else:
            event = self.ob_config.add_autotest_cricket_event()
            self.__class__.selection_id = event.selection_ids[event.team1]
            self.__class__.eventID = event.event_id
            self.svg_bg_id = 'surface-bet-bg-bigc'
            if self.brand != 'bma':
                self.__class__.svgBg = 'background-image: url("https://cms-stg.ladbrokes.com/cms/images/uploads/svg/857e5e8b-9f31-4396-ae7d-5d4dce231b9e.svg");'
                self.sb_bg_img_path = '/images/uploads/svg/857e5e8b-9f31-4396-ae7d-5d4dce231b9e.svg'
            else:
                self.__class__.svgBg = 'background-image: url("https://cms-stg.coral.co.uk/cms/images/uploads/svg/19db124f-c9a5-46c3-8f38-682a20e5f05b.svg");'
                self.sb_bg_img_path = '/images/uploads/svg/19db124f-c9a5-46c3-8f38-682a20e5f05b.svg'

        self.__class__.surface_bet = self.cms_config.add_surface_bet(selection_id=self.selection_id,
                                                                     eventIDs=[self.eventID],
                                                                     highlightsTabOn=True,
                                                                     edp_on=False,
                                                                     svg_icon=self.svg_icon,
                                                                     svgBgId=self.svg_bg_id,
                                                                     on_homepage=True,
                                                                     displayOnDesktop=True,
                                                                     title=self.surface_bet_title,
                                                                     contentHeader=self.surface_bet_header,
                                                                     content=self.surface_bet_content,
                                                                     categoryIDs=[10])
        self.__class__.surface_bet_title = self.surface_bet.get('title').upper()
        self.__class__.surface_bet_id = self.surface_bet.get('id')
        self.__class__.sb_cms_configurations = self.surface_bet




    def test_001_login_to_ladscoral_ampltenvironmentampgt(self):
        """
        DESCRIPTION: Login to Lads/Coral &amp;lt;Environment&amp;gt;
        EXPECTED: User should be logged in
        """
        self.site.login()
        self.site.wait_content_state("HOMEPAGE", timeout=10)
        self.navigate_to_page(name='sport/cricket', timeout=10)


    def test_002_change_the_order_of_surface_bet_created(self):
        """
        DESCRIPTION: Change the Order of surface bet created
        EXPECTED: Order of Surface bet created should be as per CMS config
        """
        #covered in test case

    def test_003_validate_the_surface_bet_title(self):
        """
        DESCRIPTION: Validate the surface bet Title
        EXPECTED: Title Name should be displayed as per CMS config
        """
        #covered in below steps

    def test_004_validate_the_surface_bet_is_displayed_on_cricket_landing_pages(self):
        """
        DESCRIPTION: Validate the surface bet is displayed on cricket landing pages
        EXPECTED: Surface bet created should reflect on cricket landing pages as per CMS config
        """
        # checking whether there are surface bets in slp
        wait_for_result(lambda: self.site.sports_page.tab_content.has_surface_bets(expected_result=True), timeout=15)
        surface_bet_content = self.site.sports_page.tab_content.has_surface_bets(expected_result=True)
        self.assertTrue(surface_bet_content, "Surface Bets Content is not Shown on cricket")
        # reading the surface bets in slp
        self.__class__.surface_bets = self.site.sports_page.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(self.surface_bets, msg='No Surface Bets found')
        self.assertIn(self.surface_bet_title, [k.upper() for k in list(self.surface_bets.keys())],
                      f'surface bet : "{self.surface_bet_title}" is not found in {list(self.surface_bets.keys())}')
        # getting the surface bet which is created among the surface bets in slp
        surface_bet_contents = self.surface_bets.get(self.surface_bet_title)
        surface_bet_contents.scroll_to()
        self.assertEqual(surface_bet_contents.header.icontext,
                         '#cricket', f'Svg Icon is not same as configured in cms')
        if tests.settings.backend_env != 'prod':
            self.assertEqual(surface_bet_contents.get_attribute('style'), self.svgBg,
                             f'svg Background is not same as cms config')
        self.assertEqual(surface_bet_contents.header.title.upper(), self.sb_cms_configurations['title'].upper(),
                         f'Actual title : "{surface_bet_contents.header.title.upper()}" is not same as '
                         f'Expected title : "{self.sb_cms_configurations["title"].upper()}"')
        self.assertEqual(surface_bet_contents.content_header.upper(),
                         self.sb_cms_configurations['contentHeader'].upper(),
                         f'Actual Content Header :"{surface_bet_contents.content_header.upper()}" is not same as'
                         f'Expected Content Header : "{self.sb_cms_configurations["contentHeader"].upper()}"')
        self.assertEqual(surface_bet_contents.content.strip().upper(),
                         self.sb_cms_configurations['content'].strip().upper(),
                         f'Actual Content : "{surface_bet_contents.content.strip().upper()}" is not same as '
                         f'Expected Content : "{self.sb_cms_configurations["content"].strip().upper()}"')



    def test_005_validate_the_surface_bet_content_header(self):
        """
        DESCRIPTION: Validate the surface bet 'Content header'
        EXPECTED: Content Header' should be displayed as per CMS config
        """
        #coverd in above step

    def test_006_validate_the_surface_bet_content(self):
        """
        DESCRIPTION: Validate the surface bet 'Content'
        EXPECTED: Content' should be displayed as per CMS config
        """
        #coverd in above step

    def test_007_verify_the_surface_bet_display_from_and_to_date(self):
        """
        DESCRIPTION: Verify the Surface Bet Display From and To date
        EXPECTED: Surface bet should be displayed based on CMS config start date
        EXPECTED: Surface bet should be displayed based on CMS config end date
        """
        #Already covered


    def test_008_validate_the_svg_icon_and_svg_background(self):
        """
        DESCRIPTION: Validate the SVG icon and SVG background
        EXPECTED: SVG icon and SVG background should be displayed as per CMS config
        """
        #coverd in above step

    def test_009_verify_surface_bet_display_from_and_display_to_date_has_set_to_past_future_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' and 'Display to' date has set to past/future in CMS
        EXPECTED: Surface bet should not be displayed in FE
        """
        #past time
        self.__class__.time_format = '%Y-%m-%dT%H:%M:%S.%f'
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-21)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=-20)[:-3] + 'Z'
        self.cms_config.update_surface_bet(self.surface_bet_id, displayFrom=start_time,
                                           displayTo=end_time)
        self.verify_surface_bets_on_fe(expected_result=False)

        #making surface bet appear again
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-20)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=24, days=1)[:-3] + 'Z'
        self.cms_config.update_surface_bet(self.surface_bet_id, displayFrom=start_time,
                                           displayTo=end_time)
        self.verify_surface_bets_on_fe(expected_result=True)

        #future time
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=20)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, hours=24, days=1)[:-3] + 'Z'
        self.cms_config.update_surface_bet(self.surface_bet_id, displayFrom=start_time,
                                           displayTo=end_time)
        self.verify_surface_bets_on_fe(expected_result=False)
    def test_010_verify_surface_bet_display_from_has_set_to_past_and_display_to_in_a_few_mins_from_the_current_time(self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to past and 'Display to' in a few minutes from the current
        time.
        EXPECTED: Surface bet should disappear in FE
        """
        start_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                             url_encode=False, hours=-21)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, minutes=2)[:-3] + 'Z'
        self.cms_config.update_surface_bet(self.surface_bet_id, displayFrom=start_time,
                                           displayTo=end_time)
        self.verify_surface_bets_on_fe(expected_result=True)
        self.verify_surface_bets_on_fe(expected_result=False)



    def test_011_verify_surface_bet_display_from_has_set_to_few_mins_from_current_time_and_display_to_from_the_future(self):
        """
        DESCRIPTION: Verify Surface bet 'Display from' has set to few mins from current time and 'Display to' from the future
        EXPECTED: Surface bet should display as per 'Display from' time
        """
        start_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                             url_encode=False, minutes=2)[:-3] + 'Z'
        start_time_cms = get_date_time_as_string(date_time_obj=datetime.utcnow(), time_format=self.time_format,
                                           url_encode=False, minutes=2)[:-3] + 'Z'
        end_time = get_date_time_as_string(date_time_obj=datetime.now(), time_format=self.time_format,
                                           url_encode=False, hours=22)[:-3] + 'Z'
        self.cms_config.update_surface_bet(self.surface_bet_id, displayFrom=start_time_cms,
                                           displayTo=end_time)
        self.verify_surface_bets_on_fe(expected_result=False)
        self.wait_up_to_time_complete(start_time)
        self.verify_surface_bets_on_fe(expected_result=True)
    def test_012_verify_surface_bets_left_and_right_scroll(self):
        """
        DESCRIPTION: Verify Surface bets left and right scroll
        EXPECTED: User should be able to scroll from left to right &amp; from right to left
        """
        #applicable only if more than 3 surface bets


    def test_013_verify_user_is_able_to_select_the_selections_on_surface_bet(self):
        """
        DESCRIPTION: Verify user is able to select the selections on Surface bet
        EXPECTED: User should be able to select &amp; selections should be highlighted
        """
        surface_bet = self.site.cricket.tab_content.surface_bets.items_as_ordered_dict.get(
            self.sb_cms_configurations['title'].upper())
        if surface_bet.bet_button.is_enabled():
            surface_bet.bet_button.click()
        if self.device_type == 'mobile':
            quick_bet = self.site.quick_bet_panel
            wait_for_haul(5)
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            quick_bet.place_bet.click()
            bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.bet_receipt.reuse_selection_button.click()
            self.site.open_betslip()
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.bet_receipt.footer.reuse_selection_button.click()
        surface_bet.scroll_to()
        self.assertTrue(surface_bet.bet_button.is_enabled(),
                        f'bet button is not selected after clicking on reuse selection')
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_014_verify_edited_field_changes_are_reflecting_in_fe_for_surface_bet(self):
        """
        DESCRIPTION: Verify Edited field changes are reflecting in FE for Surface bet
        EXPECTED: Edited fields data should be updated for Surface bet
        """
        surface_bet_content = "MODIFIED-BB1428"
        self.sb_cms_configurations = self.cms_config.update_surface_bet(self.surface_bet_id, content=surface_bet_content)
        surface_bets = self.site.sports_page.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertIn(self.surface_bet_title, [k.upper() for k in list(surface_bets.keys())],
                      f'surface bet : "{self.surface_bet_title}" is not found in {list(surface_bets.keys())}')
        wait_for_haul(20)
        surface_bet_contents = self.verify_surface_bets_on_fe(expected_result=True)
        surface_bet_contents.scroll_to()
        expected_sb_content = surface_bet_contents.content.strip().upper()
        actual_sb_content = self.sb_cms_configurations['content'].strip().upper()
        for i in range(0,10):
            if expected_sb_content != actual_sb_content:
                self.device.refresh_page() # Without refresh SB content is not updating in frontend
                self.site.wait_content_state('cricket')
                wait_for_haul(3)
                surface_bet_contents = self.verify_surface_bets_on_fe(expected_result=True)
                surface_bet_contents.scroll_to()
                expected_sb_content = surface_bet_contents.content.strip().upper()
            else:
                break
        self.assertEqual(expected_sb_content, actual_sb_content,
                         f'Actual Content : "{actual_sb_content}" is not same as '
                         f'Expected Content : "{expected_sb_content}"')


    def test_015_verify_surface_bet_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet disappears in FE upon deletion in CMS
        EXPECTED: Surface bet should disappear in FE
        """
        # ******** Removing Surface Bet *************************
        surface_bet_id = self.surface_bet.get('id')
        self.cms_config.delete_surface_bet(surface_bet_id)
        self.cms_config._created_surface_bets.remove(surface_bet_id)
        # ******** Verification of Surface Bet *************************
        self.verify_surface_bets_on_fe(expected_result=False)
