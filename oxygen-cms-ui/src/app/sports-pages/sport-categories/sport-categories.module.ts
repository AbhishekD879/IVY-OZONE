import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {SharedModule} from '../../shared/shared.module';
import {DialogService} from '../../shared/dialog/dialog.service';

import {SportCategoriesRoutingModule} from './sport-categories-routing.module';
import {SportCategoriesListComponent} from './sport-categories-list/sport-categories-list.component';
import {SportCategoriesCreateComponent} from './sport-categories-create/sport-categories-create.component';
import {SportCategoriesEditComponent} from './sport-categories-edit/sport-categories-edit.component';
import { MatCheckboxModule } from '@angular/material/checkbox';
import {SportsModulesService} from '../../sports-modules/sports-modules.service';
import {SportTabEditComponent} from './sport-tab-edit/sport-tab-edit.component';
import {SportCategoryService} from '@app/client/private/services/http/menu/sportCategory.service';
import {SportTabFiltersComponent} from '@app/sports-pages/sport-categories/sport-tab-filters/sport-tab-filters.component';
import {LeagueFilterCreateComponent} from "@app/sports-pages/sport-categories/league-filter-create/league-filter-create.component";
import {LeagueFilterEditComponent} from "@app/sports-pages/sport-categories/league-filter-edit/league-filter-edit.component";
import { InsightsModule } from './insights/insights.module';
  
@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    SportCategoriesRoutingModule,
    MatCheckboxModule,
    InsightsModule,
  ],
  declarations: [
    SportCategoriesListComponent,
    SportCategoriesCreateComponent,
    SportCategoriesEditComponent,
    SportTabEditComponent,
    SportTabFiltersComponent,
    LeagueFilterCreateComponent,
    LeagueFilterEditComponent,
  ],
  providers: [
    DialogService,
    SportsModulesService,
    SportCategoryService
  ],
  entryComponents: [
    SportCategoriesCreateComponent
  ]
})
export class SportCategoriesModule { }
