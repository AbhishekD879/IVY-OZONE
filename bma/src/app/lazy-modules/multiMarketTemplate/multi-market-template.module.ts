import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MultiMarketTemplateComponent } from '@app/lazy-modules/multiMarketTemplate/components/multi-market-template.component';
import { SharedModule } from '@sharedModule/shared.module';
@NgModule({
  imports: [CommonModule, SharedModule],
  declarations: [MultiMarketTemplateComponent],
  exports: [MultiMarketTemplateComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class MultiMarketTemplateModule {
  static entry = MultiMarketTemplateComponent;
}