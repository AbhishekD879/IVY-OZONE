import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FanzoneClubComponent } from '@ladbrokesMobile/fanzone/components/fanzoneClub/fanzone-club.component';
import { FanzoneHomeComponent } from '@ladbrokesMobile/fanzone/components/fanzoneHome/fanzone-home.component';
import { FanzoneNowNextComponent } from '@ladbrokesMobile/fanzone/components/fanzoneNowNext/fanzone-now-next.component';
import { FanzoneStatsComponent } from '@ladbrokesMobile/fanzone/components/fanzoneStats/fanzone-stats.component';
import { FanzoneSelectYourTeamComponent } from '@ladbrokesMobile/fanzone/components/fanzoneSelectYourTeam/fanzone-select-your-team.component';
import { FanzonePreferenceCentreComponent } from '@ladbrokesMobile/fanzone/components/fanzonePreferenceCentre/fanzone-preference-centre.component';
import { FanzoneVacationComponent } from '@ladbrokesMobile/fanzone/components/fanzoneVacation/fanzone-vacation.component';
import { FanzoneGamesComponent } from '@ladbrokesMobile/fanzone/components/fanzoneGames/fanzone-games.component';

const routes: Routes = [{
  path: ':sport',
  component: FanzoneHomeComponent,
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
  component: FanzoneSelectYourTeamComponent
}, {
  path: ':sport/preference-centre',
  component: FanzonePreferenceCentreComponent
}, {
  path: ':sport/vacation',
  component: FanzoneVacationComponent
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
export class FanzoneRoutingModule { }
