import { TestBed } from '@angular/core/testing';
import { PrivateMarketsGuard } from './private-markets-guard.service';
import { Router } from '@angular/router';
import { ModuleRibbonService } from '@core/services/moduleRibbon/module-ribbon.service';

describe('PrivateMarketsGuard', () => {
    beforeEach(() => {
        TestBed.configureTestingModule({
          providers: [
            {
              provide: ModuleRibbonService,
              useValue: { isPrivateMarketsTab: () => true },
            },
            {
              provide: Router,
              useValue: { navigateByUrl: () => true },
            }
          ],
        });
      })
      it('should call' , ()=> {
        const guard = TestBed.runInInjectionContext(() => PrivateMarketsGuard({routeConfig: {data: {feature: 'retailFeatureKey'}}} as any ,{} as any) as any) as any;
        expect(guard).toBeTruthy();
      })
      it('should call' , ()=> {
        TestBed.overrideProvider(ModuleRibbonService, { useValue: { isPrivateMarketsTab: () => false }});
        const guard = TestBed.runInInjectionContext(() => PrivateMarketsGuard({routeConfig: {data: {feature: 'retailFeatureKey'}}} as any ,{} as any) as any) as any;
        expect(guard).toBeFalsy();
      })
});
