import { HttpClientModule } from '@angular/common/http';
import { Injector, NgModule, NgModuleFactory, NO_ERRORS_SCHEMA, Compiler } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from '@ladbrokesDesktop/app-routing.module';
import { RootComponent } from '@ladbrokesDesktop/app.component';
import { BmaModule } from '@bmaModule/bma.module';
import { SharedModule } from '@sharedModule/shared.module';
import { CoreModule } from '@coreModule/core.module';
import { DesktopModule } from '@desktop/desktop.module';
import { LocaleService } from '@core/services/locale/locale.service';
import * as sbDesktopLangData from '@app/lazy-modules/locale/translations/en-US/sbdesktop.lang';
import { runOnAppInit, STORE_PREFIX } from '@frontend/vanilla/core';
import { VanillaInitModule } from '@vanillaInitModule/vanilla-init.module';
import { CoralSportsClientConfigModule } from '@app/client-config/client-config.module';
import { HostAppBootstrapper } from '@app/host-app/host-app-bootstrapper.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';

@NgModule({
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    CoreModule,
    VanillaInitModule,
    AppRoutingModule,
    SharedModule.forRoot(),
    BmaModule,
    DesktopModule,
    CoralSportsClientConfigModule.forRoot(),
  ],
  declarations: [
    RootComponent
  ],
  providers: [
    { provide: STORE_PREFIX, useValue: 'coralsports.' },
    runOnAppInit(HostAppBootstrapper)
  ],
  bootstrap: [
  ],
  schemas: [NO_ERRORS_SCHEMA],
})
export class AppModule {
  constructor(
    private compiler: Compiler,
    private injector: Injector,
    private localeService: LocaleService,private routingState: RoutingState) {
    this.routingState.loadRouting();
    const paths = {
      '@lazy-modules/locale/translation.module': import('@lazy-modules/locale/translation.module').then(module => module.TranslationModule),
      '@lazy-modules/performanceMark/performanceMark.module': import('@lazy-modules/performanceMark/performanceMark.module')
      .then(module => module.PerformanceMarkModule),
      '@lazy-modules/awsFirehose/awsFirehose.module': import('@lazy-modules/awsFirehose/awsFirehose.module')
      .then(module => module.AWSFirehoseModule),
      '@lazy-modules/arcUser/arcUser.module': import('@lazy-modules/arcUser/arcUser.module')
        .then(module => module.ArcUserModule),
      '@lazy-modules/serviceClosure/service-closure.module': import('@lazy-modules/serviceClosure/service-closure.module')
      .then(module => module.ServiceClosureModule),
      '@lazy-modules/freeRideHelper/freeRideHelper.module': import('@lazy-modules/freeRideHelper/freeRideHelper.module')
      .then(module => module.FreeRideHelperModule),
      '@lazy-modules/flagSource/flag-source.module': import('@lazy-modules/flagSource/flag-source.module')
      .then(module => module.FlagSourceModule)
    };

    for (const path in paths) {
      if(path) {
        paths[path].then((loadedModule: any) => {
          return this.loadModuleFactory(loadedModule);
        }).then((moduleFactory: NgModuleFactory<any>) => moduleFactory.create(this.injector));
      }
    }
    this.localeService.setLangData(sbDesktopLangData);
  }

  loadModuleFactory(loadedModule: any): NgModuleFactory<any> {
    if (loadedModule instanceof NgModuleFactory) {
      return loadedModule;
    } else {
      return this.compiler.compileModuleAsync(loadedModule) as any;
    }
  }
}
