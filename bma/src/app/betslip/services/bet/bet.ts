import * as _ from 'underscore';

import { el } from '../json-element';
import { LocaleService } from '@core/services/locale/locale.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { UserService } from '@core/services/user/user.service';
import { StorageService } from '@core/services/storage/storage.service';
import { FreeBetService } from '@betslip/services/freeBet/free-bet.service';
import { OverAskService } from '@betslip/services/overAsk/over-ask.service';
import { SportsLegPriceService } from '@betslip/services/sportsLegPrice/sports-leg-price.service';
import { BetStakeService } from '@betslip/services/betStake/bet-stake.service';
import { FreeBet } from '@betslip/services/freeBet/free-bet';
import { BetStake } from '@betslip/services/betStake/bet-stake';
import { BetslipFiltersService } from '@betslip/services/betslipFilters/betslip-filters.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

import { ILiveServChannels } from '@core/models/live-serv-channels.model';
import { IOutcome } from '@core/models/outcome.model';
import { IBetPayout } from '@core/models/bet-payout.model';
import { IBet, IBetInfo, IBetPayload, IBetPlaced, IBetPrice, IOddsBoost } from '@betslip/services/bet/bet.model';
import { IFreeBet, IFreebetObj } from '@betslip/services/freeBet/free-bet.model';
import { IBetError } from '@betslip/services/betError/bet-error.model';
import { ILeg } from '@betslip/services/models/bet.model';
import { ILegPart } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { BetLiveUpdateHistory } from './bet-live-update-history';

export class Bet {

  isMocked: boolean;
  uid: string;
  storeId: string;
  placed: IBetPlaced;
  bsId: number;
  docId: number|string;
  type: string;
  typeInfo: string;
  errs: IBetError[];
  betOffer;
  payout;
  error: string;
  errorMsg: string;
  disabled: boolean;
  isReferred?: string;
  isConfirmed?: string;

  winPlace: string;
  _stake: BetStake|number;
  _freeBet: FreeBet;

  oddsBoosts: IOddsBoost[];
  oddsBoost: IOddsBoost;

  history: BetLiveUpdateHistory;
  maxPayout: string;
  isLotto?: boolean;

  constructor(
    public params: Partial<IBet>,
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
  ) {
    this.isMocked = params.isMocked;
    this.uid = params.uid;
    this.bsId = 1;
    this.placed = params.placed;
    this.docId =  params.docId;
    this.type = params.type;
    this.betOffer = params.betOffer;
    this.errs = params.errs;
    this.payout = params.payout;
    this.maxPayout = params.maxPayout;

    this.winPlace = params.winPlace;
    this._stake = params.stake && params.stake.doc
      ? params.stake
      : this.betStakeService.construct(_.extend({ lines: this.lines }, params.stake));

    this.setBetTypeInfo();

    this.history = new BetLiveUpdateHistory(this);
  }

  get lines(): number {
    return this.isEachWay ? this.params.lines * 2 : this.params.lines;
  }
  set lines(value:number){}
  get stake(): BetStake|number {
    return <BetStake>this._stake;
  }

  set stake(value: BetStake|number) {
    (this._stake as BetStake).perLine = <number>value;
  }

  get freeBet(): IFreeBet {
    return this._freeBet;
  }

  set freeBet(value: IFreeBet) {
    this._freeBet = this.freeBetService.construct(value);
  }

  get freeBets(): FreeBet[] {
    return this.params.freeBets;
  }
  set freeBets(value: FreeBet[]){}
  get isEachWay(): boolean {
    return this.winPlace === 'EACH_WAY';
  }

  set isEachWay(value: boolean) {
    this.winPlace = value ? 'EACH_WAY' : 'WIN';
    (this.stake as BetStake).lines = this.lines;
  }

  get legs(): ILeg[] {
    return this.isEachWay
      ? Bet.findEachWayLegs(this.params.allLegs, this.params.legIds)
      : Bet.findLegs(this.params.allLegs, this.params.legIds);
  }

  set legs(value: ILeg[]){}

  get price(): IBetPrice {
    return _.first(this.legs).selection?.price || {};
  }

  set price(priceParams: IBetPrice) {
    _.first(this.legs).selection.price = priceParams;
  }

  get betComplexName(): string {
    let name;
    if (this.legs[0].combi === 'FORECAST') {
      switch (this.lines) {
        case 1:
          name = this.localeService.getString('bs.forecast');
          break;
        case 2:
          name = this.localeService.getString('bs.reverseForecast');
          break;
        default:
          name = this.localeService.getString('bs.combinationForecast');
          break;
      }
    } else if (this.legs[0].combi === 'TRICAST') {
      if (this.lines === 1) {
        name = this.localeService.getString('bs.tricast');
      } else {
        name = this.localeService.getString('bs.combinationTricast');
      }
    }

    if (name && this.lines > 1) {
      name += ` ${this.lines}`;
    }

    return name;
  }
  set betComplexName(value:string){}
  clearErr(): void {
    if (this.type === 'SGL') {
      this.legs[0].parts[0].outcome.errorMsg = null;
      this.legs[0].parts[0].outcome.error = null;
      this.legs[0].parts[0].outcome.handicapErrorMsg = null;
    }
  }

