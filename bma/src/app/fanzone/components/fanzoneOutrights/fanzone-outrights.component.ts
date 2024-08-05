import { Component, OnInit, OnDestroy, Input, ChangeDetectorRef } from '@angular/core';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { ChannelService } from '@app/core/services/liveServ/channel.service';
import { CacheEventsService } from '@app/core/services/cacheEvents/cache-events.service';
import { UpdateEventService } from '@app/core/services/updateEvent/update-event.service';
import { FanzoneAppModuleService } from '@app/fanzone/services/fanzone-module.service';
import { FanzoneDetails } from '@app/core/services/fanzone/models/fanzone.model';
import { fanzoneStorageData } from '@app/fanzone/models/fanzone.model';
import { ISportEvent } from '@app/core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';
import { FANZONE_OUTRIGHTS } from '@app/fanzone/constants/fanzoneconstants';
import { SafeResourceUrl, DomSanitizer } from '@angular/platform-browser';
import { DeviceService } from '@core/services/device/device.service';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { DomToolsService } from '@coreModule/services/domTools/dom.tools.service';
import { PlatformLocation } from '@angular/common';

@Component({
  selector: 'app-fanzone-outrights',
  template: ``,
  styleUrls: ['./fanzone-outrights.component.scss']
})
export class FanzoneAppOutrightsComponent implements OnInit, OnDestroy {
  @Input() fanzoneTeam?: fanzoneStorageData;

  fanzoneDetails: FanzoneDetails;
  leagueSrcLink: SafeResourceUrl;
  isDesktop: boolean;
  leagueTableOpened: boolean = false;
  fanzoneCompetitionIds: string = '';
  timelineBarContainer: HTMLElement = this.windowRefService.document.querySelector('.timeline-bar-container');
  public eventEntity: ISportEvent[];
  private BODY_CLASS: string = 'league-standings-opened';
  private readonly tagName: string = FANZONE_OUTRIGHTS.PUBSUB_CHANNEL_NAME;

  constructor(
    public pubSubService: PubSubService,
    protected changeDetectorRef: ChangeDetectorRef,
    protected channelService: ChannelService,
    protected cacheEventsService: CacheEventsService,
    protected updateEventService: UpdateEventService,
    protected fanzoneModuleService: FanzoneAppModuleService,
    protected fanzoneHelperService: FanzoneHelperService,
    protected filtersService: FiltersService,
    protected gtmService: GtmService,
    protected device: DeviceService,
    protected sanitizer: DomSanitizer,
    protected windowRefService: WindowRefService,
    protected domToolsService: DomToolsService,
    loc: PlatformLocation
    ) {
      loc.onPopState(() => this.removeStandingsClass());
  }

