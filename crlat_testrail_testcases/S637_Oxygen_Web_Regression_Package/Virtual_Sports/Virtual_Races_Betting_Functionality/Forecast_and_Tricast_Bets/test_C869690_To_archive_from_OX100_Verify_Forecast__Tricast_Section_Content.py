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
class Test_C869690_To_archive_from_OX100_Verify_Forecast__Tricast_Section_Content(Common):
    """
    TR_ID: C869690
    NAME: [To archive from OX100] Verify 'Forecast' / 'Tricast' Section Content
    DESCRIPTION: This test case verifies the content within 'Forecast'/'Tricast' section for
    DESCRIPTION: *   Virtual Motorsports (Class ID 288)
    DESCRIPTION: *   Virtual Cycling (Class ID 290)
    DESCRIPTION: *   Virtul Horse Racing (Class ID 285)
    DESCRIPTION: *   Virtual Greyhound Racing (Class ID 286)
    DESCRIPTION: *   Virtual Grand National (Class ID 26604)
    DESCRIPTION: **JIRA Tickets** :
    DESCRIPTION: *   [BMA-9397 ('Extend Forecast and Tricast betting to Virtual Sports')][1]
    DESCRIPTION: *   [BMA-12165 (Betslip - Implement selection order for Forecast and Tricast bets (1st, 2nd, 3rd))][2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-9397
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-12165
    PRECONDITIONS: 1. To get event information use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/<event_id>?racingForm=outcome&translationLang=LL
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. User should be logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_go_to_virtual_sports(self):
        """
        DESCRIPTION: Load Oxygen and go to "Virtual Sports"
        EXPECTED: Virtual Horse Racing page is opened by default
        EXPECTED: Next event is shown
        """
        pass

    def test_002_add_two_or_three_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two or three selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_003_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: Bet Slip is opened
        EXPECTED: Added selections are shown
        """
        pass

    def test_004_verify_forecast__tricasts_section(self):
        """
        DESCRIPTION: Verify 'Forecast' / 'Tricasts' section
        EXPECTED: 'Forecast / Tricasts' section is shown below the 'Singles' options
        EXPECTED: Section is expanded by default
        EXPECTED: Section is collapsiable/expandible
        EXPECTED: Section header is** 'Forecast / Tricasts (n)'**
        EXPECTED: where n - the number of Forecast / Tricast bets
        """
        pass

    def test_005_verify_forecast__tricast_section_content(self):
        """
        DESCRIPTION: Verify 'Forecast' / 'Tricast' section content
        EXPECTED: 'Forecast' / 'Tricast' section consists of:
        EXPECTED: *   Event details
        EXPECTED: *   Field **'Selections:' **with selections details
        EXPECTED: *   **'Forecast (k) / Tricast (k)' **section
        EXPECTED: *   **'Reverse Forecast (k) ', 'Combination Tricast (k)', 'Combination Forecast (k)'** sections - depending on quantity of added selections
        EXPECTED: *   **'Stake:'** fields for each section
        EXPECTED: where  k - the number of combinations/outcomes contained in the forecast / tricast bet
        """
        pass

    def test_006_verify_event_details(self):
        """
        DESCRIPTION: Verify event details
        EXPECTED: Event name is shown
        EXPECTED: Event name corresponds to the** 'name' **attribute on event level
        """
        pass

    def test_007_verify_selections_details(self):
        """
        DESCRIPTION: Verify '**Selections:**' details
        EXPECTED: *   Selection order number, runner number and selection name are shown for each selection
        EXPECTED: *   Selection names correspond to the** 'name'** attribute on outcome level
        EXPECTED: *   Selection numbers correspond to the** 'draw' **attribute
        EXPECTED: *   Selections are shown in the order as they were added to the Bet Slip
        EXPECTED: NOTE: selection order number is not shown for Combination Tricast/Forecast
        """
        pass

    def test_008_verify_fieldsforecast_ktricast_kreverse_forecast_k_combination_tricast_kcombination_forecast_k(self):
        """
        DESCRIPTION: Verify fields:
        DESCRIPTION: **'Forecast (k)'**
        DESCRIPTION: **'Tricast (k)'*
        DESCRIPTION: '**Reverse Forecast (k) **'
        DESCRIPTION: '**Combination Tricast (k)**'
        DESCRIPTION: '**Combination Forecast (k)**'
        EXPECTED: Sections appearance depends on number of added selections
        EXPECTED: 'Stake:' field is shown below the each section header
        EXPECTED: Free bet drop down is shown under the 'Stake:' field if free bets are available
        """
        pass

    def test_009_verify_the_fields_displaying(self):
        """
        DESCRIPTION: Verify the fields displaying
        EXPECTED: Fields are displayed according to the latest designs
        """
        pass

    def test_010_repeat_this_test_case_for_all_virtual_races_horse_racing_class_id_285_greyhounds_class_id_286_motorsports_class_id_288_cycling_class_id_290_grand_national_class_id_26604(self):
        """
        DESCRIPTION: Repeat this test case for all virtual races:
        DESCRIPTION: * Horse Racing class id 285
        DESCRIPTION: * Greyhounds class id 286
        DESCRIPTION: * Motorsports class id 288
        DESCRIPTION: * Cycling class id 290
        DESCRIPTION: * Grand National class id 26604
        EXPECTED: 
        """
        pass
