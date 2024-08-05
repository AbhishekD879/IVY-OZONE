import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {SportsQuickLinksRoutingModule} from './sports-quick-links-routing.module';
import {SharedModule} from '@app/shared/shared.module';
import {SportsQuickLinksListComponent} from './sports-quick-links/sports-quick-links-list/sports-quick-links-list.component';
import {SportsQuickLinksCreateComponent} from './sports-quick-links/sports-quick-links-create/sports-quick-links-create.component';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {SportsQuickLinksEditComponent} from './sports-quick-links/sports-quick-links-edit/sports-quick-links-edit.component';
import {ConfigStructureAPIService} from '@app/system-configuration/structure-page/service/structure.api.service';
import {SportQuickLinksService} from './sports-quick-links/sport-quick-links.service';
import {QuickLinksModuleComponent} from './quick-links-module/quick-links-module.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    SportsQuickLinksRoutingModule
  ],
  declarations: [
    QuickLinksModuleComponent,
    SportsQuickLinksListComponent,
    SportsQuickLinksCreateComponent,
    SportsQuickLinksEditComponent
  ],

  entryComponents: [
    QuickLinksModuleComponent,
    SportsQuickLinksListComponent,
    SportsQuickLinksCreateComponent
  ],
  providers: [
    DialogService,
    SportQuickLinksService,
    ConfigStructureAPIService
  ],
  exports: []
})
export class SportsQuickLinksModule { }
