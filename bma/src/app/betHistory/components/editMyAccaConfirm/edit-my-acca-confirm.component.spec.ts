import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { EditMyAccaConfirmComponent } from './edit-my-acca-confirm.component';

describe('EditMyAccaConfirmComponent', () => {
  let editMyAccaService;
  let pubSubService;
  let windowRefService;
  let component: EditMyAccaConfirmComponent;

  beforeEach(() => {
    editMyAccaService = {
      editMyAcca: jasmine.createSpy('editMyAcca').and.returnValue(of(null)),
      hasSuspendedLegs: jasmine.createSpy('hasSuspendedLegs'),
      hasLegsWithLostStatus: jasmine.createSpy('hasLegsWithLostStatus')
    };
    pubSubService = {
      API: pubSubApi,
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe')
    };
    windowRefService = {
      nativeWindow: {
        setInterval: jasmine.createSpy('setInterval'),
        clearInterval: jasmine.createSpy('clearInterval')
      }
    };

    component = new EditMyAccaConfirmComponent(
      editMyAccaService,
      pubSubService,
      windowRefService
    );
  });

  describe('submit', () => {
    it('should submit', fakeAsync(() => {
      component.bet = {
        eventSource: {},
        location: ''
      } as any;
      component['stopTimer'] = jasmine.createSpy();

      component.submit();
      tick();

      expect(editMyAccaService.editMyAcca).toHaveBeenCalled();
      expect(component['stopTimer']).toHaveBeenCalled();
    }));

    it('should not submit while loading', () => {
      component.loading = true;
      component.submit();
      expect(editMyAccaService.editMyAcca).not.toHaveBeenCalled();
    });
  });

  describe('isDisabled', () => {
    it('should disalbe confirm button', () => {
      component.bet = {
        eventSource: { validateBetStatus: 'pending' }
      } as any;
      expect(component.isDisabled).toBe(true);
    });

    it('should enable confirm button', () => {
      component.bet = {
        eventSource: {
          validateBetStatus: 'ok',
          leg: [{ removing: true }, {}]
        }
      } as any;
      editMyAccaService.hasSuspendedLegs.and.returnValue(false);
      editMyAccaService.hasLegsWithLostStatus.and.returnValue(false);
      expect(component.isDisabled).toBe(false);
    });
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(pubSubService.subscribe).toHaveBeenCalledTimes(1);
  });

  it('ngOnDestroy', () => {
    component['stopTimer'] = jasmine.createSpy();
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledTimes(1);
    expect(component['stopTimer']).toHaveBeenCalledTimes(1);
  });

  it('startTimer', () => {
    component['getTimerValue'] = jasmine.createSpy();
    windowRefService.nativeWindow.setInterval.and.callFake(cb => cb());

    component['startTimer'](1);

    expect(windowRefService.nativeWindow.setInterval).toHaveBeenCalledTimes(1);
    expect(component['getTimerValue']).toHaveBeenCalledTimes(2);
  });

  it('stopTimer', () => {
    component['stopTimer']();
    expect(windowRefService.nativeWindow.clearInterval).toHaveBeenCalledTimes(1);
  });

  it('getTimerValue', () => {
    expect(component['getTimerValue'](-2)).toBe('00:00');
    expect(component['getTimerValue'](3)).toBe('00:03');
    expect(component['getTimerValue'](12)).toBe('00:12');
  });
});
