import { QuickStakeComponent } from '@app/quickbet/components/quickStake/quick-stake.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync, flush, tick } from '@angular/core/testing';
import { of } from 'rxjs';

describe('QuickStakeComponent', () => {
  let component ,userService, pubsubService, changeDetectorRef, cmsService,locale,windowRef;

  beforeEach(() => {
    userService = {
      currencySymbol: '$'
    };
    pubsubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };

    changeDetectorRef = {
      markForCheck: jasmine.createSpy('markForCheck')
    };
    cmsService={
      getQuickStakes:jasmine.createSpy('getQuickStakes').and.returnValue(of(['10','20','30','40']))
    };
    locale={
      getString: jasmine.createSpy().and.returnValue('Ladbrokes'),
    }
    windowRef = {
      document: {
        getElementsByClassName : jasmine.createSpy().and.returnValue([ {'style' :  {
          backgroundColor : ''
        }}])
      }
    };

    component = new QuickStakeComponent(userService, pubsubService, changeDetectorRef,cmsService,locale,windowRef);
  });

  describe('ngOnInit', () => {
    it('should subscribe to session events to handle currency change', () => {
      spyOn(component as any,'formatquickbetStakes');
      component.betslipType='global_stakes';
      component.ngOnInit();
      expect(pubsubService.subscribe).toHaveBeenCalledWith('QuickStakeController', [pubsubService.API.SESSION_LOGIN,
        pubsubService.API.SESSION_LOGOUT], component.reformatKrCurrency);

      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should format quick stakes for Kr user', () => {
      userService.currencySymbol = 'Kr';
      component.ngOnInit();

      expect(component.quickStakePrefix).toEqual('+Kr');
      expect(component.quickStakeItems).toEqual(['10', '20', '30', '40']);
    });

    it('should format quick stakes for Kr user is formatted', () => {
      userService.currencySymbol = 'Kr';
      component.quickStakeItems = ['10','20', '30', '40'];
      component.ngOnInit();

      expect(component.quickStakePrefix).toEqual('+Kr');
      expect(component.quickStakeItems).toEqual(['10', '20', '30', '40']);
    });

    it('should format quick stakes for Kr user', () => {
      userService.currencySymbol = '$';
      component.ngOnInit();

      expect(component.quickStakePrefix).toEqual('+$');
      expect(component.quickStakeItems).toEqual(['10', '20', '30', '40']);
    });

    it('should format quick stakes is formatted', () => {
      userService.currencySymbol = '$';
      component.quickStakeItems = ['20', '30', '40'];
      component.ngOnInit();

      expect(component.quickStakePrefix).toEqual('+$');
      expect(component.quickStakeItems).toEqual(['10', '20', '30', '40']);
    });
    it('should format quick stakes is nodata', () => {
      cmsService={
        getQuickStakes:jasmine.createSpy('getQuickStakes').and.returnValue(of(undefined))
      };
      component = new QuickStakeComponent(userService, pubsubService, changeDetectorRef,cmsService,locale,windowRef);
      component.ngOnInit();
      expect(component.quickStakePrefix).toEqual('+$');
      expect(component.quickStakeItems).toEqual(undefined);
    });
  });

  it('should unsubscribe onDestroy', () => {
    component.ngOnDestroy();

    expect(pubsubService.unsubscribe).toHaveBeenCalledWith('QuickStakeController');
  });

  it('should handle quick stake select', fakeAsync(() => {
    const notifyListener = jasmine.createSpy('notifyListener');
    const quickStake = '50';
    const clickTransition=spyOn(component,'clickTransition');
    component.quickStakeSelect.subscribe(notifyListener);
    component.setQuickStake(quickStake,0);
    tick();
    expect(clickTransition).toHaveBeenCalled();
    expect(notifyListener).toHaveBeenCalledWith(quickStake);
  }));

  it ('should handle Freebet select', () => {
    const event = { output:'selectedChange', value: 12 } as any;
    component.fbChange.emit = jasmine.createSpy('fbChange.emit');
    component.onFreebetChange(event);
    expect(component.fbChange.emit).toHaveBeenCalledWith(event);
  });

  it('trackByIndex', () => {
    const result = component.trackByIndex(2);

    expect(result).toBe(2);
  });
  describe('formatquickbetStakes' , () => {
    it('more than 2 decimal', () => {
      component.formatquickbetStakes(['10.223']);
      expect(component.quickStakeItems.length).toBe(1)
    })
    it('less than 2 decimal', () => {
      component.formatquickbetStakes(['10'])
      expect(component.quickStakeItems.length).toBe(1)
    })
  })
  describe('#clickTransition', () => {
    it('clickTransition', fakeAsync(() => {
      component.clickTransition('one');
      tick()
      expect(true).toEqual(true);
      flush();
    })
    );
    it('clickTransition qb', fakeAsync(() => {
      locale.getString = jasmine.createSpy().and.returnValue('bma')
      component.clickTransition('one');
      tick()
      expect(true).toEqual(true);
      flush();
    })
    );
  });
    describe('#reformatKrCurrency', () => {
    it('reformatKrCurrency', () => {
      component.quickStakeItems = ['10','20']
      component.user = {
        currencySymbol : 'Kr'
      } as any
      spyOn(component as any,'isFormatted')
      component.reformatKrCurrency();
      expect(component.quickStakeItems).toEqual(['100','200'])

    })
    it('reformatKrCurrency', () => {
      component.quickStakeItems = ['10','20']
      component.user = {
        currencySymbol : '$'
      } as any
      spyOn(component as any,'isFormatted')
      component.reformatKrCurrency();
      expect(component.quickStakeItems).toEqual(['10','20'])
    })
  });
  describe('#isFormatted', () => {
    it('isFormatted', () => {
      component.quickStakeItems = ['10','20']
      const retVal = component.isFormatted();
      expect(retVal).toBeTruthy();
    })
  })
});
