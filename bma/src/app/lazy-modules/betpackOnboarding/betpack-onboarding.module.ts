import { CommonModule } from '@angular/common';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { BetpackOnboardingComponent } from '@lazy-modules/betpackOnboarding/components/betpackOnboarding/betpack-onboarding.component';
import { SharedModule } from '@sharedModule/shared.module';
@NgModule({
  imports: [CommonModule, SharedModule],
  providers: [],
  exports: [BetpackOnboardingComponent],
  declarations: [
    BetpackOnboardingComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class BetpackOnBoardingModule {
  static entry = BetpackOnboardingComponent;
}