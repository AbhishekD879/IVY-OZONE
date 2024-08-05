import { BetSummaryComponent } from '@app/quickbet/components/betSummary/bet-summary.component';
import { CurrencyPipe } from '@angular/common';

describe('#BetSummaryComponent', () => {
  let component: BetSummaryComponent;
  let userService;
  let currencyPipe;
  let bppProviderService;

  beforeEach(() => {
    userService = {
      currencySymbol: '£'
    };

    currencyPipe = {
      transform: jasmine.createSpy('transformCurrency')
    };
    bppProviderService = {
      quickBet: jasmine.createSpy('quickBet')
    };

    component = new BetSummaryComponent(
      userService,
      currencyPipe,
      bppProviderService
    );

    component.selection = {
      userService: {},
      categoryId: '16',
      className: 'Football Auto Test',
      currency: '£',
      eventIsLive: true,
      freebetValue: 1,
      isEachWay: false,
      potentialPayout: '28.25',
      stake: '1'
    } as any;
  });


  it('should create BetSummaryComponent instance', () => {
    expect(component).toBeTruthy();
  });

  it('@getTotalStake', () => {
    component.getTotalStake();
    expect(currencyPipe.transform).toHaveBeenCalledWith(2, userService.currencySymbol, 'code');
  });

  it('@getTotalStake', () => {
    component.selection.isEachWay = true;
    component.selection.freebetValue = 0;
    component.selection.stake = '0';

    component.getTotalStake();
    expect(currencyPipe.transform).toHaveBeenCalledWith(0, userService.currencySymbol, 'code');
  });

  it('@getPotentialPayout', () => {
    component.getPotentialPayout();
    expect(currencyPipe.transform).toHaveBeenCalledWith('28.25', userService.currencySymbol, 'code');
  });

  it('@getPotentialPayout with undefined potentialPayout', () => {
    component.selection.potentialPayout = undefined;
    component.getPotentialPayout();
    expect(currencyPipe.transform).not.toHaveBeenCalled();
  });

  it('@getStake', () => {
    component.getStake();
    expect(currencyPipe.transform).toHaveBeenCalledWith(1, userService.currencySymbol, 'code');
  });

  describe('CurrencyPipe', () => {
    beforeEach(() => {
      component['currencyPipe'] = new CurrencyPipe('en-US');
    });

    it('should transform total stake to correct currency code', () => {
      expect(component.getTotalStake()).toBe('£2.00');

      component['user'] = {
        currencySymbol: 'NZD'
      } as any;
      expect(component.getTotalStake()).toBe('NZD2.00');
    });

    it('should transform potential payout to correct currency code', () => {
      expect(component.getPotentialPayout()).toBe('£28.25');

      component['user'] = {
        currencySymbol: 'NZD'
      } as any;
      expect(component.getPotentialPayout()).toBe('NZD28.25');
    });
  });

  describe('isCapped', () => {
    it('should return maxpayout value', () => {
      const spy = spyOn(component.showMaxPayOutMessage as any, 'emit');
      component.selection.potentialPayout = '200';
      component.maxPayOutValue ='100';
      component.isCapped();
      expect(spy).toHaveBeenCalledWith(true);
      expect(currencyPipe.transform).toHaveBeenCalledWith('100', userService.currencySymbol, 'code');
    });
    it('should return POTENTIAL RETUENS value', () => {
      spyOn(component as any,'getPotentialPayout');
      const spy =  spyOn(component.showMaxPayOutMessage as any, 'emit');
      component.selection.potentialPayout = '100';
      component.maxPayOutValue ='200';
      component.isCapped();
      expect(spy).toHaveBeenCalledWith(false);
      expect(component.getPotentialPayout).toHaveBeenCalled();
    });
  });
});
