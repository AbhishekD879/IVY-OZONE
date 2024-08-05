import { async } from '@angular/core/testing';
import { FreeBetsNotificationComponent } from '@shared/components/freeBetsNotification/free-bets-notification.component';

describe('FreeBetsNotificationComponent', () => {
  let component: FreeBetsNotificationComponent;
  let changeDetectorRef;
  let device;
  const deviceViewType = {
    mobile: true,
    desktop: false,
    tablet: false
  }
  beforeEach(async(() => {
    device = {
      getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue(deviceViewType)
    };
    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      detach: jasmine.createSpy('detach'),
    };
  }));

  beforeEach(() => {
    component = new FreeBetsNotificationComponent(device, changeDetectorRef);
  });

  it('constructor should define component and detect if device is tablet', () => {
    expect(component).toBeDefined();
    expect(device.getDeviceViewType).toHaveBeenCalled();
  });

  describe('ngOnInit', () => {
    it('should detectChanges', () => {
      component.hasFanzones = true;
      component.hasFreeBets = false;
      component.ngOnInit();
      
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
    it('should detectChanges', () => {
      component.hasFanzones = false;
      component.hasFreeBets = true;
      component.ngOnInit();
    
      expect(changeDetectorRef.detectChanges).toHaveBeenCalled();
    });
  });

  describe('closeNotification', () => {

    it('should close notification', () => {
      component.closeNotification();
    });
  });

  describe('Banner message', ()=>{
    it('should return Freebets available test', () => {
      component.hasFreeBets = true;
      component.freebetsConfig = {freeBetsAvailableText: 'abcd'};

      expect(component.bannerMsg()).toEqual('abcd ');
    });

    it('should return bet tokens available test', () => {
      component.hasBetTokens = true;
      component.freebetsConfig = {betTokensAvailableText: 'bet tokens available'};

      expect(component.bannerMsg()).toEqual('bet tokens available ');
    });

    it('should return tokens & Freebets available test', () => {
      component.hasFreeBets = true;
      component.hasBetTokens = true
      component.freebetsConfig = {freebetAndTokensAvailableText: 'tokens & freebets available'};

      expect(component.bannerMsg()).toEqual('tokens & freebets available ');
    });
    it('should return fanzone & Freebets available test', () => {
      component.hasFreeBets = true;
      component.hasBetTokens = false;
      component.hasFanzones = true
      component.freebetsConfig = {freeBetsAvailableText: 'freebets available'};

      expect(component.bannerMsg()).toEqual('freebets available ');
    });
    it('should return Fanzone available test ', () => {
      component.hasFanzones = true;
      component.hasFreeBets = false;
      component.hasBetTokens = false;
      component.freebetsConfig = {fanZonesAvailableText: 'Fanzone available'};

      expect(component.bannerMsg()).toEqual('Fanzone available ');
    });
    it('should return Fanzone available test2 ', () => {
      component.hasFanzones = true;
      component.hasFreeBets = false;
      component.freebetsConfig = {fanZonesAvailableText: 'Fanzone available'};

      expect(component.bannerMsg()).toEqual('Fanzone available ');
    });
    it('should return Fanzone available test2 ', () => {
      component.hasFanzones = false;
      component.hasFreeBets = false;
      component.hasBetTokens = false;
      component.freebetsConfig = {betTokensAvailableText: ''};

      expect(component.bannerMsg()).toEqual('');
    });
  })
});
