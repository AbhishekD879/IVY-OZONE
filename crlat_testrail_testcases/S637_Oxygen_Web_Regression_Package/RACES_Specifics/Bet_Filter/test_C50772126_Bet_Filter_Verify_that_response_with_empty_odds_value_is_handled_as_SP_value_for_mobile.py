import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C50772126_Bet_Filter_Verify_that_response_with_empty_odds_value_is_handled_as_SP_value_for_mobile(Common):
    """
    TR_ID: C50772126
    NAME: [Bet Filter] Verify that response with empty odds value is handled as 'SP' value for mobile
    DESCRIPTION: This test case verifies proper front-end handling of a response case from https://api.racemodlr.com with empty "odds" value in it, and ability to use the processed selection value for bet placement in QuickBet/Betslip module on a mobile device.
    PRECONDITIONS: In order to properly run this test case you need to have a configured **Charles** application on your desktop.
    PRECONDITIONS: Please use following instruction to configure the basic interception for the application: https://confluence.egalacoral.com/display/SPI/Charles+-+HTTP%28S%29+Debugging
    PRECONDITIONS: In order to find out the API url used for Requests/Responses sending/receiving open the Development Tools in your browser, switch to 'Horse Racing' landing page and tap/click on 'Bet Filter' button.
    PRECONDITIONS: Once that is done, filter the responses with following input 'api.race'. Copy the Request URL from the response.
    PRECONDITIONS: ![](index.php?/attachments/get/66425162)
    PRECONDITIONS: In order to intercept request within the Oxygen App, please open your **Charles app**, select 'Proxy' -> 'Breakpoint Settings' option in the header menu.
    PRECONDITIONS: ![](index.php?/attachments/get/66425163)
    PRECONDITIONS: Once 'Breakpoint Settings' modal is opened, make sure that 'Enable Breakpoints' checkbox is checked, and click 'Add' button.
    PRECONDITIONS: ![](index.php?/attachments/get/66425164)
    PRECONDITIONS: In the 'Edit Breakpoint' sub-modal window paste the 'Host name and Domain name' of the previously copied Request URL into the 'Host' field (i.e. api.racemodlr.com).
    PRECONDITIONS: Also, paste the 'Path' of the previously copied Request URL into the 'Path' field(i.e. /cypher/ladbrokesTest2/0/).
    PRECONDITIONS: Select 'HTTPS' protocol within 'Protocol' dropdown and check the 'Response' checkbox'.
    PRECONDITIONS: ![](index.php?/attachments/get/66425165)
    PRECONDITIONS: Once that is done, click 'OK' button to close the sub-modal window, and another 'OK' button to close the modal window.
    PRECONDITIONS: (!) Test case can only be run when 'Bet Filter Results' page contains Unsuspended(Active) selections.
    PRECONDITIONS: 1) User is logged out
    PRECONDITIONS: 2) Oxygen App is opened in a mobile responsive view of a Chrome Web Browser.
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to Horse Racing landing page
        EXPECTED: '/horse-racing/featured' page is opened
        """
        pass

    def test_002_clicktap_bet_filter_button(self):
        """
        DESCRIPTION: Click/Tap 'Bet Filter' button
        EXPECTED: '/bet-finder' page is opened
        EXPECTED: (!) Please 'Execute' the response through the 'Breakpoint' through the **Charles** application should it occur when this page is opened
        EXPECTED: ![](index.php?/attachments/get/66425166)
        EXPECTED: ![](index.php?/attachments/get/66425167)
        """
        pass

    def test_003_choose_specific_meeting_in_the_all_meetings_dropdown_and_clicktap_find_bets(self):
        """
        DESCRIPTION: Choose specific meeting in the 'All Meetings' dropdown and click/tap 'Find Bets'
        EXPECTED: '/bet-finder/results' page is opened with infinite spinner being shown at the top
        EXPECTED: 'Breakpoint' is shown within the **Charles** application
        EXPECTED: ![](index.php?/attachments/get/66425166)
        """
        pass

    def test_004_while_the_breakpoint_with_a_response_is_shown_in_charles_select_edit_response___json_text__remove_the_value_shown_within_double_quotes_for_one_of_the_odds_parameters_and_click_execute_buttonindexphpattachmentsget66425168indexphpattachmentsget66425169indexphpattachmentsget66425170(self):
        """
        DESCRIPTION: While the Breakpoint with a response is shown in Charles, select 'Edit Response' -> 'JSON Text',  remove the value shown within double quotes for one of the "odds" parameters and click 'Execute' button
        DESCRIPTION: ![](index.php?/attachments/get/66425168)
        DESCRIPTION: ![](index.php?/attachments/get/66425169)
        DESCRIPTION: ![](index.php?/attachments/get/66425170)
        EXPECTED: '/bet-finder/results' page is shown with the list of results
        EXPECTED: Race card of the edited runner contains 'SP' selection/button
        """
        pass

    def test_005_tap_on_the_sp_selection_of_the_edited_odds_valueindexphpattachmentsget66425171(self):
        """
        DESCRIPTION: Tap on the 'SP' selection of the edited 'odds' value
        DESCRIPTION: ![](index.php?/attachments/get/66425171)
        EXPECTED: QuickBet is summoned
        EXPECTED: QuickBet contains bet with the 'SP' odds value
        EXPECTED: ![](index.php?/attachments/get/66425176)
        EXPECTED: 'Potential Returns' value is calculated as 'N/A'
        EXPECTED: ![](index.php?/attachments/get/66425177)
        EXPECTED: (!) Note - if selection contains both SP and LP values, when user taps on the SP selection, added into QuickBet(BetSlip) value will be shown with a dropdown, containing both LP and SP, with LP selected by default.
        """
        pass

    def test_006_enter_the_stake_into_a_stake_field_and_tap_login__place_bet(self):
        """
        DESCRIPTION: Enter the stake into a 'Stake' field and tap 'Login & Place Bet'
        EXPECTED: 'Login/Register' modal window interface is summoned
        """
        pass

    def test_007_login_into_the_app_through_loginregister_modal_window_interface(self):
        """
        DESCRIPTION: Login into the app through 'Login/Register' modal window interface
        EXPECTED: Bet is successfully placed on the 'SP' odds value"
        EXPECTED: 'Potential Returns' value remains as 'N/A'
        EXPECTED: ![](index.php?/attachments/get/66425178)
        """
        pass

    def test_008_close_the_bet_receipt_and_open_my_account___settings_changing_following_valuesquickbet___offdecimal___checked(self):
        """
        DESCRIPTION: Close the 'Bet Receipt' and open 'My Account' -> 'Settings', changing following values:
        DESCRIPTION: QuickBet -> 'Off'
        DESCRIPTION: Decimal -> 'Checked'
        EXPECTED: Changes are applied as soon as user provides them
        EXPECTED: Changes made in 'Settings' are stored in: Dev Tools -> Application -> Local Storage -> '#environment_address' -> 'OX.USER'
        EXPECTED: ![](index.php?/attachments/get/66425172)
        EXPECTED: ![](index.php?/attachments/get/66425173)
        """
        pass

    def test_009_log_out_of_the_oxygen_app(self):
        """
        DESCRIPTION: Log out of the oxygen app
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_1_7(self):
        """
        DESCRIPTION: Repeat steps 1-7
        EXPECTED: Selection is added into Betslip on Step 5 (**Betslip needs to be opened manually**)
        EXPECTED: Betslip contains bet with the 'SP' odds value
        EXPECTED: ![](index.php?/attachments/get/66425180)
        EXPECTED: 'Potential Returns' and 'Total Potential Returns' values are calculated and remain as 'N/A' event after bet placement
        EXPECTED: ![](index.php?/attachments/get/66425181)
        """
        pass
