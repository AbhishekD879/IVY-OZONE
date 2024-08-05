import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.cash_out
@vtest
class Test_C8212243_Verify_Cash_Out_MS_availability_for_platforms_which_do_not_support_SSE(Common):
    """
    TR_ID: C8212243
    NAME: Verify Cash Out MS availability for platforms which do not support SSE
    DESCRIPTION: This test case verifies Cash Out MS availability on different platforms and devices that do not support Server-sent events
    DESCRIPTION: technology
    DESCRIPTION: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    DESCRIPTION: - WS connection to Cashout MS is created when user lands on myBets page
    PRECONDITIONS: In CMS
    PRECONDITIONS: * Load CMS and log in
    PRECONDITIONS: * Go to System Configuration section
    PRECONDITIONS: * Switch on and save 'isV4Enabled' checkbox
    PRECONDITIONS: NB! CMS config will be removed when [BMA-55051 [OxygenUI] Remove support of old cashout flow][1] is released
    PRECONDITIONS: [1]:https://jira.egalacoral.com/browse/BMA-55051
    PRECONDITIONS: In Oxygen app
    PRECONDITIONS: *  User should be logged in
    PRECONDITIONS: *  User should have bets with CashOut option available (at least 2 bets with enabled cash out should be placed)
    PRECONDITIONS: *  Open Dev Tools -> Network AND Console tabs -> XHR filter and console
    PRECONDITIONS: Endpoints to CashOut MS
    PRECONDITIONS: * https://cashout-dev1.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev1
    PRECONDITIONS: * https://cashout-dev0.coralsports.dev.cloud.ladbrokescoral.com/bet-details?token={token} - dev0
    PRECONDITIONS: List of platforms that support Server-sent events
    PRECONDITIONS: * https://caniuse.com/#search=server%20sent%20event
    """
    keep_browser_open = True

    def test_001_load_app_on_ms_edge_desktop_and_type_windoweventsource_in_console(self):
        """
        DESCRIPTION: Load app on MS Edge Desktop and type **!!window.EventSource** in console
        EXPECTED: * App is loaded
        EXPECTED: * **!!window.EventSource = false** is returned in console
        """
        pass

    def test_002_go_to_cash_out_page_or_cash_out_widget(self):
        """
        DESCRIPTION: Go to Cash Out page OR Cash Out widget
        EXPECTED: * GET **getBetDetails** request is sent to bpp to retrieve all cashout bets
        EXPECTED: * No GET bet-details request is sent to Cash Out MS
        """
        pass

    def test_003_trigger_any_update_in_openbet_ti_tool_eg_price_changesuspensionunsuspenstion(self):
        """
        DESCRIPTION: Trigger any update in Openbet TI tool e.g. price change/suspension/unsuspenstion
        EXPECTED: * Updates are reflected on Cash out page
        EXPECTED: * **getBetDetail** request is sent for any update
        """
        pass

    def test_004_try_to_make_full_partial_cash_out(self):
        """
        DESCRIPTION: Try to make full/ partial cash out
        EXPECTED: * Full/ partial cash out is successful
        """
        pass

    def test_005_go_to_edp_event_above_where_bets_with_cash_out_options_are_present(self):
        """
        DESCRIPTION: Go to EDP (event above) where bets with Cash Out options are present
        EXPECTED: The next requests are sent to bpp:
        EXPECTED: * GET **getBetDetails** request is sent to BPP to retrieve all cashout bets
        EXPECTED: * GET **getBetsPlaced** request is sent to BPP to retrieve all placed bets
        EXPECTED: * GET **getBetDetails** request is sent to BPP to retrieve all bets for current event by betID
        EXPECTED: * No GET **bet-details** request is sent to Cash Out MS
        """
        pass

    def test_006_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps #3-4
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_1_6_for_at_list_for_the_next_platforms_ie11_android_device_43_version(self):
        """
        DESCRIPTION: Repeat steps #1-6 for at list for the next platforms:
        DESCRIPTION: * IE11
        DESCRIPTION: * Android device 4.3 version
        EXPECTED: 
        """
        pass
