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
class Test_C10436245_Ladbrokes_Verify_detailed_information_for_each_selection_on_the_Race_Card_EDP(Common):
    """
    TR_ID: C10436245
    NAME: [Ladbrokes] Verify detailed information for each selection on the Race Card (EDP)
    DESCRIPTION: This test case verifies 'SHOW MORE'/'SHOW LESS' button and info that it expands for each selection on the Race Card (EDP)
    DESCRIPTION: AUTOTEST
    DESCRIPTION: MOBILE: [C24228656]
    DESCRIPTION: DESKTOP: [C24354463]
    PRECONDITIONS: * Event(s) with Racing Post data are available
    PRECONDITIONS: * A user is on a Race Card (Event Details page) of an event with available Racing Post
    PRECONDITIONS: NOTE
    PRECONDITIONS: * Racing Post information is present in a response from DF API https://raceinfo-api.ladbrokes.com/race_info/ladbrokes/[eventID]
    PRECONDITIONS: * Racing Post information or it’s parts for the specific event can be absent so it will be absent in the UI as well
    """
    keep_browser_open = True

    def test_001_verify_the_show_more__button_is_present_after_form_value_text_for_the_specific_horse(self):
        """
        DESCRIPTION: Verify the 'SHOW MORE ⋁' button is present after 'Form: [value]' text for the specific horse
        EXPECTED: * The blue 'SHOW MORE ⋁' button is displayed
        EXPECTED: * No more text below 'SHOW MORE ⋁' button for the horse
        """
        pass

    def test_002_tap_show_more__button(self):
        """
        DESCRIPTION: Tap 'SHOW MORE ⋁' button
        EXPECTED: * The 'SHOW MORE ⋁' button is changed to 'SHOW LESS ⋀'
        EXPECTED: * The further information from Racing Post is displayed:
        EXPECTED: **Mobile**
        EXPECTED: - Runner Age
        EXPECTED: - Runner Weight
        EXPECTED: - RPR
        EXPECTED: - Runner Comment
        EXPECTED: - CD/C/BF (if a course winner and/or if a beaten favorite)
        EXPECTED: - Star Rating
        EXPECTED: **Desktop**
        EXPECTED: - Runner Age
        EXPECTED: - Runner Weight
        EXPECTED: - RPR
        EXPECTED: - Runner Comment
        EXPECTED: - CD/C/BF (if a course winner and/or if a beaten favorite)
        EXPECTED: - Star Rating (aligned to the rigth)
        EXPECTED: - Detailed Form
        """
        pass

    def test_003_verify_runner_age(self):
        """
        DESCRIPTION: Verify Runner Age
        EXPECTED: Runner Age = 'horseAge' attribute from Racing Post response
        """
        pass

    def test_004_verify_runner_weight(self):
        """
        DESCRIPTION: Verify Runner Weight
        EXPECTED: Runner Weight = 'weight' attribute from Racing Post response
        """
        pass

    def test_005_verify_rpr(self):
        """
        DESCRIPTION: Verify RPR
        EXPECTED: PRP = 'rating' attribute from the Racing Post response
        """
        pass

    def test_006_verify_runner_comment(self):
        """
        DESCRIPTION: Verify Runner Comment
        EXPECTED: Runner Comment = 'spotlight' attribute from the Racing Post response
        """
        pass

    def test_007_verify_cdcbf(self):
        """
        DESCRIPTION: Verify CD/C/BF
        EXPECTED: CD/C/BF = 'courseDistanceWinner' attribute from the Racing Post response
        """
        pass

    def test_008_verify_star_rating(self):
        """
        DESCRIPTION: Verify Star Rating
        EXPECTED: Star Rating = 'starRating' attribute from the Racing Post response
        """
        pass

    def test_009_verify_detailed_form(self):
        """
        DESCRIPTION: Verify Detailed Form
        EXPECTED: * Information in the table view
        EXPECTED: * Detailed Form = 'formfigs' array from the Racing Post response
        """
        pass

    def test_010_tap_show_less__button(self):
        """
        DESCRIPTION: Tap 'SHOW LESS ⋀' button
        EXPECTED: * The blue 'SHOW MORE ⋁' button is displayed
        EXPECTED: * No more text below 'SHOW MORE ⋁' button for the horse
        """
        pass
