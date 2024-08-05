from voltron.pages.shared.components.right_column_widgets.right_column import RightColumn
from voltron.pages.coral.contents.my_bets.bet_history.bet_history import CoralBetHistoryDesktop


class CoralRightColumn(RightColumn):
    _slide_content_bet_history = CoralBetHistoryDesktop
