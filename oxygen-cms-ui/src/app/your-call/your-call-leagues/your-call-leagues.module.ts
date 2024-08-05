import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { YourCallLeaguesRoutingModule } from './your-call-leagues-routing.module';
import { YcLeaguesCreateComponent } from './yc-leagues-create/yc-leagues-create.component';
import { YcLeaguesEditComponent } from './yc-leagues-edit/yc-leagues-edit.component';
import { YcLeaguesListComponent } from './yc-leagues-list/yc-leagues-list.component';
import { YourCallAPIService } from '../service/your-call.api.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    YourCallLeaguesRoutingModule
  ],
  declarations: [
    YcLeaguesCreateComponent,
    YcLeaguesEditComponent,
    YcLeaguesListComponent
  ],
  providers: [
    YourCallAPIService
  ],
  entryComponents: [
    YcLeaguesCreateComponent
  ]
})
export class YourCallLeaguesModule { }
