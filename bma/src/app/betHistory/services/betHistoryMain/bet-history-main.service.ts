import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import {
  Observable, of as observableOf, empty, throwError, from
} from 'rxjs';
import { map, expand, reduce, concatMap, mergeMap } from 'rxjs/operators';

import { BetHistoryApiModule } from '@betHistoryModule/bet-history-api.module';
import { LocaleService } from '@core/services/locale/locale.service';
import { betHistoryConstants } from '../../constants/bet-history.constant';
import { TimeService } from '@core/services/time/time.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { UserService } from '@core/services/user/user.service';
import environment from '@environment/oxygenEnvConfig';
import { ICategoriesData } from '@shared/models/categories-data.model';
import { CommandService } from '@core/services/communication/command/command.service';
import { IDateRangeObject } from '../../models/date-object.model';
import { IBetHistorySingleSummary } from '../../models/bet-win-history-summary.model';
import { YourCallHistoryBetBuilderService } from '../../services/yourCallHistoryBetBuilder/your-call-history-bet-builder.service';
import { IRegularBetStatuses } from '../../models/regular-bet-statuses.model';
import { IYourCallBetStatuses } from '../../models/your-call-bet-statuses.model';
import {
  IBppRequest, IAccountHistoryResponse, IGetBetHistoryRequest, IPrice,
  IPotentialPayout, IRemovedLegsMap
} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBetHistoryBet, IBetHistoryLeg, IBetHistoryPart, IPageBets,
  IDetailedBetObject, IBetReturns, IBetReturnsValue, IBetHistoryHandicap,
  IBetHistoryEachWayTerms, IBetHistoryStake, IBetCount, ICelebration, ISiteCoreBanner } from '../../models/bet-history.model';
import { IBetHistoryOutcome, IOutcomeResult } from '@core/models/outcome.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import TotePotPoolBet from '@app/betHistory/betModels/totePotPoolBetClass/TotePotPoolBetClass';
import TotePoolBet from '@betHistoryModule/betModels/totePoolBet/tote-pool-bet.class';
import { ISwitcherConfig } from '@app/core/models/switcher-config.model';
import { SportsConfigHelperService } from '@sb/services/sportsConfig/sport-config-helper.service';
import { CHANNEL } from '@shared/constants/channel.constant';
import { ICashOutBet, ICashOutBetLeg } from '@app/betHistory/models/bet-history-cash-out.model';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { VanillaApiService } from '@frontend/vanilla/core';
import { ISiteCoreTeaserFromServer } from '@app/core/models/aem-banners-section.model';
import { ISystemConfig } from '@app/core/services/cms/models';
import { CmsService } from '@app/core/services/cms/cms.service';

/**
 * Service which provide fetching event functionality
 */
@Injectable({ providedIn: BetHistoryApiModule })
export class BetHistoryMainService {
  poolType: ISwitcherConfig;
  lottoType: ISwitcherConfig;
  regularType: ISwitcherConfig;

  // Set YC bet statuses
  readonly ycBetStatuses: IYourCallBetStatuses = betHistoryConstants.ycBetStatuses;
  /**
   * Statuses for regular resulted bets
   * @type {{N: {-: string, P: string, L: string}, Y: {L: string, W: string, V: string, P: string}}}
   */
  readonly regularResultStatuses: IRegularBetStatuses = {
    N: {
      '-': 'pending',
      P: 'placed',
      L: 'lost'
    },
    Y: {
      L: 'lost',
      W: 'won',
      V: 'void',
      P: 'placed'
    }
  };

  /**
   * Statuses for tote resulted bets
   * @type {{-: string, L: string, W: string, V: string, P: string}}
   */
  readonly toteResultStatuses: object = {
    '-': 'pending',
    L: 'lost',
    W: 'won',
    V: 'void',
    P: 'placed'
  };

  readonly categoriesData: ICategoriesData;

  constructor(
    private locale: LocaleService,
    private timeService: TimeService,
    private filterService: FiltersService,
    private bppService: BppService,
    private userService: UserService,
    protected commandService: CommandService,
    protected yourCallHistoryBetBuilder: YourCallHistoryBetBuilderService,
    private coreTools: CoreToolsService,
    private sportsConfigHelperService: SportsConfigHelperService,
    private windowRef: WindowRefService,
    private cmsService: CmsService,
    private vanillaApiService: VanillaApiService,
  ) {
    this.categoriesData = environment.CATEGORIES_DATA;
  }

  extendCashoutBets(bets) {
    (bets || []).forEach(bet => bet.betId = bet.betId ? bet.betId : bet.id);
  }

  /*
   * Wrapper for getHistory function, set date range for year.
   * @param {string} filter
   * @param {string} betType
   * @return {promise}
   */
  getHistoryForYear(filter: string, betType: string): Observable<IPageBets> {
    const d = new Date(),
      newFromDate = this.filterService.date(new Date(d.setFullYear(d.getFullYear() - 1)), 'yyyy-MM-dd HH:mm:ss');
    return this.getHistory(newFromDate, filter, this.getSettleType(betType));
  }

