import { Component, Input, OnInit, OnDestroy, OnChanges, SimpleChanges } from '@angular/core';
import * as _ from 'underscore';

// eslint-disable-next-line max-len
import { HandleLiveServeUpdatesService } from '@core/services/handleLiveServeUpdates/handle-live-serve-updates.service';
import { MultipleEventsToteBetService } from '@uktote/components/multipleEventsToteBet/multiple-events-tote-bet.service';
import { UkToteService } from '@uktote/services/ukTote/uk-tote.service';
import { StorageService } from '@core/services/storage/storage.service';
import { UkToteBetBuilderService } from '@uktote/services/ukTotebetBuilder/uk-tote-bet-builder.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { UkToteLiveUpdatesService } from '@core/services/ukTote/uktote-live-update.service';

import { TotePotBet } from '@uktote/models/totePotBet/tote-pot-bet';

import { ISportEvent } from '@core/models/sport-event.model';
import { IUkTotePoolBet } from '@uktote/models/tote-pool.model';
import { ToteBetLeg } from '@uktote/models/toteBetLeg/tote-bet-leg';
import { IUkToteAllChannelsModel, IUkToteLiveUpdateModel } from '@core/services/ukTote/uktote-update.model';
import { ISwitcherConfig } from '@core/models/switcher-config.model';

import { UK_TOTE_CONFIG } from '../../constants/uk-tote-config.contant';
import { IRacingEvent } from '@core/models/racing-event.model';

@Component({
  selector: 'multiple-events-tote-bet',
  templateUrl: 'multiple-events-tote-bet.component.html'
})
export class MultipleEventsToteBetComponent implements OnInit, OnDestroy, OnChanges {
  @Input() poolBetVal: IUkTotePoolBet;
  @Input() isUKorIRE: boolean;

  loading: boolean = false;
  potBet: TotePotBet;
  legFilter: number;
  legSwitchers: ISwitcherConfig[];
  isScoop6Pool: boolean;
  requestFailed: boolean = false;

  private ids: IUkToteAllChannelsModel;
  private channels: string[];

