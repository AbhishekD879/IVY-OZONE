import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';

// Components
import { BetGeniusScoreboardComponent } from './components/betGeniusScoreboard/bet-genius-scoreboard.component';
import { ImgScoreboardProviderComponent } from './components/imgArenaScoreboard/components/img-scoreboard-provider.component';
import { EventTitleBarComponent } from './components/eventTitleBar/event-title-bar.component';
import { FallbackScoreboardComponent } from '@edp/components/fallbackScoreboard/fallback-scoreboard.component';
import { OptaScoreboardComponent } from '@app/edp/directives/opta-scoreboard.component';
import { ScoreboardComponent } from './components/scoreboard/scoreboard.component';
import { SportEventMainComponent } from '@app/edp/components/sportEventMain/sport-event-main.component';
import { SportEventPageComponent } from '@app/edp/components/sportEventPage/sport-event-page.component';
import { AggregatedMarketsComponent } from '@edp/components/markets/aggregatedMarkets/aggregated-markets.component';
import { SingleMarketsComponent } from '@edp/components/markets/singleMarkets/single-markets.component';
import { MarketsGroupComponent } from '@edp/components/marketsGroup/markets-group.component';
import { CorrectScoreComponent } from '@edp/components/markets/correctScore/correct-score.component';
import { ScorecastComponent } from '@edp/components/markets/scorecast/scorecast.component';
import { YourCallPlayerStatsComponent } from '@edp/components/markets/playerStats/your-call-player-stats.component';
import { EdpSurfaceBetsCarouselComponent } from '@edp/components/surfaceBetsCarousel/surface-bets-carousel.component';
import { ScoreboardLinkComponent } from '@edp/components/scoreboardLink/scoreboard-link.component';

// Services
import { SportEventPageProviderService } from '@app/edp/components/sportEventPage/sport-event-page-provider.service';
import { SportEventMainProviderService } from '@app/edp/components/sportEventMain/sport-event-main-provider.service';
import { FootballExtensionService } from './services/footballExtension/football-extension.service';
import { TennisExtensionService } from './services/tennisExtension/tennis-extension.service';
import { CorrectScoreService } from '@edp/components/markets/correctScore/correct-score.service';
import { YourCallPlayerStatsGTMService } from '@edp/components/markets/playerStats/your-call-player-stats-grm.service';
import { ScorecastService } from '@edp/components/markets/scorecast/scorecast.service';
import { MarketsGroupService } from '@edp/services/marketsGroup/markets-group.service';
import { ScoreMarketService } from '@edp/services/scoreMarket/score-market.service';
import { EventMarketsComponent } from '@edp/components/eventMarkets/event-markets.component';
import { ScorerComponent } from './components/markets/scorer/scorer.component';
import { SportEventPageService } from './services/sportEventPage/sport-event-page.service';
import { MarketsOptaLinksService } from '@edp/services/marketsOptaLinks/markets-opta-links.service';
import { LazyEventVideoStreamModule } from '@lazy-modules/eventVideoStream/event-video-stream.module';
import { AsyncScriptLoaderService } from '../core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [
    SharedModule,
    LazyEventVideoStreamModule
  ],
  providers: [
    SportEventPageService,
    SportEventPageProviderService,
    SportEventMainProviderService,
    FootballExtensionService,
    TennisExtensionService,
    CorrectScoreService,
    YourCallPlayerStatsGTMService,
    ScorecastService,
    ScoreMarketService,
    MarketsGroupService,
    MarketsOptaLinksService
  ],
  declarations: [
    EventMarketsComponent,
    BetGeniusScoreboardComponent,
    ImgScoreboardProviderComponent,
    EventTitleBarComponent,
    FallbackScoreboardComponent,
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
