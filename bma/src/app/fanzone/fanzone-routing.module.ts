import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FanzoneAppClubComponent } from '@app/fanzone/components/fanzoneClub/fanzone-club.component';
import { FanzoneAppHomeComponent } from '@app/fanzone/components/fanzoneHome/fanzone-home.component';
import { FanzoneAppNowNextComponent } from '@app/fanzone/components/fanzoneNowNext/fanzone-now-next.component';
import { FanzoneAppStatsComponent } from '@app/fanzone/components/fanzoneStats/fanzone-stats.component';
import { FANZONE } from '@app/fanzone/constants/fanzoneconstants';
import { FanzoneSelectYourTeamAppComponent } from '@app/fanzone/components/fanzoneSelectYourTeam/fanzone-select-your-team.component';
import { FanzonePreferenceCentreAppComponent } from '@app/fanzone/components/fanzonePreferenceCentre/fanzone-preference-centre.component';
import { FanzoneAppVacationComponent } from '@app/fanzone/components/fanzoneVacation/fanzone-vacation.component';
import { FanzoneAppGamesComponent } from '@app/fanzone/components/fanzoneGames/fanzone-games.component';

const routes: Routes = [
  {
    path: FANZONE.FanzoneRoutes.homepath,
    component: FanzoneAppHomeComponent,
    children: [{
      path: FANZONE.FanzoneRoutes.nowandnextpath,
      component: FanzoneAppNowNextComponent,
    }, {
      path: FANZONE.FanzoneRoutes.clubpath,
      component: FanzoneAppClubComponent,
    }, {
      path: FANZONE.FanzoneRoutes.statspath,
      component: FanzoneAppStatsComponent
    }, {
      path: FANZONE.FanzoneRoutes.gamespath,
      component: FanzoneAppGamesComponent
    }],
  }, {
    path: FANZONE.FanzoneRoutes.showyourcolors,
    component: FanzoneSelectYourTeamAppComponent
  }, {
    path: ':sport/preference-centre',
    component: FanzonePreferenceCentreAppComponent
  }, {
    path: 'vacation',
    component: FanzoneAppVacationComponent
  }
];
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