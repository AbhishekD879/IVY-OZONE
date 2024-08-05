import { Component,
  OnInit,
  Input,
  ViewEncapsulation,
  OnDestroy,
  OnChanges,
  ChangeDetectionStrategy,
  SimpleChanges,
  ChangeDetectorRef
} from '@angular/core';
import { LocaleService } from '@core/services/locale/locale.service';
import { ISportSegment } from '@app/inPlay/models/sport-segment.model';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { IOutputModule } from '@featured/models/output-module.model';
import { GtmService } from '@core/services/gtm/gtm.service';
import * as _ from 'underscore';
import { ISportEvent } from '@core/models/sport-event.model';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { RoutingHelperService } from '@app/core/services/routingHelper/routing-helper.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { Subscription } from 'rxjs';
import { ISportInstanceMap } from '@app/core/services/cms/models/sport-instance.model';
import { SportsConfigHelperService } from '@app/sb/services/sportsConfig/sport-config-helper.service';

@Component({
  selector: 'featured-inplay',
  styleUrls: ['./featured-inplay.component.scss'],
  templateUrl: './featured-inplay.component.html',
  // eslint-disable-next-line
  encapsulation : ViewEncapsulation.None,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FeaturedInplayComponent implements OnInit, OnDestroy, OnChanges {
  @Input() module: IOutputModule;
  @Input() sportName: string;
  @Input() eventsCount: number;

  isSingleSportView: boolean = false;
  title: string;
  seeAllTitle: string;
  trackingKeys: string[];
  sports: ISportInstanceMap = {};
  renderData: { key: string; value: ISportEvent[] }[] = [];
  private componentName = 'featuredInplay';
  private sportsConfigSubscription: Subscription;

  constructor(private localeService: LocaleService,
    private gtmService: GtmService,
    private sportEventHelperService: SportEventHelperService,
    private pubSubService: PubSubService,
    private routingHelperService: RoutingHelperService,
    private sportsConfigService: SportsConfigService,
    private sportsConfigHelperService: SportsConfigHelperService,
    private changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit(): void {
    this.isSingleSportView = !!this.sportName;
    this.title = this.localeService.getString('sb.inPlay');
    this.pubSubService.subscribe(this.componentName, this.pubSubService.API.DELETE_EVENT_FROM_CACHE, (eventId: number) => {
      this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
      this.removeEvent(eventId);
      this.render();
    });
    this.setSeeAllTitle();
    this.render();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.module) {
      this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
      this.render();
    }
    if (changes.eventsCount) {
      this.setSeeAllTitle();
    }
    this.changeDetectorRef.markForCheck();
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.componentName);
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
  }

  /**
   * Returns title based of module location
   * @param {ISportSegment} sportSegment
   * @param {ITypeSegment} typeSegment
   * @returns {string}
   */
  getTitle(sportSegment: ISportSegment, typeSegment: ITypeSegment): string {
    return this.isSingleSportView ? typeSegment.typeName : sportSegment.categoryName;
  }

  /**
   * Track by id
   * @param index
   * @param value
   */
  trackById(index: number, value: ISportEvent): number {
    return value.id;
  }
  /**
   * Removing event from module
   * @param eventId
   */
  removeEvent(eventId: number): void {
    const sports = this.module.data;
    _.each(sports, (sportSegment: ISportSegment) => {
      _.each(sportSegment.eventsByTypeName, (typeSegment: ITypeSegment) => {
        const index = _.findIndex(typeSegment.events, { id: eventId });
        if (index > -1) {
          typeSegment.events.splice(index, 1);
        }
      });
    });
    this.changeDetectorRef.markForCheck();
  }

  /**
   * Track by index and events len
   * @param index
   * @param value
   * @returns {string}
   */
  trackByKey(index: number, value: ISportEvent[]): number {
    return index;
  }

  /**
   * GTM Show all link click
   */
  sendGTM(): void {
    this.gtmService.push('trackEvent', {
      'eventCategory': 'in-play module ',
      'eventAction': this.isSingleSportView ? 'sportpage' : 'homepage',
      'eventLabel': 'see all'
    });
  }
  /**
   * For footbal we need to render primary markets
   */
  getSelectedMarket(eventEntity: ISportEvent): string {
    let selectedMarketName: string = eventEntity.markets && eventEntity.markets.length ?
      eventEntity.markets[0].name : '';
    if (this.sportEventHelperService.isFootball(eventEntity) &&
      eventEntity.primaryMarkets &&
      eventEntity.primaryMarkets.length) {
      selectedMarketName = eventEntity.primaryMarkets[0].name;
      this.changeDetectorRef.markForCheck();
    }
    return selectedMarketName;
  }
  /**
   * Builds url for inplay page
   */
  buildInplayUrl(): string {
    return this.routingHelperService.formInplayUrl(this.sportName || '');
  }
  /**
   * Updates title for see all link
   */
  private setSeeAllTitle(): void {
    this.seeAllTitle = `${this.localeService.getString('sb.seeAll')} (${this.eventsCount})`;
    this.changeDetectorRef.markForCheck();
  }

  /**
   * As we need to render different data on different pages (home / SLP)
   * we need to build new data structure to render in one view
   *
   */
  private render(): void {
    this.renderData = [];
    this.trackingKeys = [];
    _.each(this.module.data, (sportSegment: ISportSegment) => {
      _.each(sportSegment.eventsByTypeName, (typeSegment: ITypeSegment) => {
        const trackingKey: string = this.isSingleSportView ? typeSegment.typeName : sportSegment.categoryName;
        if (!this.renderData[trackingKey]) {
          this.renderData[trackingKey] = [];
          this.trackingKeys.push(trackingKey);
        }
        this.renderData[trackingKey] = _.union(this.renderData[trackingKey], typeSegment.events);
      });
    });
    this.changeDetectorRef.detectChanges();
    if (this.trackingKeys.length) {
      this.sportsConfigSubscription = this.sportsConfigService.getSports(this.isSingleSportView ? [this.sportName] : this.trackingKeys)
        .subscribe((sportInstanceMap: ISportInstanceMap) => {
          this.trackingKeys.forEach((trackingKey: string) => {
            const sportName = this.isSingleSportView ?
              this.sportsConfigHelperService.getSportConfigName(this.sportName)
              : this.sportsConfigHelperService.getSportConfigName(trackingKey);
            this.sports[trackingKey] = sportInstanceMap[sportName];
          });
          this.changeDetectorRef.detectChanges();
        });
    }
  }
}
