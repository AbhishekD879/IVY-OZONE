from voltron.pages.shared.contents.my_bets.cashout import BetWithReceipt


class MultipleTotePool(BetWithReceipt):

    @property
    def name(self):
        """
        :return name in format:
        "{bet type} - [{all_event_names}]", e.g. 'TOTEPOOL - [Leg 1: 18:00 Chelmsford - 2. Tomshalfbrother',...]'
        """
        return '%s - [%s]' % (self.bet_type, ', '.join(
            ['%s - %s' % (bet_leg.event_name, bet_leg.outcome_name) for (bet_leg_name, bet_leg) in self.items_as_ordered_dict.items()]))
