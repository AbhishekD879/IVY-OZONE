import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LottoRoutingModule } from './lotto-routing.module';
import { SharedModule } from '../shared/shared.module';
import { LottoListComponent } from './lotto-list/lotto-list.component';
import { LottoService } from './lotto.service';
import { LottoDetailsComponent } from './lotto-details/lotto-details.component';
@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    LottoRoutingModule
  ],
  declarations: [
    LottoListComponent,
    LottoDetailsComponent
  ],
  entryComponents: [
    LottoListComponent,
    LottoDetailsComponent
  ],
  providers: [
    LottoService
  ]
})
export class LottoModule { }
