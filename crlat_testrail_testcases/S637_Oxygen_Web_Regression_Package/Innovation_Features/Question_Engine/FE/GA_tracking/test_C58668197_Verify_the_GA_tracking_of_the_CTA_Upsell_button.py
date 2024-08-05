import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C58668197_Verify_the_GA_tracking_of_the_CTA_Upsell_button(Common):
    """
    TR_ID: C58668197
    NAME: Verify the GA tracking of the CTA Upsell button
    DESCRIPTION: This test case verifies the Google Analytics tracking of the CTA Upsell button.
    PRECONDITIONS: For more information please consider https://confluence.egalacoral.com/display/SPI/GA+TRACKING+CORRECT+4
    PRECONDITIONS: 1. The Quiz is configured in the CMS.
    PRECONDITIONS: 2. The Upsell is configured.
    PRECONDITIONS: 3. Open the Correct4 https://phoenix-invictus.coral.co.uk/correct4.
    PRECONDITIONS: 4. The User is logged in.
    PRECONDITIONS: 5. The User has already played a Quiz.
    PRECONDITIONS: 6. Open DevTools in browser.
    """
    keep_browser_open = True

    def test_001_proceed_to_the_results_page(self):
        """
        DESCRIPTION: Proceed to the Results page.
        EXPECTED: The Results page is opened.
        """
        pass

    def test_002_click_on_the_cta_upsell_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the CTA Upsell button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Betslip',
        EXPECTED: 'eventAction' : 'Add to betslip',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'ecommerce': {
        EXPECTED: 'add': {
        EXPECTED: 'products': [{
        EXPECTED: 'name': '&lt;&lt;EVENT NAME&gt;&gt;',
        EXPECTED: 'category': ‘16',
        EXPECTED: 'variant': ‘434',
        EXPECTED: 'brand': 'Match Result',
        EXPECTED: 'dimension60': '11527917',
        EXPECTED: 'dimension61': '&lt;&lt;SELECTION ID&gt;&gt;',
        EXPECTED: 'dimension62': 0,
        EXPECTED: 'dimension63’: 0,
        EXPECTED: 'dimension64': ‘/correct4/after/latest-quiz’,
        EXPECTED: 'dimension65': ‘/correct4',
        EXPECTED: }]
        EXPECTED: }
        EXPECTED: }
        EXPECTED: })
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Betslip',
        EXPECTED: 'eventAction' : 'Add to betslip',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'ecommerce': {
        EXPECTED: 'add': {
        EXPECTED: 'products': [{
        EXPECTED: 'name': '&lt;&lt;EVENT NAME&gt;&gt;',
        EXPECTED: 'category': ‘16',
        EXPECTED: 'variant': ‘434',
        EXPECTED: 'brand': 'Match Result',
        EXPECTED: 'dimension60': '11527917',
        EXPECTED: 'dimension61': '&lt;&lt;SELECTION ID&gt;&gt;',
        EXPECTED: 'dimension62': 0,
        EXPECTED: 'dimension63’: 0,
        EXPECTED: 'dimension64': ‘/{sourceId}/after/latest-quiz’,
        EXPECTED: 'dimension65': ‘/{sourceId}',
        EXPECTED: }]
        EXPECTED: }
        EXPECTED: }
        EXPECTED: })
        """
        pass
