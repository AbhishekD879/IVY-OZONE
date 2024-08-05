import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from '../../shared/shared.module';
import { DialogService } from '../../shared/dialog/dialog.service';
import { NavigationPointsApiService } from './navigation-points.api.service';

import { NavigationPointsRoutingModule } from './navigation-points-routing.module';
import { NavigationPointsListComponent } from './navigation-points-list/navigation-points-list.component';
import { NavigationPointsCreateComponent } from './navigation-points-create/navigation-points-create.component';
import { NavigationPointsEditComponent } from './navigation-points-edit/navigation-points-edit.component';
import { ThemePreviewComponent } from './theme-preview/theme-preview.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    NavigationPointsRoutingModule
  ],
  declarations: [
    NavigationPointsListComponent,
    NavigationPointsCreateComponent,
    NavigationPointsEditComponent,
    ThemePreviewComponent
  ],
  providers: [
    DialogService,
    NavigationPointsApiService
  ]
})
export class NavigationPointsModule { }
