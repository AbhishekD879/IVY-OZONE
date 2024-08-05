import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ExtraNavigationPointsCreateComponent } from './extra-navigation-points-create/extra-navigation-points-create.component';
import { ExtraNavigationPointsEditComponent } from './extra-navigation-points-edit/extra-navigation-points-edit.component';
import { ExtraNavigationPointsListComponent } from './extra-navigation-points-list/extra-navigation-points-list.component';



import { SharedModule } from '../../shared/shared.module';
import { DialogService } from '../../shared/dialog/dialog.service';
import { ExtraNavigationPointsRoutingModule } from './extra-navigation-points-routing.module';
import { ExtraNavigationPointsApiService } from '@app/quick-links/extra-navigation-points/extra-navigation-points-api.service';
import { SpecialSuperBtnPreviewComponent } from './special-super-btn-preview/special-super-btn-preview.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    ExtraNavigationPointsRoutingModule
  ],
  declarations: [
    ExtraNavigationPointsListComponent,
    ExtraNavigationPointsCreateComponent,
    ExtraNavigationPointsEditComponent,
    SpecialSuperBtnPreviewComponent
  ],
  providers: [
    DialogService,
    ExtraNavigationPointsApiService
  ]
})

export class ExtraNavigationPointsModule { }
