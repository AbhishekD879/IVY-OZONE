import { catchError, map, switchMap } from 'rxjs/operators';
import { Component, OnDestroy, OnInit, ChangeDetectorRef } from '@angular/core';
import * as _ from 'underscore';

import { INPLAY_LIVESTREAM_CONFIG } from '@ladbrokesDesktop/inPlayLiveStream/constant/config';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { InPlayLiveStreamService } from '@ladbrokesDesktop/inPlayLiveStream/services/inPlayLiveStream/in-play-live-stream.service';
import { ISwitcherConfig } from '@core/models/switcher-config.model';
import { InplayMainService } from '@ladbrokesDesktop/inPlay/services/inplayMain/inplay-main.service';
import { throwError, Subscription } from 'rxjs';
import { ISportEvent } from '@core/models/sport-event.model';
import { ICompetitionGroupFormatted } from '@ladbrokesDesktop/inPlayLiveStream/models/competition-group.model';
import { IRibbonData, IRibbonItem } from '@app/inPlay/models/ribbon.model';
import { IFooter } from '@ladbrokesDesktop/inPlayLiveStream/models/footer.model';
import { IGtmEvent } from '@core/models/gtm.event.model';
import { IRequestConfig } from '@ladbrokesDesktop/inPlayLiveStream/models/request-config.model';
import { InplayHelperService } from '@ladbrokesDesktop/inPlay/services/inPlayHelper/inplay-helper.service';
import { IStreamsCssClasses } from '@core/models/streams-css-classes.model';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { GamingService } from '@core/services/sport/gaming.service';
import environment from '@environment/oxygenEnvConfig';
import { ILazyComponentOutput } from '@shared/components/lazy-component/lazy-component.model';

@Component({
  selector: 'inplay-live-stream',
  templateUrl: './inplay-live-stream.component.html',
  styleUrls: ['./inplay-live-stream.component.scss']
})
export class InPlayLiveStreamComponent implements OnInit, OnDestroy {
  cSyncName: string = `inplaySection`;
  viewByFilters: string[] = INPLAY_LIVESTREAM_CONFIG.viewByFilters;
  activeFilter: string = INPLAY_LIVESTREAM_CONFIG.viewByFilters[0];
  requestConfigLiveEvent: IRequestConfig = INPLAY_LIVESTREAM_CONFIG.requestConfigLiveEvent;
  requestConfigLiveStream: IRequestConfig = INPLAY_LIVESTREAM_CONFIG.requestConfigLiveStream;
  filterConfig = this.requestConfigLiveEvent;
  prevCategoryId = null;

  categoryName: string;
  categoryId: number;
  eventAction: string;
  events: ISportEvent[];
  footer: IFooter;
  menuItems: IRibbonItem[] = [];
  switchers: ISwitcherConfig[];
  gtmDataLayer: IGtmEvent;
  competitions: ICompetitionGroupFormatted[];
  activeEvent: ISportEvent;
  cssClassesForStreams: IStreamsCssClasses = {
    iGameMedia: 'd-live-stream-module',
    otherProviders: 'live-column watch-live'
  };
  loading: boolean = true;
  sport: GamingService;
  private sportsConfigSubscription: Subscription;
  readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;

  constructor(
    private pubSubService: PubSubService,
    private inplayHelperService: InplayHelperService,
    private inPlayLiveStreamService: InPlayLiveStreamService,
    private inplayMainService: InplayMainService,
    private changeDetectorRef: ChangeDetectorRef,
    private sportsConfigService: SportsConfigService
  ) {
    this._changeFilter = this._changeFilter.bind(this);
  }

