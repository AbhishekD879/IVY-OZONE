import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FiveASideShowDownRoutingModule } from './fiveASideShowDown-routing.module';
import {
  FiveASideLiveLeaderBoardComponent
} from '@fiveASideShowDownModule/components/fiveASideLiveLeaderBoard/fiveaside-live-leader-board.component';
import {
  FiveASidePostLeaderBoardComponent
} from '@fiveASideShowDownModule/components/fiveASidePostLeaderBoard/fiveaside-post-leader-board.component';
import {
  FiveASidePreLeaderBoardComponent
} from '@fiveASideShowDownModule/components/fiveASidePreLeaderBoard/fiveaside-pre-leader-board.component';
import {
  FiveASideShowDownLobbyComponent
} from '@fiveASideShowDownModule/components/fiveASideShowDownLobby/fiveaside-show-down-lobby.component';

import { FiveASideShowDownPipesModule } from '@fiveASideShowDownModule/pipes/fiveASideShowDown-pipes.module';
import { SharedModule } from '@sharedModule/shared.module';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  declarations: [
    FiveASideShowDownLobbyComponent,
    FiveASidePreLeaderBoardComponent,
    FiveASidePostLeaderBoardComponent,
    FiveASideLiveLeaderBoardComponent
  ],
  exports: [FiveASideShowDownPipesModule],
  imports: [
    FiveASideShowDownPipesModule,
    CommonModule,
    SharedModule,
    FiveASideShowDownRoutingModule,
    FiveASideShowDownApiModule
  ],
  providers: [
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class FiveASideShowDownModule {
  constructor(private asls: AsyncScriptLoaderService) {
    this.asls.loadCssFile('assets-fiveASideShowDown.css', true, true).subscribe();
  }
}
