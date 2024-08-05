import { Component, OnInit, OnDestroy, Input, SimpleChanges } from '@angular/core';
import * as _ from 'underscore';

import { IOutcome } from '@core/models/outcome.model';
import { IMarket } from '@core/models/market.model';
import { IUkToteLiveUpdateModel } from '@core/services/ukTote/uktote-update.model';

import { UkToteBetBuilderService } from '@uktote/services/ukTotebetBuilder/uk-tote-bet-builder.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

import { CHECKBOX_MODELS } from '@lazy-modules/forecastTricast/constants/forecast-tricast-checkboxes.constant';
import { FORECAST_CONFIG } from '@lazy-modules/forecastTricast/constants/forecast-tricast-config.contant';

import {
  HandleLiveServeUpdatesService
} from '@core/services/handleLiveServeUpdates/handle-live-serve-updates.service';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { UkToteLiveUpdatesService } from '@core/services/ukTote/uktote-live-update.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';

import { IForecastMatrixMap, ITricastMatrixMap } from '../forecastTricastCheckboxMatrix/forecast-tricast-checkbox-matrix.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { Bet } from '@app/betslip/services/bet/bet';
import { IDelta } from '@app/core/models/delta-object.model';

@Component({
  selector: 'forecast-tricast-market',
  templateUrl: './forecast-tricast-market.component.html',
  styleUrls: ['forecast-tricast-market.component.scss']
})
export class ForecastTricastMarketComponent implements OnInit, OnDestroy {
  @Input() selectedPoolType: string;
  @Input() marketEntity: IMarket;
  @Input() event: ISportEvent;
  @Input() isVirtual: boolean = false;
  @Input() isMarketDescriptionEnabled: boolean = false;
  @Input() delta: IDelta;

  channels: string[];
  expandedSummary = {};
  outcomesMap: { [key: string]: IOutcome; } = {};
  betFilter: string;
  poolTypes: string[];
  isMultipleLegsToteBet: boolean;
  forTriMsg: string;
  checkboxesMap: IForecastMatrixMap | ITricastMatrixMap;
  outcomes: IOutcome[];

  poolCssClass: string = '';
  marketDescriptionClass: string = '';
  betBuilderMsg: { warning: string } = {} as { warning: string };
  isBetAvailable: boolean;
  protected readonly MARKET_DESCRIPTION_CLASS: string = 'has-market-description';

  constructor(
    private locale: LocaleService,
    private betBuilderService: UkToteBetBuilderService,
    private ukTotesHandleLiveServeUpdatesService: HandleLiveServeUpdatesService,
    private ukToteLiveUpdatesService: UkToteLiveUpdatesService,
    private ukToteService: UkToteService,
    private pubSubService: PubSubService,
    private gtmService: GtmService
  ) { }

