import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../shared/shared.module';

import { StatContentInfoRoutingModule } from './stat-content-info-routing.module';
import { StatContentListComponent } from './stat-content-list/stat-content-list.component';
import { StatContentComponent } from './stat-content/stat-content.component';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { SportsModulesService } from '@app/sports-modules/sports-modules.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    StatContentInfoRoutingModule
  ],
  declarations: [
    StatContentListComponent,
    StatContentComponent
  ],
  providers: [
    SportsModulesService,
    SportsModulesBreadcrumbsService
  ],
  exports: [StatContentListComponent]
})
export class StatContentInfoModule { }
