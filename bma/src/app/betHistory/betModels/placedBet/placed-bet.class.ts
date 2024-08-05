import * as _ from 'underscore';


import { IBetHistoryLeg } from '../../models/bet-history.model';
import { RegularBetBase } from '../regularBetBase/regular-bet-base.class';

export class PlacedBet extends RegularBetBase {
  bybType?: any;
  source?: string;
  contestId?: string;
  winnings?: { value: string }[];
  livePriceWinnings?: { value: string}[];

  constructor(bet,
              public betModelService,
              currency,
              currencySymbol,
              cashOutMapIndex,
              cashOutErrorMessage) {
    super(bet, betModelService, currency, currencySymbol, cashOutMapIndex, cashOutErrorMessage);

    this.potentialPayout = betModelService.getPotentialPayout(this);
    const isBetSettled = bet.settled === 'Y';
    _.each(this.leg, (legItem: IBetHistoryLeg) => {
      legItem.part = betModelService.createOutcomeName(legItem.part);
      legItem.status = undefined;

      this.initializeItemsArrays(legItem);
      this.initializeCashOutMap(legItem, isBetSettled);
    });
  }
}
