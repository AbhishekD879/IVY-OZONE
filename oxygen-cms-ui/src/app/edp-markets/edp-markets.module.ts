import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../shared/shared.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { EdpListComponent } from './edp-list/edp-list.component';
import { CreateEdpMarketComponent } from './create-edp-market/create-edp-market.component';
import { EditEdpMarketComponent } from './edit-edp-market/edit-edp-market.component';

import { EdpMarketsRoutingModuleModule } from './edp-markets-routing.module';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    EdpMarketsRoutingModuleModule,
    FormsModule,
    ReactiveFormsModule
  ],
  declarations: [
    EdpListComponent,
    EditEdpMarketComponent,
    CreateEdpMarketComponent
  ],
  entryComponents: [
    CreateEdpMarketComponent
  ]
})
export class EdpMarketsModule { }