    /*
   * Wrapper for getBetsCount function, set date range for year.
   * @param {string} filter
   * @param {string} betType
   * @return {promise}
   */
  getBetsCountForYear(filter: string, betType: string): Observable<IBetCount> {
    const date = new Date(),
      newFromDate = this.filterService.date(new Date(date.setFullYear(date.getFullYear() - 1)), 'yyyy-MM-dd HH:mm:ss');

    return this.getBetsCount(newFromDate, filter, this.getSettleType(betType));
  }

  /*
   * Wrapper for getHistory function, set date range for year.
   * @param {string} filter
   * @param {string} betType
   * @return {promise}
   */
  getHistoryForTimePeriod(filter: string, betType: string, dateObject): Observable<IPageBets> {
    return this.getHistory(dateObject, filter, this.getSettleType(betType));
  }

  /*
   * Getting bet history.
   *
   * @param {date} date or dateObject with from and to dates
   * @param {string} filter
   * @param {boolean} settled
   * @return {promise}
   */
  getHistory(date: IDateRangeObject | string, filter: string, settled: string): Observable<IPageBets> {
    const reqObject = {
      detailLevel: 'DETAILED',
      fromDate: (date as IDateRangeObject).startDate || date,
      toDate: (date as IDateRangeObject).endDate || this.filterByParam('filteredToDate'),
      group: (filter && filter.toUpperCase()) || 'BET',
      pagingBlockSize: '20'
    };

    if (settled) {
      _.extend(reqObject, { settled });
    }

    return this.createRequest((reqObject as IGetBetHistoryRequest),
        response => this.normalizeResponse(response)) as Observable<IPageBets>;
  }

  /*
   * Getting bets count.
   *
   * @param {date} date or dateObject with from and to dates
   * @param {string} filter
   * @param {boolean} settled
   * @return {promise}
   */
  getBetsCount(date: IDateRangeObject | string, filter: string, settled: string): Observable<IBetCount> {
    let reqObject = {
      fromDate: (date as IDateRangeObject).startDate || date,
      toDate: (date as IDateRangeObject).endDate || this.filterByParam('filteredToDate'),
      group: (filter && filter.toUpperCase()) || 'BET',
      pagingBlockSize: '20'
    };

    if (settled) {
      reqObject = Object.assign({}, reqObject, { settled });
    }

    return this.createRequest(reqObject as IGetBetHistoryRequest, null, '/count') as Observable<IBetCount>;
  }

  /*
   * Getting detailed bet info.
   *
   * @param {string} id
   * @return {promise}
   */
  getBet(id: string): Observable<IBetHistoryBet> {
    return this.createRequest(id) as Observable<IBetHistoryBet>;
  }

  /*
   * Getting next page of bet history.
   *
   * @param {string} pageToken
   * @param {string} filter
   * @param {string} timeStamp
   * @return {promise}
   */
  getHistoryPage(pageToken: string, betType: string): Observable<IPageBets> {
    const reqObject = {
      detailLevel: 'DETAILED',
      blockSize: '20',
      pagingToken: pageToken
    };

    return this.createRequest(reqObject, (response: IAccountHistoryResponse) => this.normalizeResponse(response))
      .pipe(concatMap((data: IPageBets) => {
        if (betType === 'settled') {
          return observableOf(data);
        } else {
          return this.getEditMyAccaHistory(data);
        }
      }));
  }

  getEditMyAccaHistory(data: IPageBets): Observable<IPageBets> {
    const betGroupId = _.compact(_.pluck(data.bets, 'betGroupId'));
    const pagingBlockSize = _.reduce(data.bets, (a: number, b: IBetHistoryBet) => b.betGroupOrder ? a + Number(b.betGroupOrder) + 1 : a, 0);

    if (!pagingBlockSize) {
      return observableOf(data);
    }

    const result = [];
    let reqObject: IGetBetHistoryRequest = {
      detailLevel: 'DETAILED',
      group: 'BET',
      pagingBlockSize: 20,
      betGroupId
    };

    return this.createRequest(reqObject)
      .pipe(
        expand((oldBet: IAccountHistoryResponse | any) => {
          if (oldBet.paging.token) {
            reqObject = {
              detailLevel: 'DETAILED',
              blockSize: '20',
              pagingToken: oldBet.paging.token
            };
            return this.createRequest(reqObject);
          } else {
            return empty();
          }
        }),
        reduce((acc: IBetHistoryBet[], x: IAccountHistoryResponse | any) => acc.concat(x.bet), result),
        map((oldBets: IBetHistoryBet[]) => {
          this.addRemovedLegs(data.bets, oldBets);
          return data;
        })
    );
  }

  getHistoryByBetGroupId(betGroupId: string): Observable<IPageBets> {
    const data: IGetBetHistoryRequest = {
      detailLevel: 'DETAILED',
      group: 'BET',
      pagingBlockSize: '20',
      betGroupId
    };
    return this.createRequest(data, res => this.normalizeResponse(res, false)) as Observable<IPageBets>;
  }

