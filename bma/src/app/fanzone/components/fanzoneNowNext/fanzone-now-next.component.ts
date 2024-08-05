import { Component, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IFeaturedModel } from '@app/featured/models/featured.model';
import { IOutputModule } from '@app/featured/models/output-module.model';
import * as _ from 'underscore';
import { FanzoneFeaturedService } from '@app/fanzone/services/fanzone-featured-ms.service';
import { channelName, initStateOfFanzone, fanzoneCleanModule } from '@app/fanzone/fanzone.constant';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';
import { fanzoneStorageData } from '@app/fanzone/models/fanzone.model';
import { FanzoneDetails } from '@app/core/services/fanzone/models/fanzone.model';
import { WsUpdateEventService } from '@app/core/services/wsUpdateEvent/ws-update-event.service';
import { FANZONE_CATEGORY_ID } from "@app/fanzone/constants/fanzoneconstants";
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';

@Component({
  selector: 'app-fanzone-now-next',
  template: ``,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FanzoneAppNowNextComponent {
  fanzoneModuleData: IFeaturedModel;
  channelName = channelName;
  noEventFound: boolean = false;
  ssDown: boolean = false;
  showLoader: boolean = true;
  isConnectSucceed: boolean;
  protected onSocketUpdate: Function;
  isModuleAvailable: boolean = false;
  private isLoaderShown: boolean = true;
  fanzoneDetails: FanzoneDetails;
  fanzoneTeam: fanzoneStorageData;
  wsLiveEvent = [];
  constructor(protected fanzoneFeaturedService: FanzoneFeaturedService,
    protected pubsub: PubSubService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected fanzoneStorageService: FanzoneStorageService,
    protected fanzoneHelperService: FanzoneHelperService,
    protected wsUpdateEventService: WsUpdateEventService) {
    this.onSocketUpdate = (data: IOutputModule) => {
      this.fanzoneOnSocketUpdate(data);
    };
    this.trackByModules = this.trackByModules.bind(this);
  }

  /**
   * to initiate the logic on component initialisation
   * @returns {void}
   */
  ngOnInit(): void {
    this.wsUpdateEventService.subscribe();
    this.fanzoneTeam = this.fanzoneStorageService.get('fanzone');
    this.pubsub.subscribe(this.channelName, this.pubsub.API.FANZONE_DATA, (fanzone: FanzoneDetails) => {
      this.fanzoneDetails = fanzone;
    });
    this.fanzoneDetails = this.fanzoneHelperService.selectedFanzone;

    this.initializeAndConnectMS();
  }

  /**
   * Initializes and connect to featured MS
   * @returns {void}
   * @private
   */
  private initializeAndConnectMS(): void {
    this.fanzoneModuleData = initStateOfFanzone;
    this.isConnectSucceed = true;
    this.showLoader = true;
    this.changeDetectorRef.markForCheck();
    this.connectFeaturedMS();
  }

  /**
  * establish connection with featured MS
  * @returns {IFeaturedModel}
  */
  connectFeaturedMS(): void {
    this.pubsub.subscribe(this.channelName, this.pubsub.API.FEATURED_CONNECT_STATUS, (isConnected: boolean) => {
      if (isConnected) {
        this.showLoader = false;
        this.isConnectSucceed = isConnected;
        this.fanzoneFeaturedService.emit('login', this.fanzoneTeam.teamId);
        this.fanzoneFeaturedService.addEventListener('FEATURED_STRUCTURE_CHANGED', (featured: IFeaturedModel) => {
          this.init(featured);

          this.pubsub.publish(this.pubsub.API.FEATURED_STRUCTURE_CHANGED, []);
          this.changeDetectorRef.detectChanges();
        });
      }
      this.changeDetectorRef.markForCheck();
    });
    const connectionNameSpaceId = FANZONE_CATEGORY_ID;
    const connectionType = 'sport';
    this.fanzoneFeaturedService.startConnection(connectionNameSpaceId, connectionType);

    this.pubsub.subscribe(this.channelName, this.pubsub.API.NAMESPACE_ERROR, () => {
      this.handleErrorOnFirstLoad();
    });

    this.pubsub.subscribe(this.channelName, this.pubsub.API.WS_EVENT_UPDATED, (updatedData) => {
      this.changeDetectorRef.detectChanges();
    });

    this.pubsub.subscribe(this.channelName, this.pubsub.API.WS_EVENT_UPDATE, (updatedData) => {
      this.changeDetectorRef.detectChanges();
    });

    this.fanzoneFeaturedService.onError(() => {
      this.fanzoneModuleData = initStateOfFanzone;
      this.ssDown = true;
      this.showLoader = false;
    });
    this.changeDetectorRef.markForCheck();
  }

  /**
   * initialize the fanzone module data from featured ms
   * @returns {void}
   */
  init(featured: IFeaturedModel): void {
    const data = featured;

    if ((data === undefined || data === null) || (data && data.modules && data.modules.length === 0)) {
      this.handleErrorOnFirstLoad(false);
      if (data && data.modules) {
        this.fanzoneModuleData.modules = data.modules;
      }
      this.noEventFound = this.checkNoEventFound();
      return;
    } else {
      this.noEventFound = false;
    }
    // listeners for updates of modules
    this.addModulesEventListeners(data);
    // listeners for updates of events in each module
    this.addEventListenersForEventsInModules(data);

    this.ssDown = false;
    this.showLoader = false;
    this.fanzoneModuleData = this.addClockToEvents(data);

    this.changeDetectorRef.markForCheck();
    this.fanzoneFeaturedService.cacheEvents(this.fanzoneModuleData);
    this.isModuleAvailable = this.isFeaturedModuleAvailable;
  }

  /**
   * Add clock data for all modules events
   * @param {Object} data
   * returns {Object}
   */
   private addClockToEvents(data: IFeaturedModel): IFeaturedModel {
    data.modules = data.modules.map((module: IOutputModule) => {
      (module.data as ISportEvent[]) = this.fanzoneFeaturedService.addClock(module.data);
      return module;
    });

    return data;
  }

  /**
  * Handles new module data received from websocket updates.
  * @param {Object=} data
  * @returns {void}
  */
  protected fanzoneOnSocketUpdate(data?: IOutputModule): void {
    const module = data || fanzoneCleanModule;
    module.isLoaded = true;
    this.onModuleUpdate(module);
    this.addEventListenersWithinModule(module);
    if (!this.isSurfaceBetsModule(module)) { this.unsubscribe(module._id); }
    this.changeDetectorRef.detectChanges();
  }
  /**
   * Check if module is Surface Bets
   * @param module
   * @returns {boolean}
   */
   private isSurfaceBetsModule(module): boolean {
    return module['@type'] === 'SurfaceBetModule';
  }

   /**
   * Unsubscribe from updates
   * @param {String} _id
   */
    private unsubscribe(_id: string): void {
      this.fanzoneFeaturedService.tabModuleStates.set(_id, false);
      this.fanzoneFeaturedService.removeEventListener(_id, this.onSocketUpdate);
    }


  /**
  * Goes through each module
  * @param data {Object}
  */
  private addEventListenersForEventsInModules(data: IFeaturedModel): void {
    _.each(data.modules, (module: IOutputModule) => {
      this.addEventListenersWithinModule(module);
    });
  }

  /**
 * Check if fanzoneModuleData module is available
 * @returns {boolean}
 */
  get isFeaturedModuleAvailable(): boolean {
    return this.fanzoneModuleData && this.fanzoneModuleData.modules && this.fanzoneModuleData.modules.length > 0;
  }
  set isFeaturedModuleAvailable(value: boolean) { }

  /**
* Goes trough each event in module and sets callback for event updates
* @param module {Array}
*@returns {void}
*/
  private addEventListenersWithinModule(module: IOutputModule): void {
    this.addEventsLiveUpdatesListener(module.data);
  }

  /**
   * Live updates handler
   * @param {ISportEvent[]} events
   * @returns {void}
   */
  private addEventsLiveUpdatesListener(events: ISportEvent[]): void {
    _.each(events, (event: ISportEvent) => {
      if (event.id) {
        this.fanzoneFeaturedService.addEventListener(event.id.toString(), update => {
          this.pubsub.publish(this.pubsub.API.WS_EVENT_UPDATE, {
            events: [event],
            update
          });
        });
      }
    });
  }

  /**
   * Check if to show no events message
   * @returns {boolean}
   */
  checkNoEventFound(): boolean {
    const moduleData = this.fanzoneModuleData.modules;
    const moduleDataLength = moduleData && _.filter(moduleData, (mod: IOutputModule) => mod.isLoaded && mod.data.length === 0).length;
    const isDataNotExist = (moduleData && moduleData.length) === moduleDataLength;
    return isDataNotExist && !this.showLoader && !this.ssDown && this.isConnectSucceed;
  }

  /**
   * reconnect in case connection lost or not established
   * @returns {void}
   */
  reloadComponent(): void {
    this.fanzoneFeaturedService.reconnect();
    this.ssDown = false;
    this.isConnectSucceed = true;
    this.showLoader = true;
    this.changeDetectorRef.markForCheck();
  }

  /**
   * Function adds socket event listener and handler
   * @param {Object} data
   * @returns {void}
   */
  private addModulesEventListeners(data: IFeaturedModel): void {
    this.getModuleIds(data.modules)
      .forEach(id => this.fanzoneFeaturedService.addEventListener(id, this.onSocketUpdate));
  }

  /**
   * Function returns featured modules ids
   * @param {Array} modules
   * @returns {string[]}
   */
  private getModuleIds(modules: IOutputModule[]): string[] {
    return modules
      .filter(module => module.showExpanded)
      .map(module => module._id);
  }

  /**
   * Handles error if ss is down 
   * @param {boolean} ssDown
   * @returns {void}
   */
  handleErrorOnFirstLoad(ssDown: boolean = true): void {
    this.ssDown = ssDown;
    this.showLoader = false;
    this.changeDetectorRef.markForCheck();
  }

  trackByModules(i: number, module: IOutputModule): string {
    const isByMarketId = (module.dataSelection && module.dataSelection.selectionType === 'Market');

    let trackValue = `${i}_${module._id}`;

    if (module['@type'] === 'EventsModule' &&  !isByMarketId) {
      trackValue = `${trackValue}_${module.title}_${module.displayOrder}`;
    }

    return trackValue;
  }

  trackByModuleData(i: number, event: ISportEvent): string {
    return `${i}_${event.id}_${event.name}_${event.startTime}`;
  }

   /**
   * Operations on module update receiving
   * @param {Object} data
   */
    onModuleUpdate(data: IOutputModule): void {
      if (!data._id) {
        return;
      }
  
      this.fanzoneModuleData.modules = this.fanzoneModuleData.modules.map(module => {
        if (module._id === data._id) {
          return data;
        }
        return module;
      });
      this.fanzoneFeaturedService.cacheEvents(this.fanzoneModuleData);
    }


  /**
   * Clear subscriptions and disconnect when component destroyed
   * @returns {void}
   */
  ngOnDestroy(): void {
    this.pubsub.unsubscribe(this.channelName);
    this.fanzoneFeaturedService.disconnect();
    this.fanzoneFeaturedService.cacheEvents(this.fanzoneModuleData);
  }

}
