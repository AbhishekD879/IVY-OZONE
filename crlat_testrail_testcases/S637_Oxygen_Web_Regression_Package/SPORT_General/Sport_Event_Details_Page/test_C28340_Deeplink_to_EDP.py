import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28340_Deeplink_to_EDP(Common):
    """
    TR_ID: C28340
    NAME: Deeplink to EDP
    DESCRIPTION: This Test Case verifies Deeplink into a BMA Event page.
    DESCRIPTION: **Jira ticket: **BMA-6940 Deeplink Into A BMA Event Page
    PRECONDITIONS: Clear cash and cookies.
    PRECONDITIONS: Prepare list of valid event ids for the following sports categories:
    PRECONDITIONS: American football
    PRECONDITIONS: Aussie Rules
    PRECONDITIONS: Badminton
    PRECONDITIONS: Baseball
    PRECONDITIONS: Basketball
    PRECONDITIONS: Bowls
    PRECONDITIONS: Boxing
    PRECONDITIONS: Cricket
    PRECONDITIONS: Cycling
    PRECONDITIONS: Darts
    PRECONDITIONS: Football
    PRECONDITIONS: Formula1
    PRECONDITIONS: Gaelic Football
    PRECONDITIONS: Golf
    PRECONDITIONS: Greyhound
    PRECONDITIONS: Handball
    PRECONDITIONS: Horse Racing
    PRECONDITIONS: Hurling
    PRECONDITIONS: Ice Hockey
    PRECONDITIONS: Moto Bikes
    PRECONDITIONS: Moto Sports
    PRECONDITIONS: Movies
    PRECONDITIONS: Politics
    PRECONDITIONS: Pool
    PRECONDITIONS: Rugby League
    PRECONDITIONS: Rugby Union
    PRECONDITIONS: Snooker
    PRECONDITIONS: Speedway
    PRECONDITIONS: Tennis
    PRECONDITIONS: TVSpecials
    PRECONDITIONS: UFC/MMA
    PRECONDITIONS: Volleyball
    """
    keep_browser_open = True

    def test_001_generate_url_in_following_formatinvictuscoralcoukeventevent_id_where_event_id_should_be_taken_from_preconditions(self):
        """
        DESCRIPTION: Generate URL in following format:
        DESCRIPTION: invictus.coral.co.uk/#/event/[event\_id] where event\_id should be taken from Preconditions
        EXPECTED: 
        """
        pass

    def test_002_run_just_generated_url(self):
        """
        DESCRIPTION: Run just generated URL
        EXPECTED: *   Event details page is opened.
        EXPECTED: *   All related information to the event from URL should be correctly displayed.
        """
        pass

    def test_003_repeate_steps_1_2_for_all_categories_from_the_preconditions(self):
        """
        DESCRIPTION: Repeate steps #1-2 for all categories from the Preconditions
        EXPECTED: 
        """
        pass

    def test_004_generate_url_in_following_formatinvictuscoralcoukeventevent_id1event_id2_where_event_idn_should_be_taken_from_preconditionsrun_just_generated_url(self):
        """
        DESCRIPTION: Generate URL in following format:
        DESCRIPTION: invictus.coral.co.uk/#/event/[event\_id1],[event\_id2] where [event_id*n*] should be taken from Preconditions
        DESCRIPTION: Run just generated URL
        EXPECTED: *   Event details page of the firs event from the URL is opened.
        EXPECTED: *   All related information to the first event should be correctly displayed.
        """
        pass

    def test_005_generate_url_in_following_formatinvictuscoralcoukeventevent_id_where_event_id_doesnt_exist_or_is_invalidrun_just_generated_url(self):
        """
        DESCRIPTION: Generate URL in following format:
        DESCRIPTION: invictus.coral.co.uk/#/event/[event\_id] where event\_id doesn't exist or is invalid
        DESCRIPTION: Run just generated URL
        EXPECTED: User is redirected to the 404 page.
        """
        pass

    def test_006_generate_url_in_following_formatinvictuscoralcoukeventevent_id_where_event_id_doesnt_exist_or_is_invalidrun_just_generated_url(self):
        """
        DESCRIPTION: Generate URL in following format:
        DESCRIPTION: invictus.coral.co.uk/#/event/[event\_id] where event\_id doesn't exist or is invalid
        DESCRIPTION: Run just generated URL
        EXPECTED: User is redirected to the 404 page.
        """
        pass

    def test_007_generate_url_with_other_parameters_which_are_not_needed_in_following_formatinvictuscoralcoukeventevent_idsillyparameter123run_just_generated_url(self):
        """
        DESCRIPTION: Generate URL with other parameters which are not needed in following format:
        DESCRIPTION: invictus.coral.co.uk/#/event/[event_id]&[sillyparameter=123]
        DESCRIPTION: Run just generated URL
        EXPECTED: *   Event details page is opened.
        EXPECTED: *   All related information to the event from the URL should be correctly displayed.
        EXPECTED: *   All not needed parameters should be skipped.
        """
        pass

    def test_008_generate_url_with_affiliate_parameters_in_following_formatinvictuscoralcoukeventevent_ididnmemberincomeaccessprofile2sbxml0000crefererbtaga_1b_7c_gavnkrun_just_generated_url(self):
        """
        DESCRIPTION: Generate URL with affiliate parameters in following format:
        DESCRIPTION: invictus.coral.co.uk/#/event/[event\_id]&id=N&member=incomeaccess&profile=2sbxml0000&creferer=BTAG:a\_1b\_7c\_GavNK
        DESCRIPTION: Run just generated URL
        EXPECTED: *   Event details page is opened.
        EXPECTED: *   All related information to the eventfrom the URL should be correctly displayed.
        EXPECTED: *   Affiliate parameters shuld be written into banner_domainclick cookie file.
        """
        pass

    def test_009_proceed_with_registration_flow(self):
        """
        DESCRIPTION: Proceed with registration flow
        EXPECTED: *   User is successfully registered.
        EXPECTED: *   Affiliate parameters should be correctly set into IMS.
        """
        pass
