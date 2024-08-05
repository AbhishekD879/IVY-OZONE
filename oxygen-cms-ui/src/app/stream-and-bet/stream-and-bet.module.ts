import {NgModule} from '@angular/core';
import {StreamAndBetComponent} from './stream-and-bet.component';
import {StreamAndBetConfigurationRoutingModule} from './stream-and-bet-routing.module';
import {SharedModule} from '../shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {StreamAndBetCategoryComponent} from './stream-and-bet-category/stream-and-bet-category.component';
import {AddStreamAndBetNodeComponent} from './add-stream-and-bet-node/add-stream-and-bet-node.component';
import {EditStreamAndBetNodeComponent} from './edit-stream-and-bet-node/edit-stream-and-bet-node.component';

import {TreeModule} from 'angular-tree-component';

@NgModule({
  imports: [
    SharedModule,
    StreamAndBetConfigurationRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    TreeModule.forRoot()
  ],
  declarations: [StreamAndBetComponent,
    StreamAndBetCategoryComponent,
    AddStreamAndBetNodeComponent,
    EditStreamAndBetNodeComponent],
  entryComponents: [AddStreamAndBetNodeComponent,
    EditStreamAndBetNodeComponent]
})
export class StreamAndBetModule {
}