  constructor(
    private ukTotesHandleLiveServeUpdatesService: HandleLiveServeUpdatesService,
    private ukToteLiveUpdatesService: UkToteLiveUpdatesService,
    private ukToteBetBuilderService: UkToteBetBuilderService,
    private multipleEventsToteBetService: MultipleEventsToteBetService,
    private ukToteService: UkToteService,
    private storageService: StorageService,
    private pubSubService: PubSubService
  ) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.poolBetVal && changes.poolBetVal.currentValue && changes.poolBetVal.previousValue) {
      this.ngOnInit();
    }
  }

  ngOnInit(): void {
    this.loading = true;
    this.isScoop6Pool = this.poolBet && (this.poolBet.poolType === UK_TOTE_CONFIG.scoopSixPoolType || this.poolBet.poolType === UK_TOTE_CONFIG.scoopSevenPoolType);
    this.requestFailed = false;
    this.ukToteService.loadEventsByMarketIds(this.poolBet.marketIds)
      .then((toteEvents: ISportEvent[]) => {
        return this.ukToteService.extendToteEvents(toteEvents, this.isScoop6Pool).toPromise();
      })
      .then((toteEvents: ISportEvent[]) => {
        return this.multipleEventsToteBetService.setRacingForm(toteEvents).toPromise();
      })
      .then((eventsData: IRacingEvent[]) => {
        this.potBet = this.createPotBet(eventsData);
        this.setBetStatus();
        this.setIds();
        this.legFilter = this.potBet.legs[0].index;
        this.createLegsSwitchers();
        this.pubSubService.subscribe('multipleEventsToteBet', this.pubSubService.API.UK_TOTE_LEG_UPDATED, this.updateSwitcher.bind(this));
        this.pubSubService.publishSync(this.pubSubService.API.BETBUILDER_UPDATED, true);
        this.loading = false;
        this.subscribeForLiveUpdates();
      })
      .catch((error) => {
        this.requestFailed = true;
        this.loading = false;
        console.warn(error);
      });
  }

  ngOnDestroy(): void {
    this.unsubscribeFromLiveUpdates();
    this.pubSubService.unsubscribe('multipleEventsToteBet');
  }

  /**
   * Get pool bet
   * @returns {Object} - pool bet
   */
  get poolBet(): IUkTotePoolBet {
    return this.poolBetVal;
  }
  set poolBet(value:IUkTotePoolBet){}

  /**
   * Get chosen pool leg
   * @returns {Object} - object of class toteBetLeg
   */
  get chosenPoolLeg(): ToteBetLeg {
    return this.potBet && _.find(this.potBet.legs, { index: this.legFilter});
  }
  set chosenPoolLeg(value:ToteBetLeg){}

  /**
   * Creates ToteBetLeg models for each Tote bet leg
   * @param {ISportEvent[]} events - array of event objects
   */
  createPotBet(events: IRacingEvent[]): TotePotBet {
    return new TotePotBet(this.poolBet, events, UK_TOTE_CONFIG, this.ukToteService);
  }

  /**
   * Updates status of Leg switcher
   * @param {object} leg - object of class toteBetLeg, whether it filled or not.
   */
  updateSwitcher(leg: ToteBetLeg): void {
    const switcherToUpdate = _.find(this.legSwitchers, (switcher: ISwitcherConfig) => switcher.viewByFilters === leg.index);
    switcherToUpdate.filled = leg.filled;
    this.triggerBetBuilder();
  }

  reloadComponent() {
    this.ngOnDestroy();
    this.ngOnInit();
  }

  /**
   * Generates legs switchers for pool bet
   * @private
   */
  private createLegsSwitchers(): void {
    this.legSwitchers = _.map(this.potBet.legs, leg => {
      return {
        onClick: () => this.goToFilter(leg.index),
        viewByFilters: leg.index,
        name: leg.name,
        filled: leg.filled,
        suspended: this.potBet.isSuspended
      };
    });
  }

  /**
   * Reinitialize bet builder
   * @private
   */
  private triggerBetBuilder(): void {
    this.ukToteBetBuilderService.add({
      betModel: this.potBet,
      poolType: this.potBet.pool.type
    });
  }

  /**
   * Update status of leg with received live update
   * @param {IUkToteLiveUpdateModel} liveUpdate - received live update
   * @private
   */
  private updateLeg(liveUpdate: IUkToteLiveUpdateModel): void {
    this.multipleEventsToteBetService.changeLegsWithLiveUpdate(this.potBet.legs, liveUpdate);
    this.setBetStatus();
  }

  /**
   * Subscribe for live updates
   * @private
   */
  private subscribeForLiveUpdates(): void {
    this.channels = this.ukToteLiveUpdatesService.getAllChannels(this.ids);
    this.storageService.set('toteLiveChannels', this.channels);
    this.ukTotesHandleLiveServeUpdatesService.subscribe(this.channels, this.updateLeg.bind(this));
  }

  /**
   * Unsubscribe for live updates
   * @private
   */
  private unsubscribeFromLiveUpdates(): void {
    this.ukTotesHandleLiveServeUpdatesService.unsubscribe(this.channels);
  }

  /**
   * Switchers onclick event handlers
   * @param {number} legFilter
   * @private
   */
  private goToFilter(legFilter: number): void {
    if (this.legFilter === legFilter) {
      return;
    }
    this.legFilter = legFilter;
    this.pubSubService.publish(this.pubSubService.API.RELOCATE_BET_BUILDER);
  }

  /**
   * Set ids property which contains all ids of events, markets
   * and outcomes for tote pool bet
   * @private
   */
  private setIds(): void {
    this.ids = this.ukToteService.getAllIdsForEvents(this.potBet.events);
  }

  /**
   * Set isSuspended status of tote bet
   * @private
   */
   private setBetStatus(): void {
    this.potBet.updateBetStatus();
  }
}

