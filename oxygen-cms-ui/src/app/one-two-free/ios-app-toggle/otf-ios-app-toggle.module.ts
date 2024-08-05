import {NgModule} from '@angular/core';
import {SharedModule} from '../../shared/shared.module';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

import {OtfIosAppToggleRoutingModule} from '@app/one-two-free/ios-app-toggle/otf-ios-app-toggle-routing.module';
import {OtfIosAppTogglePageComponent} from '@app/one-two-free/ios-app-toggle/page/otf-ios-app-toggle-page.component';
import {OtfIosAppToggleApiService} from '@app/one-two-free/service/otfIosAppToggle.api.service';

@NgModule({
  imports: [
    SharedModule,
    FormsModule,
    ReactiveFormsModule,
    OtfIosAppToggleRoutingModule
  ],
  declarations: [
    OtfIosAppTogglePageComponent
  ],
  providers: [
    OtfIosAppToggleApiService
  ],
  entryComponents: [
    OtfIosAppTogglePageComponent
  ]
})
export class OtfIOSAppToggleModule {

}