  ngOnInit(): void {
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.FANZONE_DATA, (fanzone: FanzoneDetails) => {
      this.fanzoneDetails = fanzone;
      Object.keys(fanzone).length &&  this.loadFanzoneOutrights();
    });
    this.fanzoneDetails = this.fanzoneHelperService.selectedFanzone;

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.OUTCOME_UPDATED, (market: IMarket) => {
      this.filterOutcomes(market);
      this.changeDetectorRef.detectChanges();
    });

    this.pubSubService.subscribe(this.tagName,
      [this.pubSubService.API.DELETE_EVENT_FROM_CACHE, this.pubSubService.API.DELETE_MARKET_FROM_CACHE],
      () => {
        this.changeDetectorRef.detectChanges();
      }
    );

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.DELETE_SELECTION_FROMCACHE, () => {
      this.changeDetectorRef.detectChanges();
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.SUSPENDED_EVENT, () => {
      this.changeDetectorRef.detectChanges();
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.LIVE_MARKET_FOR_EDP, (market: IMarket) => {
      this.filterOutcomes(market);
      this.changeDetectorRef.detectChanges();
    });

    this.loadFanzoneOutrights();

    this.isDesktop = this.device.isDesktop;
    const url = `${environment.FANZONE_PREMIER_LEAGUE_ENDPOINT}?team=${this.fanzoneTeam.teamName}&view=${this.isDesktop}`;
    this.leagueSrcLink = this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }

  ngOnDestroy(): void {
    !this.isDesktop && this.setZIndex('1002');
    this.cacheEventsService.clearByName('event');
    this.pubSubService.publish('UNSUBSCRIBE_LS', FANZONE_OUTRIGHTS.PUBSUB_MODULE_NAME);
    this.pubSubService.unsubscribe(this.tagName);
  }

  /**
   * Load Fanzone Outrights Data
   */
  public loadFanzoneOutrights(): void {
    this.fanzoneCompetitionIds = this.fanzoneDetails && this.prepareCompetitionIds(this.fanzoneDetails.primaryCompetitionId, this.fanzoneDetails.secondaryCompetitionId);
    if (this.fanzoneCompetitionIds) {
      this.fanzoneModuleService.getFanzoneOutrights(this.fanzoneCompetitionIds, this.fanzoneTeam.teamId).then((events) => {
        this.eventEntity = this.filtersService.orderBy(events, FANZONE_OUTRIGHTS.BY_LEAGUE_EVENTS_ORDER);
        this.liveConnection();
        this.changeDetectorRef.detectChanges();
      }).catch(() => {
        this.eventEntity = [];
      });
    }
  }

  /**
   * Prepare CompetitionIds
   * @param {String} primaryId
   * @param {String} secondaryId
   * @return {String}
   */
  private prepareCompetitionIds(primaryId, secondaryId): string {
    return primaryId.concat(",").concat(secondaryId.split(",").map(id => id.trim()).join(","));
  }

  /**
   * handler is called whenever data is received
   * subscribe for updates from events via liveServe PUSH updates (iFrame)!
   */
  public liveConnection(): void {
    this.cacheEventsService.store('event', this.eventEntity);
    this.updateEventService.init();
    const channel = this.channelService.getLSChannelsFromArray(this.eventEntity);
    this.pubSubService.publish('SUBSCRIBE_LS', {
      channel,
      module: FANZONE_OUTRIGHTS.PUBSUB_MODULE_NAME
    });
  }

  /**
   * filtered outcomes based on teamExtIds
   * @param {Array} market
   * @returns void
   */
  filterOutcomes(updatedMarket?: IMarket): void {
    this.eventEntity.forEach((event: ISportEvent) => {
      return event.markets.forEach((market: IMarket) => {
        if (updatedMarket && updatedMarket.id === market.id) {
          market.outcomes = this.applyFilters(market);
        }
      });
    });
  }

  /**
   * return the filtered outcomes which matched with teamId
   * @param {Array} market
   * @return {Array}
   */
  applyFilters(market: IMarket): IOutcome[] {
    return market.outcomes.filter(outcome => outcome.teamExtIds 
      && (outcome.teamExtIds.indexOf(this.fanzoneDetails.teamId) >= 0));
  }

  /**
   * on click of premier league table link should open fanzone league table dialog modal and track gtm
   * Toggles class to body element to enable/disable scrolling depending on clicking the  league table link.
   */
  leagueStandingsOpened(): void {
    this.leagueTableOpened = !this.leagueTableOpened;
    const body = this.windowRefService.document.body;
    if (this.leagueTableOpened) {
      this.pubSubService.publish('NETWORK_INDICATOR_INDEX_HIDE', true);
      this.domToolsService.addClass(body, this.BODY_CLASS);
      !this.isDesktop && this.setZIndex('0');

      const gtmData = {
        eventAction: FANZONE_OUTRIGHTS.PREMIER_LEAGUE.LEAGUE_TABLE,
        eventCategory: FANZONE_OUTRIGHTS.PREMIER_LEAGUE.INLINE_STATS,
        eventLabel: FANZONE_OUTRIGHTS.PREMIER_LEAGUE.PREMIER_LEAGUE,
        categoryID: FANZONE_OUTRIGHTS.PREMIER_LEAGUE.CATEGORYID,
        typeID: FANZONE_OUTRIGHTS.PREMIER_LEAGUE.TYPEID
      };
      this.gtmService.push(FANZONE_OUTRIGHTS.PREMIER_LEAGUE.TRACK_EVENT, gtmData);
    } else {
      this.pubSubService.publish('NETWORK_INDICATOR_INDEX_HIDE', false);
      this.domToolsService.removeClass(body, this.BODY_CLASS);
      !this.isDesktop && this.setZIndex('1002');
    }
  }

  /**
   * @param {string} value
   * @returns void
   * */
  setZIndex(value: string): void {
    const footerElement = this.windowRefService.document.querySelector("#footer-menu-nav");
    this.domToolsService.css(footerElement, 'z-index', value);
    this.timelineBarContainer && (this.timelineBarContainer.style.zIndex = value);
  }

  /**
   * remove league standings Class
   * @returns {void}
   */
  public removeStandingsClass(): void {
    const body = this.windowRefService.document.body;
    this.domToolsService.removeClass(body, this.BODY_CLASS);
  }
}