  addRemovedLegs(bets: IBetHistoryBet[], editedBets: IBetHistoryBet[]): void {
    const removedLegsMap = this.getRemovedLegs(editedBets);

    _.each(bets, (bet: IBetHistoryBet) => {
      const removedLegs = removedLegsMap[bet.id];
      if (removedLegs) {
        bet.leg = _.union(bet.leg, removedLegs);
      }
    });
  }

  getRemovedLegs(bets: IBetHistoryBet[]): IRemovedLegsMap {
    const removedLegsMap = {}; // { [key: betId]: legArray[{}] }
    const groupedBetEditHistory = _.groupBy(bets, (bet: IBetHistoryBet) => bet.betGroupId);

    _.each(groupedBetEditHistory, betList => {
      const removedBetLegs = [];
      const newBetLegIds = _.map(betList[0].leg, (leg: IBetHistoryLeg) => leg.part[0].outcome[0].id);

      _.each(betList, (bet: IBetHistoryBet) => {
        _.each(bet.leg, (leg: IBetHistoryLeg) => {
          const outcome = leg.part[0].outcome[0];

          if (!_.contains(newBetLegIds, outcome.id) && !_.some(removedBetLegs, legItem => legItem.part[0].outcome[0].id === outcome.id)) {
            leg.removedLeg = true;
            leg.resultedBeforeRemoval = this.isLegResultedBeforeRemoval(outcome, bet);

            if (leg.resultedBeforeRemoval) {
              removedBetLegs.unshift(leg);
            } else {
              removedBetLegs.push(leg);
            }
          }
        });
      });

      if (removedBetLegs.length) {
        removedLegsMap[betList[0].id] = removedBetLegs;
      }
    });
    return removedLegsMap;
  }

  /**
   * Check if bet is "simple" (not edited acca with last leg) single
   *
   * @param bet
   */
  isSingleBet(bet: IBetHistoryBet): boolean {
    return bet.betType === 'SGL' && !(bet.leg && bet.leg.length && bet.leg.some((l: IBetHistoryLeg) => l.removedLeg));
  }

  /**
   * @param eventName
   * @param eventStartTime
   * @returns {string}
   */
  formToteBetEventName(eventName: string, eventStartTime: string): string {
    const raceLocalTime = this.filterService.getTimeFromName(eventName),
      userLocalTime = this.timeService.getLocalHourMin(eventStartTime),
      name = this.filterService.clearEventName(eventName),
      localTime = raceLocalTime.length > 0 ? raceLocalTime : userLocalTime;

    return `${localTime} ${name}`;
  }

  /*
   * Create object of detailed bet for view.
   * TODO seems not in use - remove?
   * @param {object} data
   * @param {boolean} isPoolBet
   * @return {object} betInfo
   */
  getDetailedBetObject(data: IBetHistoryBet, isPoolBet: boolean): IDetailedBetObject {
    const betInfo: IDetailedBetObject = {
        betType: data.betType && (data.betType as { name: string; }).name,
        poolType: data.poolType && this.getPoolType(data.poolType),
        poolName: data.poolName && this.getPoolName(data.poolName),
        lines: data.numLines,
        receipt: data.receipt,
        stake: ((data.stake as IBetHistoryStake).value - (data.stake as IBetHistoryStake).tokenValue).toFixed(2),
        totalStake: (data.stake as IBetHistoryStake).value,
        tokenValue: (data.stake as IBetHistoryStake).tokenValue,
        winLines: data.numLinesWin,
        currency: this.userService.currencySymbol,
        legs: [],
        numLegs: data.numLegs
      },
      legArr = data.leg || data.poolLeg;

    _.forEach((legArr), (leg: IBetHistoryLeg) => {
      const legPart = leg.part || leg.poolPart;
      let handicapRawValue;
      _.forEach(legPart, (part: IBetHistoryPart) => {
        if (part.handicap && part.handicap.length > 0) {
          handicapRawValue = part.handicap[1];
        }
        if (part.eachWayTerms) {
          part.eachWayTerms = part.eachWayTerms[0];
        }

        if (isPoolBet) {
          if (betInfo.poolType === 'Football') {
            this.collectFootballPoolLegs(betInfo, part.outcome.name, leg.name, leg.startTime, part.outcome.outcomeResult);
          } else {
            this.collectTotePoolLegs(betInfo, leg, part.outcome);
          }
        } else {
          betInfo.legs.push(this.collectLegs(part.outcome[0], part.price[0], handicapRawValue,
            leg.legType.code, (part.eachWayTerms as IBetHistoryEachWayTerms)));
        }
      });
    });

    return betInfo;
  }

