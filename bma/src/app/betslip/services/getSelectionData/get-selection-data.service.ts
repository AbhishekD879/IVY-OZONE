import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import * as _ from 'underscore';
import { Observable } from 'rxjs';

import { IConstant } from '@core/services/models/constant.model';
import {
  IBetslipMarket,
  IBetslipEvent,
  IBetslipOutcome,
  ISelectionRealtedData
} from '@betslip/services/getSelectionData/get-selection-data.models';
import { IOutcome } from '@core/models/outcome.model';
import { IOutcomeDetailsResponse } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';

import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { TimeService } from '@core/services/time/time.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { BetslipBetDataUtils } from '@betslip/models/betslip-bet-data.utils';
import { BETSLIP_VALUES } from '@betslip/constants/bet-slip.constant';
import environment from '@environment/oxygenEnvConfig';
import { BetslipStorageService } from '@betslip/services/betslip/betslip-storage.service';

@Injectable({ providedIn: BetslipApiModule })
export class GetSelectionDataService {
  racingCodes: string[];
  outcomeData: any;

  private clearEventName: Function;
  private readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;
  constructor(
    private locale: LocaleService,
    private siteServerService: SiteServerService,
    private betslipStorageService: BetslipStorageService,
    private filter: FiltersService,
    private time: TimeService,
    private fracToDecService: FracToDecService
  ) {
    this.clearEventName = this.filter.clearEventName.bind(this.filter);
    this.fillRacingCodes();
  }

  /**
   * Get selections data from SS and parse it for rendering
   * return {Object} parsed data
   */
  getOutcomeData(outcomesIds: string[]): Observable<ISelectionRealtedData[]> {
    const ids: number[] = _.map(outcomesIds, (id: string) => Number(id));

    return Observable.create(observer => {
      (this.betslipStorageService.eventToBetslipObservable ?
        this.betslipStorageService.useEventToBetslipObservable().toPromise() :
      this.siteServerService.getEventsByOutcomeIds({ outcomesIds: ids, racingFormOutcome: true }))
        .then(data => {
          observer.next(this.getSelectionRelatedData(data as IBetslipEvent[]));
          observer.complete();
        })
        .catch(err => observer.error(err));
    });
  }

