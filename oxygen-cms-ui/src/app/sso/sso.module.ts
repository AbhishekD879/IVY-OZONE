import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {SharedModule} from '../shared/shared.module';
import {SsoPageComponent} from './single-sso-page/pageComponent/sso.page.component';
import {AllSsoPageComponent} from './all-sso-page/pageComponent/all.sso.page.component';
import {SsoCreateComponent} from './all-sso-page/createSsoDialog/sso.create.component';
import {SsoApiService} from './service/sso.api.service';
import {SsoPagesRoutingModule} from './sso-routing.module';

@NgModule({
  imports: [
    SharedModule,
    CommonModule,
    SsoPagesRoutingModule
  ],
  declarations: [
    AllSsoPageComponent,
    SsoPageComponent,
    SsoCreateComponent
  ],
  providers: [
    SsoApiService
  ],
  entryComponents: [SsoCreateComponent]
})
export class SsoModule { }
