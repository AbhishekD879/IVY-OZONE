import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C64378736_Verify_the_title_is_labelled_as_Automatic_Prize_Payout_for_prize_automation(Common):
    """
    TR_ID: C64378736
    NAME: Verify the title is labelled as "Automatic Prize Payout" for prize automation
    DESCRIPTION: Verify the title is labelled as "Automatic Prize Payout" for prize automation
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: Contest should be created and Prizes are added
    PRECONDITIONS: ***How to Configure Menu Item***
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    """
    keep_browser_open = True

    def test_001_login_as_cms_admin(self):
        """
        DESCRIPTION: Login as CMS admin
        EXPECTED: User should successful login to CMS
        """
        pass

    def test_002_navigate_to_5a_side_showdown_tab_in_left_menu_andlick_5a_side_show_down_label(self):
        """
        DESCRIPTION: Navigate to 5a side showdown tab in left menu and
        DESCRIPTION: lick 5a side show down label
        EXPECTED: user should able to navigate to contest page on clicking
        """
        pass

    def test_003_create_contest_or_click_any_contest_existing(self):
        """
        DESCRIPTION: Create contest or click any contest existing
        EXPECTED: User should able to create contest on clicking
        EXPECTED: create contest button or User should able to click the existing contest
        """
        pass

    def test_004_verify_automatic_prize_payout_label_is_displayed_above_prize_payout_section(self):
        """
        DESCRIPTION: Verify "Automatic Prize Payout" label is displayed above prize payout section
        EXPECTED: "Automatic Prize Payout" label is displayed above prize payout section
        """
        pass
