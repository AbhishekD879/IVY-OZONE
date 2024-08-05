import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { BetSelection } from '@betslip/services/betSelection/bet-selection';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { BetStake } from '@betslip/services/betStake/bet-stake';
import { IStake } from '@betslip/services/betStake/bet-stake.model';
import { IFreeBet } from '@betslip/services/freeBet/free-bet.model';
import { IOutcome } from '@core/models/outcome.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';

import * as _ from 'underscore';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { StorageService } from '@core/services/storage/storage.service';
import { IBetslipBetData, IHandicapOutcome } from '../../models/betslip-bet-data.model';
import { IBetslipMultipleStake } from '../../models/betslip-stake.model';
import { Bet } from '../bet/bet';
import { BetSelectionsService } from '../betSelections/bet-selections.service';
import { FreeBet } from '../freeBet/free-bet';
import { BetslipDataService } from './betslip-data.service';
import { ISportEvent } from '@core/models/sport-event.model';

@Injectable({ providedIn: BetslipApiModule })
export class BetslipStorageService {
  eventToBetslipObservable: Observable<ISportEvent[]> = null;

  constructor(private storageService: StorageService,
              private localeService: LocaleService,
              private betslipDataService: BetslipDataService,
              private betSelectionsService: BetSelectionsService,
              private fracToDecService: FracToDecService,
              private pubsub: PubSubService,
              private nativeBridgeService: NativeBridgeService) {
  }

  set setEventToBetslipObservable(value: null | Observable<ISportEvent[]>) {
    this.eventToBetslipObservable = value;
  }

  /**
   * Returns event observable to prevent redundant calls to server:
   */
  useEventToBetslipObservable(): Observable<ISportEvent[]> {
    const event$ = this.eventToBetslipObservable;

    this.setEventToBetslipObservable = null;

    return event$;
  }

  /**
   * Restore user stake data:
   * - user stake amout
   * - user eachWay option
   * - user freeBet
   * @params {array} bets array from controller
   */
  restoreUserStakeData(bets: IBetslipBetData[]) {
    const dataInStorage = this.restore();

    _.each(bets, (bet: IBetslipBetData | any) => {
      // remember data only for signles
      if (bet.type !== 'SGL') {
        return;
      }

      // get bet data from storage
      const data = _.find(dataInStorage, (betSelection: IBetSelection | any) => {
        return `${bet.combiName || bet.type}|${bet.outcomeId}` === betSelection.id || (bet.Bet && bet.Bet.params.lottoData?.id.includes( betSelection.details?.draws[0].id));
      });
      if (!data) {
        return;
      }

      if(bet.Bet && !bet.Bet.params.lottoData?.isLotto){
        bet.stake.perLine = data.userStake;
      }else if(bet.Bet && bet.Bet.params.lottoData?.id === data.id){
        bet.Bet.params.lottoData.details.stake = data.userStake;
        bet.Bet.params.lottoData.accaBets.forEach((accaBet)=>{
          accaBet.stake = accaBet.userStake;
        });
      }
      bet.Bet.isEachWay = data.userEachWay && data.details?.isEachWayAvailable?.toString()=="true";

      if (bet.Bet.freeBets && bet.Bet.freeBets.length > 0 && data.userFreeBet && data.userFreeBet.length > 0) {
        _.each(bet.Bet.freeBets, (freeBet: IFreeBet) => {
          if (freeBet.id === data.userFreeBet) {
            bet.selectedFreeBet = freeBet;

            bet.Bet.freeBet = freeBet;

            bet.stake.freeBetAmount = Math.floor(freeBet.value / (bet.stakeMultiplier * (bet.Bet.isEachWay ? 2 : 1)) * 100) / 100;
            bet.freeBetText = this.localeService.getString('bs.noFreeBetsAvalaible');
          }
        });
      }
    });

    if (this.storageService.get('multipleUserStakes')) {
      this.restoreMultipleUserStakes();
      this.restoreMultiplesFreeBetData(bets);
    }
  }

  restore(): IBetSelection[] {
    const sessionData = this.storageService.get('betSelections');
    return !sessionData?.islotto ? (<IBetSelection[]>this.storageService.get('betSelections') || []) :
            (this.zip(this.storageService.get('betSelections')) || []);
  }

  /**
   * Store ids of suspended outcomes in storage
   */
  storeSuspended(selections: IBetSelection[]): void {
    this.storageService.set('betSuspendedSelections', selections);
  }

