import { Component, Input, OnInit, OnDestroy, ElementRef} from '@angular/core';
import { TimeService } from '@core/services/time/time.service';
import { RacingResultsService } from '@core/services/sport/racing-results.service';
import { IRacingEvent } from '@core/models/racing-event.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { IOutcome } from '@core/models/outcome.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import * as _ from 'underscore';
import { RacingPostApiService } from '@app/core/services/racing/racingPost/racing-post-api.service';
import { racing } from '@app/lazy-modules/locale/translations/en-US/racing.lang';
import { IRacingPostHRResponse, IRacingPostGHResponse } from '@app/core/services/racing/racingPost/racing-post.model';
import { CmsService } from '@core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { IStreamControl } from '@app/tote/models/stream-control.model';
import { DeviceService } from '@core/services/device/device.service';
import environment from '@environment/oxygenEnvConfig';

@Component({
  templateUrl: 'racing-event-resulted.component.html',
  styleUrls: ['./racing-event-resulted.component.scss'],
  selector: 'racing-event-resulted'
})
export class RacingEventResultedComponent implements OnInit, OnDestroy {
  @Input() eventEntity: IRacingEvent;
  @Input() filter: string;
  @Input() isGreyhoundEdp:boolean;
  @Input() streamControl?: IStreamControl;
  unPlaced: boolean = false;
  totalResults: boolean;
  eventDateSufx: string;
  antepostTerms: string;
  isCashout: boolean;
  resultsResponseError: string;
  isGreyhoundsFullResultsEnabled: boolean;
  greyhoundsFullResultsData:IRacingPostGHResponse;
  preloadStream:boolean;
  isDesktop: boolean;
  isCoral: boolean;

  private readonly tagName: string = 'RacingEventResulted';
  nativeVideoPlayerPlaceholderRef: ElementRef
  constructor(protected timeService: TimeService,
    private racingResultsService: RacingResultsService,
    private racingPostApiService: RacingPostApiService,
    private locale: LocaleService,
    private pubsubService: PubSubService,
    private gtmService: GtmService,
    private cmsService: CmsService,
    protected nativeBridgeService: NativeBridgeService,
    protected windowRef: WindowRefService,
    protected deviceService: DeviceService
    ) { }

