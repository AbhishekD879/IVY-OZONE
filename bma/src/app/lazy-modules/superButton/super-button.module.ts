import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SuperButtonComponent } from '@app/lazy-modules/superButton/components/super-button.component';
import { CommonModule } from '@angular/common';

@NgModule({
  imports: [CommonModule],
  declarations: [SuperButtonComponent],
  exports: [SuperButtonComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class SuperButtonModule {
  static entry = SuperButtonComponent;
}
