import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import {SystemConfigComponent} from './system-config/system-config.component';
import {ConfigPageComponent} from './config-page/configuration-page/config.page.component';
import {StructureComponent} from './structure-page/structure/structure.component';

const systemConfigurationRoutes: Routes = [
  {
    path: '',
    component: SystemConfigComponent,
    children: [
      {
        path: '',
        children: [
          { path: 'config',  component: ConfigPageComponent },
          { path: 'structure',  component: StructureComponent },
        ]
      }
    ]
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(systemConfigurationRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class SystemConfigurationRoutingModule { }