  clearUserData(): void {
    (this._stake as BetStake).perLine = '';
    this.isEachWay = false;
    this.freeBet = null;
  }

  clone(): Bet {
    if (this.params.stake && this.params.stake.clone) {
      this.params.stake = this.params.stake.clone();
    }
    return new Bet(
      this.params,
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
  }

  doc(): IBet {
    const legRefs = el('legRef', _.map(this.legs, (leg: ILeg) => ({ documentId: leg.docId })));
    const betObject = [
      el('betTypeRef', { id: this.type }),
      (this.stake as BetStake).doc(),
      el('lines', { number: this.lines })
    ];

    if (this.freeBet && this.freeBet.id) {
      betObject.push(this.freeBet.doc());
    } else if (this.storageService.get('oddsBoostActive') && this.oddsBoost) {
      betObject.push(this.getOddsBoostObj());
    }

    return (
      el('bet', { documentId: this.docId }, betObject.concat(legRefs)).bet
    );
  }

  static findLegs(legs: ILeg[], legIds: string[]): ILeg[] {
    return legs.filter(leg => {
      return legIds.map(Number).indexOf(Number(leg.docId)) !== -1;
    });
  }

  static findEachWayLegs(allLegs: ILeg[], legIds: string[]): ILeg[] {
    const ewLegs = _.where(allLegs, { winPlace: 'EACH_WAY' });
    const ownLegs = Bet.findLegs(allLegs, legIds);

    return _.map(ownLegs, leg => {
      return leg.winPlace === 'EACH_WAY'
        ? leg
        : _.find(ewLegs, { firstOutcomeId: leg.firstOutcomeId });
    });
  }

  static getPayout(payout: { legType: string; potential: number; }[] = []): number {
    const payoutW = _.find(payout, p => p.legType === 'W');
    return payoutW && Number(payoutW.potential);
  }

  getEventLiveServChannels(): ILiveServChannels {
    return this.legs.reduce((totalLeg, leg) => {
      return (<any[]>leg.parts).reduce((totalPart, part) => {
        if (part.outcome.details && totalPart) {
          return {
            marketliveServChannels: totalPart.marketliveServChannels
              .concat(part.outcome.details.marketliveServChannels),
            eventliveServChannels: totalPart.eventliveServChannels
              .concat(part.outcome.details.eventliveServChannels),
            outcomeliveServChannels: totalPart.outcomeliveServChannels
              .concat(part.outcome.details.outcomeliveServChannels)
          };
        }
        return undefined;
      }, totalLeg);
    }, {
      marketliveServChannels: [],
      eventliveServChannels: [],
      outcomeliveServChannels: []
    });
  }

  getSelectionIds() {
    return this.legs.reduce((totalLeg, leg: ILeg) => {
      return (<any[]>leg.parts).reduce((totalPart, part: any) => {
        if (part.outcome.details && totalPart) {
          return {
            eventIds: totalPart.eventIds.concat(part.outcome.details.eventId),
            marketIds: totalPart.eventIds.concat(part.outcome.details.marketId),
            outcomeIds: totalPart.outcomeIds.concat(part.outcome.details.outcomeId),
            classIds: totalPart.classIds.concat(part.outcome.details.classId),
            categoriesIds: totalPart.categoriesIds.concat(part.outcome.details.categoryId),
            typeIds: totalPart.typeIds.concat(part.outcome.details.typeId)
          };
        }
        return undefined;
      }, totalLeg);
    }, {
      eventIds: [],
      marketIds: [],
      outcomeIds: [],
      classIds: [],
      categoriesIds: [],
      typeIds: []
    });
  }

  static isDisabled(bet: Bet, _params: Partial<IBet>): boolean {
    return bet.type === 'SGL' // only singles can be disabled
      ? (_params.errs && _params.errs.length > 0) ||
      bet.legs.every((leg: any) => {
        return leg.parts.some(part => {
          return (!!part.outcome.errorMsg ||
            part.outcome.errorMsg === '' || !!part.outcome.handicapErrorMsg ||
            part.outcome.handicapErrorMsg === '') &&
            !part.outcome.priceChange &&
            !part.outcome.handicapChange && !part.outcome.stakeError;
        });
      }) : undefined;
  }

  static getSportType(bet: Bet): boolean {
    let isRacing = false;
    _.each(bet.legs, (leg: any) => {
      const outcome = leg.parts[0].outcome;
      if (!outcome.details || outcome.details.categoryId === '19' || outcome.details.categoryId === '21') {
        isRacing = true;
      }
    });
    return isRacing;
  }

  static isCS(item): boolean {
    return item.outcome.outcomeMeaningMajorCode === 'CS';
  }

  info(): Partial<IBetInfo> {
    return Bet.getInfo(this);
  }

  static getInfo(bet): Partial<IBetInfo> {
    const type = bet.params.type === 'TMP' ? 'SGL' : bet.params.type;
    if(bet.params?.lottoData?.isLotto) {
      return {
        Bet: bet,
        stakeMultiplier: bet.params.lines,
        stake: (bet.stake as BetStake),
        error: (bet.params.errs && bet.params.errs.length > 0 && bet.params.errs[0].subCode),
        errorMsg: bet.params.errorMsg,
        type,
        typeInfo: bet.typeInfo
      };
    }

    let infoObj: Partial<IBetInfo> = {
      Bet: bet,
      stakeMultiplier: bet.params.lines,
      stake: (bet.stake as BetStake),
      error: (bet.params.errs && bet.params.errs.length > 0 && bet.params.errs[0].subCode),
      errorMsg: bet.params.errorMsg,
      type,
      typeInfo: bet.typeInfo,
      potentialPayout: Bet.getPayout(bet.payout),
      liveServChannels: bet.getEventLiveServChannels(),
      eventIds: bet.getSelectionIds(),
      disabled: Bet.isDisabled(bet, bet.params),
      isRacingSport: Bet.getSportType(bet)
    };

    if (type === 'SGL' && bet.price.type !== 'DIVIDEND') {
      _.each(bet.legs, (leg: any) => {
        const outcome = leg.parts[0].outcome;
        let prices,
          eachWay;
        if (outcome.details && leg.combi !== 'SCORECAST') {
          prices = _.extend({}, outcome.prices[0], {
            priceType: leg.price.type
          });
          eachWay = bet.params.eachWayAvailable === 'Y' && outcome.details.eachwayCheckbox &&
            outcome.outcomeMeaningMinorCode !== '1' && outcome.outcomeMeaningMinorCode !== '2';
        }
        if (leg.combi === 'SCORECAST' && outcome.details) {
          const cs = _.filter(leg.parts, Bet.isCS), // correct score market
            os = _.reject(leg.parts, Bet.isCS); // first or last goalscorer market

          // set priceDec to scorecast outcome
          if (leg.price.props) {
            leg.price.props.priceDec = bet.fracToDec.getDecimal(leg.price.props.priceNum, leg.price.props.priceDen);
          }
          infoObj = _.extend(infoObj, {
            className: outcome.details.info.className,
            sport: outcome.details.info.sport,
            typeId: outcome.details.typeId,
            eventName: outcome.details.info.event,
            marketName: bet.localeService.getString(`bs.${os[0].outcome.outcomeMeaningMajorCode}`),
            outcomeName: `${os[0].outcome.name}, ${cs[0].outcome.name}`,
            outcomeId: _.map(leg.parts, (item: { outcome: { id: string }}) => item.outcome.id).join('|'),
            time: new Date(outcome.details.info.time),
            combiName: leg.combi,
            price: leg.price.props,
            isSP: false
          });
        } else if (!leg.combi && outcome.details) {
          infoObj = _.extend(infoObj, {
            isMarketBetInRun: outcome.details.isMarketBetInRun,
            errorMsg: outcome.errorMsg,
            handicapErrorMsg: outcome.handicapErrorMsg,
            error: infoObj.error || outcome.error,
            handicapError: infoObj.handicapError || outcome.handicapError,
            price: prices,
            isBPGAvailable: outcome.details.isGpAvailable,
            isEachWayAvailable: Boolean(eachWay),
            eachWayPlaces: outcome.details.eachWayPlaces || outcome.details.markets && outcome.details.markets[0].eachWayPlaces,
            previousOfferedPlaces: outcome.details.previousOfferedPlaces || outcome.details.markets && outcome.details.markets[0].referenceEachWayTerms && outcome.details.markets[0].referenceEachWayTerms.places,
            drilldownTagNames:outcome.details.markets && outcome.details.markets[0].drilldownTagNames,
            eachWayFactorDen: eachWay ? outcome.details.eachwayCheckbox.eachwayPriceDen : '',
            eachWayFactorNum: eachWay ? outcome.details.eachwayCheckbox.eachwayPriceNum : '',
            priceDec: (prices && bet.fracToDec.getDecimal(prices.priceNum, prices.priceDen)),
            winOrEach: false,
            sportId: outcome.details.info.sportId,
            className: outcome.details.info.className,
            typeId: outcome.details.typeId,
            sport: outcome.details.info.sport,
            marketId: Number(outcome.marketId),
            marketName: bet.filters.filterAddScore(outcome.details.market, outcome.name),
            eventName: outcome.details.info.event,
            time: new Date(outcome.details.info.time),
            localTime: outcome.details.info.localTime,
            outcomeName: bet.filters.filterPlayerName(outcome.name),
            isStarted: outcome.details.info.isStarted,
            // TODO: Assertions against outcome name are duplicated in other places. Try to unify them.
            isSP: (prices.priceType === 'SP' && !outcome.details.isSPLP) ||
            outcome.name === 'UNNAMED FAVOURITE' ||
            outcome.name === 'UNNAMED 2nd FAVOURITE',
            isSPLP: outcome.details.isSPLP,
            pricesAvailable: outcome.details.pricesAvailable,
            outcomeId: outcome.id,
            removed: outcome.removed
          });
        }
      });
    } else if (type === 'SGL' && bet.price.type === 'DIVIDEND') {
      // Forecast or Tricast
      const leg = bet.legs[0];
      const outcomes = _.pluck(leg.parts, 'outcome');
      const outcome = outcomes[0];
      infoObj.combiType = leg.combi;
      infoObj.combiName = `${leg.combi}${bet.lines > 1 ? '_COM' : ''}`;
      infoObj.price = bet.sportsLegPriceService.convert(bet.legs[0].price);
      infoObj.isSP = true;
      infoObj.isFCTC = true;
      infoObj.outcomes = outcomes;
      infoObj.outcomeId = _.pluck(outcomes, 'id').join('|');
      infoObj.time = new Date(outcome.details.info.time);
      infoObj.localTime = outcome.details.info.localTime;
      infoObj.eventName = outcome.details.info.event;
      infoObj.sport = outcome.details.info.sport;
      const badOutcome = outcomes.find(_outcome => _outcome.errorMsg);
      if (badOutcome) {
        infoObj.error = infoObj.error || badOutcome.error;
        infoObj.errorMsg = infoObj.errorMsg || badOutcome.errorMsg;
      }
    } else {
      infoObj.outcomes = [];
      infoObj.isSP = false;
      _.each(bet.legs, (leg: any) => {
        if (leg.parts[0].outcome.details) {
          const prices = _.extend({}, leg.parts[0].outcome.prices[0], {
              priceType: leg.price.type
            }),
            eachWay = leg.parts[0].outcome.details.eachwayCheckbox,
            outcome: Partial<IOutcome> = {
              price: prices,
              isEachWayAvailable: Boolean(eachWay),
              eachWayFactorDen: eachWay ? eachWay.eachwayPriceDen : '',
              eachWayFactorNum: eachWay ? eachWay.eachwayPriceNum : ''
            };
          if (leg.price.type === 'SP') {
            infoObj.isSP = true;
          }
          infoObj.outcomes.push(outcome);
        }
      });
    }

    // Single bet
    if (infoObj.type === 'SGL' && !infoObj.combiType) {
      infoObj.outcomeIds = [infoObj.outcomeId];
      // Forecasts, tricasts, combicasts and other bet types containing many outcomes
    } else if (bet.type === 'SGL' && infoObj.combiType) {
      infoObj.outcomeIds = infoObj.outcomes.map(outcome => outcome.id);
      // multiples
    } else {
      infoObj.outcomeIds = bet.legs.map(leg => leg.firstOutcomeId);
    }

    infoObj.isSuspended = /_SUSPENDED$/.test(infoObj.error);

    infoObj.id = `${infoObj.combiName || type}|${infoObj.outcomeIds.join('|')}`;
    infoObj.Bet.storeId = infoObj.id;

    return infoObj;
  }

  storeOldPrices(outcome: IOutcome, payload: IBetPayout): void {
    const oldP = this.fracToDec.getDecimal(outcome.prices[0].priceNum, outcome.prices[0].priceDen),
      newP = this.fracToDec.getDecimal(parseInt(<string>payload.lp_num, 10), parseInt(<string>payload.lp_den, 10)),
      isPriceChangeUp = +oldP < +newP;
    outcome.oldModifiedPrice = _.extend({ isPriceChangeUp, isPriceChangeDown: !isPriceChangeUp }, outcome.prices[0]);
  }

  static updateOriginalPrices(outcome: IOutcome, payload: IBetPayload): void {
    if (outcome.originalPrice) {
      outcome.originalPrice.priceDen = <number>payload.lp_den || outcome.prices[0].priceDen;
      outcome.originalPrice.priceNum = <number>payload.lp_num || outcome.prices[0].priceNum;
    }
  }

  static setPriceData(bet: Bet, leg: ILeg, outcome: IOutcome, payload: IBetPayload): void {
    if ((payload.lp_den && payload.lp_num) || outcome.originalPrice) {
      outcome.prices[0].priceDen = <number>(payload.lp_den || outcome.originalPrice.priceDen);
      outcome.prices[0].priceNum = <number>(payload.lp_num || outcome.originalPrice.priceNum);
      outcome.prices[0].priceDec = bet.fracToDec.getDecimal(outcome.prices[0].priceNum, outcome.prices[0].priceDen);
    }
    const price = outcome.prices[0];
    if (price) {
      leg.selection.price.props = leg.selection.price.props || {};
      leg.selection.price.props.priceNum = price.priceNum;
      leg.selection.price.props.priceDen = price.priceDen;
      leg.selection.price.props.priceDec = price.priceDec;
      leg.selection.selectionPrice.priceNum = price.priceNum;
      leg.selection.selectionPrice.priceDen = price.priceDen;
      leg.selection.selectionPrice.priceDec = price.priceDec;
      leg.selection.params.price.priceNum = price.priceNum;
      leg.selection.params.price.priceDen = price.priceDen;
      leg.selection.params.price.priceDec = price.priceDec;
      bet.price.props = bet.price.props || {};
      bet.price.props.priceNum = price.priceNum;
      bet.price.props.priceDen = price.priceDen;
      bet.price.props.priceDec = price.priceDec;
    }
  }

  makeHandicapChangeMsg(payload: IBetPayload, outcome: IOutcome, handicapValue: string|number): string {
    return payload.errorMsg || this.localeService.getString('bs.HANDICAP_CHANGED', [
      this.betslipFilters.handicapValueFilter(outcome.prices[0].handicapValueDec),
      this.betslipFilters.handicapValueFilter(<string>handicapValue)
    ]);
  }

  updateHandicap(leg: ILeg, outcome: IOutcome, payload: IBetPayload, handicapValue): void {
    Bet.setHandicapData(leg, outcome, payload, handicapValue, this);
  }

  static setHandicapData(leg: ILeg, outcome: IOutcome, payload: IBetPayload, handicapValue, bet: Bet): void {
    // set old value if it was not changed
    outcome.prices[0].handicapValueDec = handicapValue || outcome.prices[0].handicapValueDec;
    outcome.prices[0].rawHandicapValue = payload.raw_hcap || outcome.prices[0].rawHandicapValue;
    outcome.name = Bet.updateOutcomeName(handicapValue, outcome, bet);
    const handicapObj = {
      range: {
        type: 'MATCH_HANDICAP',
        low: handicapValue,
        high: handicapValue
      }
    };

    if (leg.selection.legParts[0].range && leg.parts[0].range) {
      leg.selection.legParts[0].range.high = handicapValue;
      leg.selection.legParts[0].range.low = handicapValue;
      leg.parts[0].range.low = handicapValue;
      leg.parts[0].range.high = handicapValue;
    } else {
      _.extend(leg.selection.legParts[0], handicapObj);
      _.extend(leg.parts[0], handicapObj);
    }
  }

  static updateOutcomeName(handicapValue: string, outcome: IOutcome, bet: Bet): string {
    const handicap = `(${bet.betslipFilters.handicapValueFilter(handicapValue)})`;
    return outcome.name.replace(/[(][-+]\d+.\d+[)]/g, handicap);
  }

  update(payload: IBetPayload, type: string): void {
    Bet.updateSelf(payload, type, this);
    if (this.legs[0].selection?.isFCTC && ((this.legs[0].selection.combi=="FORECAST" && payload.fc_avail=="N") || (this.legs[0].selection.combi=="TRICAST" && payload.tc_avail=="N"))) {
      const outcome = this.legs[0].parts[0].outcome;
      outcome.disabled = true;
      outcome.fc_avail = payload.fc_avail;
      outcome.tc_avail = payload.tc_avail;
      this.params.errs = [{ live: outcome.errorMsg }];
    }
  }

  // eslint-disable-next-line complexity
  static updateSelf(payload: IBetPayload, type: string, bet): void {
    // const bet = this;
    if (bet.type === 'SGL') {                     // since we update only singles
      let outcome = bet.legs[0].parts[0].outcome; // singles have only one leg
      let priceChange = false,
        handicapChange = false;
      if (bet.params.errs === undefined) {
        bet.params.errs = [];
      }
      const isFCTCSuspended = bet.legs[0].selection?.isFCTC && (outcome.fc_avail=="N" || outcome.tc_avail=="N");
      // Disable bet placement
      switch (type) {
        case 'outcome':

          // find changed outcome if bet is complex (forecast, tricast)
          if (bet.betComplexName && payload.unique_id) {
            outcome = _.find(bet.legs[0].parts, (part: ILegPart) => {
              return (part.outcome as IOutcome).id === payload.unique_id.replace(/_.+$/, '');
            }).outcome;
          }

          // update outcome status isStarted
          if (payload.started === 'Y') {
            outcome.details.info.isStarted = true;
          }

          // update prices only if they are not equal and not tricast/forecast
          if (outcome.prices.length && !payload.raw_hcap && payload.lp_den && !bet.betComplexName) {
            const areDifferentPrices = parseInt(outcome.prices[0].priceDen, 10) !== parseInt(<string>payload.lp_den, 10) ||
              parseInt(outcome.prices[0].priceNum, 10) !== parseInt(<string>payload.lp_num, 10);
            const isPlaceBetPriceError = payload.placeBet;

            if (areDifferentPrices) {
              priceChange = true;

              // show "price change" error message only for unsuspended markets/events/outcomes
              if ((outcome.details.outcomeStatusCode !== 'S' && outcome.details.marketStatusCode !== 'S' &&
                outcome.details.eventStatusCode !== 'S') || payload.status === 'A') {
                outcome.error = 'PRICE_CHANGED';
                outcome.handicapError = null;
                outcome.handicapErrorMsg = null;
              }

              bet.storeOldPrices(outcome, payload);
            }

            if (areDifferentPrices || isPlaceBetPriceError) {
              /**
               * do not update price if overask is in process
               * but trader has not made a decision yet
               */
              if (!(bet.overaskService.isInProcess && !bet.overaskService.hasTraderMadeDecision)) {
                Bet.updateOriginalPrices(outcome, payload);
                Bet.setPriceData(bet, bet.legs[0], outcome, payload);
                bet.pubSubService.publish('ODDS_BOOST_REBOOST');
              }
            }
          }

          // update handicap only if they are not equal
          if (outcome.prices.length && payload.raw_hcap &&
            (outcome.prices[0].handicapValueDec !== payload.hcap_values[outcome.outcomeMeaningMinorCode])) {
            /* if outcome is not disabled then we show handicap change msg
             one exception is when outcome is disabled at the moment, and we receive handicap update
             along with unsuspension status
            */
            if ((outcome.details.outcomeStatusCode !== 'S' && outcome.details.marketStatusCode !== 'S' &&
              outcome.details.eventStatusCode !== 'S') || payload.status === 'A') {
              /* handicap value for outcome.outcomeMeaningMinorCode === 'L'
              && 'H' should be the same(payload.hcap_values[H]) */
              const newHandicapValue = payload.hcap_values &&
                payload.hcap_values[outcome.outcomeMeaningMinorCode === 'L' ? 'H' : outcome.outcomeMeaningMinorCode]
                  .replace(/["'()+]/g, ''); // '(+2.0)' => '2.0'
              if (newHandicapValue !== outcome.prices[0].handicapValueDec) {
                outcome.handicapError = 'HANDICAP_CHANGED';
                outcome.handicapErrorMsg = bet.makeHandicapChangeMsg(payload, outcome, newHandicapValue);
                handicapChange = true;

                if (outcome.error === 'PRICE_CHANGED') {
                  outcome.error = null;
                  outcome.oldModifiedPrice = null;
                }
              }
              /* do not update handicap if overask is in process
               but trader has not made a decision yet
               */
              if (!(bet.overaskService.isInProcess && !bet.overaskService.hasTraderMadeDecision)) {
                Bet.setHandicapData(bet.legs[0], outcome, payload, newHandicapValue, bet);
              }
            }
          }

          if (payload.status === 'A') {
            const setMsg = payload.placeBet || outcome.error === 'PRICE_CHANGED';
            const isAlreadySuspended = outcome.errorMsg === bet.localeService.getString('bs.OUTCOME_SUSPENDED');
            outcome.details.outcomeStatusCode = 'A';
            outcome.error = setMsg ? outcome.error : null;
            outcome.errorMsg = setMsg && !isAlreadySuspended ? outcome.errorMsg : null;
          }
          if (payload.status === 'S' || outcome.details.outcomeStatusCode === 'S') {
            outcome.details.outcomeStatusCode = 'S';
            outcome.error = 'OUTCOME_SUSPENDED';
            outcome.errorMsg = bet.localeService.getString('bs.OUTCOME_SUSPENDED');
            bet.params.errs[0] = <IBetError>{ live: outcome.errorMsg };
            break;
          }

          // set err in case outcome is unsuspended but event is still suspended
          if (outcome.details.outcomeStatusCode !== 'S' && outcome.details.eventStatusCode === 'S') {
            outcome.error = 'SELECTION_SUSPENDED';
            outcome.errorMsg = bet.localeService.getString('bs.SELECTION_SUSPENDED');
            break;
          }
          // set err in case market and event are unsuspended but outcome still suspended
          if (outcome.details.outcomeStatusCode !== 'S' && outcome.details.eventStatusCode !== 'S' &&
            outcome.details.marketStatusCode === 'S') {
            outcome.errorMsg = bet.localeService.getString('bs.MARKET_SUSPENDED');
            break;
          }

          outcome.priceChange = priceChange || outcome.priceChange;
          outcome.handicapChange = handicapChange || outcome.handicapChange;
          outcome.details.outcomeStatusCode = 'A';

          if (isFCTCSuspended) {
            break;
          }
          if (!_.some(bet.legs[0].parts, (part: ILegPart) => !!(part.outcome as IOutcome).errorMsg)) {
            delete bet.params.errs;
          }
          break;
        case 'market':
          if (payload.status === 'S') {
            outcome.details.marketStatusCode = 'S';
            outcome.error = 'MARKET_SUSPENDED';
            outcome.errorMsg = bet.localeService.getString('bs.MARKET_SUSPENDED');
            bet.params.errs[0] = { live: outcome.errorMsg };
            break;
          }
          outcome.details.marketStatusCode = 'A';

          // set err in case market and outcome are unsuspended but event is still suspended
          if (outcome.details.marketStatusCode !== 'S' && outcome.details.eventStatusCode === 'S') {
            outcome.errorMsg = bet.localeService.getString('bs.SELECTION_SUSPENDED');
            break;
          }
          // set err in case market and event are unsuspended but outcome still suspended
          if (outcome.details.marketStatusCode !== 'S' && outcome.details.eventStatusCode !== 'S' &&
            outcome.details.outcomeStatusCode === 'S') {
            outcome.errorMsg = bet.localeService.getString('bs.OUTCOME_SUSPENDED');
            break;
          }
          if (isFCTCSuspended) {
            break;
          }
          bet.legs[0].parts.forEach(part => {
            part.outcome.error = null; // unsuspend selection in status is not 'S'
            part.outcome.errorMsg = null; // unsuspend selection in status is not 'S'
            part.outcome.handicapErrorMsg = null; // unsuspend selection in status is not 'S'
          });
          delete bet.params.errs;
          break;
        case 'event':
          if (payload.started) {
            if (payload.started === 'Y') {
              outcome.details.info.isStarted = true;
              Bet.updateOriginalPrices(outcome, payload);
              Bet.setPriceData(bet, bet.legs[0], outcome, payload);
            } else {
              outcome.details.info.isStarted = false;
              Bet.updateOriginalPrices(outcome, payload);
              Bet.setPriceData(bet, bet.legs[0], outcome, payload);
            }
          }

          if (payload.started === 'Y' && !outcome.details.isMarketBetInRun) {
            outcome.details.eventStatusCode = 'S';
            outcome.error = 'EVENT_STARTED';
            outcome.errorMsg = bet.localeService.getString('bs.EVENT_STARTED');
            bet.params.errs[0] = { live: outcome.errorMsg };
            break;
          }

          if (payload.status === 'S') {
            outcome.details.eventStatusCode = 'S';
            outcome.error = 'SELECTION_SUSPENDED';
            outcome.errorMsg = bet.localeService.getString('bs.SELECTION_SUSPENDED');
            bet.params.errs[0] = { live: outcome.errorMsg };
            break;
          } else if ((payload.started !== 'Y' || // unsuspend selection in status is not 'S' and not started
            (payload.started !== 'Y' && payload.status !== 'S') ||
            (outcome.details.isMarketBetInRun && payload.started === 'Y')) &&
            !outcome.outcomeSuspended && !outcome.marketSuspended) {
            outcome.details.eventStatusCode = 'A';
          }
          // set market err in case event is active but market is still suspended
          if (outcome.details.eventStatusCode !== 'S' && outcome.details.marketStatusCode === 'S') {
            outcome.error = 'MARKET_SUSPENDED';
            outcome.errorMsg = bet.localeService.getString('bs.MARKET_SUSPENDED');
            break;
          }
          // set outcome err in case event and market are unsuspended but outcome still suspended
          if (outcome.details.eventStatusCode !== 'S' && outcome.details.marketStatusCode !== 'S' &&
            outcome.details.outcomeStatusCode === 'S') {
            outcome.error = 'OUTCOME_SUSPENDED';
            outcome.errorMsg = bet.localeService.getString('bs.OUTCOME_SUSPENDED');
            break;
          }
          if (isFCTCSuspended) {
            break;
          }
          bet.legs[0].parts.forEach(part => {
            part.outcome.error = null; // unsuspend selection in status is not 'S'
            part.outcome.errorMsg = null; // unsuspend selection in status is not 'S'
            part.outcome.handicapErrorMsg = null; // unsuspend selection in status is not 'S'
          });
          delete bet.params.errs;
          break;
        case 'removed':
          outcome.disabled = true;
          outcome.error = 'SELECTION_REMOVED';
          outcome.errorMsg = bet.localeService.getString('bs.SELECTION_REMOVED', [payload.name]);
          outcome.removed = true;
          bet.params.errs[0] = { live: outcome.errorMsg };
          break;

        case 'noLiveServ':
          outcome.priceChange = false;
          // update prices only if they are not equal
          if (outcome.prices.length && (outcome.prices[0].priceDen !== payload.lp_den ||
            outcome.prices[0].priceNum !== payload.lp_num)) {
            Bet.setPriceData(bet, bet.legs[0], outcome, payload);
            outcome.priceChange = true;
          }
          outcome.error = 'PRICE_CHANGED';
          outcome.errorMsg = payload.errorMsg;

          if (payload.status === 'S' && !outcome.priceChange) {
            outcome.disabled = true;
            bet.params.errs[0] = { live: outcome.errorMsg };
          } else {
            if (isFCTCSuspended) {
              break;
            }
            outcome.disabled = false;
            delete bet.params.errs;
          }
          break;
        case 'stakeError':
          if (payload.type === 'max') {
            const maxLimit = payload.bet.stake && payload.bet.stake.max || bet.stake.params.max;
            if (payload.bet.combiName === 'SCORECAST') {
              bet.params.error = 'STAKE_TOO_HIGH';
              bet.params.errorMsg = bet.localeService.getString('bs.maxStake', [maxLimit, bet.user.currencySymbol]);
            } else {
              outcome.error = 'STAKE_TOO_HIGH';
              outcome.errorMsg = bet.localeService.getString('bs.maxStake', [maxLimit, bet.user.currencySymbol]);
            }
          } else if (payload.type === 'min') {
            // on bet placement this error is overridden by checkStake method in betslip component
            const minLimit = payload.bet.stake && payload.bet.stake.min || bet.stake.params.min;
            if (payload.bet.combiName === 'SCORECAST') {
              bet.params.error = 'STAKE_TOO_LOW';
              bet.params.errorMsg = bet.localeService.getString('bs.minStake', [minLimit, bet.user.currencySymbol]);
            } else {
              outcome.error = 'STAKE_TOO_LOW';
              outcome.errorMsg = bet.localeService.getString('bs.minStake', [minLimit, bet.user.currencySymbol]);
            }
          }
          outcome.stakeError = true;
          break;
        case 'clearError':
          bet.legs[0].parts.forEach(part => {
            part.outcome.error = null;
            part.outcome.errorMsg = null;
            part.outcome.handicapErrorMsg = null;
          });
          break;
        default:
          break;
      }
    } else {
      if (type === 'stakeError') {
        if (payload.type === 'max') {
          const maxLimit = payload.bet.stake && payload.bet.stake.max || bet.stake.params.max;
          bet.error = 'STAKE_TOO_HIGH';
          bet.errorMsg = bet.localeService.getString('bs.maxStake', [maxLimit, bet.user.currencySymbol]);
        } else if (payload.type === 'min') {
          const minLimit = payload.bet.stake && payload.bet.stake.min || bet.stake.params.min;
          bet.params.error = 'MINIMUM_STAKE';
          bet.params.errorMsg = bet.localeService.getString('bs.minStake', [minLimit, bet.user.currencySymbol]);
        }
      }
    }
  }

  getOddsBoostObj(): IFreebetObj {
    const id = { id: this.oddsBoost.id };
    const odds = {
      enhancedOdds: this.oddsBoost.enhancedOdds ? this.getMultipleOddsBoostObj() : [{
        documentId: this.legs[0].docId,
        priceNum: this.oddsBoost.enhancedOddsPriceNum,
        priceDen: this.oddsBoost.enhancedOddsPriceDen
      }]
    };

    return el('freebet', _.extend(id, odds));
  }

  private setBetTypeInfo(): void {
    this.typeInfo = '';

    if (this.type.startsWith('AC')) {
      this.typeInfo = this.localeService.getString(`bs.ACC_info`);
    } else if (/^(SS|DS)/.test(this.type)) {
      this.typeInfo = this.localeService.getString('bs.SSDS_info', [this.params.lines]);
    } else {
      this.typeInfo = this.localeService.getString(`bs.${this.type}_info`);
    }

    if (this.typeInfo === 'KEY_NOT_FOUND') {
      this.typeInfo = '';
    }
  }
  
 /**
  * when place bet with 'WinOrEACH_WAY' condition we need sent documentId as even numbers
  * @returns Object: {documentId:, priceNum, priceDen }
  */
 private getMultipleOddsBoostObj() {
   return this.legs[0].winPlace === 'EACH_WAY' ? _.each(this.oddsBoost.enhancedOdds, (item, index) => {
     item.documentId = this.legs[index].docId;
   }) : this.oddsBoost.enhancedOdds;
  }
}
