import { Component, Input, OnInit, ChangeDetectorRef, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';

import { OddsCardComponent } from '../odds-card.component';
import { FiltersService } from '@core/services/filters/filters.service';
import { MarketTypeService } from '@shared/services/marketType/market-type.service';
import { TimeService } from '@core/services/time/time.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { TemplateService } from '@shared/services/template/template.service';
import { EventService } from '@sb/services/event/event.service';
import { IOutcome } from '@core/models/outcome.model';
import { SportsConfigHelperService } from '@sb/services/sportsConfig/sport-config-helper.service';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';

@Component({
  selector: 'odds-card-enhanced',
  templateUrl: 'odds-card-enhanced-multiples.component.html'
})

export class OddsCardEnhancedMultiplesComponent extends OddsCardComponent implements OnInit, OnDestroy {

  @Input() gtmModuleTitle?: string;

  nameOverride: string;
  private readonly tagName: string = 'OddsCardEnhancedMultiplesComponent';

  constructor(
    eventFactory: EventService,
    marketTypeService: MarketTypeService,
    templateService: TemplateService,
    timeService: TimeService,
    filters: FiltersService,
    routingHelper: RoutingHelperService,
    router: Router,
    sportsConfigHelperService: SportsConfigHelperService,
    seoDataService: SeoDataService,
    gtmService :GtmService,
    private pubSubService: PubSubService,
    private changeDetectorRef: ChangeDetectorRef
  ) {
    super(eventFactory, marketTypeService, timeService,
      filters, routingHelper, templateService, router, sportsConfigHelperService,seoDataService,gtmService);
  }

  ngOnInit(): void {
    // temporary solution till nameOverride will be implemented on featured MS side
    super.ngOnInit();
    this.nameOverride = this.nameOverride ||
      (this.featured && this.featured.isSelection && this.eventName);

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.WS_EVENT_UPDATE, () => {
      this.changeDetectorRef.detectChanges();
    });
  }

  ngOnDestroy() {
    this.pubSubService.unsubscribe(this.tagName);
  }

  trackById(outcome: IOutcome): string {
    return outcome.id;
  }

  nameOfEvent(outcome: { name: string }): string {
    return this.nameOverride || outcome.name;
  }

  filterOutcomes(outcomes: IOutcome[]): IOutcome[] {
    if (this.limitSelections || this.limitSelections === 0) {
      outcomes = outcomes.slice(0, Number(this.limitSelections));
    }
    return outcomes;
  }
}
