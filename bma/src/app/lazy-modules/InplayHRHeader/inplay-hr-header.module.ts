import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { InplayHRHeaderComponent } from './inplay-hr-header.component';

@NgModule({
  imports: [SharedModule],
  declarations: [InplayHRHeaderComponent],
  exports: [InplayHRHeaderComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class InplayHRHeaderModule {
  static entry = InplayHRHeaderComponent;
}
