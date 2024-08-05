import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C44100910_Verify_call_to_OB_SS_on_Races_LP_and_EDP(Common):
    """
    TR_ID: C44100910
    NAME: Verify call to OB SS on Races LP and EDP
    DESCRIPTION: TC verifies number of SS requests when user navigates to HORSE RACING / GREYHOUNDS Landing Page and Event Details Page
    PRECONDITIONS: 1. App is opened
    PRECONDITIONS: 2. DevTools is opened on Network tab
    """
    keep_browser_open = True

    def test_001_navigate_to_hr_landing_page_refresh_page(self):
        """
        DESCRIPTION: Navigate to HR landing page, refresh page
        EXPECTED: 
        """
        pass

    def test_002_search_for_class_openbet_ss_requestsex_httpsss_aka_oriladbrokescomopenbet_ssviewerdrilldown231classtranslationlangenresponseformatjsonsimplefilterclasscategoryidequals21simplefilterclassisactivesimplefilterclasssitechannelscontainsm(self):
        """
        DESCRIPTION: Search for "class?" Openbet SS requests
        DESCRIPTION: ex. https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/Class?translationLang=en&responseFormat=json&simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M
        EXPECTED: Only one such request should be sent to OB with parameter simpleFilter=class.categoryId:equals:21 (21=HR; 19=GH)
        """
        pass

    def test_003_repeat_steps_for_hr_edp_gh_lp_gh_edp(self):
        """
        DESCRIPTION: Repeat steps for HR EDP, GH LP, GH EDP
        EXPECTED: 
        """
        pass
