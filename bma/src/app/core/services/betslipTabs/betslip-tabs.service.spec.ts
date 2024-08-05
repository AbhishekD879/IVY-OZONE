import { of as observableOf } from 'rxjs';
import { BetslipTabsService } from './betslip-tabs.service';

describe('BetslipTabsService', () => {

  let service: BetslipTabsService;

  let locale;
  let pubsub;
  let device;
  let cmsService;

  beforeEach(() => {
    locale = {
      getString: jasmine.createSpy().and.returnValue('tab')
    };
    pubsub = {
      publish: jasmine.createSpy()
    };
    device = {
      isMobile: true
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({}))
    };

    service = new BetslipTabsService(locale, pubsub, device, cmsService);
  });

  it('createTab', () => {
    expect(service.createTab('betslip', 0, '/betslip')).toEqual({
      title: 'tab',
      name: 'tab',
      id: 0,
      url: '/betslip'
    });
    expect(locale.getString).toHaveBeenCalledTimes(1);
    expect(locale.getString).toHaveBeenCalledWith('app.betslipTabs.betslip');
  });

  describe('getTabsList', () => {
    it('getTabsList (shopBetHistory)', () => {
      service.getTabsList().subscribe(tabs => {
        expect(tabs.length).toEqual(4);
      });
    });

    it('getTabsList (cashout tab disabled)', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({
        CashOut: {
          isCashOutTabEnabled: false
        }
      }));

      service.getTabsList().subscribe(tabs => {
        expect(tabs.length).toEqual(3);
      });
    });

    it('getTabsList (shopBetHistory)', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({
        Connect: { // TODO: rename to retail after changes in cms.
          shopBetHistory: true
        }
      }));

      service.getTabsList().subscribe(tabs => {
        expect(tabs.length).toEqual(5);
      });
    });
  });

  describe('redirectToBetSlipTab', () => {
    it('return null when link is not defined in dictionary', () => {
      const mockInput = '/link';

      expect(service.redirectToBetSlipTab(mockInput)).toEqual(null);
      expect(pubsub.publish).not.toHaveBeenCalled();
    });

    it('return string when link is defined in dictionary', () => {
      const mockInput = 'CASH OUT';

      expect(service.redirectToBetSlipTab(mockInput)).toEqual(mockInput);
      expect(pubsub.publish).not.toHaveBeenCalled();
    });

    it('call publish method and return string', () => {
      const mockInput = 'CASH OUT';
      const expectedPublishMethod = 'LOAD_CASHOUT_BETS';
      device = {
        isMobile: false
      };
      service = new BetslipTabsService(locale, pubsub, device, cmsService);

      expect(service.redirectToBetSlipTab(mockInput, true)).toEqual(mockInput);
      expect(pubsub.publish).toHaveBeenCalledWith(expectedPublishMethod);
    });
  });
});
