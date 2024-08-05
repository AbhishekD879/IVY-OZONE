import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FiveASideShowDownLobbyComponent } from './components/fiveASideShowDownLobby/fiveaside-show-down-lobby.component';
import { FiveASidePreLeaderBoardComponent } from './components/fiveASidePreLeaderBoard/fiveaside-pre-leader-board.component';
import { FiveASidePostLeaderBoardComponent } from './components/fiveASidePostLeaderBoard/fiveaside-post-leader-board.component';
import { FiveASideLiveLeaderBoardComponent } from './components/fiveASideLiveLeaderBoard/fiveaside-live-leader-board.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'lobby'
  },
  {
    path: 'lobby',
    component: FiveASideShowDownLobbyComponent
  },
  {
    path: 'pre-leader-board/:id',
    component: FiveASidePreLeaderBoardComponent
  },
  {
    path: 'pre-leader-board/:id',
    component: FiveASidePreLeaderBoardComponent
  },
  {
    path: 'post-leader-board',
    component: FiveASidePostLeaderBoardComponent
  },
  {
    path: 'live-leader-board',
    component: FiveASideLiveLeaderBoardComponent
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
