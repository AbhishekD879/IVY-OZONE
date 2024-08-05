import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FanzonesComponent } from './fanzone-list/fanzones.component';
import { FanzoneClubCreateComponent } from './fanzone-club/fanzone-club-create/fanzone-club-create.component';
import { FanzoneClubEditComponent } from './fanzone-club/fanzone-club-edit/fanzone-club-edit.component';
import { FanzoneClubListComponent } from './fanzone-club/fanzone-club-list/fanzone-club-list.component';
import { FanzoneCreateComponent } from './fanzone-create/fanzone-create.component';
import { FanzoneEditComponent } from './fanzone-edit/fanzone-edit.component';
import { FanzonesAPIService } from './services/fanzones.api.service';
import { FanzoneSycComponent } from './fanzone-syc/fanzone-syc.component';
import { FanzonePreferenceCentreComponent } from './fanzone-preference-centre/fanzone-preference-centre.component';
import { FanzoneOptinEmailComponent } from './fanzone-optin-email/fanzone-optin-email.component';
import { FanzoneNewSeasonComponent } from './fanzone-new-season/fanzone-new-season.component';
import { FanzoneComingBackComponent } from './fanzone-coming-back/fanzone-coming-back.component';
import { FanzoneNewSignpostingComponent } from './fanzone-new-signposting/fanzone-new-signposting.component';
import { FanzoneNewGamingPopUpComponent } from './fanzone-new-gaming-pop-up/fanzone-new-gaming-pop-up.component';

const routes: Routes = [
  { path: '', component: FanzonesComponent },
  { path: 'create', component: FanzoneCreateComponent },
  { path: 'fanzone/:id', component: FanzoneEditComponent },
  { path: 'club', component: FanzoneClubListComponent },
  { path: 'club-create', component: FanzoneClubCreateComponent },
  { path: 'club/:id', component: FanzoneClubEditComponent },
  { path: 'show-your-colors', component: FanzoneSycComponent },
  { path: 'preference-centre', component: FanzonePreferenceCentreComponent },
  { path: 'fanzone-on-vacation', component: FanzoneNewSeasonComponent},
  { path: 'fanzone-coming-soon', component: FanzoneComingBackComponent },
  { path: 'new-signposting', component: FanzoneNewSignpostingComponent },
  { path: 'new-gaming-pop-up', component: FanzoneNewGamingPopUpComponent },
  { path: 'fanzone-optin-email', component: FanzoneOptinEmailComponent }
];

@NgModule({
  declarations: [],
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: [
    FanzonesAPIService
  ]
})
export class FanzoneRoutingModule { }
