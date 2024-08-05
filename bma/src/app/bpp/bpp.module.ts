import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { BppErrorService } from './services/bppError/bpp-error.service';
import { BppService } from './services/bpp/bpp.service';
import { BppProvidersService } from './services/bppProviders/bpp-providers.service';
import { ProxyHeadersService } from './services/proxyHeaders/proxy-headers.service';
import { BppAuthService } from './services/bppProviders/bpp-auth.service';

import { SharedModule } from '@sharedModule/shared.module';
import { BppCacheService } from '@app/bpp/services/bppProviders/bpp-cache.service';

@NgModule({
  declarations: [],
  imports: [ SharedModule ],
  exports: [],
  providers: [
    BppErrorService,
    ProxyHeadersService,
    BppService,
    BppCacheService,
    BppProvidersService,
    BppAuthService
  ],
  schemas: [NO_ERRORS_SCHEMA]
})

export class BppModule {}
