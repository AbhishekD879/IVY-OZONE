import { Component, ChangeDetectorRef, ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';
import { LocaleService } from '@core/services/locale/locale.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { MarketTypeService } from '@shared/services/marketType/market-type.service';
import { TimeService } from '@core/services/time/time.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { TemplateService } from '@shared/services/template/template.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { SmartBoostsService } from '@sb/services/smartBoosts/smart-boosts.service';
import { UserService } from '@core/services/user/user.service';
import { BetslipSelectionsDataService } from '@core/services/betslipSelectionsData/betslip-selections-data';
import { CommandService } from '@core/services/communication/command/command.service';
import { PriceOddsButtonAnimationService } from '@shared/components/priceOddsButton/price-odds-button.animation.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FavouritesService } from '@app/favourites/services/favourites.service';
import { SportsConfigService } from '@sb/services/sportsConfig/sports-config.service';
import { ScoreParserService } from '@core/services/scoreParser/score-parser.service';
import { SportEventHelperService } from '@core/services/sportEventHelper/sport-event-helper.service';
import { SeoDataService } from '@coreModule/services/seoData/seo-data.service';
import { OddsCardSportComponent } from '@app/shared/components/oddsCard/oddsCardSport/odds-card-sport.component';

@Component({
  selector: 'list-template',
  templateUrl: 'list-template.component.html',
  styleUrls: ['list-template.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class ListTemplateComponent extends OddsCardSportComponent {

  allShown: boolean = false;
  limit: number;
  selectionsLimit: number = 8;

  constructor(
    templateService: TemplateService,
    marketTypeService: MarketTypeService,
    public timeService: TimeService,
    locale: LocaleService,
    filtersService: FiltersService,
    coreToolsService: CoreToolsService,
    routingHelper: RoutingHelperService,
    pubSubService: PubSubService,
    router: Router,
    smartBoostsService: SmartBoostsService,
    userService: UserService,
    commandService: CommandService,
    windowRef: WindowRefService,
    betSlipSelectionsData: BetslipSelectionsDataService,
    priceOddsButtonService: PriceOddsButtonAnimationService,
    routingState: RoutingState,
    gtmTrackingService: GtmTrackingService,
    gtmService: GtmService,
    favouritesService: FavouritesService,
    sportsConfigService: SportsConfigService,
    scoreParserService: ScoreParserService,
    sportEventHelperService: SportEventHelperService,
    changeDetectorRef: ChangeDetectorRef,
    seoDataService: SeoDataService
  ) {
    super(
      templateService, marketTypeService, timeService, locale, filtersService, coreToolsService,
      routingHelper, pubSubService, router, smartBoostsService, userService, commandService, windowRef, betSlipSelectionsData,
      priceOddsButtonService, routingState, gtmTrackingService, gtmService, favouritesService, sportsConfigService, scoreParserService,
      sportEventHelperService, changeDetectorRef, seoDataService
    )
    this.limit = this.selectionsLimit;
  }

  toggleShow(): void {
    this.allShown = !this.allShown;
    if (this.allShown) {
      this.limit = undefined;
    } else {
      this.limit = this.selectionsLimit;
    }
  }

  /**
   * Checking for display markets count
   */
   isShowMarketsCount(): boolean {
     if(!this.event.marketsCount && this.event.categoryCode === 'GOLF'){
      this.event.marketsCount = this.event.markets.length;
     }
    return !this.sportsViewTypes.outrights && this.event.marketsCount > 1 && this.isOddsSports;
  }

}
