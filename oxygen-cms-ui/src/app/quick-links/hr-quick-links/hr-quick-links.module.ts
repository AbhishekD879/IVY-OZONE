import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {SharedModule} from '../../shared/shared.module';
import {DialogService} from '../../shared/dialog/dialog.service';

import {HrQuickLinksRoutingModule} from './hr-quick-links-routing.module';
import {HrQuickLinksListComponent} from './hr-quick-links-list/hr-quick-links-list.component';
import {HrQuickLinksCreateComponent} from './hr-quick-links-create/hr-quick-links-create.component';
import {HrQuickLinksEditComponent} from './hr-quick-links-edit/hr-quick-links-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    HrQuickLinksRoutingModule
  ],
  declarations: [
    HrQuickLinksListComponent,
    HrQuickLinksCreateComponent,
    HrQuickLinksEditComponent
  ],
  providers: [
    DialogService
  ],
  exports: [HrQuickLinksListComponent]
})
export class HrQuickLinksModule { }
