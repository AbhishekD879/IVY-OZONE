import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870179_Add_new_item_to_A_Z_menu_and_verify_on_the_FE(Common):
    """
    TR_ID: C44870179
    NAME: "Add new item to A-Z menu and verify on the FE
    DESCRIPTION: This Test case verifies adding new item to A-Z menu and reflecting on FE
    DESCRIPTION: Verify all Sports Pages Tier 3
    DESCRIPTION: (TIER 3 sports list:Athletics, Boxing, Curling, Cycling, Esports, Formula 1, Golf, Hurling, Motor Bikes, Motor Sports, Net Ball, Politics, Rowing, Royal Specials, Speedway, Squash, Table Tennis, TV Specials, UFC/MMA, Winter Sports, Chess, Hockey, Badminton, Baseball,Pool)
    PRECONDITIONS: Application is loaded
    PRECONDITIONS: Access to CMS
    PRECONDITIONS: Access to OpenBet Ti
    """
    keep_browser_open = True

    def test_001_open_cms__sports_pages__sports_categories(self):
        """
        DESCRIPTION: Open CMS > Sports Pages > Sports Categories
        EXPECTED: Sports Categories page is loaded on CMS
        """
        pass

    def test_002_click_on_create_sport_category(self):
        """
        DESCRIPTION: click on Create Sport Category
        EXPECTED: A pop-up window appears to enter details for the new sport. Fill in the details. and save changes.
        EXPECTED: eg : For testing purpose, give same details as Football sport and give a Test name for the sport.
        """
        pass

    def test_003_verify_on_the_fe(self):
        """
        DESCRIPTION: Verify on the FE
        EXPECTED: Verify if the newly added sport appears in the A-Z menu.
        EXPECTED: Please note that changes made in CMS may take upto 10 mins to reflect on FE
        """
        pass

    def test_004_verify_navigation_to_all_tier_3_sport_pages(self):
        """
        DESCRIPTION: Verify navigation to all Tier 3 sport pages
        EXPECTED: Click on any of Tier 3 sport and user should land on the corresponding sport Landing page.
        """
        pass
