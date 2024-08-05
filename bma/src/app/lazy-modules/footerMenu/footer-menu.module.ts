import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { FooterMenuComponent } from '@lazy-modules/footerMenu/footer-menu.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule
  ],
  declarations: [ FooterMenuComponent ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class FooterMenuModule {
  static entry = FooterMenuComponent;
}
