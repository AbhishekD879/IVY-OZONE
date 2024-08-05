import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { LeagueLinksRoutingModule } from './league-links-routing.module';
import { LeagueLinksListComponent } from './league-links-list/league-links-list.component';
import { LeagueLinksEditComponent } from './league-links-edit/league-links-edit.component';
import { LeagueLinksCreateComponent } from './league-links-create/league-links-create.component';
import { StatisticLinksService } from '../service/statistic-links.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    LeagueLinksRoutingModule
  ],
  declarations: [
    LeagueLinksListComponent,
    LeagueLinksEditComponent,
    LeagueLinksCreateComponent
  ],
   providers: [
    StatisticLinksService
  ],
  entryComponents: [
    LeagueLinksCreateComponent
  ]
})
export class LeagueLinksModule { }