  createOutcomeData(outcomeDetail: IOutcomeDetailsResponse, selection: IBetSelection): Partial<IOutcome> {
    let rawHandicapValue;
    const unpipePoperties = ['name', 'marketDesc', 'eventDesc', 'typeDesc', 'className'];
    unpipePoperties.forEach((propertyName: string) => {
      if (outcomeDetail[propertyName]) {
        outcomeDetail[propertyName] = this.filter.removeLineSymbol(outcomeDetail[propertyName]);
      }
    });

    const timeParse = Date.parse(selection.details.info.time);
    const time = isNaN(timeParse) ? selection.details.info.time : timeParse;

    const raceLocalTime = this.filter.getTimeFromName(outcomeDetail.eventDesc),
      userLocalTime = this.time.getLocalHourMin(time);

    let priceType = selection.price && selection.price.priceType;

    if (outcomeDetail.priceType) {
      priceType = outcomeDetail.priceType;
      selection.price.priceType = priceType;
      selection.details.isSPLP = BetslipBetDataUtils.isSPLP(outcomeDetail as any);
      selection.details.isGpAvailable = outcomeDetail.isGpAvailable;
    }

    if (priceType === 'LP') {
      selection.price.priceNum = Number(outcomeDetail.priceNum);
      selection.price.priceDen = Number(outcomeDetail.priceDen);
      selection.price.priceDec = this.fracToDecService.fracToDec(selection.price.priceNum, selection.price.priceDen);
    }

    if (outcomeDetail.handicap) {
      rawHandicapValue = this.formatHandicapValue(+outcomeDetail.handicap);
      outcomeDetail.handicap = this.getCorrectDecRawHandicapValue(outcomeDetail);
      selection.price.handicapValueDec = outcomeDetail.handicap;
      selection.price.rawHandicapValue = rawHandicapValue;
    }

    return {
      id: outcomeDetail.id,
      name: this.modifyOutcomeName(outcomeDetail , outcomeDetail.handicap),
      marketId: outcomeDetail.marketId,
      prices: [selection.price],
      liveServChannels: selection.details.outcomeliveServChannels.replace(',', ''),
      outcomeStatusCode: outcomeDetail.outcomeStatusCode || 'A',
      marketStatusCode: outcomeDetail.marketStatusCode || 'A',
      errorMsg: this.getErrorMsg(this.getErrorCodeByOutcomeDetail(outcomeDetail)),
      outcomeMeaningMinorCode: selection.details.outcomeMeaningMinorCode,
      details: {
        info: {
          sport: outcomeDetail.category,
          event: this.clearEventName(outcomeDetail.eventDesc, outcomeDetail.category),
          time: time,
          localTime: raceLocalTime.length > 0 ? raceLocalTime : userLocalTime,
          market: outcomeDetail.marketDesc,
          sportId: selection.details.info.sportId,
          className: outcomeDetail.className,
          isStarted: selection.details.info.isStarted
        },
        isRacing: this.racingCheck(Number(outcomeDetail.categoryId)),
        outcomeStatusCode: outcomeDetail.outcomeStatusCode || 'A',
        marketStatusCode: outcomeDetail.marketStatusCode || 'A',
        eventStatusCode: outcomeDetail.eventStatusCode || 'A',
        classId: outcomeDetail.classId,
        categoryId: outcomeDetail.categoryId,
        typeId: outcomeDetail.typeId,
        eventId: outcomeDetail.eventId,
        marketId: outcomeDetail.marketId,
        outcomeId: outcomeDetail.id,
        handicap: outcomeDetail.handicap,
        // market
        market: outcomeDetail.marketDesc,
        markets: [{
          id: outcomeDetail.marketId,
          name: outcomeDetail.marketDesc,
          drilldownTagNames: selection.details.marketDrilldownTagNames || outcomeDetail.marketDrilldownTagNames,
          rawHandicapValue,
          cashoutAvail: selection.details.marketCashoutAvail
        }],
        selectionName: outcomeDetail.name,
        prices: selection.price,
        pricesAvailable: !!selection.price.priceNum,
        isEachWayAvailable: !!outcomeDetail.eachWayPlaces,
        eachWayPlaces: outcomeDetail.eachWayPlaces,
        previousOfferedPlaces:outcomeDetail.previousOfferedPlaces,
        eachwayCheckbox: this.eachwayCheckboxOptionByDetails(outcomeDetail),
        isSPLP: selection.details.isSPLP,
        isGpAvailable: selection.details.isGpAvailable,
        drilldownTagNames: selection.details.eventDrilldownTagNames || outcomeDetail.eventDrilldownTagNames,
        cashoutAvail: selection.details.cashoutAvail,
        eventliveServChannels: selection.details.eventliveServChannels.replace(',', ''),
        marketliveServChannels: selection.details.marketliveServChannels.replace(',', ''),
        outcomeliveServChannels: selection.details.outcomeliveServChannels.replace(',', ''),
        isMarketBetInRun: selection.details.isMarketBetInRun
      }
    };
  }

  /**
   * Return handicap value with correct sign(if fbResult === AWAY than sign should be opposite)
   * Workaround till https://jira.openbet.com/browse/LCRCORE-20926 will be fixed.
   * @param outcomeDetail
   */
  private getCorrectDecRawHandicapValue(outcomeDetail: IOutcomeDetailsResponse): string {
    return outcomeDetail.fbResult === 'A'
      ? this.formatHandicapValue(-outcomeDetail.handicap)
      : this.formatHandicapValue(+outcomeDetail.handicap);
  }

  /**
   * Change handicap value to x.y format
   * @param handicap
   */
  private formatHandicapValue(handicap: number): string {
    return handicap.toFixed(1);
  }

  private fillRacingCodes(): void {
    this.racingCodes = [];

    _.each(environment.CATEGORIES_DATA.racing, (item: { id: string; }) => {
      this.racingCodes.push(item.id);
    });
  }

  /**
   * Add handicap value to outcome name
   * params {string} name
   * params {string} handicap
   * return {string}
   */
  private modifyOutcomeName(outcomeDetail: IOutcomeDetailsResponse, handicap: string): string {
    return handicap.length ? `${outcomeDetail.name} ${this.filter.makeHandicapValue(handicap, outcomeDetail)}` : outcomeDetail.name;
  }

