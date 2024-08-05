import pytest
from tests.Common import Common
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.csp
@vtest
class Test_C65581910_Verify_universal_view_for_inplay_and_sports_ribbon_before_user_login(Common):
    """
    TR_ID: C65581910
    NAME: Verify universal view for Inplay and Sports ribbon before user login.
    DESCRIPTION: This testcases verifies Universal view before user login
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > Inplay/Sports Ribbon
    PRECONDITIONS: Create atleast a record in each module
    PRECONDITIONS: Select Universal Radio button while creating record.
    PRECONDITIONS: For Universal,There is atleast one record for each module added to the Homepage in CMS
    """
    keep_browser_open = True
    title = vec.olympics.WRESTLING

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > sports pages > Inplay/Sports Ribbon
        """
        sports = self.cms_config.get_sport_categories()
        for sport in sports:
            if sport['imageTitle'] == vec.olympics.WRESTLING:
                self.cms_config.update_sport_category(sport_category_id=sport['id'])
                break
        else:
            raise VoltronException(f'{vec.olympics.WRESTLING} sport not found in sports categories')

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application.
        EXPECTED: Application should launch successfully.
        """
        # Covered in above step

    def test_002_navigate_to_homepage(self):
        """
        DESCRIPTION: Navigate to Homepage
        EXPECTED: Home page should be opened.
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage', timeout=20)

    def test_003_verify_universal_view_by_default_before_login(self):
        """
        DESCRIPTION: Verify universal view (by default) before login
        EXPECTED: User should able to view Universal records for each module (Inplay/Sports Ribbon) as configured in CMS.
        """
        sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
        self.assertTrue(sports, msg='No inplay sports found in the module')
        self.__class__.sport_name = sports[-1]
        self.cms_config.update_inplay_sport_module(sport_name=self.sport_name.title(),
                                                   universalSegment=True)
        self.device.refresh_page()
        inplay_sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
        self.assertIn(self.sport_name, inplay_sports, msg=f'Segmented record {self.sport_name} is not displayed among {inplay_sports}')
        title = self.title if self.site.brand == 'ladbrokes' else self.title.upper()
        sports = list(self.site.home.menu_carousel.items_as_ordered_dict.keys())
        self.assertIn(title, sports,
                      msg=f'Created sport category "{title}" is not appearing, actual categories "{sports}"')
