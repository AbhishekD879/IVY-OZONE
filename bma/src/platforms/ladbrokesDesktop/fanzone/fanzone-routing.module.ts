import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FanzoneClubComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneClub/fanzone-club.component';
import { FanzoneHomeDesktopComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneHome/fanzone-home.component';
import { FanzoneNowNextComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneNowNext/fanzone-now-next.component';
import { FanzoneStatsComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneStats/fanzone-stats.component';
import { FanzoneSelectYourTeamDesktopComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneSelectYourTeam/fanzone-select-your-team.component';
import { FanzoneVacationDesktopComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneVacation/fanzone-vacation.component';
import { FanzoneGamesComponent } from '@ladbrokesDesktop/fanzone/components/fanzoneGames/fanzone-games.component';

const routes: Routes = [{
  path: ':sport',
  component: FanzoneHomeDesktopComponent,
  children: [{
    path: ':teamName/now-next',
    component: FanzoneNowNextComponent,
  }, {
    path: ':teamName/club',
    component: FanzoneClubComponent,
  }, {
    path: ':teamName/stats',
    component: FanzoneStatsComponent,
  },
  {
    path: ':teamName/games',
    component: FanzoneGamesComponent,
  },
  {
    path: '**',
    redirectTo: 'now-next'
  }
  ]
}, {
  path: ':sport/show-your-colours',
  component: FanzoneSelectYourTeamDesktopComponent
}, {
  path: ':sport/vacation',
  component: FanzoneVacationDesktopComponent
}]

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class FanzoneDesktopRoutingModule { }
