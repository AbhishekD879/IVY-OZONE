import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FiveASideShowDownLobbyComponent } from './components/fiveASideShowDownLobby/fiveaside-show-down-lobby.component';
import { FiveASidePreLeaderBoardComponent } from './components/fiveASidePreLeaderBoard/fiveaside-pre-leader-board.component';
import { FiveASidePostLeaderBoardComponent } from './components/fiveASidePostLeaderBoard/fiveaside-post-leader-board.component';
import { FiveASideLiveLeaderBoardComponent } from './components/fiveASideLiveLeaderBoard/fiveaside-live-leader-board.component';
import { FiveASideLeaderBoardComponent
} from '@app/fiveASideShowDown/components/fiveASideLeaderBoard/fiveaside-leader-board.component';
import { RgyCheckGuard } from '@core/guards/rgy-check.guard';
import { rgyellow } from '../bma/constants/rg-yellow.constant';

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
  },
  {
    path: 'pre-leader-board/:id',
    component: FiveASidePreLeaderBoardComponent,
    canActivate: [ RgyCheckGuard ],
    data: {moduleName: rgyellow.FIVE_A_SIDE}
  },
  {
    path: 'pre-leader-board/:id',
    component: FiveASidePreLeaderBoardComponent,
    canActivate: [ RgyCheckGuard ],
    data: {moduleName: rgyellow.FIVE_A_SIDE}
  },
  {
    path: 'post-leader-board/:id',
    component: FiveASidePostLeaderBoardComponent,
    canActivate: [ RgyCheckGuard ],
    data: {moduleName: rgyellow.FIVE_A_SIDE}
  },
  {
    path: 'live-leader-board',
    component: FiveASideLiveLeaderBoardComponent,
    canActivate: [ RgyCheckGuard ],
    data: {name: rgyellow.FIVE_A_SIDE}
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
