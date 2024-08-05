import { DatePipe } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { LocaleService } from '@core/services/locale/locale.service';
import * as sbLangData from '@localeModule/translations/en-US/sb.lang';

import { SharedModule } from '@sharedModule/shared.module';
import { OutcomeTemplateHelperService } from '@sb/services/outcomeTemplateHelper/outcome-template-helper.service';
import { BuildYourBetTabComponent } from '@sb/components/buildYourBetTab/build-your-bet-tab.component';
import { BuildYourBetHomeComponent } from '@sb/components/buildYourBetHome/build-your-bet-home.component';
import { SmartBoostsService } from '@sb/services/smartBoosts/smart-boosts.service';
import { OutrightsSportTabComponent } from '@sb/components/outrightsSportTab/outrights-sport-tab.component';
import { PrivateMarketsTabComponent } from '@sb/components/privateMarketsTab/private-markets-tab.component';
import { PrivateMarketsTermsAndConditionsComponent } from '@sb/components/privateMarketsTab/private-markets-terms-and-conditions.component';
import { SbFiltersService } from '@sb/services/sbFilters/sb-filters.service';
import { SportTabsService } from '@sb/services/sportTabs/sport-tabs.service';
import { CurrentMatchesService } from '@sb/services/currentMatches/current-matches.service';
import { DividendsService } from '@sb/services/dividents/dividends.service';
import { EnhancedMultiplesService } from '@sb/services/enhancedMultiples/enhanced-multiples.service';
import { EventService } from '@sb/services/event/event.service';
import { EventFiltersService } from '@sb/services/eventFilters/event-filters.service';
import { EventsByClassesService } from '@sb/services/eventsByClasses/events-by-classes.service';
import { IsPropertyAvailableService } from '@sb/services/isPropertyAvailable/is-property-available.service';
import { LiveStreamService } from '@sb/services/liveStream/live-stream.service';
import { MarketSortService } from '@sb/services/marketSort/market-sort.service';
import { StreamTrackingService } from '@sb/services/streamTracking/stream-tracking.service';
import { OlympicsService } from '@sb/services/olympics/olympics.service';

import { MatchResultsSportTabComponent } from '@app/sb/components/matchResultsSportTab/match-results-sport-tab.component';
import { AsyncScriptLoaderService } from '../core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [
    HttpClientModule,
    FormsModule,
    SharedModule
  ],
  providers: [
    EventFiltersService,
    EnhancedMultiplesService,
    IsPropertyAvailableService,
    DividendsService,
    EventsByClassesService,
    LiveStreamService,
    StreamTrackingService,
    MarketSortService,
    SportTabsService,
    OutcomeTemplateHelperService,
    EventService,
    CurrentMatchesService,
    SbFiltersService,
    DatePipe,
    SmartBoostsService,
    OlympicsService
  ],
  declarations: [
    OutrightsSportTabComponent,
    BuildYourBetTabComponent,
    PrivateMarketsTabComponent,
    PrivateMarketsTermsAndConditionsComponent,
    MatchResultsSportTabComponent,
    BuildYourBetHomeComponent
  ],
  exports: [
    BuildYourBetTabComponent,
    PrivateMarketsTabComponent,
    PrivateMarketsTermsAndConditionsComponent,
    MatchResultsSportTabComponent,
    BuildYourBetHomeComponent,
    OutrightsSportTabComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class SbModule {
  constructor(private localeService: LocaleService,private asls: AsyncScriptLoaderService) {
    this.localeService.setLangData(sbLangData);
    this.asls.loadCssFile('assets-sb.css', true, true).subscribe();
  }
}