  /*
   * Create object of general bet history for view.
   * TODO seems not in use - remove?
   * @param {array} betHistory
   * @param {object} betIds
   *
   * @return {object}
   */
  createBetObject(betHistory: IBetHistoryBet[], betIds: object[]): any {
    const result = {
      betDetails: [],
      betIds
    };
    _.forEach(betHistory, (bet: IBetHistoryBet) => {
      if ((bet.leg && !bet.leg[0]) && !bet.poolLeg) {
        return;
      }

      const status = this.getBetStatus(bet),
        returns = this.getBetReturns(bet, status),
        freeBetValue = (bet.stake as IBetHistoryStake).tokenValue,
        stakeValue = (bet.stake as IBetHistoryStake).poolStake || (bet.stake as IBetHistoryStake).value,
        stake = freeBetValue ? stakeValue - freeBetValue : stakeValue,
        totalStake = stakeValue,
        unitStake = stake / bet.numLines,
        resultBet = {
          betId: bet.id,
          timeStamp: bet.timeStamp, // TODO: check if needed during conversion
          date: bet.date,
          cashedOut: bet.status === 'C',
          status,
          betType: this.getBetType(bet.betType && (bet.betType as { name: string; }).name, bet.leg && bet.leg[0].legType.code),
          poolType: bet.poolType && this.getPoolType(bet.poolType),
          poolName: bet.poolName && this.getPoolName(bet.poolName),
          sortType: this.getSortCode(bet.leg),
          selections: (bet.leg && this.getSelectionNames(bet.leg, bet.legType)) || (bet.poolLeg && this.collectPoolSelections(bet.poolLeg)),
          currency: this.userService.currencySymbol,
          stake: totalStake !== freeBetValue && stake,
          freebet: freeBetValue > 0 && freeBetValue,
          returns: returns.value,
          returnsStatus: returns.status,
          unitStake,
          totalStake,
          ycBet: bet.ycBet,
          ycStatus: bet.ycStatus,
          manualBetDetail: bet.manualBetDetail,
          externalRefId: bet.externalRefId
        };

      // do not include overask pending bets
      if (resultBet.status !== 'pending') {
        result.betDetails.push(resultBet);

        if (!betIds[bet.id]) {
          result.betIds[bet.id] = {};
        }
      }
    });

    return result;
  }

  /*
   * Set status of the bet.
   *
   * @param {object} bet
   * @return {string} e.g. 'Settled'
   */
   // tslint:disable-next-line: cyclomatic-complexity
   getLottoBetStatus(draws: any){
    const winnings = draws.some(item => item.winnings && parseFloat(item.winnings.value) > 0)
    return winnings ? 'won' : 'lost';
   }

   // eslint-disable-next-line complexity
   getBetStatus(bet: IBetHistoryBet): string {
    if (bet.ycBet) {
      return this.getYCBetStatus(bet);
    }

    const settled = bet.settled === 'Y',
      pending = bet.status === 'P',
      winnings = bet.winnings &&
        (+bet.winnings.value > 0 || (bet.winnings[0] && bet.winnings[0].value > 0)) &&
        bet.numLinesWin !== '0',
      refund = bet.refund && (+bet.refund.value > 0 || (bet.refund[0] && bet.refund[0].value > 0)),
      cancelled = ((bet.numLinesVoid === '1') || (bet.status === 'X' || refund)),
      cashedOut = bet.status === 'C';

    const isWonEWPlaceBet = bet.leg && bet.leg.length && bet.leg.map((leg: IBetHistoryLeg, index: number) => {
      let isWonEWPlaceLeg = false;
      if (this.coreTools.getOwnDeepProperty(bet, `leg[${index}].part[0].outcome.length`, null)) {
        const partPath = bet.leg[index].part[0],
          eWTerms = partPath.eachWayTerms && partPath.eachWayTerms[0].eachWayPlaces;
        isWonEWPlaceLeg = bet.legType === 'E' && partPath.outcome[0].result.value === 'P' &&
          Number(partPath.outcome[0].result.places) <= Number(eWTerms);
      }
      return isWonEWPlaceLeg;
    }).every(isWonEWPlaceLeg => isWonEWPlaceLeg);

    switch (true) {
      case (pending):
        return 'pending'; // Overask bet, referred to the trader
      case (!settled):
        return 'open'; // Settled means bet has result
      case (cashedOut):
        return 'cashed out';
      case (winnings):
      case (isWonEWPlaceBet):
        return 'won';
      case (cancelled):
        return 'void'; // Stake is cancelled if there are refunds
      default :
        return 'lost'; // Stake is lost in other cases
    }
  }

  /**
   * Extract parameters from bet needed to form returns status and value
   * @param {Object} bet from SS OXI
   * @returns {{returns: Number as float, refund: Number as float, estReturn: Number as float}}
   */
  extractBetTypeReturnsParams(bet: IBetHistoryBet): IBetReturns {
    const betType = bet.poolType || bet.lotteryName;
    return {
      returns: betType ? bet.winnings && bet.winnings.value : bet.winnings && bet.winnings[0].value,
      refund: betType ? bet.refund && bet.refund.value : bet.refund && bet.refund[0].value,
      estReturn: betType ? bet.potentialPayout && +(bet.potentialPayout as IPotentialPayout).value : bet.potentialPayout &&
        +bet.potentialPayout[0].value
    };
  }

  getBetReturnsValue(bet: IBetHistoryBet, betStatus: string): IBetReturnsValue {
    const { returns, refund, estReturn } = this.extractBetTypeReturnsParams(bet);
    let status, value;

    if ((betStatus === 'lost' || betStatus === 'void') && (bet.poolType || bet.status !== 'X')) {
      value = refund || 0;
      status = 'refund';
    } else if (returns && returns > 0) {
      value = returns;
      status = 'returns';
    } else if (estReturn && estReturn > 0) {
      value = estReturn;
      status = 'estimate';
    } else {
      return { value: 'N/A', status: 'none' };
    }

    return { value, status };
  }

