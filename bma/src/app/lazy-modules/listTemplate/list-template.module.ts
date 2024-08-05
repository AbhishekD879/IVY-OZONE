import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ListTemplateComponent } from '@lazy-modules-module/listTemplate/components/list-template.component';
import { SharedModule } from '@sharedModule/shared.module';

@NgModule({
  imports: [CommonModule, SharedModule],
  declarations: [ListTemplateComponent],
  exports: [ListTemplateComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class ListTemplateModule {
  static entry = ListTemplateComponent;
}
