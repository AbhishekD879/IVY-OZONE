import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { InPlaySportTabComponent } from '@coralDesktop/lazy-modules/InPlaySportTab/in-play-sport-tab.component';
import { DesktopModule } from '@coralDesktop/desktop/desktop.module';

@NgModule({
  imports: [SharedModule, DesktopModule],
  declarations: [InPlaySportTabComponent],
  exports: [InPlaySportTabComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class InPlaySportTabModule {
  static entry = InPlaySportTabComponent;
}
