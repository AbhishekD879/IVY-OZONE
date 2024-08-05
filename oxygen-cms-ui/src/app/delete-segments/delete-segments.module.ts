import {NgModule} from '@angular/core';
import {SharedModule} from '../shared/shared.module';

import {ManagementModule} from '../management/management.module';

import { DeleteSegmentsComponent } from './delete-segments.component';
import { DeleteSegmentsRoutingModule } from './delete-segments-routing.module';

@NgModule({
  imports: [
    SharedModule,
    DeleteSegmentsRoutingModule,
    ManagementModule
  ],
  declarations: [
    DeleteSegmentsComponent
  ],
  providers: [
  ]
})

export class DeleteSegmentsModule { }
