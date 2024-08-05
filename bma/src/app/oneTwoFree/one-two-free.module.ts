import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';

import { OneTwoFreeComponent } from '@app/oneTwoFree/components/mainOneTwoFree/one-two-free.component';
import { OneTwoFreeDialogComponent } from '@app/oneTwoFree/components/one-two-free-dialog.component';
import {
  LoginSplashScreenComponent
} from '@app/oneTwoFree/components/mainOneTwoFree/components/loginSplashScreen/login-splash-screen.component';
import { OneTwoFreeRoutingModule } from './one-two-free.routing.module';

@NgModule({
  declarations: [
    OneTwoFreeComponent,
    OneTwoFreeDialogComponent,
    LoginSplashScreenComponent
  ],
  imports: [
    SharedModule,
    OneTwoFreeRoutingModule,
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class OneTwoFreeModule {}