  /**
   * Check for event is racing or not
   * params {string} id
   * return {Boolean}
   */
  private racingCheck(id: number): boolean {
    return _.contains(this.racingCodes, id.toString());
  }

  /**
   * SP events got no prices, in this case we could get undefined error.
   * params {Object} outcome
   * return {Object} with priceType data
   */
  private priceTypeParse(outcome: IBetslipOutcome, market: IBetslipMarket): IConstant {
    return _.has(outcome, 'prices') && outcome.prices.length && market.priceTypeCodes !== 'SP,'
      ? {
        priceType: 'LP',
        priceNum: outcome.prices[0].priceNum,
        priceDen: outcome.prices[0].priceDen
      }
      : { priceType: 'SP' };
  }

  /**
   * Check that selection should be rendered with eachway checkbox.
   * State of checkbox should be saved in the session storage.
   * If Checkbox is selected to true, selection in placeBet && checkBet f-ty should be changed from winplaceref = WIN to EACH_WAY
   * If Checkbox is selected to true, return of this selection should be calculated by formula:
   * Estimated Returns && Extra profit, where Extra profit = stakeAmount * (outcome.price.priceNum / infoObj.price.priceDen) *
   *                 (market.eachWayFactorNum / market.eachWayFactorDen) + stakeAmount);
   * Only Racing events could have eachway option
   * params {Object} market
   * return {Object} - if eachway available we store prices for rendering.
   */
  private eachwayCheckboxOption(market: IBetslipMarket): IConstant | null {
    return market.isEachWayAvailable
      ? {
        eachwayPriceNum: market.eachWayFactorNum,
        eachwayPriceDen: market.eachWayFactorDen
      } : null;
  }

  private eachwayCheckboxOptionByDetails(outcomeDetail: IOutcomeDetailsResponse): IConstant | null {
    return outcomeDetail.eachWayPlaces
      ? {
        eachwayPriceNum: outcomeDetail.eachWayNum,
        eachwayPriceDen: outcomeDetail.eachWayDen
      } : null;
  }

  /**
   * Returns proper error message
   * @params{string} code
   * @returns{string} error message
   */
  private getErrorMsg(code: string): string | undefined {
    return code ? this.locale.getString(`bs.${code}`) : undefined;
  }

  /**
   * Returns error code acording to event/market/outcome status
   * @params{object} event
   * @params{object} market
   * @params{object} outcome
   * @returns{string | null} status code
   */
  private getErrorCode(eventItem: IBetslipEvent, market: IBetslipMarket, outcome: IBetslipOutcome): string | null {
    if (eventItem.eventStatusCode === 'S') {
      return BETSLIP_VALUES.ERRORS.SELECTION_SUSPENDED;
    } else if (market.marketStatusCode === 'S') {
      return BETSLIP_VALUES.ERRORS.MARKET_SUSPENDED;
    } else if (outcome.outcomeStatusCode === 'S') {
      return BETSLIP_VALUES.ERRORS.OUTCOME_SUSPENDED;
    } else if (!!eventItem.isStarted && !market.isMarketBetInRun) {
      return BETSLIP_VALUES.ERRORS.EVENT_STARTED;
    }
    return null;
  }

  /**
   * Returns error code according to bbp (+ ss call) outcomeDetails
   * @params{object} outcomeDetails
   * @returns{string | null} status code
   */
  private getErrorCodeByOutcomeDetail(outcomeDetails: IOutcomeDetailsResponse): string | null {
    if (outcomeDetails.eventStatusCode === 'S') {
      return BETSLIP_VALUES.ERRORS.SELECTION_SUSPENDED;
    } else if (outcomeDetails.marketStatusCode === 'S') {
      return BETSLIP_VALUES.ERRORS.MARKET_SUSPENDED;
    } else if (outcomeDetails.outcomeStatusCode === 'S') {
      return BETSLIP_VALUES.ERRORS.OUTCOME_SUSPENDED;
    } else if (outcomeDetails.isStarted && !outcomeDetails.isMarketBetInRun) {
      return BETSLIP_VALUES.ERRORS.EVENT_STARTED;
    }
    return null;
  }

