import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28758_Verify_Olympics_Sport_Menu_Ribbon(Common):
    """
    TR_ID: C28758
    NAME: Verify Olympics Sport Menu Ribbon
    DESCRIPTION: This Test Case verified Olympics Sport Menu Ribbon
    PRECONDITIONS: **JIRA Ticket:**
    PRECONDITIONS: BMA-10048 Olympics: Sport Ribbon Menu
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_the_olympics_page(self):
        """
        DESCRIPTION: Navigate to the Olympics page
        EXPECTED: Olympics page is opened
        """
        pass

    def test_003_verify_presense_of_olympics_sports_menu_ribbon(self):
        """
        DESCRIPTION: Verify presense of Olympics Sports Menu Ribbon
        EXPECTED: -Olympics Sports Menu Ribbon is applicable only to Olympics page
        EXPECTED: -Olympics Sports Menu Ribbon is applicable to both logged in and logged out customers
        EXPECTED: -Every item is tappable icon with label
        """
        pass

    def test_004_verify_menu_item_names(self):
        """
        DESCRIPTION: Verify Menu item names
        EXPECTED: Menu item names correspond to the names set in CMS
        """
        pass

    def test_005_verify_menu_item_if_there_are_no_events_available_for_particular_sport(self):
        """
        DESCRIPTION: Verify Menu item if there are no events available for particular sport
        EXPECTED: Menu item is still visible in the Sports Menu Ribbon
        """
        pass

    def test_006_verify_menu_item_icons_format(self):
        """
        DESCRIPTION: Verify Menu item icons' format
        EXPECTED: -'Filename' support only PNG or JPEG format
        EXPECTED: -It is possible not to upload an icon image
        """
        pass