  /**
   * Update local storage after livePrice update
   * @params{object} update
   * @params{string} outcomeId
   */
  updateStorage(update, outcomeId: string) {
    const betData = <IBetSelection[]>this.storageService.get('betSelections');

    const stake = _.find(betData, (bet: IBetSelection) => _.contains(bet.outcomesIds, outcomeId));

    if (!stake) {
      return;
    }

    if (update.lp_den && update.lp_num) {
      stake.price.priceDen = update.lp_den;
      stake.price.priceNum = update.lp_num;
      stake.price.priceDec = this.fracToDecService.getDecimal(update.lp_num, update.lp_den);
    }

    if (update.raw_hcap) {
      (stake.handicap as IHandicapOutcome).raw = update.raw_hcap;
    }

    if (update.ew_avail && stake.details) {
      stake.details.isEachWayAvailable = update.ew_avail === 'Y';
    }

    this.storageService.set('betSelections', betData);
  }

  removeFanzoneSelections(outcomeId) {
    const betData = <IBetSelection[]>this.storageService.get('betSelections');
    const index = betData.findIndex((bet: IBetSelection) => bet.outcomesIds[0] === outcomeId);
    if (index !== -1) {
      betData.splice(index, 1);
    }
    this.storageService.set('betSelections', betData);  
  }

  store(): void {
    this.storeMultipleUserStakes();
    this.storageService.set('betSelections', this.zip(this.betSelectionsService.data));
  }

  setFreeBet(bet: IBetslipBetData): void {
    _.each(<BetSelection[]>this.betSelectionsService.data, (selection: BetSelection) => {
      if (bet.id === selection.id) {
        if (bet.selectedFreeBet) {
          selection.userFreeBet = bet.selectedFreeBet.id;
        } else {
          selection.userFreeBet = '';
        }
      }
    });

    this.store();
  }

  getOutcomesIds(selections: IBetSelection[] = this.restore()): string[] {
    return selections.reduce((ids: string[], sel: IBetSelection) => {
      return _.union(ids, sel.outcomesIds);
    }, []);
  }

  /**
   * Function gets outcomes id's stored in locale storage and compares it to id's
   * that we have received from SS, if we have not received some of the outcomes, this means
   * that outcome is no longer available on siteServ. I case we have some outcomes that are no longer
   * available - we delete them from locale storadge and show console.warn message
   * if we have all id's in locale storadge same as we have received from SS - we just return outcomes
   */
  filterSelections(outcomes: IOutcome[]): IOutcome[] {
    if (outcomes.length === 0) {
      this.clean();
      return [];
    }
    const selectionInStorage = this.restore();
    const requestedIds = this.getOutcomesIds(selectionInStorage);
    const idsFromServer = _.reduce(outcomes, (ids: string[], outcome: IOutcome) => {
          ids.push(outcome.id);
          return ids;
        }, []);
    const difference = _.difference(requestedIds, idsFromServer);

    if (difference.length === 0) {
      return outcomes;
    }

    for (let i = 0; i < selectionInStorage.length; i++) {
      if (difference.indexOf(selectionInStorage[i].outcomesIds[0]) !== -1) {
        console.warn(`Selection was removed due to absense of outcome on site serve: ${selectionInStorage[i].outcomesIds[0]}`);
        this.betSelectionsService.removeSelectionById(<number>selectionInStorage[i].id);
        selectionInStorage.splice(i, 1);
        i--;
      }
    }
    this.storageService.set('betSelections', selectionInStorage);

    return outcomes;
  }

  clean(): number {
    this.betSelectionsService.data = [];
    this.store();
    this.pubsub.publish(this.pubsub.API.FLUSH_VS_STORAGE);

    this.pubsub.publishSync(this.pubsub.API.ACCA_NOTIFICATION_CHANGED, {});
    this.nativeBridgeService.accaNotificationChanged();

    this.betslipDataService.setDefault();
    this.betSelectionsService.flush();
    this.syncWithNative();

    return 0;
  }

  /**
   * Synchronize with native
   */
  syncWithNative(): void {
    this.pubsub.publish(this.pubsub.API.SYNC_BETSLIP_TO_NATIVE, this.getOutcomesForWrapper());
  }

  /**
   * Clears betslip data
   * @param {boolean} closeSlideOut
   * @param {boolean} isOveraskCanceled
   * @private
   */
  cleanBetslip(closeSlideOut = false, isOveraskCanceled: boolean): void {
    this.clean();

    this.storageService.remove('vsm-betmanager-coralvirtuals-en-selections');
    this.storageService.remove('vsbr-selection-map');
    this.storageService.remove('lastMadeBet');
    this.storageService.remove('lastMadeBetSport');

    this.pubsub.publishSync(this.pubsub.API.OVERASK_CLEAN_BETSLIP, {closeSlideOut, isOveraskCanceled});
  }

  /**
   * Clear overask stored data
   * @private
   */
  clearStateInStorage(): void {
    this.storageService.remove('overaskIsInProcess');
    this.storageService.remove('overaskUsername');
    this.storageService.remove('overaskPlaceBetsData');
  }

