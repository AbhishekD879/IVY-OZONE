import { CashOutMessageComponent } from './cash-out-message.component';
import { of as observableOf } from 'rxjs';

describe('CashOutMessageComponent', () => {
  let component: CashOutMessageComponent;
  let device, infoDialog, dialogService, componentFactoryResolver, cmsService, gtmService;

  beforeEach(() => {
    device = {
      isOnline: jasmine.createSpy().and.returnValue(true)
    };
    infoDialog = {
      openConnectionLostPopup: jasmine.createSpy()
    };
    dialogService = jasmine.createSpyObj('dialogService', ['openDialog']);
    componentFactoryResolver = jasmine.createSpyObj('componentFactoryResolver', ['resolveComponentFactory']);
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        cashOutMessaging: {
          cashOutMessage: 'Cash out not available',
          findOut: 'find here',
          enable: true
        }
      }))
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    component = new CashOutMessageComponent(
      device,
      infoDialog,
      dialogService,
      componentFactoryResolver,
      cmsService,
      gtmService
    );
  });

  it('sendGTMData', () => {
    component.isMarketLevelDisabled = true;
    component['sendGTMData']();
    expect(gtmService.push).toHaveBeenCalled();
  });

  it('sendGTMData', () => {
    component.isMarketLevelDisabled = false;
    component['sendGTMData']();
    expect(gtmService.push).toHaveBeenCalled();
  });

  describe('openCashOutPopUp', () => {
    it('openCashOutPopUp: no internet', () => {
      component['device'].isOnline = jasmine.createSpy().and.returnValue(false);
      component['openCashOutPopUp']();
      expect(infoDialog.openConnectionLostPopup).toHaveBeenCalledTimes(1);
      expect(dialogService.openDialog).not.toHaveBeenCalled();
    });

    it('openCashOutPopUp: no internet', () => {
      const map = new Map();
      map.set('123', true);
      component.gaTrackDetails = map;
      component.isEventLevelDisabled = true;
      component['openCashOutPopUp']();
      expect(dialogService.openDialog).toHaveBeenCalledTimes(1);
    });
  });

  describe('sendGTMData', () => {
    it('should call openDialog when openCashOutPopUp is called ', () => {
      const map = new Map();
      map.set('123', true);
      component.gaTrackDetails = map;
      component.openCashOutPopUp();
      expect(dialogService.openDialog).toHaveBeenCalled();
    });
  });

  describe('dialogOpen', () => {
    it('should call openCashOutPopUp ', () => {
      const map = new Map();
      map.set('123', true);
      component.gaTrackDetails = map;
      const openCashOutPopUp = spyOn(component as any, 'openCashOutPopUp');
      component.dialogOpen();
      expect(openCashOutPopUp).toHaveBeenCalled();
    });
  });

  describe ('formCashOutMsg', () => {
    it('length less than 67',() => {
      component['formCashOutMsg']('Cash out not available');
      expect(component.cashOutMessage).toBe('Cash out not available');
    });
   it('length more than 67',() => {
    const msg = ' Csfd ftd yugdygds uyudsf dyfy udyf navailablilitydafgfsgfsgfdsgsfdgfdgsd. ';
    component['formCashOutMsg'](msg);
    const test = `${msg.substring(0, 67)}...`;
    });
  });

  describe('constructor', () => {
    it('should call constructor with out config ', () => {
      cmsService = { getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({}))};
      const emptyComponent = new CashOutMessageComponent(device, infoDialog, dialogService, componentFactoryResolver, cmsService, gtmService
      );
      expect(emptyComponent.findOut).not.toBe('find out');
    });
  });
});


