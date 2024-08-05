import { fakeAsync, flush } from '@angular/core/testing';

import { PriceOddsButtonOnPushComponent } from './price-odds-button-onpush.component';

describe('PriceOddsButtonOnPush', () => {
  let elementRef;
  let component: PriceOddsButtonOnPushComponent;

  beforeEach(() => {
    elementRef = {
      nativeElement: {
        classList: {
          add: jasmine.createSpy('add'),
          remove: jasmine.createSpy('remove')
        }
      }
    };
    component = new PriceOddsButtonOnPushComponent(elementRef);

  });

  it('Component should be created', () => {
    expect(component).toBeTruthy();
  });

  describe('ngOnChanges', () => {
    let changes;

    beforeEach(() => {
      component.disabled = undefined;
      spyOn<any>(component, 'isDisabled').and.returnValue(false);
      spyOn<any>(global, 'requestAnimationFrame').and.callFake((fn: Function) => { fn(); });

      changes = {
        priceDec: {
          firstChange: false,
          previousValue: null,
          currentValue: 0
        }
      };
    });

    it('should toggle class "bet-down"', fakeAsync(() => {
      changes.priceDec.previousValue = 5;
      changes.priceDec.currentValue = 3;
      const className = 'bet-down';

      component.ngOnChanges(changes);
      expect(elementRef.nativeElement.classList.add).toHaveBeenCalledWith(className);
      flush();
      expect(elementRef.nativeElement.classList.remove).toHaveBeenCalledWith(className);
    }));

    it('should toggle class "bet-up"', fakeAsync(() => {
      changes.priceDec.previousValue = 3;
      changes.priceDec.currentValue = 5;
      const className = 'bet-up';

      component.ngOnChanges(changes);

      expect(elementRef.nativeElement.classList.add).toHaveBeenCalledWith(className);
      flush();
      expect(elementRef.nativeElement.classList.remove).toHaveBeenCalledWith(className);
    }));
    it('should convert handicap value when value is positive', fakeAsync(() => {
      changes.priceDec.previousValue = 3;
      changes.priceDec.currentValue = 5;
      component.handicapVal = '1,';
      component.ngOnChanges(changes);
      flush();
      expect(component.handicapVal).toEqual('1');
    }));
    it('should convert handicap value when value is null', fakeAsync(() => {
      changes.priceDec.previousValue = 3;
      changes.priceDec.currentValue = 5;
      component.handicapVal = '';
      component.ngOnChanges(changes);
      flush();
      expect(component.handicapVal).toEqual('');
    }));
    it('should convert handicap value when value is negative', fakeAsync(() => {
      changes.priceDec.previousValue = 3;
      changes.priceDec.currentValue = 5;
      component.handicapVal = '-1,';
      component.ngOnChanges(changes);
      flush();
      expect(component.handicapVal).toEqual('-1');
    }));
    it('check is it a football or not expect football', fakeAsync(() => {
      changes.priceDec.previousValue = 3;
      changes.priceDec.currentValue = 5;
      component.categoryId = '16';
      component.ngOnChanges(changes);
      flush();
      expect(component.categoryId).toEqual('16');
    }));
    it('check is it a football or not expect not a football', fakeAsync(() => {
      changes.priceDec.previousValue = 3;
      changes.priceDec.currentValue = 5;
      component.categoryId = '3';
      component.ngOnChanges(changes);
      flush();
      expect(component.categoryId).not.toEqual('16');
    }));
  });

  describe('isDisabled', () => {
    beforeEach(() => {
      component.disabled = undefined;
      component.eventStatusCode = undefined;
      component.marketStatusCode = undefined;
      component.outcomeStatusCode = undefined;
      component.displayed = undefined;
      component.nonRunner = undefined;
      component.priceType = undefined;
      component.isRacing = true;
    });

    it('should set button enabled', () => {
      expect(component['isDisabled']()).toEqual(null);
    });

    it('should set button enabled if no priceType for racing outcome', () => {
      component.priceType = 'SP';
      component.isRacing = true;
      expect(component['isDisabled']()).toEqual(null);
    });

    it('should set button disabled if no priceType but racing outcome', () => {
      component.isRacing = false;
      expect(component['isDisabled']()).toEqual('disabled');
    });

    it('should set button disabled if event suspended', () => {
      component.eventStatusCode = 'S';

      expect(component['isDisabled']()).toEqual('disabled');
    });

    it('should set button disabled if market suspended', () => {
      component.marketStatusCode = 'S';

      expect(component['isDisabled']()).toEqual('disabled');
    });

    it('should set button disabled if outcome suspended', () => {
      component.outcomeStatusCode = 'S';

      expect(component['isDisabled']()).toEqual('disabled');
    });

    it('should set button disabled if event undisplayed', () => {
      component.displayed = 'N';

      expect(component['isDisabled']()).toEqual('disabled');
    });

    it('should set button disabled if nonRunner', () => {
      component.nonRunner = true;

      expect(component['isDisabled']()).toEqual('disabled');
    });
  });

});
