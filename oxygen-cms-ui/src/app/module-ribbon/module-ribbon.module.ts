import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { SharedModule } from '../shared/shared.module';

import { ModuleRibbonListComponent } from './module-ribbon-list/module-ribbon-list.component';
import { EditModuleRibbonTabComponent } from './edit-module-ribbon-tab/edit-module-ribbon-tab.component';
import { ModuleRibbonConfigurationRoutingModule } from './module-ribbon-routing.module';
import { CreateModuleRibbonTabComponent } from './create-module-ribbon-tab/create-module-ribbon-tab.component';
import { ModuleRibbonService } from '@app/module-ribbon/module-ribbon.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    ModuleRibbonConfigurationRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    ModuleRibbonListComponent,
    EditModuleRibbonTabComponent,
    CreateModuleRibbonTabComponent
  ],
  entryComponents: [
    CreateModuleRibbonTabComponent
  ],
  providers: [
    ModuleRibbonService
  ]
})
export class ModuleRibbonModule {
}
