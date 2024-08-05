import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ModuleRibbonListComponent } from './module-ribbon-list/module-ribbon-list.component';
import { EditModuleRibbonTabComponent } from './edit-module-ribbon-tab/edit-module-ribbon-tab.component';

const moduleRibbonConfigurationRoutes: Routes = [
  { path: '',  component: ModuleRibbonListComponent },
  { path: ':id',  component: EditModuleRibbonTabComponent }
];

@NgModule({
  imports: [
    RouterModule.forChild(moduleRibbonConfigurationRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class ModuleRibbonConfigurationRoutingModule { }
