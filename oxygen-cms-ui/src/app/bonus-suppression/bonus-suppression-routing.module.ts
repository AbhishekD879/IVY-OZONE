import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

import { ManageBonusSuppressionModulesComponent } from './manage-bonus-suppression-modules/manage-bonus-suppression-modules.component';
import { ModulesConfigurationComponent } from './modules-configuration/modules-configuration.component';

const routes: Routes = [{
  path: '',
  children: [{
    path: '',
    component: ManageBonusSuppressionModulesComponent
  }, {
    path: 'modules',
    component: ModulesConfigurationComponent
  }]
}];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ]
})
export class BonusSuppressionRoutingModule { }
