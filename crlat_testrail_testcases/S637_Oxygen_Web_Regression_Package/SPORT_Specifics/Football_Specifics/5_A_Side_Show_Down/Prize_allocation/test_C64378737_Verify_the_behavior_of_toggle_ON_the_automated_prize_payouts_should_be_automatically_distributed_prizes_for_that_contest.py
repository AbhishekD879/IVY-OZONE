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
class Test_C64378737_Verify_the_behavior_of_toggle_ON_the_automated_prize_payouts_should_be_automatically_distributed_prizes_for_that_contest(Common):
    """
    TR_ID: C64378737
    NAME: Verify the behavior of toggle  ON , the automated prize payouts should be automatically distributed prizes for that contest.
    DESCRIPTION: Verify the behavior of toggle  ON , the automated prize payouts should be automatically distributed prizes for that contest.
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

    def test_002_navigate_to_5a_side_showdown_tab_in_left_menu_and_click_5a_side_show_down_label(self):
        """
        DESCRIPTION: Navigate to 5a side showdown tab in left menu and click 5a side show down label
        EXPECTED: user should able to navigate to contest page on clicking
        """
        pass

    def test_003_create_contest_or_click_any_contest_existing(self):
        """
        DESCRIPTION: Create contest or click any contest existing
        EXPECTED: User should able to create contest on clicking create contest button or User should able to click the existing contest
        """
        pass

    def test_004_navigate_to_automatic_prize_payout_label_above_the_prize_pool_section_in_contest_deatil_page(self):
        """
        DESCRIPTION: Navigate to Automatic Prize Payout label above the prize pool section in contest deatil page
        EXPECTED: User should able to navigate to Automatic Prize Payout  in contest detail page
        """
        pass

    def test_005_verify_toggle_on_button_is_displayed_default__beside_automatic_prize_payout_label(self):
        """
        DESCRIPTION: Verify toggle ON button is displayed default , beside Automatic Prize Payout label
        EXPECTED: Retrieving data. Wait a few seconds and try to cut or copy again.
        """
        pass

    def test_006_verify_automatic_prize_payout_trigger_after_the_90m_of_match(self):
        """
        DESCRIPTION: Verify "Automatic Prize Payout" trigger after the 90m of match
        EXPECTED: "Automatic Prize Payout" should trigger after 90m of match duration and prize payouts should be automatically distributed prizes for that contest.
        """
        pass