  ngOnInit(): void {
    // Update data on sport change
    this.pubSubService.subscribe(this.cSyncName, this.pubSubService.API.SPORT_CHANGED, item => {
      this.filterConfig = this.activeFilter === this.viewByFilters[0] ? this.requestConfigLiveEvent : this.requestConfigLiveStream;
      this.inplayHelperService.unsubscribeForLiveUpdates(this.events);
      this.prevCategoryId = this.categoryId;
      this.categoryName = item.categoryName.toLowerCase();
      this.categoryId = item.categoryId;
      this.eventAction = this.activeFilter === this.viewByFilters[0] ? 'in-play' : 'live stream';
      this.inPlayLiveStreamService.sendGTM(this.eventAction, `nav - ${this.categoryName}`);

      this.sportsConfigSubscription = this.sportsConfigService.getSport(this.categoryName).subscribe((sportInstance: GamingService) => {
        this.sport = sportInstance;
      });

      this.getData(this.categoryId, this.categoryName, this.filterConfig)
        .subscribe(data => {
          this._setSwitchers();
          this.inplayHelperService.unsubscribeForSportCompetitionChanges(this.prevCategoryId, this.filterConfig.requestParams.topLevelType);
          this.inplayHelperService.subscribeForSportCompetitionChanges(this.categoryId, this.filterConfig.requestParams.topLevelType);
        });
    });

    // Update data on competition change
    this.pubSubService.subscribe(this.cSyncName, this.pubSubService.API.INPLAY_LS_COMPETITION_ADDED, () => {
      if (this.events.length < 4) {
        this.filterConfig = this.activeFilter === this.viewByFilters[0] ? this.requestConfigLiveEvent : this.requestConfigLiveStream;
        this.getData(this.categoryId, this.categoryName, this.filterConfig, true)
          .subscribe();
      }
      this.footer = this.inPlayLiveStreamService.prepareFooter(
        this.categoryName,
        this.menuItems,
        this.filterConfig.requestParams.topLevelType);
    });

    // Update Event Counter
    this.pubSubService.subscribe(this.cSyncName, 'EVENT_COUNT_UPDATE', data => {
      this.menuItems = data;
      this._setSwitchers();
      this.footer = this.inPlayLiveStreamService.prepareFooter(
        this.categoryName,
        this.menuItems,
        this.filterConfig.requestParams.topLevelType
      );
    });

    // Delete Event From Cache
    this.pubSubService.subscribe(this.cSyncName, this.pubSubService.API.DELETE_EVENT_FROM_CACHE, eventId => {
      this.activeEvent = this.events[0];
      this.inPlayLiveStreamService.removeEventFromCollection(this.competitions, eventId);
      this.footer = this.inPlayLiveStreamService.prepareFooter(
        this.categoryName,
        this.menuItems,
        this.filterConfig.requestParams.topLevelType);
    });
    // Delete Competition From Cache
    this.pubSubService.subscribe(this.cSyncName, this.pubSubService.API.INPLAY_LS_COMPETITION_REMOVED, data => {
      this.inPlayLiveStreamService.removeCompetitionFromCollection(this.competitions, data.removed);
      if(this.categoryId.toString() === this.HORSE_RACING_CATEGORY_ID) {
        this.filterConfig = this.activeFilter === this.viewByFilters[0] ? this.requestConfigLiveEvent : this.requestConfigLiveStream;
        this.getData(this.categoryId, this.categoryName, this.filterConfig, true)
          .subscribe();
      }      
    });

    const config = this.activeFilter === this.viewByFilters[0] ? this.requestConfigLiveEvent : this.requestConfigLiveStream;

    this.inplayHelperService.getRibbonData(config).pipe(
      map((ribbon: IRibbonData) => {
        this.menuItems = this.inplayMainService.getGeFilteredRibbonItems(ribbon.items);
        this.categoryName = this.categoryName || this.menuItems[0].categoryName.toLowerCase();
        this.categoryId = this.categoryId || this.menuItems[0].categoryId;
        this.inplayHelperService.subscribeForSportCompetitionChanges(this.categoryId, 'LIVE_EVENT');
        this._setSwitchers();
        return ribbon;
      }),
      switchMap(() => {
        return this.getData(this.categoryId, this.categoryName, config);
      })
    ).subscribe(() => {}, (error) => {
      return throwError(error);
    }, () => {
      this.inplayHelperService.subscribe4RibbonUpdates();
    });

    this.pubSubService.subscribe(this.cSyncName, this.pubSubService.API.SESSION_LOGIN, () => {
      if (this.inplayMainService.isNewUserFromOtherCountry()) {
        this.ngOnDestroy();
        this.ngOnInit();
      }
    });

    this.pubSubService.subscribe(this.cSyncName, 'RELOAD_IN_PLAY', () => {
      this.ngOnDestroy();
      this.ngOnInit();
    });
  }

