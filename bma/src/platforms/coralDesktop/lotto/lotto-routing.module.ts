import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LottoSegmentPageComponent } from '@lottoModule/components/lottoSegmentPage/lotto-segment-page.component';
import { LinesummaryComponent } from '@lottoModule/components/linesummary/linesummary.component';

// Overridden
import { DesktopLottoMainComponent } from '@coralDesktop/lotto/components/lottoMain/lotto-main.component';

const routes: Routes = [{
  path: '',
  children: [
  {
    path: '',
    component: DesktopLottoMainComponent,
    data: { segment: 'lotto' },
    children: [
    {
      path: 'linesummary/:lottery',
      component: LinesummaryComponent,
      data: { segment: 'lotto.linesummary' },
    },
    {
      path: 'linesummary',
      component: LinesummaryComponent,
      data: { segment: 'lotto.linesummary' },
    },
     {
      path: '',
      component: LottoSegmentPageComponent,
      data: { segment: 'lotto'},
    }, {
      path: ':lottery',
      component: LottoSegmentPageComponent,
      data: { segment: 'lotto.lottery'},
    }]
  }]
}];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [
    RouterModule
  ],
  providers: []
})
export class LottoRoutingModule { }
