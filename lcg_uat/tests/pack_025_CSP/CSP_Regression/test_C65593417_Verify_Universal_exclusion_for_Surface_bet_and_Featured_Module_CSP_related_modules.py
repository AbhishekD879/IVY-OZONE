import pytest
import tests
import voltron.environments.constants as vec
import time
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.mobile_only
@pytest.mark.reg156_fix
@vtest
class Test_C65593417_Verify_Universal_exclusion_for_Surface_bet_and_Featured_Module_CSP_related_modules(BaseFeaturedTest):
    """
    TR_ID: C65593417
    NAME: Verify Universal exclusion for Surface bet & Featured Module CSP related modules.
    DESCRIPTION: Verify Universal exclusion for Surface bet & Featured Module CSP related modules
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > Surface bet/Featured Module
    PRECONDITIONS: Create atleast a record in each module
    PRECONDITIONS: Create a Universal exclusion record by selecting universal radio button, select segment in Exclusion segments text box
    PRECONDITIONS: User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    """
    keep_browser_open = True
    segment = vec.bma.CSP_CMS_SEGEMENT
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT

    def verify_surface_bet(self, surface_bet_presence=True):
        """
        To Verify presence of surface
        """
        surface_bet = self.site.home.tab_content.has_surface_bets()
        if surface_bet:
            surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
            self.assertTrue(surface_bets, msg='No Surface Bets found')
            surface_bet = surface_bets.get(self.surface_bet_title)
            if surface_bet_presence:
                self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')
            else:
                self.assertFalse(surface_bet, msg=f'"{self.surface_bet_title}" is found in "{list(surface_bets.keys())}"')
        elif not surface_bet_presence:
            self.assertFalse(surface_bet, msg=f'"{self.surface_bet_title}" is found on homepage')

    def verify_featured_module(self, featured_module_presence=True):
        """
        To verify presence of featured tab
        """
        wait_time = 5  # Wait time in seconds
        max_polling_time = 120  # Maximum polling time in seconds (2 minutes)
        start_time = time.time()
        if featured_module_presence:
            featured_module = None
            while time.time() - start_time < max_polling_time:
                featured_module = self.site.home.get_module_content(self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
                featured_module.scroll_to()
                self.sections = featured_module.accordions_list.items_as_ordered_dict
                self.sections = [section.upper() for section in self.sections]
                if self.module_featured_type_name not in self.sections:
                    wait_for_haul(wait_time)
                else:
                    break
            self.module_featured_type_name = next(
                (section for section in self.sections if section.upper() == self.module_featured_type_name), None)
            section = featured_module.accordions_list.items_as_ordered_dict.get(self.module_featured_type_name)
            self.assertTrue(section, msg=f'Section "{self.module_featured_type_name}" is not found on FEATURED tab')
        else:
            featured_module = None
            while time.time() - start_time < max_polling_time:
                featured_module = self.site.home.get_module_content(
                    self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
                featured_module.scroll_to()
                self.sections = featured_module.accordions_list.items_as_ordered_dict
                self.sections = [section.upper() for section in self.sections]
                if self.module_featured_type_name in self.sections:
                    wait_for_haul(wait_time)
                else:
                    break
            self.module_featured_type_name = next(
                (section for section in self.sections if section.upper() == self.module_featured_type_name), None)
            section = featured_module.accordions_list.items_as_ordered_dict.get(self.module_featured_type_name)
            self.assertFalse(section, msg=f'Featured module is appearing in exclusion mode')

    def test_000_preconditions(self):
        """"
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Sports pages > Sports category
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            type_id = event['event']['typeId']
            eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(event_selection.values())[0]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
            selection_id = event.selection_ids[event.team1]
            eventID = event.event_id
        surface_bet = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                      categoryIDs=[0, 16],
                                                      eventIDs=[eventID], exclusionList=[self.segment])
        self.__class__.surface_bet_title = surface_bet.get('title').upper()

        Featured_module = self.cms_config.add_featured_tab_module(select_event_by='Event',
                                                id=eventID,
                                                show_all_events=True,
                                                events_time_from_hours_delta=-10,
                                                module_time_from_hours_delta=-10,
                                                exclusionList=[self.segment]
                                                )
        self.__class__.module_featured_type_name = Featured_module['title'].upper()

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        # Covered in above pre-condition step

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        # Covered in above pre-condition step

    def test_003_click_on_super_button_link(self):
        """
        DESCRIPTION: click on super button link.
        EXPECTED: User should be able to view existing super buttons should be displayed.
        """
        # Covered in above pre-condition step

    def test_004_click_on_super_button_cta_button(self):
        """
        DESCRIPTION: Click on super button CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segments inclusion with text boxes
        """
        # Covered in above pre-condition step

    def test_005_select_universal_radio_button(self):
        """
        DESCRIPTION: Select Universal radio button
        EXPECTED: Upon selecting Universal radio button ,Segment(s) Exclusion text field should be enabled and able to enter text (ex: Football)
        """
        # Covered in above pre-condition step

    def test_006_click_on_create_button(self):
        """
        DESCRIPTION: Click on create button
        EXPECTED: On successful creation, page should redirect to super button module page
        """
        # Covered in above pre-condition step

    def test_007_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state("homepage")

    def test_008_login_in_fe_with_userexcept_specific_segmented_user__which_is_excluded(self):
        """
        DESCRIPTION: Login in FE with user(except specific segmented user  which is excluded)
        EXPECTED: Universal user should able to view surface and featured module(as we have configured segment(s) Exclusion as Football)
        """
        self.site.login()
        self.verify_surface_bet()
        self.verify_featured_module()

    def test_009_login_with_specific_excluded_segmented_user(self):
        """
        DESCRIPTION: Login with specific excluded segmented user
        EXPECTED: Excluded record should not displayed for specific segmented user.
        """
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        wait_for_haul(5)
        self.verify_surface_bet(surface_bet_presence=False)
        self.verify_featured_module(featured_module_presence=False)

    def test_010_repeat_same_steps_for_remaining_all_other_modules_as_per_pre_conditions_(self):
        """
        DESCRIPTION: Repeat same steps for remaining all other modules (as per pre conditions )
        EXPECTED: Excluded record should not displayed for specific segmented user.
        """
        # Already Covered in above steps
