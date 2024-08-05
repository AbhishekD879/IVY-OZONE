import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../shared/shared.module';

import { FeatureListComponent } from './feature-list/feature-list.component';
import { FeatureEditComponent } from './feature-edit/feature-edit.component';
import { FeatureCreateComponent } from './feature-create/feature-create.component';
import { FeaturesRoutingModule } from './features-routing.module';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    FeaturesRoutingModule
  ],
  declarations: [
    FeatureListComponent,
    FeatureEditComponent,
    FeatureCreateComponent
  ],
  entryComponents: [
    FeatureCreateComponent
  ]
})
export class FeaturesModule { }
