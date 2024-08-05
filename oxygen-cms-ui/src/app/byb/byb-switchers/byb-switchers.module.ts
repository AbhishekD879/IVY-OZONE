import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { BYBSwitchersRoutingModule } from './byb-switchers-routing.module';
import { BYBSwitchersCreateComponent } from './byb-switchers-create/byb-switchers-create.component';
import { BYBSwitchersEditComponent } from './byb-switchers-edit/byb-switchers-edit.component';
import { BYBSwitchersListComponent } from './byb-switchers-list/byb-switchers-list.component';
import { BybAPIService } from '../service/byb.api.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    BYBSwitchersRoutingModule
  ],
  declarations: [
    BYBSwitchersCreateComponent,
    BYBSwitchersEditComponent,
    BYBSwitchersListComponent
  ],
  providers: [
    BybAPIService
  ],
  entryComponents: [
    BYBSwitchersCreateComponent
  ]
})
export class BYBSwitchersModule { }
