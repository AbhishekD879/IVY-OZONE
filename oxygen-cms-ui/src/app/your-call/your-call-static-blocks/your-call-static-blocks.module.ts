import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { YourCallStaticBlocksRoutingModule } from './your-call-static-blocks-routing.module';
import { YcStaticBlocksListComponent } from './yc-static-blocks-list/yc-static-blocks-list.component';
import { YcStaticBlocksEditComponent } from './yc-static-blocks-edit/yc-static-blocks-edit.component';
import { YcStaticBlocksCreateComponent } from './yc-static-blocks-create/yc-static-blocks-create.component';
import { YourCallAPIService } from '../service/your-call.api.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    YourCallStaticBlocksRoutingModule
  ],
  declarations: [
    YcStaticBlocksListComponent,
    YcStaticBlocksEditComponent,
    YcStaticBlocksCreateComponent
  ],
  providers: [
    YourCallAPIService
  ],
  entryComponents: [
    YcStaticBlocksCreateComponent
  ]
})
export class YourCallStaticBlocksModule { }