  ngOnInit(): void {
    this.betFilter = this.verifyPoolType(this.selectedPoolType);
    this.setBetProperties(this.betFilter);
    this.sortMarketOutcomes();
    this.setMarketDescriptionClass();
    this.prepareIdsForLiveUpdates(this.event);
    const ids = this.ukToteService.getAllIdsForEvents([this.event]);
    this.channels = this.ukToteLiveUpdatesService.getAllChannels(ids);
    this.ukTotesHandleLiveServeUpdatesService.subscribe(this.channels, this.updateEvent.bind(this));

    this.betBuilderMsg.warning = this.getBetBuilderWarning(this.checkboxesMap);
    this.updateFCTCmarkets(this.delta);
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.delta) {
      this.updateFCTCmarkets(changes.delta.currentValue);
    }
  }

  updateFCTCmarkets(delta: IDelta): void {
    if (delta?.updateEventId && this.event.id.toString() === delta.updateEventId.toString()) {
      if(delta.fcMktAvailable === 'Y' || delta.fcMktAvailable === 'N') {
        this.marketEntity.fcMktAvailable = delta.fcMktAvailable;
      }
      if(delta.tcMktAvailable==='Y' || delta.tcMktAvailable === 'N') {
        this.marketEntity.tcMktAvailable = delta.tcMktAvailable;
      }
    }
  }
  
  ngOnDestroy(): void {
    this.ukTotesHandleLiveServeUpdatesService.unsubscribe(this.channels);
    this.pubSubService.unsubscribe('GTM');
  }

  trackByOutcomes(index: number, outcome: IOutcome): string {
    return `${index}${outcome.isDisplayed}${outcome.id}${outcome.name}${outcome.marketId}`;
  }

  onMapUpdate(map: IForecastMatrixMap | ITricastMatrixMap): void {
    const checkedElms = _.reduce(map, (memo, obj) => {
      memo += _.filter(_.values(obj), el => el === 'checked').length;
      return memo;
    }, 0);

    this.betBuilderMsg.warning = this.getBetBuilderWarning(checkedElms);
    this.checkMap(checkedElms);
  }

  isSuspended(outcome: IOutcome): boolean {
    return this.event.eventStatusCode === 'S' ||
          this.marketEntity.marketStatusCode === 'S' ||
          outcome.outcomeStatusCode === 'S' ||
          (this.betFilter === 'FC' && this.marketEntity.fcMktAvailable === 'N') ||
          (this.betFilter === 'TC' && this.marketEntity.tcMktAvailable === 'N');
  }

  addToBetslip(): void {
    const type = this.getCastType();
    const outcomes = this.getCheckedOutcomes(type);
    const eventOb = this.event;

    this.pubSubService.publish(this.pubSubService.API.ADD_TO_BETSLIP_BY_SELECTION, {
      isFCTC: true,
      type: type,
      outcomes: outcomes,
      doNotRemove: true,
      GTMObject: {
        tracking:{
          location: eventOb.localTime,
          module: FORECAST_CONFIG.eventDefaults.MODULE,
        },
        selectionID: outcomes[0].id,
      }
    });

    this.pubSubService.subscribe('GTM', this.pubSubService.API.PUSH_TO_GTM, (data) => {
      const outcomesList = type + '|' + outcomes.map(outcome => outcome.id).join('|');
      data.bets.forEach((bet: Bet) => {
        if(outcomesList === bet.storeId){
          this.sendGTMData(bet.betComplexName, outcomes, eventOb);
        }
      });
    });
    this.resetMap();
    this.isBetAvailable = false;
  }

  /**
   * Sends data to GA tracking
   * @returns void
   */
  private sendGTMData(type, outcomes, eventOb): void {
    const selectionIDs = outcomes.map(selection => selection.id).join(',');
    const productsDetails = {
      add: {
        products: [{
          brand: type,
          category: eventOb.categoryId,
          dimension60: eventOb.id,
          dimension61: selectionIDs,
          dimension62: FORECAST_CONFIG.eventDefaults.INPLAY,
          dimension63: FORECAST_CONFIG.eventDefaults.CUSTOMER_BUILT,
          dimension64: eventOb.localTime,
          dimension65: FORECAST_CONFIG.eventDefaults.MODULE,
          dimension86: FORECAST_CONFIG.eventDefaults.ODDSBOOST_VALUE,
          dimension87: FORECAST_CONFIG.eventDefaults.STREAM_ACTIVE,
          dimension88: FORECAST_CONFIG.eventDefaults.STREAM_ID,
          name: eventOb.originalName,
          quantity: FORECAST_CONFIG.eventDefaults.QUANTITY_VAL,
          variant: eventOb.typeId
        }]
      }
    }
    const gtmData = {
      event: 'trackEvent',
      eventAction: 'add to betslip',
      eventCategory: 'betslip',
      eventLabel: 'success',
      ecommerce: productsDetails
    };
    this.gtmService.push(gtmData.event, gtmData);
  }

  private sortMarketOutcomes(): void {
    this.outcomes = _.chain(this.marketEntity.outcomes).sortBy((outcome: IOutcome) => {
      return outcome.name.toLowerCase();
    }).sortBy((outcome: IOutcome) => {
      return outcome.displayOrder;
    }).sortBy((outcome: IOutcome) => {
      const sortNumber = this.event.categoryCode === 'GREYHOUNDS' ? outcome.trapNumber : outcome.runnerNumber;
      return Number(sortNumber);
    }).value();
  }

  private prepareIdsForLiveUpdates(event: ISportEvent): void {
    event.linkedEventId = event.id;
    _.each(event.markets, (market: IMarket) => {
      market.linkedMarketId = market.id;
      _.each(market.outcomes, (outcome: IOutcome) => {
        outcome.linkedOutcomeId = outcome.id;
      });
    });
  }

  private updateEvent(liveUpdate: IUkToteLiveUpdateModel): void {
    const { payload } = liveUpdate;
    this.ukToteLiveUpdatesService.updateEventWithLiveUpdate(this.event, liveUpdate);
    if (payload.status === 'S') {
      this.resetMap();
      this.onMapUpdate(this.checkboxesMap);
    }
  }

  private checkMap(checkedElms: number): void {
    this.isBetAvailable = (checkedElms > 0 && ((this.betFilter === 'FC' && checkedElms >= 2)
      || (this.betFilter === 'TC' && checkedElms >= 3)));
  }

  /**
   * generate warning message if not enough
   * selections selected for tricast (3) or forecast(2)
   */
  private getBetBuilderWarning(checkedElms): string {
    if (checkedElms > 0 && ((this.betFilter === 'FC' && checkedElms < 2)
      || (this.betFilter === 'TR' && checkedElms < 3))) {
      return this.locale.getString('racing.addSelection');
    }
    return null;
  }

  private getPoolCssClass(): string {
    if (this.betFilter === 'FC') {
      return 'execta-pool';
    } else if (this.betFilter === 'TC') {
      return 'trifecta-pool';
    } else {
      return '';
    }
  }

  /**
   * Set isMultipleLegsToteBet which identifies whether chosen bet has multiple legs
   * @private
   */
  private setBetProperties(betFilter: string): void {
    this.poolCssClass = this.getPoolCssClass();
    const num = betFilter === 'FC' ? 'two' : 'three';
    this.forTriMsg = this.locale.getString('racing.forTriMsg', { num });
    /**
     * For one leg bet types
     */
    // TODO isMultipleLegsToteBet - correct condition for placing multiple bet
    if (!this.isMultipleLegsToteBet) {

      /**
       * Checkboxes Map
       * @member {Object}
       */
      this.checkboxesMap = this.generateCheckboxMap(this.marketEntity ? this.marketEntity.outcomes
        : [], betFilter);
    }

    this.betBuilderService.clear(null);
  }

  /**
   * Generate Checkbox Map
   * @param {Array} outcomes
   * @param {String} poolType
   * return {Object} map
   */
  private generateCheckboxMap(outcomes: IOutcome[], poolType: string): IForecastMatrixMap | ITricastMatrixMap {
    const map = {};
    const currentModel = CHECKBOX_MODELS[poolType];

    if (currentModel) {
      _.each(outcomes, (outcome: IOutcome) => {
        const clone = {};
        /* eslint-disable */
        for (const key in currentModel) {
          clone[key] = currentModel[key];
        }
        /* eslint-enable */
        map[outcome.id] = clone;
        this.outcomesMap[outcome.id] = outcome;
      });
    }
    return map;
  }

  private verifyPoolType(selectedPoolType: string): string {
    return selectedPoolType === 'Forecast' ? 'FC' : 'TC';
  }

  private getCastType(): string {
    const anyChecked = _.some(this.checkboxesMap, map => map['any'] === 'checked');
    const type = this.selectedPoolType.toUpperCase();
    return anyChecked ? `${type}_COM` : type;
  }

  private getCheckedOutcomes(type: string): IOutcome[] {
    if (type === 'FORECAST') {
      return this.getOutcomesByPlace(['1st', '2nd']);
    } else if (type === 'TRICAST') {
      return this.getOutcomesByPlace(['1st', '2nd', '3rd']);
    } else {
      const outcomes = [];
      _.each(this.checkboxesMap, (el, id) => {
        if (el['any'] === 'checked') {
          outcomes.push(this.outcomesMap[id]);
        }
      });
      return _.sortBy(outcomes, (outcome: IOutcome) => outcome.displayOrder);
    }
  }

  private getOutcomesByPlace(places: string[]): IOutcome[] {
    const outcomes = [];
    _.each(places, (place: string) => {
      outcomes.push(
        this.outcomesMap[_.findKey(this.checkboxesMap, el => el[place] === 'checked')]
      );
    });
    return outcomes;
  }

  private resetMap(): void {
    _.each(this.checkboxesMap, (el) => {
      _.each(el, (val: string, key: string) => {
        el[key] = 'open';
      });
    });
  }

  /**
   * Sets class based on market description availability
   */
  private setMarketDescriptionClass(): void {
      const market = this.event.sortedMarkets && this.event.sortedMarkets.find((sortedMarket: IMarket) => {
        return sortedMarket.label === this.selectedPoolType;
      });
      if (this.isMarketDescriptionEnabled && market && market.description) {
        this.marketDescriptionClass = this.MARKET_DESCRIPTION_CLASS;
      } else {
        this.marketDescriptionClass = '';
      }
  }
}
