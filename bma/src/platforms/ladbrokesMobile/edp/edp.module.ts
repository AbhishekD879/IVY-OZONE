import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';


// Components
import { FallbackScoreboardComponent } from '@edp/components/fallbackScoreboard/fallback-scoreboard.component';
import { OptaScoreboardComponent } from '@app/edp/directives/opta-scoreboard.component';
import { MarketsGroupComponent } from '@edp/components/marketsGroup/markets-group.component';
import { YourCallPlayerStatsComponent } from '@edp/components/markets/playerStats/your-call-player-stats.component';
import { EdpSurfaceBetsCarouselComponent } from '@edp/components/surfaceBetsCarousel/surface-bets-carousel.component';
import { ScoreboardLinkComponent } from '@edp/components/scoreboardLink/scoreboard-link.component';

// Services
import { SportEventPageProviderService } from '@app/edp/components/sportEventPage/sport-event-page-provider.service';
import { SportEventMainProviderService } from '@app/edp/components/sportEventMain/sport-event-main-provider.service';
import { CorrectScoreService } from '@edp/components/markets/correctScore/correct-score.service';
import { YourCallPlayerStatsGTMService } from '@edp/components/markets/playerStats/your-call-player-stats-grm.service';
import { MarketsGroupService } from '@edp/services/marketsGroup/markets-group.service';
import { ScoreMarketService } from '@edp/services/scoreMarket/score-market.service';
import { FootballExtensionService } from '@edp/services/footballExtension/football-extension.service';
import { TennisExtensionService } from '@edp/services/tennisExtension/tennis-extension.service';
import { BetGeniusScoreboardComponent } from '@edp/components/betGeniusScoreboard/bet-genius-scoreboard.component';
import { ImgScoreboardProviderComponent } from '@edp/components/imgArenaScoreboard/components/img-scoreboard-provider.component';

import { ScoreboardComponent } from '@edp/components/scoreboard/scoreboard.component';
import { MarketsOptaLinksService } from '@edp/services/marketsOptaLinks/markets-opta-links.service';
import { SportEventPageService } from '@edp/services/sportEventPage/sport-event-page.service';
// Overridden
import { ScorecastService } from '@ladbrokesMobile/edp/components/markets/scorecast/scorecast.service';
import { EventTitleBarComponent } from '@ladbrokesMobile/edp/components/eventTitleBar/event-title-bar.component';
import { SportEventMainComponent } from '@ladbrokesMobile/edp/components/sportEventMain/sport-event-main.component';
import { EventMarketsComponent } from '@ladbrokesMobile/edp/components/eventMarkets/event-markets.component';
import { ScorecastComponent } from '@ladbrokesMobile/edp/components/markets/scorecast/scorecast.component';
import { SportEventPageComponent } from '@ladbrokesMobile/edp/components/sportEventPage/sport-event-page.component';
import { AggregatedMarketsComponent } from '@ladbrokesMobile/edp/components/markets/aggregatedMarkets/aggregated-markets.component';
import { SingleMarketsComponent } from '@ladbrokesMobile/edp/components/markets/singleMarkets/single-markets.component';
import { FiveAsideLauncherComponent } from '@ladbrokesMobile/edp/components/fiveAsideLauncher/five-a-side-launcher.component';
import { CorrectScoreComponent } from '@ladbrokesMobile/edp/components/markets/correctScore/correct-score.component';
import { ScorerComponent } from '@ladbrokesMobile/edp/components/markets/scorer/scorer.component';
import { LazyEventVideoStreamModule } from '@ladbrokesMobile/lazy-modules/eventVideoStream/event-video-stream.module';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [
    SharedModule,
    LazyEventVideoStreamModule
  ],
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
    EventMarketsComponent,
    BetGeniusScoreboardComponent,
    ImgScoreboardProviderComponent,
    EventTitleBarComponent,
    FallbackScoreboardComponent,
    FiveAsideLauncherComponent,
    OptaScoreboardComponent,
    ScoreboardComponent,
    SportEventMainComponent,
    SportEventPageComponent,
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
    EventMarketsComponent,
    BetGeniusScoreboardComponent,
    ImgScoreboardProviderComponent,
    EventTitleBarComponent,
    FallbackScoreboardComponent,
    OptaScoreboardComponent,
    ScoreboardComponent,
    FiveAsideLauncherComponent,
    SportEventMainComponent,
    EdpSurfaceBetsCarouselComponent,
    SportEventPageComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class EdpModule {
  static entry = SportEventMainComponent;
  constructor( private asls: AsyncScriptLoaderService){
    this.asls.loadCssFile('assets-edp.css', true, true).subscribe();
  }
}