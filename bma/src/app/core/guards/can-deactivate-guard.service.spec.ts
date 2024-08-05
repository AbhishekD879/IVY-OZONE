import { TestBed } from '@angular/core/testing';
import { CanDeactivateGuard } from './can-deactivate-guard.service';

describe('CanDeactivateGuard', () => {

  it('should call', () => {
    const guard = TestBed.runInInjectionContext(() => CanDeactivateGuard({canChangeRoute: () => true,  onChangeRoute: () => false} as any,{} as any,{} as any, {} as any) as any) as any;
    expect(guard).toBeTruthy();
  })

  it('should call', () => {
    const guard = TestBed.runInInjectionContext(() => CanDeactivateGuard({canChangeRoute: () => false, onChangeRoute: () => false} as any,{} as any,{} as any, {} as any) as any) as any;
    expect(guard).toBeFalsy();
  })
});
