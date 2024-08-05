import { NgModule } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { FiveASideEntryConfirmationComponent
} from '@ladbrokesMobile/lazy-modules/fiveASideShowDown/components/fiveASideEntryConfirmation/fiveaside-entry-confirmation.component';
import { FiveASideContestSelectionComponent
} from '@lazy-modules-module/fiveASideShowDown/components/fiveASideContestSelection/fiveaside-contest-selection.component';
import { FiveasideBetHeaderComponent
} from '@app/lazy-modules/fiveASideShowDown/components/fiveASideBetHeader/fiveaside-bet-header.component';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
import { FiveASideEntryInfoService } from '@app/fiveASideShowDown/services/fiveaside-entryInfo-handler.service';
import { FiveAsideLiveServeUpdatesSubscribeService } from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates-subscribe.service';
import { FiveAsideLiveServeUpdatesService } from '@app/fiveASideShowDown/services/fiveaside-live-serve-updates.service';
import { FiveasideRulesEntryAreaService } from '@app/fiveASideShowDown/services/fiveaside-rules-entry-area.service';
import { FiveASideShowDownLobbyService } from '@app/fiveASideShowDown/services/fiveaside-show-down-lobby.service';
import { FiveasideWidgetService } from '@app/lazy-modules/fiveASideShowDown/services/fiveaside-widget.service';
import { FiveasideLeaderBoardService } from '@app/fiveASideShowDown/services/fiveaside-leader-board.service';

@NgModule({
  declarations: [FiveASideEntryConfirmationComponent, FiveasideBetHeaderComponent, FiveASideContestSelectionComponent],
  imports: [
    SharedModule,
    FiveASideShowDownApiModule
  ],
  providers:[FiveAsideLiveServeUpdatesSubscribeService,
    FiveasideWidgetService,
    FiveASideShowDownLobbyService,
    FiveASideEntryInfoService,
    FiveAsideLiveServeUpdatesService,
    FiveasideLeaderBoardService,
    FiveasideRulesEntryAreaService],
  exports: [
    FiveASideEntryConfirmationComponent,
    FiveasideBetHeaderComponent,
    FiveASideContestSelectionComponent
  ]
})
export class FiveASideEntryConfirmationModule {
  static entry = {FiveASideEntryConfirmationComponent, FiveasideBetHeaderComponent,FiveASideContestSelectionComponent};
}
