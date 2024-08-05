import { BetFilterDialogComponent } from './bet-filter-dialog.component';

describe('BetFilterDialogComponent', () => {
  let deviceService;
  let gtmService;
  let windowRef;
  let component: BetFilterDialogComponent;

  beforeEach(() => {
    deviceService = {};
    windowRef = {};
    gtmService = {
      push: jasmine.createSpy('push')
    };

    component = new BetFilterDialogComponent(
      deviceService,
      gtmService,
      windowRef
    );
    component.dialog = {
      close: jasmine.createSpy('close'),
      changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') }
    };
    component.params = {
      selectMode: jasmine.createSpy('selectMode'),
      cancel: jasmine.createSpy('cancel')
    };
  });

  describe('selectMode', () => {
    it('online', () => {
      component.selectMode('online');
      expect(component.dialog.close).toHaveBeenCalledTimes(1);
      expect(component.params.selectMode).toHaveBeenCalledWith('online');
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'bet filter',
        eventAction: 'you\'re betting',
        eventLabel: 'online'
      });
    });

    it('in shop', () => {
      component.selectMode('in-shop');
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
        eventCategory: 'bet filter',
        eventAction: 'you\'re betting',
        eventLabel: 'in-shop'
      });
    });
  });

  it('cancel', () => {
    component.cancel();
    expect(component.params.cancel).toHaveBeenCalledTimes(1);
  });
});
