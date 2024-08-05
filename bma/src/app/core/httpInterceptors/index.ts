import { HTTP_INTERCEPTORS } from '@angular/common/http';

import { LocaleInterceptor } from './locale-interceptor.service';
import { MaintenanceInterceptor } from './maintenance-interceptor.service';
import { BrowserUrlInterceptor } from './browser-url-interceptor';

export const httpInterceptorProviders = [
  { provide: HTTP_INTERCEPTORS, useClass: LocaleInterceptor, multi: true },
  { provide: HTTP_INTERCEPTORS, useClass: MaintenanceInterceptor, multi: true },
  { provide: HTTP_INTERCEPTORS, useClass: BrowserUrlInterceptor, multi: true }
];
