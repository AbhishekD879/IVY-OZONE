import { NgModule } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { StatisticalContentInformationComponent } from './components/statisticalContent/statistical-content-information.component';
@NgModule({
  declarations: [StatisticalContentInformationComponent],
  imports: [
    SharedModule
  ],
  providers:[],
  exports: [
    StatisticalContentInformationComponent
  ]
})
export class StatisticalContentInformationModule {
  static entry = {StatisticalContentInformationComponent};
}
