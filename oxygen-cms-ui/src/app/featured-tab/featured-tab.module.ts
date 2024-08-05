import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../shared/shared.module';

import { FeaturedTabRoutingModule } from './featured-tab-routing.module';
import { FeaturedModulesListComponent } from './featured-modules-list/featured-modules-list.component';
import { FeaturedModuleComponent } from './featured-module/featured-module.component';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    FeaturedTabRoutingModule
  ],
  declarations: [
    FeaturedModulesListComponent,
    FeaturedModuleComponent
  ],
  providers: [
    SportsModulesService,
    SportsModulesBreadcrumbsService
  ],
  exports: [FeaturedModulesListComponent]
})
export class FeaturedTabModule { }
