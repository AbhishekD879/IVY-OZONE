from collections import namedtuple


class Account(object):
    """
    src/app/lazy-modules/locale/translations/en-US/account.lang.ts
    """
    ACCOUNT_CLOSURE = 'Account Closure'
    CONTINUE = 'Continue'
    CANCEL = 'Cancel'
    _account_closure_reasons = namedtuple('account_closure_reasons', ['reason1', 'reason2', 'reason3',
                                                                      'reason4', 'reason5', 'reason6'])
    _account_closure_reasons_reason1 = 'Do not have time to gamble'
    _account_closure_reasons_reason2 = 'Not interested in online gambling anymore'
    _account_closure_reasons_reason3 = 'Not happy with your product'
    _account_closure_reasons_reason4 = 'Not happy with your offers'
    _account_closure_reasons_reason5 = 'I now use another provider'
    _account_closure_reasons_reason6 = 'Prefer not to specify'
    ACCOUNT_CLOSURE_REASONS = _account_closure_reasons(reason1=_account_closure_reasons_reason1,
                                                       reason2=_account_closure_reasons_reason2,
                                                       reason3=_account_closure_reasons_reason3,
                                                       reason4=_account_closure_reasons_reason4,
                                                       reason5=_account_closure_reasons_reason5,
                                                       reason6=_account_closure_reasons_reason6)
    LIKE_TO_DO = 'Please select a closure reason below:'
    ACCOUNT_CLOSED_TEXT = 'You have already closed your account. If you wish to reactivate your account, please'
    GO_TO_REACTIVATION = 'go to Reactivation'
    CONFIRM_PASSWORD = 'Please confirm with your password below:'
    INVALID_PASSWORD = 'Your password is invalid. Please try again'

    _closure_step_two = namedtuple('closure_step_two', ['about_to_close', 'consequences', 'consequence_info',
                                                        'consequence_deposit', 'consequence_bet', 'after_confirm',
                                                        'after_confirm_action1', 'after_confirm_action2'])
    _closure_step_two_about_to_close = 'You are about to close your account'
    _closure_step_two_consequences = 'Consequences of Account Closure'
    _closure_step_two_consequence_info = 'You will no longer be able to:'
    _closure_step_two_consequence_deposit = 'Deposit funds in your account'
    _closure_step_two_consequence_bet = 'Bet with real or play money stakes'
    _closure_step_two_after_confirm = 'After Confirmation'
    _closure_step_two_after_confirm_action1 = 'You should close any open gaming sessions',
    _closure_step_two_after_confirm_action2 = 'You will not be able to add any funds to open gaming session'
    CLOSURE_STEP_TWO = _closure_step_two(about_to_close=_closure_step_two_about_to_close,
                                         consequences=_closure_step_two_consequences,
                                         consequence_info=_closure_step_two_consequence_info,
                                         consequence_deposit=_closure_step_two_consequence_deposit,
                                         consequence_bet=_closure_step_two_consequence_bet,
                                         after_confirm=_closure_step_two_after_confirm,
                                         after_confirm_action1=_closure_step_two_after_confirm_action1,
                                         after_confirm_action2=_closure_step_two_after_confirm_action2)

    HEADER_CLOSED = 'YOUR ACCOUNT IS NOW CLOSED'
    BODY_CLOSED = '<p>Your account closure request was successfully submitted and you have been logged out of your account.</p>' \
                  '<p>If you wish to  reactivate your account in future please log in and follow the instructions.</p>'
    OK = 'OK'
    TIMEOUT_LINK = 'Time Out'
    REALITY_CHECK_LINK = 'Reality Check'
    ACCOUNT_CLOSURE_DIALOG_HEADER = 'Confirmation of account closure'
    ACCOUNT_CLOSURE_DIALOG_TEXT = 'If you don\'t feel that Account Closure is the correct option for you, please try '
    ACCOUNT_CLOSURE_CONFIRM = 'I confirm that I wish to close my Coral account'
    ACCOUNT_CLOSURE_BOX_ERROR = 'Please, select the box to confirm'
    ACCOUNT_CLOSURE_CONFIRM_ERROR = 'Sorry an error occured, please try again'
    REACTIVATION_PAGE_TITLE = 'Reactivation'
    REACTIVATION_PAGE_SUB_TITLE = 'Reactivate your account'
    REACTIVATION_PASSWORD_LABEL = 'To reactivate your account please confirm with the password below:'
    REACTIVATION_NOTES = '<b>Please note:</b> after successful reactivation you will be automatically redirected to the Coral home page'
    REACTIVATION_WELCOME = 'Your account has been successfully reactivated'
    REACTIVATION_ERR_REQUIRED_PASS = 'Password is required'
    REACTIVATION_ERR_WRONG_PASS = 'Your password is invalid. Please try again'
    REACTIVATION_ERR_DEFAULT = 'Oops, Something went wrong, please try again or call our customer support at 0800 731 6191 to reopen your account'
    ACCOUNT_CLOSURE_CONTROL_SECTION_MESSAGE = 'Control which sections of your account should be accessible through the options below.'
    CURRENT_STATUS = 'Current status: open'
    CURRENT_STATUS_CLOSED = 'Current status: closed'

    _expected_product_list = namedtuple('expected_product_list', ('bingo', 'poker', 'sports', 'casino'))

    EXPECTED_PRODUCT_LIST = _expected_product_list(bingo='Bingo',
                                                   poker='Poker',
                                                   sports='Sports',
                                                   casino='Casino')

    _reasons_for_closure = namedtuple('account_closure_reasons', ['reason1', 'reason2', 'reason3',
                                                                  'reason4', 'reason5'])

    _closure_reasons_reason1 = 'Do not have the time'
    _closure_reasons_reason2 = 'Not interested in online gaming anymore'
    _closure_reasons_reason3 = 'Not happy with your service/product'
    _closure_reasons_reason4 = 'Want to play at a different provider'
    _closure_reasons_reason5 = 'Prefer not to specify'

    CLOSURE_REASONS = _reasons_for_closure(reason1=_closure_reasons_reason1,
                                           reason2=_closure_reasons_reason2,
                                           reason3=_closure_reasons_reason3,
                                           reason4=_closure_reasons_reason4,
                                           reason5=_closure_reasons_reason5)

    _duration = namedtuple('duration', ['duration1', 'duration2', 'duration3',
                                        'duration4', 'duration5', 'duration6'])

    _duration1 = '1 week'
    _duration2 = '1 month'
    _duration3 = '3 months'
    _duration4 = '6 months'
    _duration5 = 'until'
    _duration6 = 'indefinite closure'

    DURATION = _duration(duration1=_duration1,
                         duration2=_duration2,
                         duration3=_duration3,
                         duration4=_duration4,
                         duration5=_duration5,
                         duration6=_duration6)

    _reasons_for_taking_break = namedtuple('_reasons_for_taking_break', ['reason1', 'reason2', 'reason3'])

    _taking_break_reason1 = 'I spend too much time playing'
    _taking_break_reason2 = 'I spend too much money playing'
    _taking_break_reason3 = 'I do not wish to provide an answer'

    REASON_FOR_TAKING_BREAK = _reasons_for_taking_break(reason1=_taking_break_reason1,
                                                        reason2=_taking_break_reason2,
                                                        reason3=_taking_break_reason3)

    _duration = namedtuple('duration', ['duration1', 'duration2', 'duration3',
                                        'duration4', 'duration5'])

    _duration1 = '1 week'
    _duration2 = '2 weeks'
    _duration3 = '3 weeks'
    _duration4 = '4 weeks'
    _duration5 = 'time-out until'

    DURATION_TIMEOUT = _duration(duration1=_duration1,
                                 duration2=_duration2,
                                 duration3=_duration3,
                                 duration4=_duration4,
                                 duration5=_duration5)

    CONSEQUENCES_INFO_MESSAGE = 'You have successfully timed out from all of our products.'

    _consequence_description = namedtuple('consequence_description',
                                          ['consequence_description_title', 'consequence_description_1',
                                           'consequence_description_2'])

    _consequence_description_title = 'Consequences of Self-exclusion'
    _consequence_description_1 = 'Your account will be restricted and you will not be able to open a new account.'
    __consequence_description_2 = 'If you have any questions, please contact our Customer Service team.'

    CONSEQUENCE_DESCRIPTION = _consequence_description(consequence_description_title=_consequence_description_title,
                                                       consequence_description_1=_consequence_description_1,
                                                       consequence_description_2=__consequence_description_2)
