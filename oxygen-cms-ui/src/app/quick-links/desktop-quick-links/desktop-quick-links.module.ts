import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {SharedModule} from '../../shared/shared.module';
import {DialogService} from '../../shared/dialog/dialog.service';

import {DesktopQuickLinksRoutingModule} from './desktop-quick-links-routing.module';
import {DesktopQuickLinksListComponent} from './desktop-quick-links-list/desktop-quick-links-list.component';
import {DesktopQuickLinksCreateComponent} from './desktop-quick-links-create/desktop-quick-links-create.component';
import {DesktopQuickLinksEditComponent} from './desktop-quick-links-edit/desktop-quick-links-edit.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    DesktopQuickLinksRoutingModule
  ],
  declarations: [
    DesktopQuickLinksListComponent,
    DesktopQuickLinksCreateComponent,
    DesktopQuickLinksEditComponent
  ],
  providers: [
    DialogService
  ],
})
export class DesktopQuickLinksModule { }
