import pytest

from tests.base_test import BaseTest
from tests.base_test import vtest


# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.portal_only_test
@pytest.mark.footer
@pytest.mark.navigation
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.safari
@vtest
class Test_C28381_Verify_Footer_Items(BaseTest):
    """
    TR_ID: C28381
    VOL_ID: C9698472
    NAME: Verify Footer items
    """
    keep_browser_open = True

    skip_list = [
        'GAMING',
        'Gaming',
        'Online rules',
        'Terms & conditions',
        'Shop rules',
        'About us',
        'Help',
        'Sport stats',
        'Live scores',
        'Affiliates',
        'Jobs',
        'Shop rules',
        'Privacy policy',
        'Responsible Gambling',
        'TEST1',
        'Oksana\'s test',
    ]

    def test_001_open_app(self):
        """
        DESCRIPTION: Validate footer presence
        """
        footer_shown = self.site.navigation_menu.is_displayed()
        self.assertTrue(footer_shown, msg='Footer navigation menu is not shown')

    def test_002_verify_endpoints_of_footer_items(self):
        """
        DESCRIPTION: Verify endpoints of footer items
        """
        footer_items = self.site.navigation_menu.items_as_ordered_dict
        for name, item in footer_items.items():
            if item.is_displayed():
                if name in self.skip_list:
                    continue
                self._logger.info(f'*** Navigating to "{name}"')
                item.click()
