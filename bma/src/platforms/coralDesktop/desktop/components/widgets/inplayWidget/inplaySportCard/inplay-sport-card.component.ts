import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import * as _ from 'underscore';

import { MarketTypeService } from '@shared/services/marketType/market-type.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { IWidgetEventNames } from '@desktop/models/wigets.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { IMarket } from '@core/models/market.model';
import { IOutcome } from '@core/models/outcome.model';
import { IDeleteMarketEventOptions } from '@core/models/update-options.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { ISportConfig, ISportInstance } from '@core/services/cms/models';
import { Subscription } from 'rxjs';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';

@Component({
  selector: 'inplay-sport-card',
  templateUrl: './inplay-sport-card.component.html'
})
export class InplaySportCardComponent implements OnInit, OnDestroy {
  @Input() event: ISportEvent;
  @Input() events: ISportEvent[];
  @Input() sportName: string;

  market: IMarket;
  outcomes: IOutcome[];
  isOutcomesExists: boolean;
  isEventSecondNameAvailable: boolean;
  eventNames: IWidgetEventNames;
  isFootball: boolean;
  marketsCount: string;
  sportConfig: ISportConfig;

  private headerHas2Columns: boolean;
  private headerHas3Columns: boolean;
  private sportsConfigSubscription: Subscription;

  constructor(
    private pubSubService: PubSubService,
    private sportEventHelperService: SportEventHelperService,
    private filtersService: FiltersService,
    private routingHelperService: RoutingHelperService,
    private router: Router,
    private marketTypeService: MarketTypeService,
    private sportsConfigService: SportsConfigService,
    private seoDataService: SeoDataService
  ) {}

  ngOnInit(): void {
    this.market = this.event.markets[0];
    this.sortOutcomes();

    // Check if event has only one event name
    this.isEventSecondNameAvailable = this.sportEventHelperService.isEventSecondNameAvailable(this.event);
    // Parse event names
    this.eventNames = this.sportEventHelperService.getEventNames(this.event);
    this.isFootball = this.sportEventHelperService.isFootball(this.event);
    this.marketsCount = `+ ${this.sportEventHelperService.getMarketsCount(this.event)}`;
    this.headerHas2Columns = this.market && !this.marketTypeService.isMatchResultType(this.market) &&
      !this.marketTypeService.isHomeDrawAwayType(this.market);

    this.sportsConfigSubscription = this.sportsConfigService.getSport(this.sportName).subscribe((sportInstance: ISportInstance) => {
      this.sportConfig = sportInstance.sportConfig;
      this.headerHas3Columns = this.sportEventHelperService.isHomeDrawAwayType(this.event, sportInstance.sportConfig);
    });

    this.watchDeletedOutcomes();
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(`in-play-sport-card-${this.event.id}`);
    this.sportsConfigSubscription && this.sportsConfigSubscription.unsubscribe();
  }

  trackById(index: number, outcome: IOutcome): string {
    return outcome && outcome.id ? `${outcome.id}_${index}` : index.toString();
  }

  /**
   * Check if live stream is available for event
   * @returns {boolean}
   */
  isStreamAvailable(): boolean {
    return this.sportEventHelperService.isStreamAvailable(this.event);
  }

  /**
   * Check if market counter should be shown
   * @returns {boolean}
   */
  showMarketsCount(): boolean {
    return this.sportEventHelperService.showMarketsCount(this.event);
  }
  /**
   * Checks if odds button wrapper should be shown
   * @param index
   * @returns {boolean}
   */
  isOddButtonShown(index: number): boolean {
    const homeDrawAwayType = 'homeDrawAwayType';
    const oneThreeType = 'oneThreeType';
    const headerHas3Columns = this.event.oddsCardHeaderType === homeDrawAwayType || this.event.oddsCardHeaderType === oneThreeType;

    const isThreeColumns = (((!this.headerHas2Columns || (this.headerHas2Columns && index !== 1)) &&
      this.headerHas3Columns) || headerHas3Columns);

    return isThreeColumns || (!this.headerHas3Columns && index !== 1);
  }

  /**
   * Redirects to event details page
   * @param {ISportEvent} event
   * @returns {*}
   */
  goToEvent(justReturn: boolean, event: ISportEvent): string | boolean {
    const edpUrl: string = this.routingHelperService.formEdpUrl(event);
    if (!justReturn) {
      this.router.navigateByUrl(edpUrl);
    }
    return edpUrl;
  }

  goToSeo(event: ISportEvent):void {
    const edpUrl: string = this.routingHelperService.formEdpUrl(event);
    this.seoDataService.eventPageSeo(event, edpUrl);
  }

  /**
   * Get sorted outcomes from market outcomes
   * @returns {IOutcome[]}
   */
  private sortOutcomes(): void {
    this.outcomes = this.market && this.market.outcomes;
    this.isOutcomesExists = this.outcomes && this.outcomes.length > 0;
    if (this.isOutcomesExists) {
      this.outcomes = _.map(this.filtersService.groupBy(this.outcomes,
        'correctedOutcomeMeaningMinorCode'), value => value[0]);
    }
  }

  /**
   *  Refresh and sort outcomes after live updates.
   */
  private watchDeletedOutcomes() {
    this.pubSubService.subscribe(`in-play-sport-card-${this.event.id}`,
      this.pubSubService.API.DELETE_SELECTION_FROMCACHE, (options: IDeleteMarketEventOptions) => {
        const eventId = options.eventId;
        if (this.event.id === parseInt(eventId, 10)) {
          this.sortOutcomes();
        }
      }
    );
  }
}
