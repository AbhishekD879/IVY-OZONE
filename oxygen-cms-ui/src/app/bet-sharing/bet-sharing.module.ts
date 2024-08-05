import {NgModule} from '@angular/core';
import {SharedModule} from '../shared/shared.module';
import {BetSharingRoutingModule} from './bet-sharing-routing.module';
import { ShareCardComponent } from './share-card/share-card.component';
import { BetSharingAPIService } from './bet-sharing.api.service';
import { CreateFtpTeamsComponent } from './share-card/create-ftp-teams/create-ftp-teams.component';


@NgModule({
  imports: [
    SharedModule,
    BetSharingRoutingModule,
  ],
  declarations: [
     ShareCardComponent,
     CreateFtpTeamsComponent,
  ],
  providers: [
   BetSharingAPIService,
  ]
})
export class BetSharingModule { }
