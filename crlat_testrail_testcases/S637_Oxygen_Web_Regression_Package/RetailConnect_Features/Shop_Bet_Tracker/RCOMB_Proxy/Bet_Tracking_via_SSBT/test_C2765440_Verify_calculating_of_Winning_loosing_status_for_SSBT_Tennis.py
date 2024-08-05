import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2765440_Verify_calculating_of_Winning_loosing_status_for_SSBT_Tennis(Common):
    """
    TR_ID: C2765440
    NAME: Verify calculating of Winning/loosing status for SSBT Tennis
    DESCRIPTION: This test case verify calculating of Winning/loosing status for SSBT Tennis
    DESCRIPTION: Winning/loosing is set into parameter 'progress'
    DESCRIPTION: RCOMB PROXY calculates it only when event is in play and when DX API returns  'unset' or 'pending' in <result> node
    DESCRIPTION: once event is finished value for 'progress' parameter is taken from DX API
    DESCRIPTION: To get data from DX API use postman collection [DX (SSBT)](https://confluence.egalacoral.com/download/attachments/53838690/DX%20%28SSBT%29.postman_collection.json?version=1&modificationDate=1524665494000&api=v2)
    PRECONDITIONS: Request creation of SSBT barcodes for Tennis sport
    PRECONDITIONS: bets should be placed on following markets
    PRECONDITIONS: * Handicap Market (Total Games) (also allowed the following differences in market name: 'Handicap')
    PRECONDITIONS: * Match Winner/ Full Time Result (also allowed the following differences in market name: 'Match Winner'; 'Full Time Result')
    PRECONDITIONS: * Total Games Over/Under
    PRECONDITIONS: * Total Games Over/Under - 1st set (also allowed the following differences in market name: '1st Set - Total Games Over/Under')
    PRECONDITIONS: * Total Games Over/Under - 2st set (also allowed the following differences in market name: '2st Set - Total Games Over/Under')
    PRECONDITIONS: * 1st Set - Winner (also allowed the following differences in market name: 'Set Winner  => Set 1')
    PRECONDITIONS: * 2th Set - Winner (also allowed the following differences in market name: 'Set Winner  => Set 2')
    PRECONDITIONS: * Set Winner (while requesting you need to specify to what set this bet is related so request for 1th and 2th sets)
    PRECONDITIONS: P.S.:
    PRECONDITIONS: Winning/ lousing status for following markets is calculated in the same way:
    PRECONDITIONS: * Set Winne
    PRECONDITIONS: * 1st Set - Winner
    PRECONDITIONS: * 2th Set - Winner
    PRECONDITIONS: the only difference:
    PRECONDITIONS: for last 2 markets we know set number from market's name
    PRECONDITIONS: for first market to find out set number we need to check response from DX Api: run GetBetSlip in the Postman and find value of tag <marketTags>
    """
    keep_browser_open = True

    def test_001__run_rcombv3barcodehttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbetsbyslipandbarcodeandepos2usingget_use_barcode_with_in_play_tennis_event_as_parameter_barcode_should_contain_bet_placed_on_the_market_handicap_market_total_games(self):
        """
        DESCRIPTION: * Run [/rcomb/v3/barcode](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodeAndEpos2UsingGET)
        DESCRIPTION: * use barcode with in-play tennis event as parameter
        DESCRIPTION: * barcode should contain bet placed on the market **'Handicap Market (Total Games)'**
        EXPECTED: * Barcodes data are retrieved correctly
        """
        pass

    def test_002__verify_progress_value_during_1th_and_2th_sets(self):
        """
        DESCRIPTION: * Verify 'progress' value during 1th and 2th sets
        EXPECTED: * If the selection is 'Team A+5.5' then 'progress' is calculated in following way:
        EXPECTED: If   (total Games Scores of all sets of Team A + 5.5) > total Games Scores of all sets of Team B
        EXPECTED: {its Winning }
        EXPECTED: else
        EXPECTED: {its losing}
        EXPECTED: *   If the selection is 'Team A -5.5' then 'progress' is calculated in following way:
        EXPECTED: If     (total Games Scores of all sets of Team A - 5.5) > total Games Scores of all sets of Team B
        EXPECTED: {its Winning }
        EXPECTED: else
        EXPECTED: {its losing}
        EXPECTED: * If the selection is 'Team B +5.5  ' then 'progress' is calculated in following way:
        EXPECTED: If    (total Games Scores of all sets of Team B + 5.5) > total Games Scores of all sets of Team A
        EXPECTED: {its Winning }
        EXPECTED: else
        EXPECTED: {its losing}
        """
        pass

    def test_003__run_rcombv3barcodehttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbetsbyslipandbarcodeandepos2usingget_use_barcode_with_in_play_tennis_event_as_parameter_barcode_should_contain_bet_placed_on_the_market_match_winner__full_time_result(self):
        """
        DESCRIPTION: * Run [/rcomb/v3/barcode](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodeAndEpos2UsingGET)
        DESCRIPTION: * use barcode with in-play tennis event as parameter
        DESCRIPTION: * barcode should contain bet placed on the market **'Match Winner / Full Time Result'**
        EXPECTED: * Barcodes data are retrieved correctly
        """
        pass

    def test_004__verify_progress_value_during_1th_and_2th_sets(self):
        """
        DESCRIPTION: * Verify 'progress' value during 1th and 2th sets
        EXPECTED: * If the selection is 'Team A' then 'progress' is calculated in following way:
        EXPECTED: if (Team A set score > Team B set score ) {
        EXPECTED: its Winning
        EXPECTED: } else if (Team A set score == Team B set score ) {
        EXPECTED: If (Team A Game Score > Team B Game Score )   {
        EXPECTED: its Winning
        EXPECTED: } else if (Team A Game Score == Team B Game Score ) {
        EXPECTED: if (Team A Point Score > Team B Point Score )   {
        EXPECTED: its Winning      	    } else {
        EXPECTED: its losing
        EXPECTED: }
        EXPECTED: } else {
        EXPECTED: its losing
        EXPECTED: }
        EXPECTED: } else {
        EXPECTED: its losing
        EXPECTED: }
        """
        pass

    def test_005__run_rcombv3barcodehttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbetsbyslipandbarcodeandepos2usingget_use_barcode_with_in_play_tennis_event_as_parameter_barcode_should_contain_bet_placed_on_the_market_total_games_overunder(self):
        """
        DESCRIPTION: * Run [/rcomb/v3/barcode](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodeAndEpos2UsingGET)
        DESCRIPTION: * use barcode with in-play tennis event as parameter
        DESCRIPTION: * barcode should contain bet placed on the market **'Total Games Over/Under'**
        EXPECTED: * Barcodes data are retrieved correctly
        """
        pass

    def test_006__verify_progress_value_during_1th_and_2th_sets(self):
        """
        DESCRIPTION: * Verify 'progress' value during 1th and 2th sets
        EXPECTED: If the Selections are
        EXPECTED: * Over 21.5
        EXPECTED: If  (Total Games Score of all sets of Team A and Team B) >   21.5 {
        EXPECTED: its Winning } else {
        EXPECTED: its losing
        EXPECTED: }
        EXPECTED: * Under 21.5
        EXPECTED: If (Total Games Score of all sets of Team A and Team B) <   21.5 {
        EXPECTED: its Winning } else {
        EXPECTED: its losing
        EXPECTED: }
        """
        pass

    def test_007__run_rcombv3barcodehttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbetsbyslipandbarcodeandepos2usingget_use_barcode_with_in_play_tennis_event_as_parameter_barcode_should_contain_bet_placed_on_the_market_total_games_overunder___1st_set(self):
        """
        DESCRIPTION: * Run [/rcomb/v3/barcode](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodeAndEpos2UsingGET)
        DESCRIPTION: * use barcode with in-play tennis event as parameter
        DESCRIPTION: * barcode should contain bet placed on the market **'Total Games Over/Under - 1st set'**
        EXPECTED: * Barcodes data are retrieved correctly
        """
        pass

    def test_008__verify_progress_value_during_1th_and_2th_sets(self):
        """
        DESCRIPTION: * Verify 'progress' value during 1th and 2th sets
        EXPECTED: If the Selections are
        EXPECTED: * Over 6.5
        EXPECTED: If (Total Games Score of 1st Set of Team A and Team B) >   6.5  {
        EXPECTED: its Winning } else {
        EXPECTED: its losing
        EXPECTED: }
        EXPECTED: * Under 6.5
        EXPECTED: If (Total Games Score of 1st Set of Team A and Team B) <   6.5 {
        EXPECTED: its Winning } else {
        EXPECTED: its losing
        EXPECTED: }
        """
        pass

    def test_009__run_rcombv3barcodehttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbetsbyslipandbarcodeandepos2usingget_use_barcode_with_in_play_tennis_event_as_parameter_barcode_should_contain_bet_placed_on_the_market_total_games_overunder___2st_set(self):
        """
        DESCRIPTION: * Run [/rcomb/v3/barcode](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodeAndEpos2UsingGET)
        DESCRIPTION: * use barcode with in-play tennis event as parameter
        DESCRIPTION: * barcode should contain bet placed on the market **'Total Games Over/Under - 2st set'**
        EXPECTED: * Barcodes data are retrieved correctly
        """
        pass

    def test_010__verify_progress_value_during_1th_and_2th_sets(self):
        """
        DESCRIPTION: * Verify 'progress' value during 1th and 2th sets
        EXPECTED: If the Selections are
        EXPECTED: * Over 6.5
        EXPECTED: If  (Total Games Score of 2nd Set of Team A and Team B) >   6.5  {
        EXPECTED: its Winning } else {
        EXPECTED: its losing
        EXPECTED: }
        EXPECTED: * Under 6.5
        EXPECTED: If (Total Games Score of 2nd Set of Team A and Team B) <   6.5 {
        EXPECTED: its Winning } else {
        EXPECTED: its losing
        EXPECTED: }
        """
        pass

    def test_011__run_rcombv3barcodehttpscoral_retail_bpp_devsymphony_solutionseuswagger_uihtmlrcomb_endpointsgetbetsbyslipandbarcodeandepos2usingget_use_barcode_with_in_play_tennis_event_as_parameter_barcode_should_contain_bet_placed_on_the_market_set_winner(self):
        """
        DESCRIPTION: * Run [/rcomb/v3/barcode](https://coral-retail-bpp-dev.symphony-solutions.eu/swagger-ui.html#!/rcomb_endpoints/getBetsBySlipAndBarcodeAndEpos2UsingGET)
        DESCRIPTION: * use barcode with in-play tennis event as parameter
        DESCRIPTION: * barcode should contain bet placed on the market **'Set Winner'**
        EXPECTED: * Barcodes data are retrieved correctly
        """
        pass

    def test_012__verify_progress_value_during_1th_and_2th_sets(self):
        """
        DESCRIPTION: * Verify 'progress' value during 1th and 2th sets
        EXPECTED: * Set Winner  => Set 1
        EXPECTED: Team A Vs Team B
        EXPECTED: If selection is Team A:
        EXPECTED: if (Team A Game Score of 1st set > Team B Game Score  of 1st set)  {
        EXPECTED: its Winning } else {
        EXPECTED: its losing
        EXPECTED: }
        EXPECTED: * Set Winner  => Set 2
        EXPECTED: If selection is Team A:
        EXPECTED: if (Team A Game Score  of 2nd set > Team B Game Score  of 2nd set)  {
        EXPECTED: its Winning } else {
        EXPECTED: its losing
        EXPECTED: }
        """
        pass