  ngOnDestroy(): void {
    this.filterConfig = this.activeFilter === this.viewByFilters[0] ? this.requestConfigLiveEvent : this.requestConfigLiveStream;
    this.inplayHelperService.unsubscribe4RibbonUpdates();
    this.inplayHelperService.unsubscribeForSportCompetitionChanges(this.categoryId, this.filterConfig.requestParams.topLevelType);
    this.inplayHelperService.unsubscribeForLiveUpdates(this.events);
    this.pubSubService.unsubscribe(this.cSyncName);
    this.inplayMainService.unsubscribeForUpdates();
    this.inplayHelperService.disconnect();
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
  }

  updateActiveEvent(event: ILazyComponentOutput): void {
    this.activeEvent = event.value;
  }

  /**
   * Go to filter (in-play, live stream)
   */
  _changeFilter(filter): void {
    this.inplayHelperService.unsubscribeForLiveUpdates(this.events);
    this.activeFilter = filter;
    this.gtmDataLayer = {
      eventAction: filter === this.viewByFilters[0] ? 'in-play' : 'live stream',
      eventLabel: 'more markets'
    };
    this.filterConfig = filter === this.viewByFilters[0] ? this.requestConfigLiveEvent : this.requestConfigLiveStream;
    const prevFilterConfig = filter === this.viewByFilters[1] ? this.requestConfigLiveEvent : this.requestConfigLiveStream;
    this.pubSubService.publish(this.pubSubService.API.EVENT_COUNT, this.activeFilter);
    this.getData(this.categoryId, this.categoryName, this.filterConfig)
      .subscribe(() => {
        this.inplayHelperService.unsubscribeForSportCompetitionChanges(this.categoryId, prevFilterConfig.requestParams.topLevelType);
        this.inplayHelperService.subscribeForSportCompetitionChanges(this.categoryId, this.filterConfig.requestParams.topLevelType);
      });
  }

  /**
   * Switchers for SINGLE SPORT
   */
  _setSwitchers(): void {
    this.switchers = this.inPlayLiveStreamService.generateSwitchers(
      this._changeFilter,
      this.viewByFilters
    );
  }

  /**
   * Get data for single sport
   * @param {Number} categoryId
   * @param {String} categoryName
   * @param {Object} requestConfig
   * @param {Object} isCompetitionAdded
   */
  getData(categoryId: number, categoryName: string, requestConfig: IRequestConfig, isCompetitionAdded?: boolean) {
    this.loading = true;
    this.competitions = [];
    this.footer = null;
    this.changeDetectorRef.detectChanges();

    return this.inPlayLiveStreamService.getData(categoryId, categoryName, requestConfig, this.menuItems).pipe(
      map(data => {
        this.events = data.events;
        if (requestConfig.requestParams.topLevelType === 'STREAM_EVENT') {
          this.activeEvent = isCompetitionAdded ? this.activeEvent : data.events[0];
        } else {
          this.activeEvent = null;
        }
        this.competitions = data.competitions;
        this.loading = false;
        this.footer = data.footer;
        this.changeDetectorRef.detectChanges();
        return data;
      }),
      catchError(error => {
        return throwError(error);
      })
    );
  }

  isCompetitionsPresent(): boolean {
    return !_.isEmpty(this.competitions);
  }
}
