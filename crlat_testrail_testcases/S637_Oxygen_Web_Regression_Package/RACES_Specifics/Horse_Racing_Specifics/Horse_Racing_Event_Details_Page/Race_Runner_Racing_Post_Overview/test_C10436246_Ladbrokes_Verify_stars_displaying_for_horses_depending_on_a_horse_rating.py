import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C10436246_Ladbrokes_Verify_stars_displaying_for_horses_depending_on_a_horse_rating(Common):
    """
    TR_ID: C10436246
    NAME: [Ladbrokes] Verify stars displaying for horses depending on a horse rating
    DESCRIPTION: This test case verifies displaying of rating for horses with a 5-star rating and with less than 5-star rating
    DESCRIPTION: AUTOTEST ID'S
    DESCRIPTION: MOBILE :[C17772088]
    DESCRIPTION: DESKTOP: [C21806707]
    PRECONDITIONS: * Event(s) with Racing Post data are available
    PRECONDITIONS: * A user is on a Race Card (Event Details page) of an event with available Racing Post
    PRECONDITIONS: NOTE
    PRECONDITIONS: * Racing Post information is present in a response from Racing Post API https://raceinfo-api.ladbrokes.com/race_info/ladbrokes/[eventID]
    PRECONDITIONS: * Racing Post information or it’s parts for the specific event can be absent so it will be absent in the UI as well
    """
    keep_browser_open = True

    def test_001_verify_displaying_stars_for_horses_selections_with_a_5_star_rating(self):
        """
        DESCRIPTION: Verify displaying stars for horses (selections) with a 5-star rating
        EXPECTED: * The number of stars is equal to the star rating retrieved from 'Racing Post' response
        EXPECTED: * There is a '★5' in a rectangle sign next to selection name
        EXPECTED: * Stars correspond to "StarRating" attribute from 'Racing Post' response
        """
        pass

    def test_002__tap_show_more_button_verify_stars_for_horses_selections_with_a_5_star_rating(self):
        """
        DESCRIPTION: * Tap 'SHOW MORE' button
        DESCRIPTION: * Verify stars for horses (selections) with a 5-star rating
        EXPECTED: * 5 yellow stars are displayed below 'Odds' button, on the same level as Age, Weight, RPR CD/C/BF info
        """
        pass

    def test_003__verify_displaying_stars_for_horses_with_less_than_a_5_star_rating(self):
        """
        DESCRIPTION: * Verify displaying stars for horses with less than a 5-star rating
        EXPECTED: * Stars are displayed below 'Odds' button, on the same level as Age, Weight, RPR CD/C/BF info
        EXPECTED: * 5 stars are displayed for all horses (selections).
        EXPECTED: * The yellow stars show the rating of the horse
        EXPECTED: * Yellow stars correspond to "StarRating" attribute from 'Racing Post' response
        """
        pass