  /**
   * creates an Array of Objects filled by data needed to create betslip view model.
   * params {Object} data
   * return result {Array} parsed data.
   */
  private getSelectionRelatedData(data: IBetslipEvent[]): ISelectionRealtedData[] {
    return _.reduce(data, (result, eventItem) => {
      _.each(eventItem.markets as IBetslipMarket[], market => {
        _.each(market.outcomes as IBetslipOutcome[], outcome => {
          result.push(_.extend({
            errorMsg: this.getErrorMsg(this.getErrorCode(eventItem, market, outcome))
          }, outcome, { details: {
              info: {
                sport: eventItem.categoryName,
                event: eventItem.name,
                time: eventItem.startTime,
                localTime: eventItem.localTime,
                market: market.name,
                sportId: eventItem.sportId,
                className: eventItem.className,
                isStarted: eventItem.isStarted
              },
              isRacing: this.racingCheck(Number(eventItem.categoryId)),
              // statuses
              outcomeStatusCode: outcome.outcomeStatusCode,
              marketStatusCode: market.marketStatusCode,
              eventStatusCode: eventItem.eventStatusCode,
              // id's
              classId: eventItem.classId,
              categoryId: eventItem.categoryId,
              typeId: eventItem.typeId,
              eventId: eventItem.id,
              marketId: market.id,
              templateMarketId: market.templateMarketId,
              outcomeId: outcome.id,
              handicap: market.rawHandicapValue,
              // liveServ data
              isMarketBetInRun: market.isMarketBetInRun,
              eventliveServChannels: eventItem.liveServChannels.replace(',', ''),
              marketliveServChannels: market.liveServChannels.replace(',', ''),
              outcomeliveServChannels: outcome.liveServChannels.replace(',', ''),
              market: market.name,
              markets: eventItem.markets,
              selectionName: outcome.name,
              prices: this.priceTypeParse(outcome, market),
              isSPLP: BetslipBetDataUtils.isSPLP(market, outcome),
              pricesAvailable: !!outcome.prices.length,
              isEachWayAvailable: market.isEachWayAvailable,
              isGpAvailable: market.isGpAvailable,
              eachwayCheckbox: this.eachwayCheckboxOption(market),
              drilldownTagNames: eventItem.drilldownTagNames,
              cashoutAvail: eventItem.cashoutAvail
            } }));
        });
      });
      this.outcomeData = this.siteServerService.outcomeForOutcomeData.length>0 ? this.siteServerService.outcomeForOutcomeData: [];
      return result;
    }, []);
  }
  
  restrictedRacecardAndSelections(marketDetails, eventDetails,outcomeDetails) {
    const restricted = {
      restrictedRaces: [],
      horseNames: [],
      eventIdDetails: []
    }
    if(outcomeDetails){
      if(outcomeDetails.every(outcome=>outcome.categoryId != this.HORSE_RACING_CATEGORY_ID)){
        return restricted;
      }
      if(eventDetails.categoryId == this.HORSE_RACING_CATEGORY_ID){
        if (marketDetails.maxAccumulators == 1 && marketDetails.minAccumulators == 1) {
          marketDetails.ismarketRestriction = true;
          const matchItem = this.filter.getTimeFromName(eventDetails.name);
          const restrictedRace = matchItem ? eventDetails.typeName.concat(" - ", matchItem):eventDetails.typeName;
          restricted.restrictedRaces.push(restrictedRace.replace(/\|/g,''));
        }
        else {
          marketDetails.ismarketRestriction = false;
        }
      }

      outcomeDetails.map(outcome=>{
        if(!restricted.eventIdDetails.includes(outcome.eventId)){
          restricted.eventIdDetails.push(outcome.eventId);
        }
        if (outcome.accMax == 1 && outcome.accMin == 1 && outcome.marketId === marketDetails.id && !marketDetails.ismarketRestriction && outcome.categoryId == this.HORSE_RACING_CATEGORY_ID) {
          restricted.horseNames.push(outcome.name.replace(/\|/g,''));
        }
      });
    }

    return restricted;
  }

}
