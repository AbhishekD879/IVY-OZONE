

import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { BetHistoryModule } from '@betHistoryModule/bet-history.module';
import { DesktopModule } from '@desktopModule/desktop.module';

// Components
import { BetGeniusScoreboardComponent } from '@edp/components/betGeniusScoreboard/bet-genius-scoreboard.component';
import { ImgScoreboardProviderComponent } from '@edp/components/imgArenaScoreboard/components/img-scoreboard-provider.component';
import { FallbackScoreboardComponent } from '@edp/components/fallbackScoreboard/fallback-scoreboard.component';
import { OptaScoreboardComponent } from '@app/edp/directives/opta-scoreboard.component';
import { ScoreboardComponent } from '@edp/components/scoreboard/scoreboard.component';
import { AggregatedMarketsComponent } from '@edp/components/markets/aggregatedMarkets/aggregated-markets.component';
import { SingleMarketsComponent } from '@edp/components/markets/singleMarkets/single-markets.component';
import { MarketsGroupComponent } from '@edp/components/marketsGroup/markets-group.component';
import { CorrectScoreComponent } from '@edp/components/markets/correctScore/correct-score.component';
import { ScorecastComponent } from '@edp/components/markets/scorecast/scorecast.component';
import { YourCallPlayerStatsComponent } from '@edp/components/markets/playerStats/your-call-player-stats.component';
import { EdpSurfaceBetsCarouselComponent } from '@edp/components/surfaceBetsCarousel/surface-bets-carousel.component';

// Services
import { SportEventPageProviderService } from '@app/edp/components/sportEventPage/sport-event-page-provider.service';
import { SportEventMainProviderService } from '@app/edp/components/sportEventMain/sport-event-main-provider.service';
import { FootballExtensionService } from '@edp/services/footballExtension/football-extension.service';
import { TennisExtensionService } from '@edp/services/tennisExtension/tennis-extension.service';
import { CorrectScoreService } from '@edp/components/markets/correctScore/correct-score.service';
import { YourCallPlayerStatsGTMService } from '@edp/components/markets/playerStats/your-call-player-stats-grm.service';
import { ScorecastService } from '@edp/components/markets/scorecast/scorecast.service';
import { MarketsGroupService } from '@edp/services/marketsGroup/markets-group.service';
import { ScoreMarketService } from '@edp/services/scoreMarket/score-market.service';
import { SportEventPageService } from '@edp/services/sportEventPage/sport-event-page.service';
import { MarketsOptaLinksService } from '@edp/services/marketsOptaLinks/markets-opta-links.service';

// Overridden app components
import { EventMarketsComponent } from '@coralDesktop/edp/components/eventMarkets/event-markets.component';
import { DesktopEventTitleBarComponent } from '@coralDesktop/edp/components/eventTitleBar/event-title-bar.component';
import { DesktopSportEventMainComponent } from '@coralDesktop/edp/components/sportEventMain/sport-event-main.component';
import { DesktopSportEventPageComponent } from '@coralDesktop/edp/components/sportEventPage/sport-event-page.component';
import { ScorerComponent } from '@edp/components/markets/scorer/scorer.component';

import { ScoreboardLinkComponent } from '@edp/components/scoreboardLink/scoreboard-link.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [
    SharedModule,
    DesktopModule,
    BetHistoryModule],
  providers: [
    SportEventPageProviderService,
    SportEventMainProviderService,
    FootballExtensionService,
    TennisExtensionService,
    CorrectScoreService,
    YourCallPlayerStatsGTMService,
    ScorecastService,
    ScoreMarketService,
    MarketsGroupService,
    MarketsOptaLinksService,
    SportEventPageService
  ],
  declarations: [
    // Overridden app components
    DesktopEventTitleBarComponent,
    DesktopSportEventMainComponent,
    DesktopSportEventPageComponent,
    ImgScoreboardProviderComponent,
    BetGeniusScoreboardComponent,
    EventMarketsComponent,
    FallbackScoreboardComponent,
    OptaScoreboardComponent,
    ScoreboardComponent,
    AggregatedMarketsComponent,
    SingleMarketsComponent,
    MarketsGroupComponent,
    CorrectScoreComponent,
    ScorecastComponent,
    ScorerComponent,
    EdpSurfaceBetsCarouselComponent,
    YourCallPlayerStatsComponent,
    ScoreboardLinkComponent
  ],
  exports: [
    // Overridden app components
    DesktopEventTitleBarComponent,
    DesktopSportEventMainComponent,
    DesktopSportEventPageComponent,
    ImgScoreboardProviderComponent,
    BetGeniusScoreboardComponent,
    EventMarketsComponent,
    FallbackScoreboardComponent,
    OptaScoreboardComponent,
    EdpSurfaceBetsCarouselComponent,
    ScoreboardComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class EdpModule {
  static entry = DesktopSportEventMainComponent;
  constructor( private asls: AsyncScriptLoaderService){
    this.asls.loadCssFile('assets-edp.css', true, true).subscribe();
  }
}

