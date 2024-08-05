import {NgModule} from '@angular/core';
import {SharedModule} from '../shared/shared.module';

import {SystemConfigComponent} from './system-config/system-config.component';
import {ConfigPageComponent} from './config-page/configuration-page/config.page.component';
import {StructureComponent} from './structure-page/structure/structure.component';

import {SystemConfigurationRoutingModule} from './system-configuration-routing.module';
import {ConfigTableComponent} from './structure-page/configTable/configTable.component';
import {ConfigGroupTableComponent} from './config-page/config-group-table/config-group.table.component';

@NgModule({
  imports: [
    SharedModule,
    SystemConfigurationRoutingModule
  ],
  declarations: [
    ConfigTableComponent,
    SystemConfigComponent,
    ConfigPageComponent,
    StructureComponent,
    ConfigGroupTableComponent
  ]
})
export class SystemConfigurationModule { }
