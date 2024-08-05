import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { YourCallMarketsRoutingModule } from './your-call-markets-routing.module';
import { YcMarketsListComponent } from './yc-markets-list/yc-markets-list.component';
import { YcMarketsCreateComponent } from './yc-markets-create/yc-markets-create.component';
import { YcMarketsEditComponent } from './yc-markets-edit/yc-markets-edit.component';
import { YourCallAPIService } from '../service/your-call.api.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    YourCallMarketsRoutingModule
  ],
  declarations: [
    YcMarketsListComponent,
    YcMarketsCreateComponent,
    YcMarketsEditComponent
   ],
   providers: [
    YourCallAPIService
  ],
  entryComponents: [
    YcMarketsCreateComponent
  ]
})
export class YourCallMarketsModule { }
