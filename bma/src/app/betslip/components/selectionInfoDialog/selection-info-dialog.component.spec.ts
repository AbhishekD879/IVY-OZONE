import { SelectionInfoDialogComponent } from './selection-info-dialog.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';

describe('SelectionInfoDialogComponent', () => {
  let deviceService;
  let routingHelper;
  let router;
  let pubSubService;
  let timeService;
  let windowRef;
  let component: SelectionInfoDialogComponent;

  beforeEach(() => {
    deviceService = {};
    windowRef = {
      document: {
        body: {
          classList: {
            add: jasmine.createSpy('add')
          }
        }
      }
    };
    routingHelper = {
      formEdpUrl: jasmine.createSpy('formEdpUrl').and.returnValue('url')
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish')
    };
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('13:30')
    };

    component = new SelectionInfoDialogComponent(
      deviceService,
      routingHelper,
      router,
      pubSubService,
      timeService,
      windowRef
    );
    component.params = <any>{
      stake: {
        Bet: {
          legs: [ {
            selection: { typeName: 'test' },
            parts: [{
              outcome: {
                details: {
                  markets: [{}]
                }
              }
            }]
          }]
        },
        eventIds: {
          eventIds: ['555']
        },
        localTime: '12:30',
        eventName: 'test',
        sport: 'tennis',
        sportId: 12,
        className: 'class',
        outcomeName: 'Outcome',
        isRacingSport: false
      },
    };
    component.dialog = { changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') } };
  });

  describe('@open', () => {
    it('should not set dialog visibility', () => {
      component.params.contentReady = false;
      component.dialog.visible = true;
      component.open();
      expect(component.dialog.visible).toBeTruthy();
      expect(component.dialog.visibleAnimate).toBeFalsy();
    });

    it('should check if sport is Virtual = true', () => {
      component.params.stake.sportId = 39;
      component.open();
      expect(component.isVirtual).toBe(true);
    });

    it('should check if sport is Virtual = False', () => {
      component.params.stake.sportId = 10;
      component.open();
      expect(component.isVirtual).toBe(false);
    });

    it('should set title', () => {
      component.open();
      expect(component.title).toBe('Outcome');
      expect(component.cashoutValue).toBe(null);
    });

    it('should set event name', () => {
      component.open();
      expect(component.eventName).toBe('test');
    });

    it('should set event name (racing)', () => {
      component.params.stake.isRacingSport = true;
      component.open();
      expect(component.eventName).toBe('12:30 test');
    });

    it('should set event name (virtual)', () => {
      component.params.stake.sportId = 39;
      component.open();
      expect(component.eventName).toBe('13:30 test');
    });

    it('should not call super.open and updateDialogData', () => {
      component.dialog.visible = true;
      component.params.contentReady = false;
      component['updateDialogData'] = jasmine.createSpy('updateDialogData');
      (AbstractDialogComponent as any).open = jasmine.createSpy('open');

      component.open();

      expect(component['updateDialogData']).not.toHaveBeenCalled();
      expect((AbstractDialogComponent as any).open).not.toHaveBeenCalled();
    });
  });

  describe('@goToEvent', () => {
    it('goToEvent(single)', () => {
      component.goToEvent();
      expect(router.navigateByUrl).toHaveBeenCalledWith('url');
      expect(routingHelper.formEdpUrl).toHaveBeenCalledWith(jasmine.objectContaining({
        originalName: '12:30 test',
        name: 'test',
        id: '555',
        categoryName: 'tennis',
        categoryId: 12,
        className: 'class',
        typeName: 'test'
      }));
      expect(pubSubService.publish).toHaveBeenCalledWith('show-slide-out-betslip', false);
    });

    it('goToEvent(fctc)', () => {
      component.params.stake.isFCTC = true;
      component.params.stake.outcomes = [{
        details: {
          info: {
            sport: 'football',
            className: 'class',
            sportId: '33'
          }
        }
      }];
      component.goToEvent();
      expect(router.navigateByUrl).toHaveBeenCalledWith('url');
      expect(routingHelper.formEdpUrl).toHaveBeenCalledWith(jasmine.objectContaining({
        originalName: '12:30 test',
        name: 'test',
        id: '555',
        categoryName: 'football',
        categoryId: 33,
        className: 'class',
        typeName: 'test'
      }));
    });

    it('it should not navigate to EDP if it is Virtual sport', () => {
      component.isVirtual = true;
      component.goToEvent();
      expect(routingHelper.formEdpUrl).not.toHaveBeenCalled();
      expect(router.navigateByUrl).not.toHaveBeenCalled();
      expect(pubSubService.publish).not.toHaveBeenCalled();
    });
  });

  it('setTitle (forecast)', () => {
    const stake = component.params.stake;
    stake.isFCTC = true;
    stake.outcomes = [{ name: 'A' }, { name: 'B' }, { name: 'C' }];

    stake.combiName = 'FORECAST';
    component['setTitle']();
    expect(component.title).toBe('1st. A, 2nd. B, 3rd. C');

    stake.combiName = 'FORECAST_COM';
    component['setTitle']();
    expect(component.title).toBe('A, B, C');
  });

  it('setCashoutValue', () => {
    const details = component.params.stake.Bet.legs[0].parts[0].outcome.details;
    details.cashoutAvail = 'Y';
    details.markets[0].cashoutAvail = 'Y';
    component['setCashoutValue']();
    expect(component.cashoutValue).toBe('Y');
  });
});
