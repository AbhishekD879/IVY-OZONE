import { HttpClientModule } from '@angular/common/http';
import { Injector, NgModule, NgModuleFactory, NO_ERRORS_SCHEMA, Compiler } from '@angular/core';
import { BrowserModule, HammerModule, HammerGestureConfig, HAMMER_GESTURE_CONFIG } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { STORE_PREFIX, runOnAppInit } from '@frontend/vanilla/core';
import { AppRoutingModule } from '@coralMobile/app-routing.module';
import { RootComponent } from '@coralMobile/app.component';
import { VanillaInitModule } from '@vanillaInitModule/vanilla-init.module';
import { HostAppBootstrapper } from '@app/host-app/host-app-bootstrapper.service';

import { SharedModule } from '@sharedModule/shared.module';
import { BmaModule } from '@bmaModule/bma.module';
import { CoreModule } from '@coreModule/core.module';
import { SbModule } from '@sbModule/sb.module';
import { CoralSportsClientConfigModule } from '@app/client-config/client-config.module';
import { NativeBridgeBootstrapperService } from '@vanillaInitModule/services/NativeBridgeBootstrapper/native-bridge-bootstrapper.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
// import { CasinoPlatformLoaderModule } from '@casinocore/loader';
import { MatLegacyDialogRef as MatDialogRef, MAT_LEGACY_DIALOG_DATA as MAT_DIALOG_DATA, MatLegacyDialogModule as MatDialogModule } from '@angular/material/legacy-dialog';
import { BannersModule } from '@app/lazy-modules/banners/banners.module';

import * as Hammer from 'hammerjs';
export class HammerConfig extends HammerGestureConfig {
  overrides = {
    'swipe': { enable: true, direction: Hammer.DIRECTION_HORIZONTAL },
    'pan': { enable: true, direction: Hammer.DIRECTION_VERTICAL },
    'pinch':  { enable: false },
    'rotate': { enable: false }
  };
  // https://github.com/hammerjs/hammer.js/issues/1240
	options = {
		inputClass: Hammer.TouchMouseInput
	};
}

@NgModule({
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    BannersModule,
    CoreModule,
    VanillaInitModule,
    AppRoutingModule,
    SharedModule.forRoot(),
    BmaModule,
    SbModule,
    CoralSportsClientConfigModule.forRoot(),
   // CasinoPlatformLoaderModule,
    MatDialogModule,
    HammerModule
  ],
  declarations: [
    RootComponent
  ],
  providers: [
    { provide: STORE_PREFIX, useValue: 'coralsports.' },
    { provide: HAMMER_GESTURE_CONFIG, useClass: HammerConfig},
    { provide: MatDialogRef, useValue: {} },
    { provide: MAT_DIALOG_DATA, useValue: [] },
    runOnAppInit(HostAppBootstrapper)
  ],
  bootstrap: [
  ],
  schemas: [NO_ERRORS_SCHEMA],
})
export class AppModule {
  constructor(
    private injector: Injector,
    private compiler: Compiler,
    private nativeBridgeBootstrapper: NativeBridgeBootstrapperService,
    private routingState: RoutingState
  ) {
    this.routingState.loadRouting();
    const paths = {
      '@sharedModule/components/moduleRibbon/module-ribbon.module': import('@sharedModule/components/moduleRibbon/module-ribbon.module').then(module => module.RibbonModule),
      '@lazy-modules/locale/translation.module': import('@lazy-modules/locale/translation.module')
                                                  .then(module => module.TranslationModule),
      '@lazy-modules/performanceMark/performanceMark.module': import('@lazy-modules/performanceMark/performanceMark.module')
                                                                .then(module => module.PerformanceMarkModule),
      '@lazy-modules/awsFirehose/awsFirehose.module': import('@lazy-modules/awsFirehose/awsFirehose.module')
      .then(module => module.AWSFirehoseModule),
      '@lazy-modules/arcUser/arcUser.module': import('@lazy-modules/arcUser/arcUser.module')
        .then(module => module.ArcUserModule),
      '@lazy-modules/segmentEventManager/segment-event-manager.module':
        import('@lazy-modules/segmentEventManager/segment-event-manager.module')
          .then(module => module.SegmentEventManagerModule),
      '@lazy-modules/serviceClosure/service-closure.module': import('@lazy-modules/serviceClosure/service-closure.module')
      .then(module => module.ServiceClosureModule),
      '@lazy-modules/betpackPage/betpack-cms.module': import('@lazy-modules/betpackPage/betpack-cms.module')
      .then(module => module.BetpackCmsModule),
      '@lazy-modules/flagSource/flag-source.module': import('@lazy-modules/flagSource/flag-source.module')
      .then(module => module.FlagSourceModule)
    };

    for (const path in paths) {
      if (path) {
        paths[path].then((loadedModule: any) => {
          return this.loadModuleFactory(loadedModule);
        })
        .then((moduleFactory: NgModuleFactory<any>) => moduleFactory.create(this.injector));
      }
    }
    // Attaches Native Bridge Adapter and Portal Native Event Notifier.
    this.nativeBridgeBootstrapper.init();
  }

  loadModuleFactory(loadedModule: any): NgModuleFactory<any> {
    if (loadedModule instanceof NgModuleFactory) {
      return loadedModule;
    } else {
      return this.compiler.compileModuleAsync(loadedModule) as any;
    }
  }
}
