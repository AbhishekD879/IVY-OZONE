import argparse
import logging
import tests
from tests.base_test import BaseTest

"""
We can use this script as Pre-condition check for Sanity/Regression/UAT test runs
Updating the Quiz Popup enable/disable Status
Updating the Max Amount for QuickLink
"""

logger = logging.getLogger('voltron_logger')
parser = argparse.ArgumentParser()

parser.add_argument('--brand', '-brand', help='Brand of the product, e.g. bma, ladbrokes', default='ladbrokes', type=str)
parser.add_argument('--env', '-env', help='Backend environment, e.g. prod0, hlv0, tst0, stg0', default='hlv0', type=str)
parser.add_argument('--quicklinkmaxamount', '-quicklinkmaxamount', help='Max amount for quick link, e.g. 40', default=30, type=int)
parser.add_argument('--quizPopup', '-quizPopup', help='Quiz Popup enable/disable, e.g. True, False', default=False, type=bool)
parser.add_argument('--fanzonepopup', '-fanzonepopup', help='Fanzone Popup enable/disable, e.g. True, False', default=False, type=bool)

args = parser.parse_args()

brand = args.brand.lower()
env = args.env.lower()
quicklinkmaxamount = args.quicklinkmaxamount
quizPopup = args.quizPopup
fanzonepopup = args.fanzonepopup

base_test = BaseTest()
tests.settings.cms_env = env
tests.base_test.BaseTest.brand = brand

# Updating Quick Link Max Amount
base_test.cms_config.update_system_configuration_structure(config_item='Sport Quick Links', field_name='maxAmount',
                                                           field_value=quicklinkmaxamount)

logger.info('############### Updated Quick Link Max Amount ###############')

# Updating Fanzone Enable/Disable status
base_test.cms_config.update_system_configuration_structure(config_item='Fanzone', field_name='enabled',
                                                           field_value=fanzonepopup)

logger.info('############### Updated Fanzone Status ###############')

# Updating Quiz Popup Status
quiz_popup_data = base_test.cms_config.get_qe_pop_up_page()
quiz_id = quiz_popup_data['quizId']
pageUrls = quiz_popup_data['pageUrls']
popupText = quiz_popup_data['popupText']
popupTitle = quiz_popup_data['popupTitle']
yesText = quiz_popup_data['yesText']
remindLaterText = quiz_popup_data['remindLaterText']
dontShowAgainText = quiz_popup_data['dontShowAgainText']
base_test.cms_config.create_question_engine_pop_up(quiz_id=quiz_id, enabled=quizPopup, url=pageUrls,
                                                   pop_up_text=popupText,
                                                   pop_up_titile=popupTitle, yes_text=yesText,
                                                   remind_me_later=remindLaterText,
                                                   dont_show_again=dontShowAgainText)

logger.info('############### Updated Quiz Popup Status ###############')
