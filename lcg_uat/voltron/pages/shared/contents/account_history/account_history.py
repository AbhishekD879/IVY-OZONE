from voltron.pages.shared.contents.my_bets.bet_history.bet_history import BetHistory


class AccountHistory(BetHistory):
    _url_pattern = r'^http[s]?:\/\/.+\/account-history'
