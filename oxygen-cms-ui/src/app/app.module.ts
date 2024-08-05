import {BrowserModule} from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { InjectionToken, NgModule } from '@angular/core';
import {HTTP_INTERCEPTORS, HttpClientModule, HttpClient} from '@angular/common/http';
import {RouterModule} from '@angular/router';

import {SharedModule} from './shared/shared.module';
import {AppRoutingModule} from './app.routing';

import {AppComponent} from './app.component';

import {ApiClientService} from './client/private/services/http/index';
import {AllHttpInterceptor} from './client/private/services/http/transport/httpInterceptor';
import {BrandService} from './client/private/services/brand.service';
import {ErrorService} from './client/private/services/error.service';
import { ImageLoaderService } from '@app/client/private/services/imageLoader/image-loader-service';
import { environment } from '@environment/environment';
import { ByteToKbPipe } from '@app/client/private/pipes/byteToKb.pipe';

export const DOMAIN = new InjectionToken<string>('DOMAIN');
export const BRAND = new InjectionToken<string>('BRAND');
export const getBrandFn = (brandService: BrandService) => brandService.brand;

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    RouterModule,
    SharedModule,
    AppRoutingModule
  ],
  providers: [
    ErrorService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AllHttpInterceptor,
      multi: true
    },
    ApiClientService,
    BrandService,
    { provide: DOMAIN, useValue: environment.apiUrl },
    { provide: BRAND,
      useFactory: getBrandFn,
      deps: [BrandService]
    },
    { provide: ImageLoaderService,
      useClass: ImageLoaderService,
      deps: [HttpClient, DOMAIN, BRAND, ByteToKbPipe]
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
