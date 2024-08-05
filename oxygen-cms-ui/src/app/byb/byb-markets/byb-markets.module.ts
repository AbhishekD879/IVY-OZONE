import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { BybMarketsRoutingModule } from './byb-markets-routing.module';
import { BybMarketsListComponent } from './byb-markets-list/byb-markets-list.component';
import { BybMarketsCreateComponent } from './byb-markets-create/byb-markets-create.component';
import { BybMarketsEditComponent } from './byb-markets-edit/byb-markets-edit.component';
import { BybAPIService } from '../service/byb.api.service';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    BybMarketsRoutingModule
  ],
  declarations: [
    BybMarketsListComponent,
    BybMarketsCreateComponent,
    BybMarketsEditComponent
   ],
   providers: [
    BybAPIService
  ],
  entryComponents: [
    BybMarketsCreateComponent
  ]
})
export class BybMarketsModule { }
