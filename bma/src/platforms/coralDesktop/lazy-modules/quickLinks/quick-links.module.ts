import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CoralQuickLinksComponent as QuickLinksComponent} from '@coralDesktop/lazy-modules/quickLinks/component/quick-links.component';
import { SharedModule } from '@sharedModule/shared.module';
@NgModule({
  imports: [CommonModule, SharedModule],
  declarations: [QuickLinksComponent],
  exports: [QuickLinksComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class QuickLinksModule {
  static entry = QuickLinksComponent;
}