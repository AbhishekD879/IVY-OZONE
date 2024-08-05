import { StakeAndReturnsHeaderComponent } from '@app/betHistory/components/stakeAndReturnsHeader/stake-and-returns-header.component';
import { mybetsDataMock, mybetsDataMock1, mybetsDataMock2, mybetsDataMock3, mybetsDataMock4 } from './stake-and-returns-header.mock';


describe('StakeAndReturnsHeaderComponent', () => {
  let component, currencyPipe,gtmService,maxPayOutErrorService,windowRefService ,deviceService;
  const deviceViewType = {
    mobile: true,
    desktop: false,
    tablet: false
  }
  beforeEach(() => {
    currencyPipe = {
      transform: (v: any, s: string) => (v + s)
    };
    deviceService = { getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue(deviceViewType) };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    component = new StakeAndReturnsHeaderComponent(currencyPipe,gtmService,maxPayOutErrorService,deviceService);
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  it('#isDesktop should return true for desktop mode', ()=>{
    component.isDesktop;
    expect(deviceService.getDeviceViewType).toHaveBeenCalled();
  });

  it('#stakeValue should return the absolute stake value', ()=>{
    component.stake = 1.00;
    component.tokenValue = 0.00;
    expect(component.stakeValue).toBe(1.00);
    component.stake = 2.00;
    component.tokenValue = 1.00;
    expect(component.stakeValue).toBe(1.00);   
    component.stake = 0.00;
    component.tokenValue = 1.00;
    expect(component.stakeValue).toBe(0.00);   
    component.stake = '3.00';
    component.tokenValue = 1.00;
    expect(component.stakeValue).toBe(2.00);    
  });

  it('#estimatedReturnsValue should return estimatedReturns value', () => {
    expect(component.estimatedReturns).toBe(undefined);
    expect(component.estimatedReturnsValue).toBe('N/A');
    component.estimatedReturns = 'N/A';
    expect(component.estimatedReturnsValue).toBe('N/A');
    component.estimatedReturns = '10';
    component.currencySymbol = '$';
    expect(component.estimatedReturnsValue).toBe('10$');
    component.isEdit = true;
    expect(component.estimatedReturnsValue).toBe('10$');
    component.initialReturns = true;
    expect(component.estimatedReturnsValue).toBe('N/A');

  });

  it('#bogReturnValue should return bogReturn value', () => {
    component.livePriceWinnings = [{
      value: 1.00
    }];
    component.winnings = [{
      value: 10.00
    }];
    expect(component.bogReturnValue).toBe(9.00);
  });

  it('#bogReturnValue should return bogReturn value', () => {
    component.livePriceWinnings = undefined;
    component.winnings = undefined;
    expect(component.bogReturnValue).toBe(0);
  });
  
  describe('togglemaxPayedOut', () => {
    it('sendGTMData', () => {
      component.isMaxPayedOut = false;
      component['togglemaxPayedOut']();
      expect(gtmService.push).toHaveBeenCalled();
    });

    it('not sendGTMData', () => {
      component.isMaxPayedOut = true;
      component['togglemaxPayedOut']();
      expect(gtmService.push).not.toHaveBeenCalled();
    });
  });

  describe('isBetType', () => {
    it('if max payout true when betTag has capped ', () => {
      const better: any = mybetsDataMock;
      component['bet'] = better;
      const retVal = component.isBetType();
      expect(retVal).toBe(true);
    });
    it('if max payout false when tagName has not capped ', () => {
      const better: any = mybetsDataMock2;
      component['bet'] = better;
      const retVal = component.isBetType();
      expect(retVal).toBe(false);
    });
    it('if max payout false when tagname is null ', () => {
      const better: any = mybetsDataMock3;
      component['bet'] = better;
      const retVal = component.isBetType();
      expect(retVal).toBe(false);
    });
    it('if max payout false when no bet tags', () => {
      const better: any = mybetsDataMock1;
      component['bet'] = better;
      const retVal = component.isBetType();
      expect(retVal).toBe(false);
    });
    it('if max payout false when no eventsource  ', () => {
      const better: any = mybetsDataMock4;
      component['bet'] = better;
      const retVal = component.isBetType();
      expect(retVal).toBe(false);
    });
    it('if max payout false when no eventsource  ', () => {
      const better: any = null;
      component['bet'] = better;
      const retVal = component.isBetType();
      expect(retVal).toBe(false);
    });
  });
  
  describe('callToggleEvent', () => {
    it('should call ToggleEvent item', () => {
      component.callToggleEvent(true);
      expect(component.arrowToggleFlag).toBe(true);
    });
    it('should call ToggleEvent item', () => {
      component.callToggleEvent(false);
      expect(component.arrowToggleFlag).toBe(false);
    });
  });
});
