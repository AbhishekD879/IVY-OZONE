import { Router } from '@angular/router';
import environment from '@environment/oxygenEnvConfig';
import { GermanSupportSportTabGuard } from './german-support-sport-tab-guard.service';
import { GermanSupportService } from '@app/core/services/germanSupport/german-support.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { TestBed } from '@angular/core/testing';

describe('GermanSupportSportTabGuard', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: LocaleService,
          useValue: { getString: () => 'locale' },
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        },
        {
          provide: GermanSupportService,
          useValue: { isGermanUser: () => true, showDialog: () => true },
        }
      ],
    });
  })
  it('should call', () => {
    environment.brand = 'lads'
    const guard = TestBed.runInInjectionContext(() => GermanSupportSportTabGuard({} as any, { url: 'football/jackpot' } as any) as any) as any;
    expect(guard).toBeFalsy();
  })

  it('should call', () => {
    environment.brand = 'bma'
    const guard = TestBed.runInInjectionContext(() => GermanSupportSportTabGuard({} as any, { url: 'football/jackpot' } as any) as any) as any;
    expect(guard).toBeTruthy();
  })

  it('should call', () => {
    environment.brand = 'lads'
    const guard = TestBed.runInInjectionContext(() => GermanSupportSportTabGuard({} as any, { url: 'baseball/jackpot' } as any) as any) as any;
    expect(guard).toBeTruthy();
  })


  it('should call', () => {
    const guard = TestBed.runInInjectionContext(() => GermanSupportSportTabGuard({} as any, { url: 'baseball/jackpot' } as any) as any) as any;
    expect(guard).toBeTruthy();
  })
});
