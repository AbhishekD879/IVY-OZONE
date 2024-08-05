import { DatePipe } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { LocaleService } from '@core/services/locale/locale.service';
import * as sbLangData from '@localeModule/translations/en-US/sb.lang';
import * as sbDesktopLangData from '@localeModule/translations/en-US/sbdesktop.lang';

import { DesktopModule } from '@desktop/desktop.module';
import { SharedModule } from '@sharedModule/shared.module';
import { OutcomeTemplateHelperService } from '@app/sb/services/outcomeTemplateHelper/outcome-template-helper.service';
import { BuildYourBetTabComponent } from '@app/sb/components/buildYourBetTab/build-your-bet-tab.component';
import { SportEventComponent } from '@app/sb/components/sportEvent/sport-event.component';
import { BuildYourBetHomeComponent } from '@app/sb/components/buildYourBetHome/build-your-bet-home.component';
import { PrivateMarketsTabComponent } from '@ladbrokesMobile/sb/components/privateMarketsTab/private-markets-tab.component';
import {
  PrivateMarketsTermsAndConditionsComponent
} from '@app/sb/components/privateMarketsTab/private-markets-terms-and-conditions.component';
import { SbFiltersService } from '@app/sb/services/sbFilters/sb-filters.service';
import { SmartBoostsService } from '@sb/services/smartBoosts/smart-boosts.service';

/* eslint-disable */
import { SportTabsService } from '@app/sb/services/sportTabs/sport-tabs.service';
import { CurrentMatchesService } from '@app/sb/services/currentMatches/current-matches.service';
import { DividendsService } from '@app/sb/services/dividents/dividends.service';
import { EnhancedMultiplesService } from '@app/sb/services/enhancedMultiples/enhanced-multiples.service';
import { EventService } from '@app/sb/services/event/event.service';
import { EventFiltersService } from '@app/sb/services/eventFilters/event-filters.service';
import { EventsByClassesService } from '@app/sb/services/eventsByClasses/events-by-classes.service';
import { IsPropertyAvailableService } from '@app/sb/services/isPropertyAvailable/is-property-available.service';
import { LiveStreamService } from '@app/sb/services/liveStream/live-stream.service';
import { MarketSortService } from '@app/sb/services/marketSort/market-sort.service';
import { StreamTrackingService } from '@app/sb/services/streamTracking/stream-tracking.service';

import { OlympicsService } from '@sb/services/olympics/olympics.service';
import { MatchResultsSportTabComponent } from '@app/sb/components/matchResultsSportTab/match-results-sport-tab.component';
// Overridden app components
import { SportMainComponent } from '@ladbrokesDesktop/sb/components/sportMain/sport-main.component';
import { DesktopSportMatchesPageComponent } from '@ladbrokesDesktop/sb/components/sportMatchesPage/sport-matches-page.component';
import { DesktopSportMatchesTabComponent } from '@ladbrokesDesktop/sb/components/sportMatchesTab/sport-matches-tab.component';
import { SportTabsPageComponent } from '@sbModule/components/SportTabsPage/sport-tabs-page.component';
import { OutrightsSportTabComponent } from '@ladbrokesDesktop/sb/components/outrightsSportTab/outrights-sport-tab.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [
    HttpClientModule,
    DesktopModule,
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
    // Overridden app components
    SportMainComponent,
    DesktopSportMatchesPageComponent,
    DesktopSportMatchesTabComponent,

    SportEventComponent,
    SportTabsPageComponent,
    OutrightsSportTabComponent,
    BuildYourBetTabComponent,
    PrivateMarketsTabComponent,
    PrivateMarketsTermsAndConditionsComponent,
    MatchResultsSportTabComponent,
    BuildYourBetHomeComponent
  ],
  exports: [
    // Overridden app components
    SportMainComponent,
    DesktopSportMatchesPageComponent,
    DesktopSportMatchesTabComponent,
    SportTabsPageComponent,
    BuildYourBetTabComponent,
    PrivateMarketsTabComponent,
    PrivateMarketsTermsAndConditionsComponent,
    MatchResultsSportTabComponent,
    OutrightsSportTabComponent,
    BuildYourBetHomeComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class SbModule {
  constructor(private localeService: LocaleService,private asls: AsyncScriptLoaderService) {
    this.localeService.setLangData(sbLangData);
    this.localeService.setLangData(sbDesktopLangData);
    this.asls.loadCssFile('assets-sb.css', true, true).subscribe();
  }
}
