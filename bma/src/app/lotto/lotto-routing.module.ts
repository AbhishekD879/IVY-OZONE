import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LottoMainComponent } from './components/lottoMain/lotto-main.component';
import { LottoSegmentPageComponent } from '@lottoModule/components/lottoSegmentPage/lotto-segment-page.component';
import { LinesummaryComponent } from './components/linesummary/linesummary.component';
import { LottoNumberSelectorComponent } from './components/lottoNumberSelectorDialog/lotto-number-selector-dialog.component';

const routes: Routes = [{
  path: '',
  children: [
  {
    path: 'lottonumberselectordialog',
    component: LottoNumberSelectorComponent,
    data: { segment: 'lotto.lotto-number-selector-dialog' },
  }, {
    path: '',
    component: LottoMainComponent,
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
      data: { segment: 'lotto' },
    }, {
      path: ':lottery',
      component: LottoSegmentPageComponent,
      data: { segment: 'lotto.lottery' },
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
