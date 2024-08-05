import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { FanzoneApiModule } from '@app/fanzone/fanzone-api.module';
import { FanzoneRoutingModule } from '@app/fanzone/fanzone-routing.module';
import { FanzoneAppHomeComponent } from '@app/fanzone/components/fanzoneHome/fanzone-home.component';
import { FanzoneAppClubComponent } from '@app/fanzone/components/fanzoneClub/fanzone-club.component';
import { FanzoneAppStatsComponent } from '@app/fanzone/components/fanzoneStats/fanzone-stats.component';
import { FanzoneAppNowNextComponent } from '@app/fanzone/components/fanzoneNowNext/fanzone-now-next.component';
import { FanzoneAppOutrightsComponent } from '@app/fanzone/components/fanzoneOutrights/fanzone-outrights.component';
import { FanzoneSelectYourTeamAppComponent } from '@app/fanzone/components/fanzoneSelectYourTeam/fanzone-select-your-team.component';
import { FanzoneSharedModule } from '@app/lazy-modules/fanzone/fanzone-shared.module';
import { FanzonePreferenceCentreAppComponent } from '@app/fanzone/components/fanzonePreferenceCentre/fanzone-preference-centre.component';
import { FanzoneSharedService } from '@app/lazy-modules/fanzone/services/fanzone-shared.service';
import { FanzoneLeagueTableModalComponent } from '@app/fanzone/components/fanzoneLeagueTableModal/fanzone-league-table-modal.component';
import { FanzoneAppVacationComponent } from '@app/fanzone/components/fanzoneVacation/fanzone-vacation.component';
import { FanzoneAppGamesComponent } from '@app/fanzone/components/fanzoneGames/fanzone-games.component';

@NgModule({
  declarations: [
    FanzoneAppHomeComponent,
    FanzoneAppClubComponent,
    FanzoneAppStatsComponent,
    FanzoneAppNowNextComponent,
    FanzoneAppOutrightsComponent,
    FanzoneSelectYourTeamAppComponent,
    FanzonePreferenceCentreAppComponent,
    FanzoneLeagueTableModalComponent,
    FanzoneAppVacationComponent,
    FanzoneAppGamesComponent
  ],
  exports: [FanzoneSelectYourTeamAppComponent],
  imports: [
    CommonModule,
    SharedModule,
    FanzoneRoutingModule,
    FanzoneApiModule,
    FanzoneSharedModule
  ],
  providers: [FanzoneSharedService],
  schemas: [NO_ERRORS_SCHEMA]
})
export class FanzoneModule { }
