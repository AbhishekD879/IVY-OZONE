import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import {
  FiveASideShowDownLobbyComponent
} from '@app/fiveASideShowDown/components/fiveASideShowDownLobby/fiveaside-show-down-lobby.component';
import {
  FiveASidePreLeaderBoardComponent
} from '@app/fiveASideShowDown/components/fiveASidePreLeaderBoard/fiveaside-pre-leader-board.component';
import {
  FiveASidePostLeaderBoardComponent
} from '@app/fiveASideShowDown/components/fiveASidePostLeaderBoard/fiveaside-post-leader-board.component';
import {
  FiveASideLiveLeaderBoardComponent
} from '@app/fiveASideShowDown/components/fiveASideLiveLeaderBoard/fiveaside-live-leader-board.component';
import { CommonModule, DecimalPipe } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { FiveASideShowDownRoutingModule } from './fiveASideShowDown-routing.module';
import {
  FiveASideEntryListComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryList/fiveaside-entry-list.component';
import {
  FiveASideEntryListOverlayComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryListOverlay/fiveaside-entrylist-overlay.component';
import {
  FiveASideEntryDetailsComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryDetails/fiveaside-entry-details.component';
import {
  FiveASideEntrySummaryComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideEntrySummary/fiveaside-entry-summary.component';
import {
  FiveASideProgressBarComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideProgressBar/fiveaside-progressbar.component';
import { FracToDecService } from '@app/core/services/fracToDec/frac-to-dec.service';
import { FiveASideShowdownCardComponent } from '@app/fiveASideShowDown/components/fiveASideshowdownCard/fiveaside-showdown-card.component';
import {
  FiveASideRulesEntryAreaComponent
} from '@app/fiveASideShowDown/components/fiveASideRulesEntryArea/fiveaside-rules-entry-area.component';
import { FiveasideTermsRulesComponent } from '@app/fiveASideShowDown/components/fiveASideTermsRules/fiveaside-terms-rules.component';
import { FiveASidePrizePoolComponent } from '@app/fiveASideShowDown/components/fiveASidePrizePool/fiveaside-prize-pool.component';
import { FiveASideShowDownPipesModule } from '@app/fiveASideShowDown/pipes/fiveASideShowDown-pipes.module';
import {
  FiveASideMultiEntryProgressComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideMultiEntryProgress/fiveaside-multientry-progress.component';
import { FiveASideEntryWidgetComponent
 } from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideMyEntryWidget/fiveaside-myentry-widget.component';
import { ScrollToDirective } from '@app/fiveASideShowDown/directives/scroll.position.directive';
import { FiveasideCrestImageComponent
} from '@app/fiveASideShowDown/components/fiveASideCrestImage/fiveaside-crest-image.component';
import { FiveasidePostMutiEntryProgressComponent
} from './components/fiveASideEntry/fiveaside-post-muti-entry-progress/fiveaside-post-muti-entry-progress.component';
import {
  FiveasideWelcomeOverlayComponent
} from '@app/fiveASideShowDown/components/fiveASideWelcomeOverlay/fiveaside-welcome-overlay.component';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
import { FiveasidePreEventTutorialComponent
} from '@app/fiveASideShowDown/components/fiveasidePreEventTutorial/fiveaside-pre-event-tutorial.component';
import { FiveASideLeaderBoardComponent
} from '@app/fiveASideShowDown/components/fiveASideLeaderBoard/fiveaside-leader-board.component';
import {
  FiveASideLiveEventOverlayComponent
} from '@app/fiveASideShowDown/components/fiveASideLiveEventOverlay/five-a-side-live-event-overlay.component';
import { FiveASideSpinnerComponent
} from '@app/fiveASideShowDown//components/fiveASideSpinner/fiveaside-spinner.component';
import { AsyncScriptLoaderService } from '../core/services/asyncScriptLoader/async-script-loader.service';
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
    FiveASideShowdownCardComponent,
    FiveASideRulesEntryAreaComponent,
    FiveasideTermsRulesComponent,
    FiveASidePrizePoolComponent,
    FiveASideLiveLeaderBoardComponent,
    FiveASideMultiEntryProgressComponent,
    FiveASideEntryWidgetComponent,
    ScrollToDirective,
    FiveasideCrestImageComponent,
    FiveasidePostMutiEntryProgressComponent,
    FiveasideWelcomeOverlayComponent,
    FiveasidePreEventTutorialComponent,
    FiveASideLeaderBoardComponent,
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
  constructor(private asls: AsyncScriptLoaderService) {
    this.asls.loadCssFile('assets-fiveASideShowDown.css', true, true).subscribe();
  }
 }
