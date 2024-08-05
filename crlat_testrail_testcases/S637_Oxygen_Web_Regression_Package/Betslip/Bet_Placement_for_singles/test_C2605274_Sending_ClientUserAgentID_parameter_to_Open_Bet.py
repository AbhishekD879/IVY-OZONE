import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C2605274_Sending_ClientUserAgentID_parameter_to_Open_Bet(Common):
    """
    TR_ID: C2605274
    NAME: Sending 'ClientUserAgentID' parameter to Open Bet
    DESCRIPTION: This test case verifies sending 'ClientUserAgentID' parameter to Open Bet
    PRECONDITIONS: 1. The user is logged in and has a positive balance
    PRECONDITIONS: 2. To check request/response open Dev tools -> Network tab -> XHR/WS sorting filter
    """
    keep_browser_open = True

    def test_001_load_android_html5_web(self):
        """
        DESCRIPTION: Load Android html5 web
        EXPECTED: 
        """
        pass

    def test_002_place_bet_via__betslip_single_multiple_forecaststricasts__quick_bet__lotto_betslip__football_jackpot__tote_betslip(self):
        """
        DESCRIPTION: Place bet via:
        DESCRIPTION: - Betslip, Single; Multiple; Forecasts/Tricasts
        DESCRIPTION: - Quick Bet
        DESCRIPTION: - Lotto betslip
        DESCRIPTION: - Football Jackpot
        DESCRIPTION: - Tote betslip
        EXPECTED: * **clientUserAgent = S|H|A0000000** parameter is sent to OB in placeBet request in XHR
        EXPECTED: ![](index.php?/attachments/get/24663)
        EXPECTED: * **clientUserAgent = S|H|A0000000** parameter is sent to OB via **Remote Betslip MS** in 30011 request in WS
        EXPECTED: ![](index.php?/attachments/get/24664)
        """
        pass

    def test_003_load_ios_html5_web(self):
        """
        DESCRIPTION: Load iOS html5 web
        EXPECTED: 
        """
        pass

    def test_004_place_bet_via__betslip_single_multiple_forecaststricasts__quick_bet__lotto_betslip__football_jackpot__tote_betslip(self):
        """
        DESCRIPTION: Place bet via:
        DESCRIPTION: - Betslip, Single; Multiple; Forecasts/Tricasts
        DESCRIPTION: - Quick Bet
        DESCRIPTION: - Lotto betslip
        DESCRIPTION: - Football Jackpot
        DESCRIPTION: - Tote betslip
        EXPECTED: * **clientUserAgent = S|H|I0000000** parameter is sent to OB in placeBet request in XHR
        EXPECTED: ![](index.php?/attachments/get/24666)
        EXPECTED: * **clientUserAgent = S|H|I0000000** parameter is sent to OB via **Remote Betslip MS** in 30011 request in WS
        EXPECTED: ![](index.php?/attachments/get/24665)
        """
        pass

    def test_005_load_android_wrapper(self):
        """
        DESCRIPTION: Load Android wrapper
        EXPECTED: 
        """
        pass

    def test_006_place_bet_via__betslip__quick_bet__stream__bet__lotto_betslip__football_jackpot__tote_betslip(self):
        """
        DESCRIPTION: Place bet via:
        DESCRIPTION: - Betslip
        DESCRIPTION: - Quick Bet
        DESCRIPTION: - Stream & Bet
        DESCRIPTION: - Lotto betslip
        DESCRIPTION: - Football Jackpot
        DESCRIPTION: - Tote betslip
        EXPECTED: * **clientUserAgent = S|W|A0000000** parameter is sent to OB
        EXPECTED: ![](index.php?/attachments/get/25201)
        """
        pass

    def test_007_load_ios_wrapper(self):
        """
        DESCRIPTION: Load iOS wrapper
        EXPECTED: 
        """
        pass

    def test_008_place_bet_via__betslip__quick_bet__stream__bet__lotto_betslip__football_jackpot__tote_betslip(self):
        """
        DESCRIPTION: Place bet via:
        DESCRIPTION: - Betslip
        DESCRIPTION: - Quick Bet
        DESCRIPTION: - Stream & Bet
        DESCRIPTION: - Lotto betslip
        DESCRIPTION: - Football Jackpot
        DESCRIPTION: - Tote betslip
        EXPECTED: * **clientUserAgent = S|W|I0000000** parameter is sent to OB
        EXPECTED: ![](index.php?/attachments/get/25200)
        """
        pass

    def test_009_load_desktop_windows(self):
        """
        DESCRIPTION: Load Desktop Windows
        EXPECTED: 
        """
        pass

    def test_010_place_bet_via__betslip_single_multiple_forecaststricasts__football_jackpot__tote_betslip(self):
        """
        DESCRIPTION: Place bet via:
        DESCRIPTION: - Betslip, Single; Multiple; Forecasts/Tricasts
        DESCRIPTION: - Football Jackpot
        DESCRIPTION: - Tote betslip
        EXPECTED: * **clientUserAgent = S|H|W0000000** parameter is sent to OB in placeBet request in XHR
        """
        pass

    def test_011_place_bet_via__lotto_betslip(self):
        """
        DESCRIPTION: Place bet via:
        DESCRIPTION: - Lotto betslip
        EXPECTED: * **clientUserAgent = Y|H|W0000000** parameter is sent to OB in placeBet request in XHR
        """
        pass

    def test_012_place_bet_on_any__virtual_sport_selectionby_using_betslip(self):
        """
        DESCRIPTION: Place bet on any
        DESCRIPTION: - Virtual Sport selection
        DESCRIPTION: by using Betslip
        EXPECTED: * **clientUserAgent = R|H|W0000000** parameter is sent to OB in placeBet request in XHR
        """
        pass

    def test_013_load_desktop_mac_os_x(self):
        """
        DESCRIPTION: Load Desktop Mac OS X
        EXPECTED: 
        """
        pass

    def test_014_place_bet_via__betslipsingle_multiple_forecaststricasts__lotto_betslip__football_jackpot__tote_betslip(self):
        """
        DESCRIPTION: Place bet via:
        DESCRIPTION: - Betslip,Single; Multiple; Forecasts/Tricasts
        DESCRIPTION: - Lotto betslip
        DESCRIPTION: - Football Jackpot
        DESCRIPTION: - Tote betslip
        EXPECTED: * **clientUserAgent = S|H|O0000000** parameter is sent to OB in placeBet request in XHR
        """
        pass

    def test_015_place_bet_via__lotto_betslip(self):
        """
        DESCRIPTION: Place bet via:
        DESCRIPTION: - Lotto betslip
        EXPECTED: * **clientUserAgent = Y|H|O0000000** parameter is sent to OB in placeBet request in XHR
        """
        pass

    def test_016_place_bet_on_any__virtual_sport_selectionby_using_betslip(self):
        """
        DESCRIPTION: Place bet on any
        DESCRIPTION: - Virtual Sport selection
        DESCRIPTION: by using Betslip
        EXPECTED: * **clientUserAgent = R|H|O0000000** parameter is sent to OB in placeBet request in XHR
        """
        pass