  /**
   * Get outcomes and transform them to sync betslip with native
   * @param {Array} selections
   * @returns {Array}
   */
  private getOutcomesForWrapper(selections: Partial<IBetSelection>[] = this.restore()) {
    const outcomesData = _.map(selections, (outcome: IOutcome) => {
      return _.pick(outcome, ['outcomesIds', 'price']);
    });
    return _.each(outcomesData as unknown as Partial<IOutcome>[] , (outcome: Partial<IOutcome>) => {
      const { id = null, priceType = null, priceNum = null, priceDen = null, priceDec = null } = <any>outcome.price || {};

      outcome.price = id ? {
        id,
        priceType,
        priceNum: Number(priceNum),
        priceDen: Number(priceDen),
        priceDec: Number(priceDec)
      } : { priceType };
    });
  }

  /**
   * Restore user stakes stored in localeS torage for multiple bets.
   * @return{array} bets
   */
  private restoreMultipleUserStakes(): void {
    const lsData = <IBetslipMultipleStake>this.storageService.get('multipleUserStakes'), // shortcut
        multipleStakes = lsData.stakeData,
        activeSinglesCount = lsData.activeSinglesCount,
        activeSinglesIds = lsData.activeSinglesIds;

    // set multiples stakes only if singles amout is the same and their outcome id's are equal
    if (activeSinglesCount === this.countActiveSingles(this.betslipDataService.bets) &&
        activeSinglesIds.toString() === this.betslipDataService.getActiveSinglesIds().toString()) {
      _.each(multipleStakes, (multipleStake: IStake) => {
        const bet = this.betslipDataService.bets.find((betData: Bet) => betData.storeId === multipleStake.storeId);
        if (bet && (multipleStakes && !multipleStakes[0].isLotto)) {
          (<BetStake>bet.stake).perLine = multipleStake.stake || '';
          bet.betOffer.isAccaValid = !multipleStake.stake || multipleStake.stake >= 2;
          bet.isEachWay = multipleStake.userEachWay && bet.params.eachWayAvailable === 'Y';
        }
      });
    }
  }
  /**
   * Restore user Multiple FreeBet selection
   * @params {array} bets array from controller
   */
  private restoreMultiplesFreeBetData(bets: IBetslipBetData[]) {
    const multipleStakes = (this.storageService.get('multipleUserStakes') as IBetslipMultipleStake).stakeData;
    let bet: IBetslipBetData;
    _.each(multipleStakes, (multipleStake: IStake) => {
      bet = bets.find((betData: IBetslipBetData) => betData.Bet.storeId === multipleStake.storeId);
      if (bet && bet.Bet.freeBets && bet.Bet.freeBets.length > 0 && multipleStake.userFreeBet) {
        _.each(bet.Bet.freeBets, (freeBet: FreeBet) => {
          if (freeBet.id === multipleStake.userFreeBet) {
            bet.selectedFreeBet = freeBet;

            bet.Bet.freeBet = freeBet;

            bet.stake.freeBetAmount = Math.floor(freeBet.value / (bet.stake.lines * (bet.isEachWay ? 2 : 1)) * 100) / 100;
            bet.freeBetText = this.localeService.getString('bs.noFreeBetsAvalaible');
          }
        });
      }
    });
  }

  /**
   * Get amout of active singles
   * params{array} bets
   * return {number} active bets count
   */
  private countActiveSingles(bets: Bet[]): number {
    let amount = 0, infoObj;
    if (bets && bets.length) {
      _.each(bets, (bet: Bet) => {
        infoObj = bet.info();
        if (!bet.params.lottoData?.isLotto) {
          if (infoObj.type === 'SGL' && !infoObj.disabled && infoObj.Bet.price.type !== 'DIVIDEND') {
            amount++;
          }
        }
      });
    }
    return amount;
  }

  /**
   * Store multiple selections data in locale Storage
   */
  private storeMultipleUserStakes(): void {
    const multipleSelectionData = [];
    if (this.betslipDataService.bets.length) {
      if (!this.betslipDataService.bets[0].params.lottoData?.isLotto) {
        _.each(this.betslipDataService.bets, (bet: Bet | any, id: number) => {
          if (bet.type !== 'SGL') {
            multipleSelectionData.push({
              storeId: bet.storeId,
              betId: id,
              stake: (<BetStake>bet.stake).perLine,
              userEachWay: bet.isEachWay,
              userFreeBet: bet.freeBet ? bet.freeBet.id : ''
            });
          }
        });
      }
    }
    this.storageService.set('multipleUserStakes', {
      activeSinglesIds: this.betslipDataService.getActiveSinglesIds(),
      activeSinglesCount: this.countActiveSingles(this.betslipDataService.bets),
      stakeData: multipleSelectionData
    });
  }

  private zip(selections: BetSelection[]): IBetSelection[] {// need to change bet data interface
    return _.map(selections, (sel: BetSelection) => {
      return new BetSelection(sel).zip();
    });
  }
}