  ngOnInit(): void {
    // reload routeSegment after lost of internet connection or sleep mode
    this.isCoral = environment && environment.brand === 'bma';

    this.pubsubService.subscribe(this.tagName, this.pubsubService.API.RELOAD_RACING_EVENT_RESULTED, () => {
      this.ngOnDestroy();
      this.ngOnInit();
    });
    this.filter = 'hideStream';

    this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
      this.isGreyhoundsFullResultsEnabled = config?.GreyhoundFullResults?.enabled;

      if (this.eventEntity.isUKorIRE  && this.eventEntity.categoryCode === 'GREYHOUNDS' && this.isGreyhoundsFullResultsEnabled) {
        this.racingPostApiService.getGreyhoundRaceOneApiResultDetails(this.eventEntity.id.toString()).subscribe((eventResultData: IRacingPostGHResponse) => {
          this.greyhoundsFullResultsData = eventResultData;
        });
      }

      this.racingResultsService.getRacingResults(this.eventEntity, this.isFullResultsRequired())
        .then(() => {
          const wewMarket = this.eventEntity.resultedWEWMarket;

          if (this.eventEntity.categoryId === racing.categoryId && this.eventEntity.isUKorIRE) {
            this.getUnplacedRaceResults()
          }
        
          if (!wewMarket.outcomes.length) {
            this.resultsResponseError = this.locale.getString('racing.noRacingResultsFound');
          } else {
            this.antepostTerms = wewMarket.isEachWayAvailable ? this.formatAntepostTerms(wewMarket.terms) : '';
            this.isCashout = wewMarket.cashoutAvail === 'Y' || wewMarket.viewType === 'handicaps';
            this.extendOutcome(wewMarket.outcomes);
            this.extendOutcome(wewMarket.unPlaced);
            if (wewMarket.nonRunners && wewMarket.nonRunners.length) {
              this.extendOutcome(wewMarket.nonRunners);
            }
          }
        }, () => {
          this.resultsResponseError = this.locale.getString('racing.noRacingResultsFound');
      });
    });

    this.eventDateSufx = this.getEventDate();
    this.isDesktop = this.deviceService.isDesktop;
  }

  /**
   * get lose and non runners horses data
   */
  getUnplacedRaceResults() {
    this.racingPostApiService.getHorseRaceOneApiResultDetails(this.eventEntity.id.toString()).subscribe((eventResultData:IRacingPostHRResponse) => {
    const resultedEventData = eventResultData.document[this.eventEntity.id.toString()];
    const totalHorses = resultedEventData.horses;
    const winHorses = this.eventEntity.resultedWEWMarket.outcomes;
    const loseHorses = this.eventEntity.resultedWEWMarket.unPlaced;
    const nonRunners = this.eventEntity.resultedWEWMarket.nonRunners;
    const nonRunnersResulted = (resultedEventData.results && resultedEventData.results.nonRunners) ?
    resultedEventData.results.nonRunners.split(',').length : nonRunners.length;
    const contestHorses = totalHorses.length - nonRunnersResulted;
    const resultsDataCheck = resultedEventData.hasOwnProperty("results");
    const runnersDataCheck = resultedEventData.results.hasOwnProperty('runners');
    if (resultsDataCheck && runnersDataCheck && loseHorses && contestHorses === resultedEventData.results.runners.length) {
      this.totalResults = false;
      this.racingResultsService.mapResultPositionPlaced(winHorses, resultedEventData.results.runners);
      this.racingResultsService.mapResultPositionUnplaced(loseHorses, resultedEventData.results.runners, this.eventEntity);
    }
    else {
      this.totalResults = true;
      return console.log('racing.incompleteResultsData');
    }
  });
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe(this.tagName);
  }

  getEventDate(): string {
    return this.timeService.getFullDateFormatSufx(new Date(this.eventEntity.startTime));
  }

  formatAntepostTerms(str: string): string {
    const newStr = str
      .replace(/(odds)/ig, 'Odds')
      .replace(/(places)/ig, 'Places')
      .replace(/\d+\/\d+( odds)/ig, match => {
        return `${match}`;
      });
    return newStr.replace(/[0-9]+(?!.*[0-9])/, match => `${match}`);
  }

  private extendOutcome(outcomes: IOutcome[]): void {
    _.each(outcomes, (outcome: IOutcome) => {
      const racingForm = _.findWhere(this.eventEntity.sortedMarkets[0].outcomes,
        { runnerNumber: outcome.runnerNumber });
      if (racingForm) {
        outcome.racingFormOutcome = racingForm.racingFormOutcome;
      }
    });
  }
  
  /**
   * Sends data to GA tracking
   * @returns void
   */
  expandUnplaced(): void {
    this.unPlaced = !this.unPlaced;
    const gtmData = {
      event: racing.trackEvent,
      eventAction: racing.raceCard,
      eventCategory: racing.horseRacing,
      eventLabel: this.unPlaced ? racing.showFullResult : racing.showLessResult,
      categoryID: this.eventEntity.categoryId,
      typeID: this.eventEntity.typeId,
      eventID: this.eventEntity.id
    }
    this.gtmService.push(gtmData.event, gtmData);
  }

  /**
   * Check For horse racing and greyhounds full results required or not
   * @returns void
   */
  private isFullResultsRequired(): boolean {
    return this.eventEntity.isUKorIRE && (this.eventEntity.categoryCode === "HORSE_RACING"  
      || (this.eventEntity.categoryCode === 'GREYHOUNDS' && this.isGreyhoundsFullResultsEnabled));
  }
  /**
  * set GA tracking object
  * @param gtmEventLabel string value
  */
  setGtmData(gaEventDetails: string): void {
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'horse racing',
      'component.LabelEvent': 'event details page',
      'component.ActionEvent': 'click',
      'component.PositionEvent': 'not applicable',
      'component.LocationEvent': this.eventEntity.typeName,
      'component.EventDetails': gaEventDetails,
      'component.URLclicked': 'not applicable',
    };
    this.gtmService.push(gtmData.event, gtmData);
  }
  playStream(e: MouseEvent): void {
    e.preventDefault();
    this.setGtmData('watch replay');        
    this.filter = this.filter === 'showVideoStream' ? 'hideStream' : 'showVideoStream';
    this.preloadStream = true;
    this.pubsubService.subscribe('RacingEventComponent', this.pubsubService.API.VIDEO_STREAM_ERROR_DIALOG_CLOSED, () => {
      this.filter = 'hideStream';
    });
 
  }
 
}
