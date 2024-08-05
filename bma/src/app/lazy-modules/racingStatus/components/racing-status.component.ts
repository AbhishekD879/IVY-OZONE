import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { LocaleService } from '@core/services/locale/locale.service';
import environment from '@environment/oxygenEnvConfig';
import { DeviceService } from '@core/services/device/device.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { marketDescriptionConstants, racingStatusConstants } from '@app/lazy-modules/racingConstants/racing.constants';
import { IDelta } from '@core/models/delta-object.model';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { HandleLiveServeUpdatesService } from '@app/core/services/handleLiveServeUpdates/handle-live-serve-updates.service';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';

@Component({
  selector: 'racing-status',
  templateUrl: 'racing-status.component.html',
  styleUrls: ['./racing-status.component.scss']
})
export class RacingStatusComponent implements OnInit, OnDestroy {
  @Input() event: ISportEvent;
  @Input() isEventSelected?: boolean;
  @Input() isHrEdp?: boolean = false;
  @Input() liveServeSubscription?: boolean;
  @Input() isEventOverlay?: boolean;
  @Output() removeEventNameEmitter?: EventEmitter<string> = new EventEmitter();
  @Output() eventStatusUpdate?: EventEmitter<any> = new EventEmitter();
  
  updateEventId: string;
  isRaceOff: boolean = false;
  eventStatusCode: string = 'A';
  isInplay: boolean = false;
  isPubsubSubscribed: boolean = false;
  status: { title: string; class: string} = {
    title: '',
    class: ''
  };
  racingStatusConstants: { inPlay: string, result: string } = {
    inPlay: '',
    result: ''
  };
  protected BIRMarketsEnabled: string[] = [];
  readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;
  private readonly tagName: string = 'racingStatusComponent';
  isOverlayResultIcon: boolean;
  
  constructor(private localeService: LocaleService,
              private pubSubService: PubSubService,
              private deviceService: DeviceService,
              protected cmsService: CmsService,
              private liveServeHandleUpdatesService: HandleLiveServeUpdatesService,
              private windowRef: WindowRefService) {
              }

  ngOnInit(): void {
    this.isOverlayResultIcon = this.deviceService.isDesktop && this.isEventOverlay;
    this.getBIRMarkets();
    this.racingEventStatusHandler();
    if (this.liveServeSubscription) {
      this.liveServeHandler();
    }  
  }

  racingEventStatusHandler() {
    this.racingStatusConstants = racingStatusConstants;
    if (this.event.isResulted) {
      this.status.title = this.localeService.getString('racing.result');
      this.status.class = 'resulted';
    } else {
      if (this.event.categoryId === this.HORSE_RACING_CATEGORY_ID && (this.event.isStarted || this.event.rawIsOffCode === 'Y')) {
          this.status.title = this.localeService.getString('racing.raceOff');
          this.status.class = 'race-off';
          this.isInplay = true;
        if (!this.deviceService.isDesktop && this.isHrEdp && this.event.drilldownTagNames &&
          this.event.drilldownTagNames.includes(marketDescriptionConstants.EVFLAG_IHR)) {
          if (this.event.rawIsOffCode === 'Y') {
            let isMarketSuspended = false;
            this.event.markets.forEach(market => {
              if (market.marketStatusCode === 'S' && this.isBirMarketEnabled(market.name))
                isMarketSuspended = true;
            });
            if (this.event.eventStatusCode !== "S" && !isMarketSuspended) {
              this.status.title = this.localeService.getString('racing.inPlay');
            }
          }
          else {
            this.status.title = '';
            this.isInplay = false;
            this.status.class = '';
          }
        }
      } else { // non HR
        if (this.event.isStarted && !this.event.isLiveNowEvent) {
          this.status.title = this.localeService.getString('racing.raceOff');
          this.status.class = 'race-off';
        } else if (this.event.isStarted && this.event.isLiveNowEvent) {
          this.status.title = this.localeService.getString('racing.liveNow');
          this.status.class = 'live';
        }
      }
    }
    this.eventStatusUpdate.emit({id: this.event.id, data: this.status});
    // for BIR of horse racing for mobile platforms 
    if (!this.deviceService.isDesktop && this.isHrEdp && this.isEventSelected && this.event.drilldownTagNames
      && this.event.drilldownTagNames.includes(marketDescriptionConstants.EVFLAG_IHR)) {
      this.isPubsubSubscribed = true;
      this.pubSubService.subscribe(this.tagName, this.pubSubService.API.EXTRA_PLACE_RACE_OFF, (updateEventId: string) => {
        if (updateEventId && this.event.id.toString() === updateEventId.toString()) {
          this.isInplay = true;
          this.status.title = this.localeService.getString('racing.inPlay');
          this.status.class = 'race-off';
          this.removeEventNameEmitter.emit(updateEventId.toString());
          this.eventStatusUpdate.emit({id: this.event.id, data: this.status});
        }
      });

      this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SUSPEND_IHR_EVENT_OR_MRKT, (updateEventId: string, delta: IDelta) => {
        if (this.isInplay && updateEventId && this.event.id.toString() === updateEventId.toString()) {
          if (delta.eventStatusCode === 'A' || delta.eventStatusCode === 'S') {
            this.eventStatusCode = delta.eventStatusCode;
          }
          let isMarketSuspended = false;
          this.event.markets.forEach(market => {
              if (market.marketStatusCode === 'S' && this.isBirMarketEnabled(market.name))
                  isMarketSuspended = true;
          });
          if ((this.eventStatusCode === 'S' || this.event.eventStatusCode === 'S') 
          || ((delta.marketStatusCode === 'S' && this.isBirMarketEnabled(delta.originalName)) || isMarketSuspended)) {
            this.status.title = this.localeService.getString('racing.raceOff');
            this.status.class = 'race-off';
          } else if (this.eventStatusCode === 'A' && !isMarketSuspended) {
            this.status.title = this.localeService.getString('racing.inPlay');
            this.status.class = 'race-off';
          }
          this.eventStatusUpdate.emit({id: this.event.id, data: this.status});
        }
      });
    }
  }

  ngOnDestroy(): void {
    if(this.isPubsubSubscribed) {
      this.pubSubService.unsubscribe(this.tagName);
    }
  }

  /*
  live-serve implementation to handle the event level items updation. 
  ex:quick-navigation popup
  */
  liveServeHandler() {
  const enableLiveSubscription = this.isHrEdp ? this.event.correctedDayValue == 'racing.today' : this.event.correctedDay == 'sb.today';
    if (enableLiveSubscription) {
      const channel = this.event.liveServChannels.split(',')[0];
      this.liveServeHandleUpdatesService.subscribe([channel], (update) => {
        if (update) {
          if (update.type === 'sEVENT') {
            const updatedEventData = {
              isStarted: update.payload.started == 'Y',
              isResulted: update.payload.result_conf == 'Y',
              eventStatusCode: update.payload.status
            };
            this.event = { ...this.event, ...updatedEventData };
            this.racingEventStatusHandler();
          }
        }
      });
    }
  }
  /**
   * get BIR markets enabled and modify markets
   */
  protected getBIRMarkets(): void {
    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.BIRMarketsEnabled = config?.HorseRacingBIR?.marketsEnabled;
    });
  }
  /**
   * Checks if market is enabled in CMS for BIR
   * @param {string} marketName
   * @returns {boolean}
   */
  private isBirMarketEnabled(marketName: string = ''): boolean {
    return this.BIRMarketsEnabled?.some((market: string) => marketName.toLocaleLowerCase() === market.toLocaleLowerCase());
  }
}
