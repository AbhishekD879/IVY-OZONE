import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { OddsCardComponent } from '../odds-card.component';
import { IOutcome } from '@core/models/outcome.model';

import { TimeService } from '@core/services/time/time.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { MarketTypeService } from '@shared/services/marketType/market-type.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { TemplateService } from '@shared/services/template/template.service';
import { EventService } from '@sb/services/event/event.service';
import { SmartBoostsService } from '@sb/services/smartBoosts/smart-boosts.service';
import { SportsConfigHelperService } from '@sb/services/sportsConfig/sport-config-helper.service';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { GtmService } from '@app/core/services/gtm/gtm.service';

@Component({
  selector: 'odds-card-specials',
  templateUrl: 'odds-card-specials.component.html'
})

export class OddsCardSpecialsComponent extends OddsCardComponent implements OnInit {

  @Input() gtmModuleTitle?: string;

  outcomes: IOutcome[];
  isSmartBoosts: boolean;
  outcomeName: string;
  wasPrice: string;

  constructor(
    eventFactory: EventService,
    marketTypeService: MarketTypeService,
    templateService: TemplateService,
    router: Router,
    timeService: TimeService,
    filters: FiltersService,
    routingHelper: RoutingHelperService,
    private smartBoostsService: SmartBoostsService,
    sportsConfigHelperService: SportsConfigHelperService,
    seoDataService: SeoDataService,
    gtmService :GtmService
  ) {
    super(eventFactory, marketTypeService, timeService,
      filters, routingHelper, templateService, router, sportsConfigHelperService, seoDataService,gtmService);
  }

  get oddsName(): string {
    return this.outcomes && this.outcomes.length > 1 ? this.eventName : this.outcomeName;
  }
  set oddsName(value:string){}

  ngOnInit(): void {
    super.ngOnInit();

    const { markets } = this.event;

    this.isSmartBoosts = this.smartBoostsService.isSmartBoosts(markets[0]);
    this.outcomes = markets.length ? markets[0].outcomes : [];

    this.formNameAndWasPrice();
  }

  /**
   * Form score and selection name
   */
  formNameAndWasPrice(): void {
    let outcomeName = this.outcomes && this.outcomes.length ? this.outcomes[0].name : '';
    if (this.isSmartBoosts) {
      const parsedName = this.smartBoostsService.parseName(outcomeName);

      outcomeName = parsedName.name;
      this.wasPrice = parsedName.wasPrice;
    }
    this.outcomeName = outcomeName;
  }
}