  /**
   * Return simplified pool type
   * @param {string} poolType
   * @returns {string}
   */
  getPoolType(poolType: string): string {
    return poolType === 'Football pool' ? 'Football' : 'Tote';
  }

  /**
   * Return translated pool name;
   * @param {string} name
   * @returns {string}
   */
  getPoolName(name: string): string {
    const totePoolIndex = name.indexOf('-Pool-'),
      poolName = totePoolIndex !== -1 ? name.slice(totePoolIndex + 6) : name.replace(/\s/g, ''),
      poolTranslation = this.locale.getString(`bs.${poolName}`);

    return `Tote ${poolTranslation} Pool`;
  }

  /*
   * Set sort code name if sort code related to tricasts/forecass.
   *
   * @param {array} leg
   * @return {string} e.g. 'Reverse Tricast'
   */
  getSortCode(legs: IBetHistoryLeg[]): string {
    const sortCode = legs && legs[0] && (legs[0].legSort as { code: string; }).code,
      sortCodeValues = ['SF', 'CF', 'RF', 'TC', 'CT', 'ES'];
    return _.contains(sortCodeValues, sortCode) ? this.locale.getString(`bs.${sortCode}`) : '';
  }

  /**
   * Determine combined parts result code for multi-part bet (BetBuilder single bet):
   * The precedence of result codes is the following: L > V > - > W
   *   e.g. result will be 'V' (void), if any item is 'V' and combination doesn't contain 'L'.
   * If provided combination contains any other result code, its first item is returned (as by default for non-BYB bet)
   * @param {string[]} results
   * @returns {string}
   */
  getPartsResult(results: string[]): string {
    const hasResults = { L: false, W: false, V: false, '-': false, other: false };

    results.forEach((code: string): void => {
      const key = hasResults.hasOwnProperty(code) ? code : 'other';
      hasResults[key] = true;
    });

    switch (true) {
      case hasResults.other:
        return results[0];
      case hasResults.L:
        return 'L';
      case hasResults.V:
        return 'V';
      case hasResults['-']:
        return '-';
      case hasResults.W:
        return 'W';
    }
  }

  /**
   * @param {Array} legs
   * @returns {Array} of selection details objects
   */
  collectPoolSelections(legs: IBetHistoryLeg[]): any {
    return legs.map(leg => {
      return {
        selectionName: leg.poolPart[0].outcome.name,
        selectionPrice: {},
        selectionStartTime: leg.startTime,
        eventName: this.formToteBetEventName(leg.name, leg.startTime),
        track: leg.track
      };
    });
  }

  /**
   * Form profit/loss info
   */
  calculateTotals(totalBets: number, totalWins: number, label?: string): IBetHistorySingleSummary {
    return {
      totalStakes: this.filterService.numberWithCurrency(totalBets),
      totalReturns: this.filterService.numberWithCurrency(totalWins),
      profit: this.filterService.numberWithCurrency(totalWins - totalBets),
      iconClass: (totalWins > totalBets ? 'arrow-right-up' :
                 (totalWins < totalBets ? 'arrow-left-down' : '')),
      label: label ? this.locale.getString(`bethistory.${label}`) : ''
    };
  }

  /**
   * Generates bets map
   * @param {Array} bets - array of bets
   * @returns {Object} - bets map
   */
  generateBetsMap(bets: (TotePotPoolBet | TotePoolBet | IBetHistoryBet)[])
  : { [key: string]: (TotePotPoolBet | TotePoolBet | IBetHistoryBet)} {
    const betsMap = {};
    _.forEach(bets, (bet: IBetHistoryBet) => {
      betsMap[bet.id] = bet;
    });
    return betsMap;
  }

  makeSafeCall(observableWrapper: Observable<IPageBets>): Observable<IPageBets> {
    return this.userService.isInShopUser() ? observableOf({ bets: [] } as IPageBets) : observableWrapper;
  }

  buildSwitchers(clickHandler: Function): ISwitcherConfig[] {
    this.regularType = {
      viewByFilters: 'bet',
      name: this.locale.getString('bethistory.sports'),
      onClick: filter => clickHandler(filter)
    };
    this.lottoType = {
      viewByFilters: 'lotteryBet',
      name: this.locale.getString('bethistory.lotto'),
      onClick: filter => clickHandler(filter)
    };
    this.poolType = {
      viewByFilters: 'poolBet',
      name: this.locale.getString('bethistory.pool'),
      onClick: filter => clickHandler(filter)
    };
    return [this.regularType, this.lottoType, this.poolType];
  }

  getSwitcher(switcherName: string): ISwitcherConfig {
    return this[switcherName];
  }

