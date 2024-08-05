import { MaintenanceGuard, MaintenanceResolver } from '@core/guards/maintenance-guard.service';
import { TestBed } from '@angular/core/testing';
import { MaintenanceService } from '@core/services/maintenance/maintenance.service';
import { Router } from '@angular/router';
import { of } from 'rxjs/internal/observable/of';

describe('MaintenanceGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: MaintenanceService,
          useValue: { getActiveMaintenancePage: () => of({ data: true }), getMaintenanceIfActive: () => of({ data: true }) },
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        }
      ],
    });
  })
  it('should call MaintenanceGuard', () => {
    const guard = TestBed.runInInjectionContext(() => MaintenanceGuard({} as any, {} as any, {} as any, {} as any) as any) as any;
    let retVal;
    guard.subscribe(el => retVal = el)
    expect(retVal).toBeFalsy();
  })

  it('should call MaintenanceGuard', () => {
    const guard = TestBed.runInInjectionContext(() => MaintenanceResolver({} as any, {} as any) as any) as any;
    let retVal;
    guard.subscribe(el => retVal = el)
    expect(typeof retVal).toEqual('object');
  })

  it('should call MaintenanceGuard', () => {
    TestBed.overrideProvider(MaintenanceService, { useValue: { getMaintenanceIfActive: () => of(null) } });
    const guard = TestBed.runInInjectionContext(() => MaintenanceResolver({} as any, {} as any) as any) as any;
    let retVal;
    guard.subscribe(el => retVal = el)
    expect(typeof retVal).not.toEqual('object');
  })
});
