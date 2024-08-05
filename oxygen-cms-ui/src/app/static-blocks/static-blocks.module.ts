import { NgModule } from '@angular/core';
import { SharedModule } from '../shared/shared.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { StaticBlocksPageComponent } from './static-blocks-page/static-blocks-page.component';
import { StaticBlocksConfigurationRoutingModule } from './static-blocks-routing.module';
import { AddStaticBlockComponent } from './add-static-block/add-static-block.component';
import { EditStaticBlockComponent } from './edit-static-block/edit-static-block.component';

@NgModule({
  imports: [
    SharedModule,
    StaticBlocksConfigurationRoutingModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    StaticBlocksPageComponent,
    AddStaticBlockComponent,
    EditStaticBlockComponent
  ],
  entryComponents: [
    AddStaticBlockComponent
  ]
})
export class StaticBlocksModule { }
