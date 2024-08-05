import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FiveASideShowDownLobbyComponent } from './components/fiveASideShowDownLobby/fiveaside-show-down-lobby.component';
import { FiveASideLeaderBoardComponent
} from '@ladbrokesMobile/fiveASideShowDown/components/fiveASideLeaderBoard/fiveaside-leader-board.component';
import { RgyCheckGuard } from '@core/guards/rgy-check.guard';
import { rgyellow } from '@app/bma/constants/rg-yellow.constant';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'lobby'
  },
  {
    path: 'lobby',
    component: FiveASideShowDownLobbyComponent,
    canActivate: [ RgyCheckGuard ],
    data: {moduleName: rgyellow.FIVE_A_SIDE}
  },
  {
    path: 'leaderboard/:id',
    component: FiveASideLeaderBoardComponent,
    canActivate: [ RgyCheckGuard ],
    data: {moduleName: rgyellow.FIVE_A_SIDE}
  }];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class FiveASideShowDownRoutingModule { }
