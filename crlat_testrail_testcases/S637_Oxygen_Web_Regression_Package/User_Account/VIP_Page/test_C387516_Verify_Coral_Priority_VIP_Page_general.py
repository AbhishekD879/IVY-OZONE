import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C387516_Verify_Coral_Priority_VIP_Page_general(Common):
    """
    TR_ID: C387516
    NAME: Verify Coral Priority (VIP) Page (general)
    DESCRIPTION: This test case verifies Coral Priority (VIP) Page, accessible ONLY for logged in VIP users
    DESCRIPTION: AUTOTEST [C9698270]
    PRECONDITIONS: User must be logged in
    PRECONDITIONS: User must be a VIP (see below)
    PRECONDITIONS: **VIP IMS Level Configuration**
    PRECONDITIONS: * Non-VIP players = IMS VIP Level _1 - 10_
    PRECONDITIONS: * Bronze players = IMS VIP Level _11_
    PRECONDITIONS: * Silver players = IMS VIP Level _12_
    PRECONDITIONS: * Gold players = IMS VIP Level _13_
    PRECONDITIONS: * Platinum players = IMS VIP Level _14_
    PRECONDITIONS: * In order to grant the user a VIP level, contact UAT for assistance
    PRECONDITIONS: * VIP point API information: https://confluence.egalacoral.com/display/SPI/VIP+Points+API
    """
    keep_browser_open = True

    def test_001_tap_the_balance_button_in_order_to_open_right_hand_menu(self):
        """
        DESCRIPTION: Tap the balance button in order to open Right Hand Menu
        EXPECTED: Right Hand Menu is opened
        """
        pass

    def test_002_tap_more_info_link_on_the_vip_summary(self):
        """
        DESCRIPTION: Tap 'More Info' link on the VIP Summary
        EXPECTED: User is redirected to the VIP page
        """
        pass

    def test_003_verify_vip_page_url_and_page_header(self):
        """
        DESCRIPTION: Verify VIP Page URL and page header
        EXPECTED: * VIP Page URL is: **https://<environment>.coral.co.uk/vip**
        EXPECTED: * Page header reads **'Coral VIP'**
        """
        pass

    def test_004_verify_back__button(self):
        """
        DESCRIPTION: Verify 'Back' ('<') button
        EXPECTED: The 'back' button redirects the user to their previous page
        """
        pass

    def test_005_verify_the_vip_header(self):
        """
        DESCRIPTION: Verify the VIP Header
        EXPECTED: VIP User is able to see the following information on the page:
        EXPECTED: * VIP User's First and Last Name
        EXPECTED: * VIP level background icon
        EXPECTED: * 'VIP Level' label
        EXPECTED: * VIP level, depending on the level of the user, who is logged in
        EXPECTED: * VIP User's total number of Priority/VIP points
        EXPECTED: * 'VIP Status' setting including the on/off slider button
        """
        pass

    def test_006_verify_users_vip_level(self):
        """
        DESCRIPTION: Verify user's VIP level
        EXPECTED: VIP Level is one of the following:
        EXPECTED: * Bronze
        EXPECTED: * Silver
        EXPECTED: * Gold
        EXPECTED: * Platinum
        EXPECTED: (check Preconditions for details)
        """
        pass

    def test_007_verify_vip_status_setting(self):
        """
        DESCRIPTION: Verify 'VIP Status' setting
        EXPECTED: 'VIP Status' is enabled by default
        """
        pass

    def test_008_tap_the_vip_status_slider(self):
        """
        DESCRIPTION: Tap the 'VIP Status' slider
        EXPECTED: * Slider/button appears disabled
        EXPECTED: * 'Points Meter' and 'Total Number of Priority' are hidden from the VIP Summary on the Right Hand Menu
        """
        pass

    def test_009_verify_vip_intro_text_and_promotions_button(self):
        """
        DESCRIPTION: Verify 'VIP Intro Text' and 'Promotions' button
        EXPECTED: * There is 'VIP Intro' text and 'Promotions' button
        EXPECTED: *'VIP Intro' text reads:
        EXPECTED: _"Here at Coral.co.uk we strive to offer our most loyal customers the best possible user experience, hospitality events and promotions available online. Our Priority Program provides qualifying customers with better pricing, exclusive promotions and Priority Customer Service.
        EXPECTED: As a priority customer our VIP offers page will host personalised and Priority exclusive offers for you to take advantage of!"_
        """
        pass

    def test_010_tap_the_promotions_button(self):
        """
        DESCRIPTION: Tap the 'Promotions' button
        EXPECTED: User is taken to the Coral mobile promotions page
        """
        pass

    def test_011_verify_text_in_the_points_section(self):
        """
        DESCRIPTION: Verify text in the 'Points Section'
        EXPECTED: The text reads as follows:
        EXPECTED: _"We update Priority Points on a daily basis and when logged in you will see your current points total for the calendar month up until midnight the previous day"_
        """
        pass

    def test_012_verify_points_meters(self):
        """
        DESCRIPTION: Verify points meters
        EXPECTED: The following points meters are displayed:
        EXPECTED: * 'Sport Total' points meter
        EXPECTED: * 'Gaming Total' points meter
        EXPECTED: * 'Total' points meter
        """
        pass

    def test_013_verify_points_information(self):
        """
        DESCRIPTION: Verify Points Information
        EXPECTED: The section includes the following:
        EXPECTED: * 'Priority Points Information' label
        EXPECTED: * 'How Do I Qualify for the Priority Programme?' label
        EXPECTED: *  Main text and table
        """
        pass

    def test_014_verify_how_do_i_qualify_for_the_priority_programme_information(self):
        """
        DESCRIPTION: Verify 'How Do I Qualify for the Priority Programme?' information
        EXPECTED: The text reads as follows:
        EXPECTED: To qualify for the Priority Programme customers must reach points and deposit targets each calendar month for your play on Coral shown in the box to the right. Points can be earned on any of our products whether you play online , mobile or by using your connect card in the shop!
        EXPECTED: Priority Points are earned in the following way:
        EXPECTED: - **2** **points** for every **£10** **stake** on **Slots**, **Scratchcards** **and** **Bingo**.
        EXPECTED: - **1** **point** for every **£10** **stake** for all **other** **casino** **games**.
        EXPECTED: - **2.5** **points** for every **£10** **stake** for **sports** **single** **bets**.
        EXPECTED: - **3** **points** for every **£10** **stake** for **sports** **multiple** **bets**.
        """
        pass

    def test_015_verify_priority_point_targets_table(self):
        """
        DESCRIPTION: Verify 'Priority Point targets' table
        EXPECTED: The text reads as follows:
        EXPECTED: The table below shows the overall Priority Point targets along with the minimum deposits that must be met to qualify for the Priority Programme each calendar month.
        EXPECTED: **Bronze** :
        EXPECTED: * Deposits £1,000
        EXPECTED: * Priority Points 1,500
        EXPECTED: **Silver** :
        EXPECTED: * Deposits £2,000
        EXPECTED: * Priority Points 2,500
        EXPECTED: **Gold** :
        EXPECTED: * Deposits £4,000
        EXPECTED: * Priority Points 12,500
        EXPECTED: **Platinum** :
        EXPECTED: * Invite Only
        """
        pass

    def test_016_verify_terms_and_conditions(self):
        """
        DESCRIPTION: Verify Terms and Conditions
        EXPECTED: The following info is displayed:
        EXPECTED: **Terms And Conditions**
        EXPECTED: The criteria shown in the table above is the minimum requirement needed to be considered for each Priority Tier.
        EXPECTED: The Priority Tier calculation is based on a combination of Priority Points and Deposit Values over a four week period from the 1st of each calendar month.
        EXPECTED: Possible delay of up to 24 hours in calculating retail points.
        EXPECTED: Priority Points for each tier shown on the Programme page are to be used as a guide only.
        EXPECTED: Customers who meet the requirements in the table are not guaranteed to have access to Priority Rewards.
        EXPECTED: New Customers will be added to the VIP Programme on a weekly basis.
        EXPECTED: Priority Tier upgrades and downgrades will occur on a monthly basis.
        EXPECTED: Customers can only be downgraded one tier per calendar month.
        EXPECTED: Coral reserve the right to remove Priority status at any time.
        EXPECTED: Accounts will be reviewed on a weekly basis and customers introduced to the Priority Programme each Monday.
        EXPECTED: All other movements are made at the beginning of each new calendar month.
        EXPECTED: We reserve the right to amend Priority Tiers at any time for any reason, and to exclude or remove all benefits from customers at any time for any reason.
        EXPECTED: For additional promotional terms click here.
        EXPECTED: Promoter: Coral (Interactive) Gibraltar Limited, Europort, Gibraltar.
        """
        pass

    def test_017_repeat_step_6_for_the_following_users_bronze_players__ims_vip_level__11__silver_players__ims_vip_level__12__gold_players__ims_vip_level__13__platinum_players__ims_vip_level__14_(self):
        """
        DESCRIPTION: Repeat step #6 for the following users:
        DESCRIPTION: * Bronze players = IMS VIP Level _11_
        DESCRIPTION: * Silver players = IMS VIP Level _12_
        DESCRIPTION: * Gold players = IMS VIP Level _13_
        DESCRIPTION: * Platinum players = IMS VIP Level _14_
        EXPECTED: User's VIP level info is shown correctly according to his actual VIP level
        """
        pass
