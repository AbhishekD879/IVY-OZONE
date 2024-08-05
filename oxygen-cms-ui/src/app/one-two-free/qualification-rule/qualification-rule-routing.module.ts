import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {QualificationRulePageComponent} from '@app/one-two-free/qualification-rule/page/qualification-rule.page.component';

const qualificationRuleRoutes: Routes = [
  {
    path: '',
    component: QualificationRulePageComponent,
    children: []
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(qualificationRuleRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class QualificationRuleRoutingModule {

}
