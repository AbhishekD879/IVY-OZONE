import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProfitIndicatorComponent } from '@lazy-modules/profit-indicator/profit-indicator.component';



@NgModule({
  declarations: [
    ProfitIndicatorComponent
  ],
  imports: [
    CommonModule
  ],
  exports: [
    ProfitIndicatorComponent
  ],
})
export class ProfitIndicatorModule {
  static entry = ProfitIndicatorComponent;
}
