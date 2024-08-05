import { GermanSupportGuard } from './german-support-guard.service';
import { Router } from '@angular/router';
import environment from '@environment/oxygenEnvConfig';
import { TestBed } from '@angular/core/testing';
import { GermanSupportService } from '@app/core/services/germanSupport/german-support.service';
import { LocaleService } from '@core/services/locale/locale.service';

describe('GermanSupportGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: LocaleService,
          useValue: { getString: () => true },
        },
        {
          provide: GermanSupportService,
          useValue: { isGermanUser: () => true, showDialog: () => true },
        },
        {
          provide: Router,
          useValue: { navigate: () => Promise.resolve(true) },
        }
      ],
    });
  })
  it('should call 1', () => {
    environment.brand = 'bma';
    const guard = TestBed.runInInjectionContext(() => GermanSupportGuard({} as any, { url: 'racing' } as any) as any) as any;
    expect(guard).toBeTruthy();
  })


  it('should call 2', () => {
    environment.brand = 'lads';
    const guard = TestBed.runInInjectionContext(() => GermanSupportGuard({} as any, { url: 'racing' } as any) as any) as any;
    expect(guard).toBeFalsy();
  })

  it('should call 2 in true', () => {
    environment.brand = 'lads';
    const guard = TestBed.runInInjectionContext(() => GermanSupportGuard({} as any, { url: 'lotto' } as any) as any) as any;
    expect(guard).toBeFalsy();
  })

  it('should call 3', () => {
    environment.brand = 'lads';
    const guard = TestBed.runInInjectionContext(() => GermanSupportGuard({} as any, { url: 'tote-information' } as any) as any) as any;
    expect(guard).toBeTruthy();
  })
});