  setBybLegStatus(bet: IBetHistoryBet | ICashOutBet, leg: IBetHistoryLeg | ICashOutBetLeg): void {
    if ([CHANNEL.byb, CHANNEL.fiveASide].includes(bet.source) && leg.eventEntity) {
      leg.status = { A: 'open', S: 'suspended' }[leg.eventEntity.eventStatusCode];
    }
  }

  showFirstBet(filter: string): void {
    const firstBetElement = this.windowRef.document.getElementsByClassName('firstBet');
    const ElementsLength = firstBetElement.length;
    if (!ElementsLength) {
      return;
    }

    for (let i = 0; i < ElementsLength; i++) {
      filter === 'shopBet'? firstBetElement[i].classList.add('display-none') : firstBetElement[i].classList.remove('display-none');
    }
  }

  /**
   * Collect tote data for Pools
   * @param {Array} leg
   * @param {object} betInfo
   * @param {object} outcome
   */
  private collectTotePoolLegs(betInfo: IDetailedBetObject, leg: IBetHistoryLeg, outcome: IBetHistoryOutcome): void {
    betInfo.legs.push({
      event: this.formToteBetEventName(leg.name, leg.startTime),
      track: outcome.name,
      originalName: leg.name,
      eventId: '',
      eventDate: leg.startTime,
      outcomeName: outcome.name || leg.poolPart[0].outcome.name,
      result: this.toteResultStatuses[leg.poolPart[0].outcome.outcomeResult] || 'void'
    });
  }

  /*
 * Collect legs data for Pools
 * @param {number} outcomeName
 * @param {string} eventName
 * @param {date} startTime
 * @param {string} outcomeResult
 */
  private collectFootballPoolLegs(betInfo: IDetailedBetObject, outcomeName: string, eventName: string, startTime: string,
                                  outcomeResult: string): void {
    const legObj = {
      name: eventName,
      type: this.setSelection(outcomeName),
      startTime,
      outcomeResult
    };
    let newLegs;
    betInfo.legs.push(legObj);

    if (betInfo.numLegs <= betInfo.legs.length) {
      newLegs = _.map(_.groupBy(betInfo.legs, 'name'), values => {
        return _.reduce(values, (leg, legs) => {
          for (const key in legs) {
            if (key !== 'name' && key !== 'startTime') {
              leg[key] = _.toArray(((leg[key] || '') + legs[key]).replace(/,/g, ''))
                .sort((a, b) => a < b ? -1 : a > b ? 1 : 0)
                .reverse();
            }
          }
          return leg;
        });
      });

      betInfo.legs = newLegs;
    }
  }

  /*
   * Collect legs data of bets.
   *
   * @param {object} outcome
   * @param {object} price
   * @param {object} handicap
   * @param {object} legType
   * @param {object} ewTerms
   * @return {object} legObj
   */
  private collectLegs(outcome: IBetHistoryOutcome, price: IPrice, handicap: IBetHistoryHandicap,
                      legType: string, ewTerms: IBetHistoryEachWayTerms) {
    const format = {
        frac: `${price.priceNum}/${price.priceDen}`,
        dec: Number(price.priceDecimal).toFixed(2)
      },
      legObj = {
        event: outcome.event.name.replace(/[0-2]*[0-9]:[0-5][0-9] /g, ''),
        eventType: outcome.eventType.name,
        eventDate: outcome.event.startTime,
        eventClass: outcome.eventClass.name,
        marketName: outcome.market.name,
        legType,
        eventId: outcome.event.id,
        outcomeName: this.createOutcomeName(outcome, handicap),
        ewTerms: this.setEwTerms(ewTerms),
        priceNum: price.priceNum ? price.priceNum : '',
        priceDen: price.priceDen ? price.priceDen : '',
        odds: price.priceNum ? format[this.userService.oddsFormat] : 'SP',
        result: this.setLegResult(outcome.result)
      };

    this.sportsConfigHelperService.getSportPathByCategoryId(Number(outcome.eventCategory.id))
      .subscribe((sportPath: string) => {
        (<any>legObj).sportName = sportPath;
      });

    return legObj;
  }

  private isLegResultedBeforeRemoval(outcome: IBetHistoryOutcome, bet: IBetHistoryBet) {
    if (outcome.result && outcome.result.time) {
      return this.timeService.parseDateTime(outcome.result.time) < this.timeService.parseDateTime(bet.settledAt);
    }
    return false;
  }

  /*
   * Create outcome name with handicapValueDec value, if present
   * @param {object} outcome
   * @param {object} handicap
   * @return {string} name
   */
  private createOutcomeName(outcome: IBetHistoryOutcome, handicap: IBetHistoryHandicap): string {
    return handicap && handicap.value ? `${outcome.name}${this.filterService.makeHandicapValue(handicap.value, outcome)}` : outcome.name;
  }

  private setEwTerms(terms: IBetHistoryEachWayTerms): string {
    if (terms) {
      const eachWayPlacesNumber = Number(terms.eachWayPlaces);
      terms.eachWayPlaces = _.range(1, eachWayPlacesNumber + 1).join(',');
    }
    return terms ? this.locale.getString('bs.ewTerms', terms) : this.locale.getString('bs.none');
  }

