import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_cms_reflection, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.adhoc_suite
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.surface_bets
@pytest.mark.desktop
@pytest.mark.slow
@vtest
@pytest.mark.timeout(1200)
@pytest.mark.slow
class Test_C65865540_Verify_surface_bet_on_event_detail_page(Common):
    """
    TR_ID: C65865540
    NAME: Verify surface bet on event detail page
    DESCRIPTION: 
    PRECONDITIONS: Create a event in OB
    PRECONDITIONS: Surface bet Creation in CMS:
    PRECONDITIONS: 1.Login to Environment specific CMS
    PRECONDITIONS: 2.Navigate to Home Page --&gt;Surface bets
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
    PRECONDITIONS: 6.Check 'Universal' radio button with Exclusion Segments: Without ,Single or multiple
    PRECONDITIONS: 7.Click Save Changes
    PRECONDITIONS: Check the Sort Order of Surface bet Module
    PRECONDITIONS: Navigate to Home Page--&gt;Surface bet Module--&gt; Select newly Created Surface bet--&gt; Check the Surface bet order
    """
    keep_browser_open = True
    segment = vec.bma.CSP_CMS_SEGEMENT
    cookies = vec.bma.CSP_COOKIE_SEGMENT

    def create_event_hub_for_index(self, index_num: int):
        self.cms_config.create_event_hub(index_number=index_num)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_num, module_type='SURFACE_BET')

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
        else:
            self.assertFalse(surface_bet, msg=f"Surface bet: {name} Found on {page_name}")
        return surface_bet

    def get_surface_bet_on_EDP(self, name, expected_result=True):
        return self._fetch_and_assert_surface_bet(
            lambda: self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict.get(name),
            name=name,
            page_name="EDP page",
            expected_result=expected_result
        )

    def get_surface_bet_on_home(self, name, expected_result=True):
        def fetch_surface_bet_mobile():
            return self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(name)

        def fetch_surface_bet_others():
            return self.site.home.desktop_modules.items_as_ordered_dict.get(
                vec.SB.HOME_FEATURED_NAME).tab_content.surface_bets.items_as_ordered_dict.get(
                name)

        fetch_surface_bet_func = fetch_surface_bet_mobile if self.device_type == 'mobile' else fetch_surface_bet_others
        return self._fetch_and_assert_surface_bet(fetch_surface_bet_func, name, "Home page",
                                                  expected_result=expected_result)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create a event in OB
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)
            event1 = events[0]
            self.__class__.event_id_1 = event1['event']['id']
            self.__class__.selection_id_1 = event1['event']['children'][0]['market']['children'][0]['outcome']['id']
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
        self.__class__.surface_bet_title = "Autotest_surfacebet_C65865540"
        self.__class__.surface_bet_header = 'surface bet header'
        self.__class__.surface_bet_content = 'surface bet content'
        self.__class__.surface_bet = self.cms_config.add_surface_bet(
            selection_id=self.selection_id_1,
            eventIDs=[self.event_id_1],
            universalSegment=True,
            svg_icon="football",
            on_homepage=True,
            title=self.surface_bet_title,
            contentHeader=self.surface_bet_header,
            content=self.surface_bet_content,
            eventHubsIndexs=[index_number],
            all_sports=True,
            edp_on=True,
            categoryIDs=[]
        )

    def test_001_login_to_ladscoral_ampltenvironmentampgt(self):
        """
        DESCRIPTION: Login to Lads/Coral &amp;lt;Environment&amp;gt;
        EXPECTED: User should be logged in
        """
        self.site.login()
        self.navigate_to_edp(event_id=self.event_id_1)
        self.get_surface_bet_on_EDP(name=self.surface_bet_title.upper())

    def test_002_validate_the_surface_bet_title(self):
        """
        DESCRIPTION: Validate the surface bet Title
        EXPECTED: Title Name should be displayed as per CMS config
        """
        expected_title = self.surface_bet['title']
        sb_ = self.site.sport_event_details.tab_content.surface_bets.items_as_ordered_dict.get(
            self.surface_bet_title.upper())
        actual_title = sb_.name
        self.assertEqual(actual_title.upper(), expected_title.upper(),
                         msg=f'{actual_title.upper()} is not equal to {expected_title.upper()}')

    def test_003_validate_the_surface_bet_is_displayed_on_event_detail_page_which_is_used_to_create_surface_bet(self):
        """
        DESCRIPTION: Validate the surface bet is displayed on event detail page which is used to create surface bet
        EXPECTED: Surface bet created should reflect on edp page as per CMS config
        """
        self.site.wait_content_state(state_name='EventDetails')
        self.get_surface_bet_on_EDP(name=self.surface_bet_title.upper())

    def test_004_validate_the_surface_bet_content_header_content_svg_icon_and_svg_background(self):
        """
        DESCRIPTION: Validate the surface bet 'Content header', 'content', SVG icon and SVG background
        EXPECTED: Content Header' should be displayed as per CMS config
        EXPECTED: Content' should be displayed as per CMS config
        EXPECTED: SVG icon and SVG background should be displayed as per CMS config
        """
        # covered in C65865541

    def test_005_verify_the_surface_bet_display_from_and_to_date(self):
        """
        DESCRIPTION: Verify the Surface Bet Display From and To date
        EXPECTED: Surface bet should be displayed based on CMS config start date
        EXPECTED: Surface bet should be displayed based on CMS config enddate
        """
        # covered in above steps

    def test_006_validate_surface_bet_with_only_universal_checked(self):
        """
        DESCRIPTION: Validate surface bet with only universal checked
        EXPECTED: Surface bet should display for all Logged in &amp; Loggedout users
        """
        # covered in above step

    def test_007_validate_surface_bet_with_universal_checked_and_multiple_exculsion_segment(self):
        """
        DESCRIPTION: Validate surface bet with universal checked and multiple exculsion segment
        EXPECTED: Surface bet should NOT display for the excluded multiple users
        """
        self.__class__.sb_id = self.surface_bet.get('id')
        if self.device_type == 'mobile':
            segmentReferences = [{
                "segmentName": "Universal",
                "sortOrder": -1.0
            }]
            self.cms_config.update_surface_bet(surface_bet_id=self.sb_id,
                                               on_homepage=True,
                                               exclusionList=[self.segment],
                                               segmentReferences=segmentReferences)
            self.navigate_to_page(name="/")
            self.set_local_storage_cookies_csp(self.cookies, self.segment)
            self.device.refresh_page()
            self.site.wait_content_state(state_name="Home")
            self.get_surface_bet_on_home(name=self.surface_bet_title.upper(), expected_result=False)
            self.set_local_storage_cookies_csp(self.cookies, "")

    def test_008_verify_surface_bet_display_for_logged_in_amp_logged_out_users(self):
        """
        DESCRIPTION: Verify Surface bet display for Logged in &amp; Logged out users
        EXPECTED: Surface bet should display for all Logged in &amp; Logged out users
        """
        self.site.logout()
        self.navigate_to_edp(event_id=self.event_id_1)
        self.get_surface_bet_on_EDP(name=self.surface_bet_title.upper())

    def test_009_verify_edited_field_changes_are_reflecting_in_fe_for_surface_bet(self):
        """
        DESCRIPTION: Verify Edited field changes are reflecting in FE for Surface bet
        EXPECTED: Edited fields data should be updated for Surface bet
        """
        sb_id = self.surface_bet.get('id')
        modified_content_header = 'surface bet header modified'
        modified_title = f"{self.surface_bet_title} modified".upper()
        self.cms_config.update_surface_bet(surface_bet_id=sb_id,
                                           title=modified_title,
                                           contentHeader=modified_content_header)
        surface_bet = self.get_surface_bet_on_EDP(name=modified_title)
        surface_bet.scroll_to()
        sb_header = surface_bet.content_header
        self.assertEqual(sb_header, modified_content_header,
                         msg=f'{sb_header} is not equal to {modified_content_header}')

    def test_010_verify_surface_bet_disappears_in_fe_upon_deletion_in_cms(self):
        """
        DESCRIPTION: Verify Surface bet disappears in FE upon deletion in CMS
        EXPECTED: Surface bet should disappear in FE
        """
        self.cms_config.delete_surface_bet(surface_bet_id=self.sb_id)
        self.cms_config._created_surface_bets.remove(self.sb_id)
        self.get_surface_bet_on_EDP(name=self.surface_bet_title.upper(), expected_result=False)
