import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from voltron.utils.datafabric.datafabric import Datafabric
from voltron.utils.exceptions.general_exception import GeneralException


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2  # Coral only as race_form_info not available for Ladbrokes right now
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.race_form
@pytest.mark.races
@pytest.mark.safari
@pytest.mark.medium
@vtest
# TODO: "race_form_info" is not available in Ladbrokes right now. Test should be verified in ladbrokes once it is
#  available.
class Test_C1274037_Verify_Race_Distance(BaseRacing):
    """
    TR_ID: C1274037
    NAME: Verify Race Distance
    DESCRIPTION: This test case verifies Race Distance of individual race event on Event Details Page
    PRECONDITIONS: **JIRA Ticket **: BMA-6587 'Racecard Layout Update - Race Information'
    PRECONDITIONS: 1) To get an info about race distance of event use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?racingForm=event&translationLang=LL
    PRECONDITIONS: Where,
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   *ZZZZ - an event id*
    PRECONDITIONS: *   *LL - language (e.g. en, ukr) *
    PRECONDITIONS: See attribute **distance="Yards,YYY,"**, where YYY - is distance always in yards, to see whether distance is available for selected event
    PRECONDITIONS: 2) To convert yards into miles, furlongs and yards please do the following:
    PRECONDITIONS: *   A = 'distance'/1760 - whole number is **number of miles**
    PRECONDITIONS: *   B = 'distance' - A*1760
    PRECONDITIONS: *   C = B/220 - whole number is **number of furlongs**
    PRECONDITIONS: *   D = B - C*220 - **number of yards**
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find Racing event with form info in SiteServe response
        """
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
        event_params = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                           additional_filters=cashout_filter,
                                                           number_of_events=1)[0]
        self.__class__.eventID = event_params['event']['id']

        data = Datafabric().get_datafabric_data(event_id=self.eventID, category_id=21, raise_exceptions=False)
        if data["Error"]:
            raise GeneralException('No event with racing information found. '
                                   'Can be due to receiving 404 error from datafabric.')
        datafabric_data = data['document'][self.eventID]
        self.__class__.distance = datafabric_data.get('distance', False)

        event_params_no_distance = \
            self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        self.__class__.eventID_no_distance = event_params_no_distance['event']['id']

    def test_001_go_to_event_details_page_of_event_with_race_distance_available(self):
        """
        DESCRIPTION: Go to event details page of event with race distance available
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_002_verify_distance_presence_format_and_correctness(self):
        """
        DESCRIPTION: Verify distance presence, format and correctness
        EXPECTED: Race distance is present on the left side below time switcher tabs. The format of Race distance is :
        EXPECTED: **'Distance: Xm ****Yf**** Zy'**
        EXPECTED: where,
        EXPECTED: *   X - number of miles
        EXPECTED: *   Y - number of furlongs
        EXPECTED: *   Z - number of yards
        EXPECTED: **If any value is 0 - this part is not shown on front-end**
        """
        self.assertTrue(self.site.racing_event_details.tab_content.race_details.has_race_distance(),
                        msg='Distance not found')
        actual_distance = self.site.racing_event_details.tab_content.race_details.race_distance.value
        self.assertEqual(actual_distance.strip(), self.distance.strip(),
                         msg=f'Event distance "{actual_distance.strip()}" is not the same '
                             f'as got from SiteServe response "{self.distance.strip()}"')

    def test_003_go_to_event_details_page_of_event_with_no_race_distance_available(self):
        """
        DESCRIPTION: Go to event details page of event with NO race distance available (NO 'distance' attribute in SS response)
        EXPECTED: Distance label and values are not shown on Event details page
        """
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_no_distance)[0]['event']
        distance = event_details.get('distance', False)
        self.assertFalse(distance, msg='"distance" attribute not expected but found')
