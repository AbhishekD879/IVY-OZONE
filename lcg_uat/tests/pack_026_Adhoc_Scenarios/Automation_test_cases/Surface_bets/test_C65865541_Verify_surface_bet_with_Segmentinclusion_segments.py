import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul, wait_for_cms_reflection


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.adhoc_suite
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.surface_bets
@vtest
@pytest.mark.timeout(1200)
class Test_C65865541_Verify_surface_bet_with_Segmentinclusion_segments(Common):
    """
    TR_ID: C65865541
    NAME: Verify surface bet with Segment(inclusion segments)
    DESCRIPTION: 
    PRECONDITIONS: Create a event in OB
    PRECONDITIONS: Surface bet Creation in CMS:
    PRECONDITIONS: 1.Login to Environment specific CMS
    PRECONDITIONS: 2.Navigate to Home Page -->Surface bets
    PRECONDITIONS: 3.Click 'Create Surface bet'
    PRECONDITIONS: 4.Check the checkbox 'Enabled','Display on Highlights tab','Display on EDP' and 'Display in Desktop'
    PRECONDITIONS: 5.Enter All fields like
    PRECONDITIONS: Active Checkbox
    PRECONDITIONS: Title as 'Featured - Ladies Matches '
    PRECONDITIONS: EventId
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
    PRECONDITIONS: 6.Check 'Segment' radio button with Inclusion Segments: Without ,Single or multiple
    PRECONDITIONS: 7.Click Save Changes
    PRECONDITIONS: Check the Sort Order of Surface bet Module
    PRECONDITIONS: Navigate to Home Page-->Surface bet Module--> Select newly Created Surface bet--> Check the Surface bet order
    """
    keep_browser_open = True
    segment = vec.bma.CSP_CMS_SEGEMENT
    cookies = vec.bma.CSP_COOKIE_SEGMENT

    def create_event_hub_for_index(self, index_num: int):
        self.cms_config.create_event_hub(index_number=index_num)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_num, module_type='SURFACE_BET')

    def changing_sb_order(self, surface_bet_lists=[]):
        all_sb = self.cms_config.get_surface_bets_for_page(reference_id=0, related_to='sport', segment=self.segment)
        sb_ids = []
        for i in range(len(surface_bet_lists)):
            for sb in all_sb:
                if sb.get('title').upper() == surface_bet_lists[i].upper():
                    sb_ids.append(sb.get('id'))
                    break
        all_sb_ids = [item['id'] for item in all_sb]
        index_sb_1 = all_sb_ids.index(sb_ids[0])
        index_sb_2 = all_sb_ids.index(sb_ids[1])
        all_sb_ids[index_sb_1], all_sb_ids[index_sb_2] = all_sb_ids[index_sb_2], all_sb_ids[index_sb_1]
        sb_id = sb_ids[0]
        self.cms_config.set_surfacebet_ordering(new_order=all_sb_ids,
                                                moving_item=sb_id,
                                                segmentName=self.segment)

    def checking_order_of_surface_bet(self, surface_bet_title_1, surface_bet_title_2, changed=False):
        def check_order_poll(title1, title2, changed=False):
            items = self.site.home.tab_content.surface_bets.items_as_ordered_dict
            surface_bet_names = [name for name in items.keys()]
            index_sb1 = surface_bet_names.index(title1)
            index_sb2 = surface_bet_names.index(title2)
            if changed:
                return index_sb2 < index_sb1
            else:
                return index_sb2 > index_sb1

        return wait_for_cms_reflection(
            func=check_order_poll,
            fargs=(surface_bet_title_1, surface_bet_title_2, changed),
            refresh_count=5,
            timeout=10,
            expected_result=True,
            haul=10,
            ref=self
        )

    def create_surface_bet(self, selection_id, event_id, title, contentHeader, content, index_number):
        surface_bet = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                      eventIDs=[event_id],
                                                      inclusionList=[self.segment],
                                                      universalSegment=False,
                                                      svg_icon="football",
                                                      segmentReferences=[{
                                                          'segmentName': self.segment
                                                      }],
                                                      on_homepage=True,
                                                      title=title,
                                                      contentHeader=contentHeader,
                                                      content=content,
                                                      eventHubsIndexes=[index_number],
                                                      all_sports=True,
                                                      categoryIDs=[]
                                                      )

        self.surface_bet_dict[surface_bet.get('title')] = surface_bet

    def verify_surface_bet_on_fe(self, surface_bet_title=None, expected_result=True, timeout=10):
        if expected_result:
            sb = wait_for_cms_reflection(
                lambda: self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(surface_bet_title),
                timeout=timeout,
                refresh_count=5,
                ref=self,
                haul=5
            )
            self.assertTrue(sb, msg=f'{surface_bet_title} is not available')
        else:
            sb = wait_for_cms_reflection(
                lambda: self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(surface_bet_title),
                expected_result=expected_result,
                timeout=timeout,
                refresh_count=5,
                ref=self,
                haul=5
            )
            self.assertFalse(sb, msg=f'{surface_bet_title} is available')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create a event in OB
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)
            event1 = events[0]
            event2 = events[1]
            event_id_1 = event1['event']['id']
            self.__class__.event_id_2 = event2['event']['id']
            selection_id_1 = event1['event']['children'][0]['market']['children'][0]['outcome']['id']
            self.__class__.selection_id_2 = event2['event']['children'][0]['market']['children'][0]['outcome']['id']
        self.__class__.surface_bet_header = 'surface bet header'
        self.__class__.surface_bet_content = 'surface bet content'
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_numbers = [index['indexNumber'] for index in existing_event_hubs]
        new_index_number = next(index for index in range(1, 20) if index not in existed_index_numbers)
        US_Sports_index_number = [index['indexNumber'] for index in existing_event_hubs if
                                  index['title'] == 'US Sports']
        if len(US_Sports_index_number) == 0:
            self.create_event_hub_for_index(index_num=new_index_number)
            index_number = new_index_number
        else:
            index_number = US_Sports_index_number[0]
        self.__class__.surface_bet_dict = {}
        self.__class__.surface_bet_title1 = "Autotest_sb1_C65865541"
        self.create_surface_bet(selection_id=selection_id_1, event_id=event_id_1, title=self.surface_bet_title1,
                                contentHeader=self.surface_bet_header
                                , content=self.surface_bet_content, index_number=index_number)

    def test_001_login_to_ladscoral_ampltenvironmentampgt(self):
        """
        DESCRIPTION: Login to Lads/Coral &amp;lt;Environment&amp;gt;
        EXPECTED: User should be logged in
        """
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        self.verify_surface_bet_on_fe(self.surface_bet_title1.upper(), timeout=30, expected_result=False)
        self.set_local_storage_cookies_csp(self.cookies, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=60)

    def test_002_observe_the_surface_bet_created_on_homepage(self):
        """
        DESCRIPTION: Observe the surface bet created on homepage
        EXPECTED: Surface bet created in CMS should be reflected on homepage
        """
        surface_bet_content = self.site.home.tab_content.has_surface_bets(expected_result=True)
        self.assertTrue(surface_bet_content, "Surface Bets Content is not Shown on home page")
        self.verify_surface_bet_on_fe(self.surface_bet_title1.upper(), timeout=60)
        surface_bet_names = self.site.home.tab_content.surface_bets.items_as_ordered_dict.keys()
        self.assertIn(self.surface_bet_title1.upper(), surface_bet_names,
                      msg=f'{self.surface_bet_title1} is not present in home page among surface bets {surface_bet_names}')

    def test_003_validate_the_order_of_surface_bet_created_on_homepage(self):
        """
        DESCRIPTION: Validate the Order of surface bet created on homepage
        EXPECTED: Order of Surface bet created should be as per CMS config
        """
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_numbers = [index['indexNumber'] for index in existing_event_hubs]
        new_index_number = next(index for index in range(1, 20) if index not in existed_index_numbers)
        US_Sports_index_number = [index['indexNumber'] for index in existing_event_hubs if
                                  index['title'] == 'US Sports']
        if len(US_Sports_index_number) == 0:
            self.create_event_hub_for_index(index_num=new_index_number)
            index_number = new_index_number
        else:
            index_number = US_Sports_index_number[0]
        self.__class__.surface_bet_title2 = "Autotest_sb2_C65865541"
        self.create_surface_bet(selection_id=self.selection_id_2, event_id=self.event_id_2,
                                title=self.surface_bet_title2,
                                contentHeader=self.surface_bet_header
                                , content=self.surface_bet_content, index_number=index_number)
        wait_for_haul(60)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='Homepage')
        self.verify_surface_bet_on_fe(surface_bet_title=self.surface_bet_title2.upper())
        no_change = self.checking_order_of_surface_bet(surface_bet_title_1=self.surface_bet_title1.upper(),
                                                       surface_bet_title_2=self.surface_bet_title2.upper(),
                                                       changed=False)
        self.assertTrue(no_change,
                        msg=f'{self.surface_bet_title1} and '
                            f'{self.surface_bet_title2} is not configured as '
                            f'per order of surface bet in cms')

    def test_004_change_the_order_of_surface_bet_created(self):
        """
        DESCRIPTION: Change the Order of surface bet created
        EXPECTED: Order of Surface bet created should be as per CMS config
        """
        surface_bet_titles = [self.surface_bet_title1, self.surface_bet_title2]
        self.changing_sb_order(surface_bet_lists=surface_bet_titles)
        wait_for_haul(60)
        changed = self.checking_order_of_surface_bet(surface_bet_title_1=self.surface_bet_title1.upper(),
                                                                  surface_bet_title_2=self.surface_bet_title2.upper(),
                                                                  changed=True)
        self.assertTrue(changed,
                        msg=f'{self.surface_bet_title1} and '
                            f'{self.surface_bet_title2} is not configured as '
                            f' per order of surface bet in cms')

    def test_005_validate_the_surface_bet_title(self):
        """
        DESCRIPTION: Validate the surface bet Title
        EXPECTED: Title Name should be displayed as per CMS config
        """
        self.__class__.sb_1_response = self.surface_bet_dict.get(self.surface_bet_title1)
        self.__class__.sb_id = self.sb_1_response.get('id')
        expected_title = self.sb_1_response.get('title')
        expected_content_header = self.sb_1_response.get('contentHeader')
        expected_sb_content = self.sb_1_response.get('content')
        expected_sb_icon = self.sb_1_response.get('svgId')
        sb = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        _sb = sb.get(self.surface_bet_title1.upper())
        _sb.scroll_to()
        actual_title = _sb.name
        self.assertEqual(actual_title, expected_title.upper(), msg=f'{actual_title} not equal to {expected_title}')
        actual_content_header = _sb.content_header
        self.assertEqual(actual_content_header, expected_content_header,
                         msg=f'{actual_content_header} not equal to {expected_content_header}')
        actual_content = _sb.content
        self.assertEqual(actual_content, expected_sb_content,
                         msg=f'{actual_content} not equal to {expected_sb_content}')
        actual_sb_icon = _sb.header.icontext
        self.assertEqual(actual_sb_icon, f'#{expected_sb_icon}',
                         msg=f'{actual_sb_icon} is not equal to {expected_sb_icon}')

    def test_006_validate_the_surface_bet_is_displayed_on_all_sports(self):
        """
        DESCRIPTION: Validate the surface bet is displayed on 'All Sports'
        EXPECTED: Surface bet created should reflect on 'All Sports' pages as per CMS config
        """
        # not applicale for all sports

    def test_007_validate_the_surface_bet_is_displayed_in_the_event_hub_selected(self):
        """
        DESCRIPTION: Validate the surface bet is displayed in the event hub selected
        EXPECTED: Surface bet created should reflect in the 'eventhub' selected as per CMS config
        """
        # not applicale for event hub

    def test_008_validate_the_surface_bet_content_header(self):
        """
        DESCRIPTION: Validate the surface bet 'Content header'
        EXPECTED: Content Header' should be displayed as per CMS config
        """
        # covered in above step

    def test_009_validate_the_surface_bet_content(self):
        """
        DESCRIPTION: Validate the surface bet 'Content'
        EXPECTED: Content' should be displayed as per CMS config
        """
        # covered in above step

    def test_010_validate_the_surface_bet_was_price(self):
        """
        DESCRIPTION: Validate the surface bet 'Was Price'
        EXPECTED: Was Price' should be displayed as per OB config
        """
        # not applicable

    def test_011_verify_the_surface_bet_display_from_and_to_date(self):
        """
        DESCRIPTION: Verify the Surface Bet Display From and To date
        EXPECTED: Surface bet should be displayed based on CMS config start date
        EXPECTED: Surface bet should be displayed based on CMS config end date
        """
        # covered in above step

    def test_012_validate_the_svg_icon_and_svg_background(self):
        """
        DESCRIPTION: Validate the SVG icon and SVG background
        EXPECTED: SVG icon and SVG background should be displayed as per CMS config
        """
        # covered in above step

    def test_013_validate_surface_bet_with_segmentwith_single_inclusion(self):
        """
        DESCRIPTION: Validate surface bet with Segment(with single inclusion)
        EXPECTED: surface bet detail page should be opened with Universal (with single exclusion)
        """
        # validate in above step

    def test_014_validate_surface_bet_with_segmentwith_multiple_inclusion(self):
        """
        DESCRIPTION: Validate surface bet with Segment(with Multiple inclusion)
        EXPECTED: surface bet detail page should be opened with Universal (with Multiple exclusion)
        """
        # already covered in above step

    def test_015_activatedeactivate_the_whole_surface_bet_module_on_homepage(self):
        """
        DESCRIPTION: Activate/Deactivate the whole Surface bet module on homepage
        EXPECTED: Surface bet should display on Home page if it is activated
        EXPECTED: Surface bet should not display on Home page if it is deactivated
        """
        # it will affect other test case

    def test_016_verify_surface_bet_display_for_logged_in_amp_logged_out_users(self):
        """
        DESCRIPTION: Verify Surface bet display for Logged in &amp; Logged out users
        EXPECTED: Surface bet should display for all Logged in &amp; Loggedout users
        """
        self.site.logout()
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=15)
        self.verify_surface_bet_on_fe(self.surface_bet_title1.upper(), timeout=30, expected_result=False)
        self.site.login(username=self.username)
        self.set_local_storage_cookies_csp(self.cookies, self.segment)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='Homepage', timeout=15)
        self.verify_surface_bet_on_fe(self.surface_bet_title1.upper(), timeout=30)

    def test_017_verify_edited_field_changes_are_reflecting_in_fe_for_surface_bet(self):
        """
        DESCRIPTION: Verify Edited field changes are reflecting in FE for Surface bet
        EXPECTED: Edited fields data should be updated for Surface bet
        """
        # covered in C65865537

    def test_018_verify_surface_bet_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet disappears in FE upon deletion in CMS
        EXPECTED: Surface bet should disappear in FE
        """
        self.cms_config.delete_surface_bet(surface_bet_id=self.sb_id)
        self.cms_config._created_surface_bets.remove(self.sb_id)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='Homepage')
        self.verify_surface_bet_on_fe(surface_bet_title=self.surface_bet_title1.upper(), timeout=30,
                                      expected_result=False)