  /*
   * Get selection placed by user home draw or away team to win
   * @param {string} val
   * @return {string}
   */
  private setSelection(val: string): string {
    return {
      1: 'H',
      2: 'D',
      3: 'A'
    }[val];
  }

  /*
   * Determine the result of the leg
   * @param {string} confirmValue
   * @param {string} statusValue
   * @return {string} // e.g. 'win'
   */
  private setLegResult(res: IOutcomeResult): string {
    return this.regularResultStatuses[res.confirmed][res.value] || 'void';
  }

  /**
   * Set status of the YC bet.
   * @param {object} bet
   * @return {string} e.g. 'lost'
   */
  private getYCBetStatus(bet: IBetHistoryBet): string {
    switch (true) {
      case (bet.ycStatus === this.ycBetStatuses.lost):
        return 'lost';
      case (bet.ycStatus === this.ycBetStatuses.won):
        return 'won';
      case (bet.ycStatus === this.ycBetStatuses.void1):
      case (bet.ycStatus === this.ycBetStatuses.void2):
        return 'void'; // Stake is cancelled if there are refunds
      default :
        return 'open'; // Stake is Open/Pending
    }
  }


  /**
   * @param bet
   * @param betStatus
   * @returns {*} {value: 'value of returns', status: 'status of returns'}
   */
  private getBetReturns(bet: IBetHistoryBet, betStatus: string): IBetReturnsValue {
    const { value, status } = this.getBetReturnsValue(bet, betStatus);

    let valueCurrency = Number(value).toFixed(2);
    valueCurrency = this.filterService.currencyPosition(valueCurrency, this.userService.currencySymbol);

    return { value: valueCurrency, status };
  }

  /*
   * Set bet type label.
   *
   * @param {string} betType
   * @param {string} legType
   * @return {string} // e.g. ' Trixie (To Win)'
   */
  private getBetType(betType: string, legType: string): string {
    return betType + this.locale.getString(legType ? `bs.to${legType}` : 'W');
  }

  /*
   * Set selection names array. Modifies them if needed.
   *
   * @param {array} legs
   * @return {array}
   */
  private getSelectionNames(legs: IBetHistoryLeg[], legType: string) {
    let selectionName,
      selectionPrice: IPrice | string = '';

    return _.map(legs, (leg: IBetHistoryLeg) => {
      switch ((leg.legSort as { code: string; }).code) {
        case 'SC': // Scorecast
          // Stenhousemuir 3-2 Beau Logridge 5/1
          selectionName = `${leg.part[0].outcome[0].name} ${leg.part[1].outcome[0].name}`;
          selectionPrice = leg.part[0].price[0];
          break;

        case 'SF': // Forecast
        case 'RF': // Reverse Forecast
        case 'CF': // Combination Forecast
        case 'TC': // Tricast
        case 'ES': // Banach
        case 'CT': // Combination Tricast
          selectionName = _.map(leg.part, (p: IBetHistoryPart) => p.outcome[0].name);
          break;
        case '--': // SGL/MLTPL
        default:
          selectionName = leg.part[0].outcome[0].name;
          selectionPrice = leg.part[0].price[0];
          break;
      }

      return {
        selectionName,
        selectionPrice,
        selectionStartTime: leg.part[0].outcome[0].event.startTime,
        eventName: leg.part[0].outcome[0].event.name
      };
    });
  }

  /**
   * Extend outcomes with outcomeMeaningMinorCode property,
   * which are missed for accountHistory response
   * @param poolBets
   * @private
   */
  private extendWithMeaningMinorCode(poolBets: IBetHistoryBet[]): IBetHistoryBet[] {
    const unnamedFavouriteName = 'unnamed favourite',
      secondFavouriteName = 'unnamed 2nd favourite';

    _.forEach(poolBets, (poolBet: IBetHistoryBet) => {
      _.forEach(poolBet.poolLeg, (poolLegEntity: IBetHistoryLeg) => {
        _.forEach(poolLegEntity.poolPart, (poolPartEntity: IBetHistoryPart) => {
          const outcomeName = poolPartEntity.outcome.name.toLowerCase();
          switch (outcomeName) {
            case unnamedFavouriteName: poolPartEntity.outcome.outcomeMeaningMinorCode = '1';
              break;
            case secondFavouriteName: poolPartEntity.outcome.outcomeMeaningMinorCode = '2';
              break;
            default: poolPartEntity.outcome.outcomeMeaningMinorCode = undefined;
          }
        });
      });
    });
    return poolBets;
  }

