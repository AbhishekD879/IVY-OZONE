import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { OverAskService } from '@betslip/services/overAsk/over-ask.service';
import { Bet } from './bet';
import { ILeg } from '../models/bet.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { UserService } from '@core/services/user/user.service';
import { StorageService } from '@core/services/storage/storage.service';
import { BetStakeService } from '../betStake/bet-stake.service';
import { FreeBetService } from '@betslip/services/freeBet/free-bet.service';
import { IBet, IBetDoc } from '@betslip/services/bet/bet.model';
import { BetslipFiltersService } from '@betslip/services/betslipFilters/betslip-filters.service';
import { SportsLegPriceService } from '@betslip/services/sportsLegPrice/sports-leg-price.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ILottoBetDoc } from '@app/lotto/models/lotto.model';

@Injectable({ providedIn: BetslipApiModule })
export class BetService {

  constructor(
    private freeBetService: FreeBetService,
    private betStakeService: BetStakeService,
    private sportsLegPriceService: SportsLegPriceService,
    public overaskService: OverAskService,
    public localeService: LocaleService,
    public fracToDec: FracToDecService,
    public filters: FiltersService,
    public betslipFilters: BetslipFiltersService,
    private storageService: StorageService,
    private user: UserService,
    private pubSubService: PubSubService
  ) { }

  construct(params: Partial<IBet>): Bet {
    const instance = new Bet(
      params,
      this.freeBetService,
      this.betStakeService,
      this.sportsLegPriceService,
      this.overaskService,
      this.localeService,
      this.fracToDec,
      this.filters,
      this.betslipFilters,
      this.storageService,
      this.user,
      this.pubSubService
    );
    return instance;
  }

  parse(root: IBetDoc | ILottoBetDoc, legs: ILeg[]): Bet {
    const lines = root.lines?.number || 1,
      legIds = (root.legRef) ? (root.legRef.map(ref => {
        return ref.documentId;
      })) : root.isLotto ? root.lines?.number || '' : root.leg.documentId,
      parsedObj: Partial<IBet> = {
        betOffer: root.betOfferRef || {},
        docId: root.documentId,
        type: root.betTypeRef?.id || root.type,
        stake: this.betStakeService.parse(root.stake || {}, lines),
        lines,
        legIds: <string[]>legIds,
        allLegs: legs,
        payout: root.payout,
        maxPayout: root.maxPayout,
        freeBets: (root.freebet && this.freeBetService.parse(root.freebet.filter((freeBet) => {
          return freeBet.type === 'SPORTS';
        }))) || [],
        oddsBoosts: (root.freebet && <any[]>root.freebet.filter((freeBet) => {
          return freeBet.type === 'BETBOOST';
        })) || [],
        eachWayAvailable: root.eachWayAvailable
      };
    if(root.isLotto) {
      parsedObj.lottoData = root;
    }
    if (root.receipt) {
      parsedObj.placed = {
        id: root.id,
        docId: root.documentId,
        time: new Date(root.timeStamp),
        confirmed: (root.isConfirmed === 'Y'),
        settled: (root.isSettled === 'Y'),
        provider: root.provider,
        receipt: root.receipt
      };
    } else if (root.provider === 'OpenBetBir') {
      parsedObj.placed = {
        id: root.id,
        docId: root.documentId,
        confirmed: (root.isConfirmed === 'Y'),
        provider: root.provider,
        expectedAt: root.confirmationExpectedAt
      };
    }
    return this.construct(parsedObj);
  }
}
