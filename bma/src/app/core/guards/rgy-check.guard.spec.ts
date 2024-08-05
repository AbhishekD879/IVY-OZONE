import { TestBed, fakeAsync, flush, tick } from '@angular/core/testing';
import { RgyCheckGuard, RgyMatchGuard } from './rgy-check.guard';
import { BonusSuppressionService } from '@app/core/services/BonusSuppression/bonus-suppression.service';
import { of as observableOf } from 'rxjs';
import { Router } from '@angular/router';
import { CmsService } from '@core/services/cms/cms.service';
import { DialogService } from '@core/services/dialogService/dialog.service';

describe('RgyCheckGuard', () => {
  it('should call 1' , fakeAsync(()=> {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: BonusSuppressionService,
          useValue: { checkIfYellowFlagDisabled: () => false}
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        },
        {
          provide: CmsService,
          useValue: { getSystemConfig: () => observableOf({BonusSupErrorMsg: {url: '/url'}})},
        },
        {
          provide: DialogService,
          useValue: { openDialog: () => false, ids: {bonusSuppresionError: false}},
        }
      ],
    });

    const guard = TestBed.runInInjectionContext(() => RgyCheckGuard({data: {moduleName: 'rgy'}} as any, {url:'/sports'} as any));
    tick();
    flush();
    expect(guard).toBeFalsy();
  }))

  it('should call 1' , fakeAsync(()=> {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: BonusSuppressionService,
          useValue: { checkIfYellowFlagDisabled: () => true}
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        },
        {
          provide: CmsService,
          useValue: { getSystemConfig: () => observableOf({})},
        },
        {
          provide: DialogService,
          useValue: { openDialog: () => false, ids: {bonusSuppresionError: false}},
        }
      ],
    });

    const guard = TestBed.runInInjectionContext(() => RgyCheckGuard({data: {moduleName: 'rgy'}} as any, {url:'/sports'} as any));
    tick();
    flush();
    expect(guard).toBeTruthy();
  }))
});

describe('RgyCheckGuard', () => {
  it('should call 2' , fakeAsync(()=> {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: BonusSuppressionService,
          useValue: { checkIfYellowFlagDisabled: () => true}
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        },
        {
          provide: CmsService,
          useValue: { getSystemConfig: () => observableOf({})},
        },
        {
          provide: DialogService,
          useValue: { openDialog: () => false, ids: {bonusSuppresionError: false}},
        }
      ],
    });

    const guard = TestBed.runInInjectionContext(() => RgyMatchGuard({data: {moduleName: 'rgy'}} as any, {url:'/sports'} as any));
    tick();
    flush();
    expect(guard).toBeTruthy();
  }))
});
