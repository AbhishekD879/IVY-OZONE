import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C58438878_From_OX1022_Verify_Child_Sports_navigation_on_Virtual_Sports(Common):
    """
    TR_ID: C58438878
    NAME: From [OX102.2] Verify Child Sports navigation on Virtual Sports
    DESCRIPTION: This test case verifies Child Sports icons of Virtual Sports
    PRECONDITIONS: Get SiteServer response to verify data:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/285?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: X.XX - Current supported version of OpenBet release (2.31)
    PRECONDITIONS: LL - Language (e.g. en, ukr)
    PRECONDITIONS: Virtual Sports designs:
    PRECONDITIONS: https://app.zeplin.io/project/5d64f0e582415f9b2a7045aa
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_check_hild_sports_navigation(self):
        """
        DESCRIPTION: Check Сhild Sports navigation.
        EXPECTED: 1. Сhild Sport navigation bar should be horizontal scrollable to fit all the sports.
        EXPECTED: 2. Each Child Sport is displayed as a button with the below details:
        EXPECTED: - Title of the Child Sport as per CMS
        EXPECTED: - The countdown timer for the next event
        """
        pass

    def test_002_check_hild_sports_for_horse_racing(self):
        """
        DESCRIPTION: Check Сhild Sports for Horse Racing.
        EXPECTED: - Сhild Sports items displayed according to designs
        EXPECTED: - 'Сhild Sports' contains all sports, related to Parent sports configured on CMS
        """
        pass

    def test_003_choose_another_class_from_hild_sports_navigation_bar(self):
        """
        DESCRIPTION: Choose another class from 'Сhild Sports' navigation bar.
        EXPECTED: - User is redirected to other Child sports page
        EXPECTED: - Events/Markets related to that sport are displayed
        """
        pass

    def test_004_switch_thought_other_parent_sports_and_repeat_this_test_case_for_the_following_virtual_sports_greyhounds_football_motorsports_cycling_speedway_tennis_grand_national(self):
        """
        DESCRIPTION: Switch thought other parent sports and repeat this test case for the following virtual sports:
        DESCRIPTION: * Greyhounds
        DESCRIPTION: * Football,
        DESCRIPTION: * Motorsports,
        DESCRIPTION: * Cycling,
        DESCRIPTION: * Speedway,
        DESCRIPTION: * Tennis
        DESCRIPTION: * Grand National
        EXPECTED: 
        """
        pass

    def test_005_on_desktop_onlyhover_the_mouse_on_list_of_children_sports(self):
        """
        DESCRIPTION: On Desktop only:
        DESCRIPTION: Hover the mouse on list of Children Sports.
        EXPECTED: The User is able to see the right arrow to slide through the list of Child Sports:
        EXPECTED: ![](index.php?/attachments/get/106948350)
        """
        pass

    def test_006_on_desktop_onlyclick_on_the_right_arrow(self):
        """
        DESCRIPTION: On Desktop only:
        DESCRIPTION: Click on the right arrow.
        EXPECTED: The list is scrolled to the right.
        """
        pass

    def test_007_on_desktop_onlyhover_the_mouse_out_of_list_of_children_sports(self):
        """
        DESCRIPTION: On Desktop only:
        DESCRIPTION: Hover the mouse out of list of Children Sports.
        EXPECTED: The right arrow is not displayed.
        """
        pass

    def test_008_on_desktop_onlyhover_the_mouse_on_the_list_of_children_sports(self):
        """
        DESCRIPTION: On Desktop only:
        DESCRIPTION: Hover the mouse on the list of Children Sports.
        EXPECTED: The User is able to see the left arrow to slide through the list of Child Sports:
        EXPECTED: ![](index.php?/attachments/get/106948351)
        """
        pass
