import { Routes, RouterModule } from '@angular/router';
import { NgModule } from '@angular/core';

import { JackpotReceiptPageComponent } from '@lazy-modules/jackpot/components/jackpotReceiptPage/jackpot-receipt-page.component';

export const routes: Routes = [
  {
    path: '',
    component: JackpotReceiptPageComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class JackpotRoutingModule {}
