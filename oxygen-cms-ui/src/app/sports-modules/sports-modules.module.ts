import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SportsModulesRoutingModule } from './sports-modules-routing.module';
import { SportsModulesService } from './sports-modules.service';
import { SharedModule } from '../shared/shared.module';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { SportModulesListComponent } from '@app/sports-modules/sport-modules-list/sport-modules-list.component';
import { CreateSportModuleComponent } from './create-sport-module/create-sport-module.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    SportsModulesRoutingModule
  ],
  declarations: [
    SportModulesListComponent,
    CreateSportModuleComponent
  ],
  exports: [
    SportModulesListComponent
  ],
  providers: [
    SportsModulesService,
    SportsModulesBreadcrumbsService
  ],
  entryComponents: [
    CreateSportModuleComponent
  ]
})
export class SportsModulesModule {
}