  /**
   * Set response into the key named bets.
   *
   * @param {object} data
   * @return {object} {bets : {array}, pageToken: {string}}
   */
  public normalizeResponse(data: IAccountHistoryResponse, excludeEdited: boolean = true): Promise<IPageBets> {
    const poolBets = data.poolBet ? this.extendWithMeaningMinorCode((data.poolBet as IBetHistoryBet[])) : undefined,
      bets = {
        bets: ((data.bet) || (<IBetHistoryBet[]>data.lottoBetResponse) || (<IBetHistoryBet[]>data.lotteryBet) || poolBets || []),
        pageToken: data.paging && data.paging.token
      },
      YCBets = [];

    _.each(data.bet, (bet: IBetHistoryBet) => {
      if ('externalRefId' in bet) {
        YCBets.push(this.commandService.executeAsync(this.commandService.API.GET_YC_BETS, [bet.externalRefId.value], []));
      }
    });

    // Exclude edited bets
    if (excludeEdited) {
      bets.bets = _.filter(bets.bets, (bet: IBetHistoryBet) => bet.settleInfoAttribute !== '&lt;is_edited&gt;');
    }

    return new Promise((resolve) => {
      Promise.all(YCBets)
        .then(result => {
          _.each(result, YCBet => this.mapYCBets(YCBet, bets));
          resolve(bets);
        }, error => {
          console.warn('Bet History:retrieving YC bets error: ', error);
          resolve(bets);
        });
    }).catch(() => {}) as Promise<IPageBets>;
  }

  /**
   *
   * @param YCBet
   * @param bets
   */
   private mapYCBets(YCBet: IBetHistoryBet, bets: IPageBets): void {
     if (YCBet.data && YCBet.data[0]) {
       _.each(bets.bets, (bet: IBetHistoryBet) => {
         // Find and build YC bet history object
         if ('externalRefId' in bet && parseInt(bet.externalRefId.value, 10) === parseInt(YCBet.data[0].id, 10)) {
           this.yourCallHistoryBetBuilder.extendHistoryBet(bet, YCBet);
         }
       });
     }
  }

  private getSettleType(betType: string): string {
    return { open: 'N', settled: 'Y' }[betType] || null;
  }

  // filter parameters
  // TODO switch by `param`!
  private filterByParam(param: string): string {
    const
      toDate = this.timeService.dateTimeOfDayInISO('tomorrow'),
      fromDate = this.timeService.dateTimeOfDayInISO('yesterday'),
      weekAgo = this.timeService.dateTimeOfDayInISO('weekAgo'),
      twoWeeksAgo = this.timeService.dateTimeOfDayInISO('twoWeeksAgo'),
      filters = {
        weekAgoDate: this.filterService.date(weekAgo, 'yyyy-MM-dd HH:mm:ss'),
        twoWeeksAgoDate: this.filterService.date(twoWeeksAgo, 'yyyy-MM-dd HH:mm:ss'),
        filteredFromDate: this.filterService.date(fromDate, 'yyyy-MM-dd HH:mm:ss'),
        filteredToDate: this.filterService.date(toDate, 'yyyy-MM-dd HH:mm:ss')
      };
    return filters[param];
  }

  /**
   * Creates request for retrieving bet history with given params.
   * @param {string|number|Object} data
   * @param {Function} transformFn
   * @param {string} url
   * @return {Promise}
   */
  public createRequest(
    data: IBppRequest,
    transformFn?: Function,
    url?: string
  ): Observable<IBetHistoryBet | IBetHistoryBet[] | IPageBets | IBetCount | unknown> {
    return (this.bppService.send('getBetHistory', data, url) as Observable<any>).pipe(
      mergeMap(res => {
        if (!res || !res.response) {
          throwError(res);
          return;
        }
        if (_.isFunction(transformFn)) {
          return from(transformFn(res.response.model));
        } else
          if (res.response.model) {
          return observableOf(res.response.model);
          } else {
            return observableOf(res.response);
        }
      }),
    );
  }
  /**
   * Gets banner from sitecore
   */
  getCelebrationBannerFromSiteCore(): Observable<ISiteCoreBanner[]> {
    const APIOPTIONS: {
      [name: string]: string;
    } = {
      'prefix': '/en/coralsports'
    };
    return this.vanillaApiService.get(betHistoryConstants.celebratingSuccess.bannerUrl, '', APIOPTIONS);
  }
  /**
   * Gets banner related information from CMS and sitecore
   */
  getCelebrationBanner(): ICelebration {
    let bannerUrl: string = '';
    let siteCoreBanner: ISiteCoreTeaserFromServer[];
    let celebration: ICelebration = {
      congratsBannerImage: '',
      displayCelebrationBanner: false,
      celebrationMessage: '',
      winningMessage: '',
      cashoutMessage: '',
      duration: 0
    };
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      if(config && config.CelebratingSuccess) {
        bannerUrl = config.CelebratingSuccess.celebrationBannerURL;
        celebration = config.CelebratingSuccess;
        if(celebration && celebration.displayCelebrationBanner) {
          this.getCelebrationBannerFromSiteCore().subscribe((response: ISiteCoreBanner[]) => {
            if (response?.length > 0) {
              const [teaserResponse] = response;
              siteCoreBanner = teaserResponse.teasers ?? [];
              siteCoreBanner.forEach((siteCoreData: ISiteCoreTeaserFromServer) => {
                if (siteCoreData.itemId === bannerUrl) {
                  celebration.congratsBannerImage = siteCoreData.backgroundImage.src+"?"+window.crypto.getRandomValues(new Uint16Array(1))[0];
                }
              });
              return celebration;
            }
          }, () => {
          });
        }
      }
    });
    return celebration;
  }
}
