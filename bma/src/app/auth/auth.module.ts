import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { SessionService } from '@authModule/services/session/session.service';

@NgModule({
  imports: [

    SharedModule
  ],
  exports: [
  ],
  declarations: [
  ],
  providers: [
    SessionService
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class AuthModule { }
