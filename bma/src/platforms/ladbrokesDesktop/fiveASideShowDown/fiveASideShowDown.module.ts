import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule, DecimalPipe } from '@angular/common';
import { FiveASideShowDownRoutingModule } from './fiveASideShowDown-routing.module';
import {
  FiveASideLiveLeaderBoardComponent
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveASideLiveLeaderBoard/fiveaside-live-leader-board.component';
import {
  FiveASidePostLeaderBoardComponent
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveASidePostLeaderBoard/fiveaside-post-leader-board.component';
import {
  FiveASidePreLeaderBoardComponent
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveASidePreLeaderBoard/fiveaside-pre-leader-board.component';
import {
  FiveASideShowDownLobbyComponent
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveASideShowDownLobby/fiveaside-show-down-lobby.component';
import {
  FiveASideOddsViewComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideEntry/fiveASideOddsView/fiveaside-oddsview.component';
import {
  FiveASideEntrySummaryComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideEntry/fiveASideEntrySummary/fiveaside-entry-summary.component';
import {
  FiveASideEntryDetailsComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryDetails/fiveaside-entry-details.component';
import {
  FiveASideEntryListOverlayComponent
  // eslint-disable-next-line max-len
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryListOverlay/fiveaside-entrylist-overlay.component';
import {
  FiveASideEntryListComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryList/fiveaside-entry-list.component';
import {
  FiveASideProgressBarComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideEntry/fiveASideProgressBar/fiveaside-progressbar.component';
import { FiveASideShowDownPipesModule } from '@fiveASideShowDownModule/pipes/fiveASideShowDown-pipes.module';
import { SharedModule } from '@sharedModule/shared.module';
import {
  FiveASidePrizePoolComponent
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveASidePrizePool/fiveaside-prize-pool.component';
import { FracToDecService } from '@app/core/services/fracToDec/frac-to-dec.service';

import {
  FiveASideRulesEntryAreaComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideRulesEntryArea/fiveaside-rules-entry-area.component';
import {
  FiveasideTermsRulesComponent
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveASideTermsRules/fiveaside-terms-rules.component';
import {
  FiveASideShowdownCardComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideshowdownCard/fiveaside-showdown-card.component';
import {
  FiveASideSignPostingComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideshowdownCard/fiveAsideSignPosting/fiveaside-sign-posting.component';
import {
  FiveASideShowdownLiveScoresComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideShowDownLiveScores/fiveaside-showdown-live-scores.component';

import {
  FiveASideEntryWidgetComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideEntry/fiveASideMyEntryWidget/fiveaside-myentry-widget.component';
import {
  FiveasideCrestImageComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideCrestImage/fiveaside-crest-image.component';
import {
  TransitionGroupItemDirective
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideLiveLeaderBoard/directives/transition-group-item.directive';
import {
  TransitionGroupDirective
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideLiveLeaderBoard/directives/transition-group.directive';
import {
  FiveASideEntrySummaryPrizePoolComponent
  // eslint-disable-next-line max-len
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideEntry/fiveASideEntrySummaryPrizePool/fiveaside-entry-summary-prize-pool.component';
import {
  FiveASideMultiEntryProgressComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideEntry/fiveASideMultiEntryProgress/fiveaside-multientry-progress.component';
import { FiveASideEntryConfirmationComponent
} from '@app/lazy-modules/fiveASideShowDown/components/fiveASideEntryConfirmation/fiveaside-entry-confirmation.component';
import {
  FiveASideAnimatedScoreComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideEntry/fiveASideAnimatedScore/fiveaside-animated-score.component';
import {
  FiveasidePostMutiEntryProgressComponent
  // eslint-disable-next-line max-len
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideEntry/fiveaside-post-muti-entry-progress/fiveaside-post-muti-entry-progress.component';
import {
  FiveasideWelcomeOverlayComponent
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveASideWelcomeOverlay/fiveaside-welcome-overlay.component';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
import { FiveasidePreEventTutorialComponent
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveasidePreEventTutorial/fiveaside-pre-event-tutorial.component';
import {
  FiveASideLeaderBoardComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideLeaderBoard/fiveaside-leader-board.component';
import { FiveASideLobbyOverlayComponent
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveAsideLobbyOverlay/fiveaside-lobby-overlay.component';
import {
  FiveASideLiveEventOverlayComponent
} from '@ladbrokesDesktop/fiveASideShowDown/components/fiveASideLiveEventOverlay/five-a-side-live-event-overlay.component';
import { FiveASideSpinnerComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideSpinner/fiveaside-spinner.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  declarations: [
    FiveASideShowDownLobbyComponent,
    FiveASidePreLeaderBoardComponent,
    FiveASidePostLeaderBoardComponent,
    FiveASideLiveLeaderBoardComponent,
    FiveASideEntryListComponent,
    FiveASideEntryListOverlayComponent,
    FiveASideEntryDetailsComponent,
    FiveASideEntrySummaryComponent,
    FiveASideProgressBarComponent,
    FiveASideOddsViewComponent,
    FiveASidePrizePoolComponent,
    FiveASideShowdownCardComponent,
    FiveASideShowdownLiveScoresComponent,
    FiveASideSignPostingComponent,
    FiveASideRulesEntryAreaComponent,
    FiveasideTermsRulesComponent,
    FiveasideCrestImageComponent,
    TransitionGroupDirective,
    TransitionGroupItemDirective,
    FiveASideEntrySummaryPrizePoolComponent,
    FiveASideEntryWidgetComponent,
    FiveASideMultiEntryProgressComponent,
    FiveASideAnimatedScoreComponent,
    FiveasidePostMutiEntryProgressComponent,
    FiveasideWelcomeOverlayComponent,
    FiveasidePreEventTutorialComponent,
    FiveASideLeaderBoardComponent,
    FiveASideLobbyOverlayComponent,
    FiveASideLiveEventOverlayComponent,
    FiveASideSpinnerComponent
  ],
  exports: [FiveASideShowDownPipesModule,
    ],
  imports: [
    FiveASideShowDownPipesModule,
    CommonModule,
    SharedModule,
    FiveASideShowDownRoutingModule,
    FiveASideShowDownApiModule
  ],
  providers: [FracToDecService,
    DecimalPipe
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class FiveASideShowDownModule {
  static entry = FiveASideEntryConfirmationComponent;
  constructor(private asls: AsyncScriptLoaderService) {
    this.asls.loadCssFile('assets-fiveASideShowDown.css', true, true).subscribe();
  }
}
