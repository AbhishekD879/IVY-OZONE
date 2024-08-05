import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C29470_To_edit_Tracking_of_Pageview_events(Common):
    """
    TR_ID: C29470
    NAME: [To edit ] Tracking of Pageview events
    DESCRIPTION: This Test Case verifies the recording of a page view in the Google Analytic's data Layer and the URL/location when a user selects any on the page.
    DESCRIPTION: **Jira ticket: **BMA-6471 Google Analytics - Send pageview events for all navigation on the site
    DESCRIPTION: To edit
    DESCRIPTION: Step 3 - remove '?tab=Featured' from expected result.
    PRECONDITIONS: 1. Launch Invictus application
    PRECONDITIONS: 2. Open Console window
    """
    keep_browser_open = True

    def test_001_in_console_window_type_consoletabledatalayer_and_press_enter_button(self):
        """
        DESCRIPTION: In Console window type "console.table(dataLayer)" and press Enter button
        EXPECTED: Table with following events is displayed:
        EXPECTED: *   "gtm.js"
        EXPECTED: *   "content-view" with default for Home page content-name: "/"
        EXPECTED: *   "gtm.dom"
        EXPECTED: *   "gtm.load"
        """
        pass

    def test_002_perform_following_navigation1__featured_tab2__next_races3__in_play4__live_stream5__enhanced_multiples6__featured_taband_repeat_step_1(self):
        """
        DESCRIPTION: Perform following navigation:
        DESCRIPTION: 1.  Featured tab
        DESCRIPTION: 2.  Next Races
        DESCRIPTION: 3.  In-Play
        DESCRIPTION: 4.  Live Stream
        DESCRIPTION: 5.  Enhanced Multiples
        DESCRIPTION: 6.  Featured tab
        DESCRIPTION: and repeat step #1
        EXPECTED: "content-name" column near "content-view" events  appropriately should be following:
        EXPECTED: *   "/?tab=NextRaces"
        EXPECTED: *   "/?tab=InPlay"
        EXPECTED: *   "/?tab=LiveStream"
        EXPECTED: *   "/?tab=Multiples"
        EXPECTED: *   "/?tab=Featured"
        """
        pass

    def test_003_tap_on_a_z_sports_icon_and_repeat_step_1(self):
        """
        DESCRIPTION: Tap on A-Z Sports icon and repeat step #1
        EXPECTED: Two new events should be added to the table:
        EXPECTED: *   "gtm.click"
        EXPECTED: *   "content-view" with "content-name" - "/az-sports?tab=Featured"
        """
        pass

    def test_004_navigate_through_different_sports_and_repreat_step_1(self):
        """
        DESCRIPTION: Navigate through different sports and repreat step #1
        EXPECTED: "content-name" column should correstond to "content-view" events depending which sports user select, e.g.:
        EXPECTED: *   "americannfootball?tab=Featured"
        EXPECTED: *   "aussierules?tab=Featured"
        EXPECTED: *   "badminton?tab=Featured"
        EXPECTED: *   "baseball?tab=Featured"     etc.
        """
        pass

    def test_005_open_football_sports_landing_page_and_perform_following_navigation1__in_play2__coupons3__today4__tomorrow5__future6__outrights7__jackpotand_repeat_step_1(self):
        """
        DESCRIPTION: Open Football sports landing page and perform following navigation:
        DESCRIPTION: 1.  In-Play
        DESCRIPTION: 2.  Coupons
        DESCRIPTION: 3.  Today
        DESCRIPTION: 4.  Tomorrow
        DESCRIPTION: 5.  Future
        DESCRIPTION: 6.  Outrights
        DESCRIPTION: 7.  Jackpot
        DESCRIPTION: and repeat step #1
        EXPECTED: "content-name" column should correspond to "content-view" events:
        EXPECTED: *   "/footbal/live"
        EXPECTED: *   "/footbal/coupons"
        EXPECTED: *   "/footbal/today"
        EXPECTED: *   "/footbal/tomorrow"
        EXPECTED: *   "/footbal/future"
        EXPECTED: *   "/footbal/outrights"
        EXPECTED: *   "/footbal/jackpot"
        """
        pass

    def test_006_open_horseracing_landing_page_perform_following_navigation1__today2__tomorrow3__future4__results5__switch_sorting_type_to_by_meetingsand_repeat_step_1(self):
        """
        DESCRIPTION: Open Horseracing landing page, perform following navigation:
        DESCRIPTION: 1.  Today
        DESCRIPTION: 2.  Tomorrow
        DESCRIPTION: 3.  Future
        DESCRIPTION: 4.  Results
        DESCRIPTION: 5.  Switch sorting type to "By Meetings"
        DESCRIPTION: and repeat step #1
        EXPECTED: "content-name" column should correspond to "content-view" events:
        EXPECTED: *   "/horseracing/tomorrow"
        EXPECTED: *   "/horseracing/future"
        EXPECTED: *   "/horseracing/results"
        EXPECTED: *   "/horseracing/results/byMeetings"
        """
        pass

    def test_007_open_any_event_and_repeat_step_1(self):
        """
        DESCRIPTION: Open any event and repeat step #1
        EXPECTED: "content-name" column should correspond to "content-view" event:
        EXPECTED: *   "/horseracing/event/XXXXXXX", XXXXXXX - event id
        """
        pass

    def test_008_tap_on_log_in_button_tap_on_forgot_password_link_and_repeat_step_1(self):
        """
        DESCRIPTION: Tap on Log In button, tap on 'Forgot Password?' link and repeat step #1.
        EXPECTED: "content-name" column should correspond to "content-view" event:
        EXPECTED: *   "/forgot-password"
        """
        pass

    def test_009_tap_on_join_button_fill_in_join_us_form_step_1_and_step_2_tap_on_complete_registration_button_and_repeat_step_1(self):
        """
        DESCRIPTION: Tap on 'Join' button, fill in 'Join Us' form (step 1 and step 2), tap on 'Complete Registration' button and repeat step #1
        EXPECTED: "content-name" column should correspond to "content-view" events:
        EXPECTED: *   "/signup"
        EXPECTED: *   "/success-registration"
        """
        pass

    def test_010_open_promotions_page_perform_following_navigation1__tennis_insurance___more_information2__back_button3__super_acca_insurance___more_information4__back_button5__basketball_acca_insurance___more_informationrepeat_step_1promotions_are_configurable_in_cms_so_data_could_be_changed(self):
        """
        DESCRIPTION: Open Promotions page, perform following navigation:
        DESCRIPTION: 1.  Tennis Insurance -> More information
        DESCRIPTION: 2.  Back button
        DESCRIPTION: 3.  Super Acca Insurance -> More information
        DESCRIPTION: 4.  Back button
        DESCRIPTION: 5.  Basketball Acca Insurance -> More information
        DESCRIPTION: repeat step #1.
        DESCRIPTION: Promotions are configurable in CMS so data could be changed.
        EXPECTED: "content-name" column should correspond to "content-view" events:
        EXPECTED: *   "/promotions"
        EXPECTED: *   "/promotions/tennis&insuurance"
        EXPECTED: *   "/promotions/"
        EXPECTED: *   "/promotions/Super\_Acca\_Insurance"
        EXPECTED: *   "/promotions"
        EXPECTED: *   "/promotions/Basketball\_Acca\_Insurance"
        """
        pass

    def test_011_open_live_stream_page_and_perform_following_navigation1__live_now2__upcomingand_repeat_step_1(self):
        """
        DESCRIPTION: Open Live Stream page and perform following navigation:
        DESCRIPTION: 1.  Live Now
        DESCRIPTION: 2.  Upcoming
        DESCRIPTION: and repeat step #1
        EXPECTED: "content-name" column should correspond to "content-view" events:
        EXPECTED: *   "/live-stream"
        EXPECTED: *   "/live-stream/allsports/livenow"
        EXPECTED: *   "/live-stream/allsports/upcoming"
        """
        pass

    def test_012_open_my_live_racing_page_and_repeat_step_1(self):
        """
        DESCRIPTION: Open My Live Racing page and repeat step #1
        EXPECTED: "content-name" column should correspond to "content-view" event:
        EXPECTED: *   "/my-live-races"
        """
        pass

    def test_013_open_virtual_sport_page_and_perform_following_navigation1__virtual_basketball2__virtual_football3__virtual_cycling4__virtual_horse_racing5__virtual_motorsports6__virtual_tennis7__virtual_greyhounds8__virtual_speedwayand_repeat_step_1(self):
        """
        DESCRIPTION: Open Virtual Sport page and perform following navigation:
        DESCRIPTION: 1.  Virtual Basketball
        DESCRIPTION: 2.  Virtual Football
        DESCRIPTION: 3.  Virtual Cycling
        DESCRIPTION: 4.  Virtual Horse Racing
        DESCRIPTION: 5.  Virtual Motorsports
        DESCRIPTION: 6.  Virtual Tennis
        DESCRIPTION: 7.  Virtual Greyhounds
        DESCRIPTION: 8.  Virtual Speedway
        DESCRIPTION: and repeat step #1.
        EXPECTED: "content-name" column should correspond to "content-view" events:
        EXPECTED: *   "/virtual-sports"
        EXPECTED: *   "/virtual-sports/virtual-basketball"
        EXPECTED: *   "/virtual-sports/virtual-football"
        EXPECTED: *   "/virtual-sports/virtual-cycling"
        EXPECTED: *   "/virtual-sports/virtual-horse-racing"
        EXPECTED: *   "/virtual-sports/virtual-motorsports"
        EXPECTED: *   "/virtual-sports/virtual-tennis"
        EXPECTED: *   "/virtual-sports/virtual-greyhounds"
        EXPECTED: *   "/virtual-sports/virtual-speedway"
        """
        pass

    def test_014_open_lotto_page_tap_on_different_lotto_icons_and_repeat_step_1(self):
        """
        DESCRIPTION: Open Lotto page, tap on different Lotto icons and repeat step #1.
        EXPECTED: "content-name" column should correspond to "content-view" events e.g.:
        EXPECTED: *   "/lotto"
        EXPECTED: *   "/lotto/irish-lotto"
        EXPECTED: *   "/lotto/german-lotto"   etc.
        """
        pass

    def test_015_open_right_menu_perform_following_navigation1__deposit2__debitcredit_cards3__paypal4__netellerand_repeat_step_1(self):
        """
        DESCRIPTION: Open Right Menu, perform following navigation:
        DESCRIPTION: 1.  Deposit
        DESCRIPTION: 2.  Debit/Credit Cards
        DESCRIPTION: 3.  PayPal
        DESCRIPTION: 4.  NETELLER
        DESCRIPTION: and repeat step #1.
        EXPECTED: "content-name" column should correspond to "content-view" events:
        EXPECTED: *   "/deposit/registered"
        EXPECTED: *   "/deposit/addcard"
        EXPECTED: *   "/deposit/paypal"
        EXPECTED: *   "/deposit/neteller"
        """
        pass

    def test_016_open_right_menu_tap_on_withdraw_and_repeat_step_1(self):
        """
        DESCRIPTION: Open Right Menu, tap on Withdraw and repeat step #1.
        EXPECTED: "content-name" column should correspond to "content-view" event:
        EXPECTED: *   "/withdraw"
        """
        pass

    def test_017_open_right_menu_tap_on_cancel_withdrawal_and_repeat_step_1(self):
        """
        DESCRIPTION: Open Right Menu, tap on Cancel Withdrawal and repeat step #1.
        EXPECTED: "content-name" column should correspond to "content-view" event:
        EXPECTED: *   "/transaction-history/withdraw/pending"
        """
        pass

    def test_018_open_right_menu_perform_following_navigation1__my_account___vaucher_code2__my_account___bet_history3__my_account___transaction_history4__my_account___gaming_history5__my_account___limits6__my_account___change_password7__my_account___responsible_gamblingand_repeat_step_1(self):
        """
        DESCRIPTION: Open Right Menu, perform following navigation:
        DESCRIPTION: 1.  My Account -> Vaucher Code
        DESCRIPTION: 2.  My Account -> Bet History
        DESCRIPTION: 3.  My Account -> Transaction History
        DESCRIPTION: 4.  My Account -> Gaming History
        DESCRIPTION: 5.  My Account -> Limits
        DESCRIPTION: 6.  My Account -> Change Password
        DESCRIPTION: 7.  My Account -> Responsible Gambling
        DESCRIPTION: and repeat step #1.
        EXPECTED: "content-name" column should correspond to "content-view" events:
        EXPECTED: *   "/my-account"
        EXPECTED: *   "/bet-history"
        EXPECTED: *   "/my-account"
        EXPECTED: *   "/transaction-history"
        EXPECTED: *   "/my-account"
        EXPECTED: *   "/gaming-history"
        EXPECTED: *   "/my-account"
        EXPECTED: *   "/limits"
        EXPECTED: *   "/my-account"
        EXPECTED: *   "/change-password"
        EXPECTED: *   "/my-account"
        EXPECTED: *   "/responsible-gmbling"
        """
        pass

    def test_019_open_right_menu_tap_on_settings_and_repeat_step_1(self):
        """
        DESCRIPTION: Open Right Menu, tap on Settings and repeat step #1.
        EXPECTED: "content-name" culumn should correspond to "content-view" event:
        EXPECTED: *   "/settings"
        """
        pass

    def test_020_open_contact_us_page_and_repeat_step_1(self):
        """
        DESCRIPTION: Open Contact Us page and repeat step #1.
        EXPECTED: "content-name" column should sorrespond to "content-view" event:
        EXPECTED: *   "/contact-us"
        """
        pass

    def test_021_tap_on_my_bets_and_perform_following_navigation1__bet_slip2__cash_out3__my_betsand_repeat_step_1(self):
        """
        DESCRIPTION: Tap on My Bets and perform following navigation:
        DESCRIPTION: 1.  Bet Slip
        DESCRIPTION: 2.  Cash Out
        DESCRIPTION: 3.  My Bets
        DESCRIPTION: and repeat step #1.
        EXPECTED: "content-name" column should correspond to "content-view" events:
        EXPECTED: *   "/open-bets"
        EXPECTED: *   "/betslip"
        EXPECTED: *   "/cashout"
        EXPECTED: *   "/open-bets"
        """
        pass

    def test_022_trigger_the_situation_whe_ss_is_down_and_repeat_step_1(self):
        """
        DESCRIPTION: Trigger the situation whe SS is down and repeat step #1.
        EXPECTED: "content-name" column should correspond to "content-view" event:
        EXPECTED: *   "/under-maintanance"
        """
        pass

    def test_023_navigate_to_big_competition_eg_world_cup_module_and_perform_following_navigation1_featured2_groups21_all22_group_a23_group_b24_3_specials4_outright5_promo6_result7_knockout(self):
        """
        DESCRIPTION: Navigate to Big Competition (e.g. World Cup) module and perform following navigation:
        DESCRIPTION: 1. Featured
        DESCRIPTION: 2. Groups
        DESCRIPTION: 2.1 All
        DESCRIPTION: 2.2 Group A
        DESCRIPTION: 2.3 Group B
        DESCRIPTION: 2.4 .......
        DESCRIPTION: 3. Specials
        DESCRIPTION: 4. Outright
        DESCRIPTION: 5. Promo
        DESCRIPTION: 6. Result
        DESCRIPTION: 7. Knockout
        EXPECTED: "content-name" column should correspond to "content-view" events:
        EXPECTED: * "/big-competition/world-cup/featured"
        EXPECTED: * "/big-competition/world-cup/groups/all"
        EXPECTED: * "/big-competition/world-cup/groups/group-a"
        EXPECTED: * "/big-competition/world-cup/specials"
        EXPECTED: * "/big-competition/world-cup/outright"
        EXPECTED: * "/big-competition/world-cup/promo"
        EXPECTED: * "/big-competition/world-cup/results"
        EXPECTED: * "/big-competition/world-cup/knockout"
        """
        pass
