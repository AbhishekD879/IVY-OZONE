import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CustomFlagFilterToggleComponent } from '@lazy-modules-module/customFlagFiltertoggle/custom-flag-filter-toggle/custom-flag-filter-toggle.component';
import { SharedModule } from '@sharedModule/shared.module';

@NgModule({
  imports: [CommonModule, SharedModule],
  declarations: [CustomFlagFilterToggleComponent],
  exports: [CustomFlagFilterToggleComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class CustomFlagFilterToggleModule {
  static entry = CustomFlagFilterToggleComponent;
}