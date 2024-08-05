import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FanzonesComponent } from './fanzone-list/fanzones.component';
import { FanzoneRoutingModule } from './fanzone-routing.module';
import { SharedModule } from '../shared/shared.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FanzoneCreateComponent } from './fanzone-create/fanzone-create.component';
import { FanzoneEditComponent } from './fanzone-edit/fanzone-edit.component';
import { FanzoneCommonComponent } from './fanzone-common/fanzone-common.component';
import { FanzoneClubListComponent } from './fanzone-club/fanzone-club-list/fanzone-club-list.component';
import { FanzoneClubCreateComponent } from './fanzone-club/fanzone-club-create/fanzone-club-create.component';
import { FanzoneClubEditComponent } from './fanzone-club/fanzone-club-edit/fanzone-club-edit.component';
import { FanzoneSycComponent } from './fanzone-syc/fanzone-syc.component';
import { FanzoneOptinEmailComponent } from './fanzone-optin-email/fanzone-optin-email.component';
import { FanzonePreferenceCentreComponent } from './fanzone-preference-centre/fanzone-preference-centre.component';
import { FanzoneComingBackComponent } from './fanzone-coming-back/fanzone-coming-back.component';
import { FanzoneNewSeasonComponent } from './fanzone-new-season/fanzone-new-season.component';
import { FanzoneNewSignpostingComponent } from './fanzone-new-signposting/fanzone-new-signposting.component';
import { FanzoneNewGamingPopUpComponent } from './fanzone-new-gaming-pop-up/fanzone-new-gaming-pop-up.component';


@NgModule({
  declarations: [
    FanzonesComponent,
    FanzoneCreateComponent,
    FanzoneEditComponent,
    FanzoneCommonComponent,
    FanzoneClubListComponent,
    FanzoneClubCreateComponent,
    FanzoneClubEditComponent,
    FanzoneSycComponent,
    FanzonePreferenceCentreComponent,
    FanzoneComingBackComponent,
    FanzoneNewSeasonComponent,
    FanzoneNewSignpostingComponent,
    FanzoneNewGamingPopUpComponent,
    FanzoneOptinEmailComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    FanzoneRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  entryComponents: [
    FanzonesComponent
  ]
})
export class FanzoneModule { }
