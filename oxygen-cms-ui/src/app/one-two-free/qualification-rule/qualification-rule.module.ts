import {NgModule} from '@angular/core';
import {SharedModule} from '../../shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {QualificationRuleRoutingModule} from '@app/one-two-free/qualification-rule/qualification-rule-routing.module';
import {QualificationRulePageComponent} from '@app/one-two-free/qualification-rule/page/qualification-rule.page.component';
import {QualificationRuleAPIService} from '@app/one-two-free/service/qualificationRule.api.service';

@NgModule({
  imports: [
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    QualificationRuleRoutingModule
  ],
  declarations: [
    QualificationRulePageComponent
  ],
  providers: [
    QualificationRuleAPIService
  ],
  entryComponents: [
    QualificationRulePageComponent
  ]
})
export class QualificationRuleModule {

}
