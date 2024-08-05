import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';

import { EditMyAccaHistoryComponent } from './edit-my-acca-history.component';

describe('EditMyAccaHistoryComponent', () => {
  let betHistoryMainService;
  let cashOutSectionService;
  let timeService;
  let localeService;
  let dialogService;
  let componentFactoryResolver;
  let deviceService;
  let component: EditMyAccaHistoryComponent;

  beforeEach(() => {
    betHistoryMainService = {
      getHistoryByBetGroupId: jasmine.createSpy('getHistoryByBetGroupId').and.returnValue(of({ bets: [] }))
    };
    cashOutSectionService = {
      createDataForRegularBets: jasmine.createSpy('createDataForRegularBets')
    };
    timeService = {
      formatByPattern: jasmine.createSpy('formatByPattern'),
      getLocalDateFromString: jasmine.createSpy('getLocalDateFromString')
    };
    localeService = {
      getString: jasmine.createSpy('getString')
    };
    dialogService = {
      openDialog: jasmine.createSpy('openDialog')
    };
    componentFactoryResolver = {
      resolveComponentFactory: jasmine.createSpy('resolveComponentFactory')
    };
    deviceService = {

    };

    component = new EditMyAccaHistoryComponent(
      betHistoryMainService,
      cashOutSectionService,
      timeService,
      localeService,
      dialogService,
      componentFactoryResolver,
      deviceService
    );
    component.bet = { eventSource: {} } as any;
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(localeService.getString).toHaveBeenCalledWith('ema.history.accaHistory');
  });

  it('onShowHistory', () => {
    component.showDialog = jasmine.createSpy();

    deviceService.isMobile = true;
    component.onShowHistory();

    deviceService.isMobile = false;
    component.onShowHistory();

    expect(component.showDialog).toHaveBeenCalledTimes(1);
  });

  it('onDrawerShown', () => {
    component['loadHistory'] = jasmine.createSpy();
    component.onDrawerShown();
    expect(component['loadHistory']).toHaveBeenCalledTimes(1);
  });

  it('showDialog', () => {
    dialogService.openDialog.and.callFake((p1, p2, p3, params) => {
      params.open({});
    });
    component['loadHistory'] = jasmine.createSpy();

    component.showDialog();

    expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledTimes(1);
    expect(dialogService.openDialog).toHaveBeenCalledTimes(1);
    expect(component['loadHistory']).toHaveBeenCalledTimes(1);
  });

  it('loadHistory', fakeAsync(() => {
    component['getCashoutValueMsg'] = jasmine.createSpy();
    cashOutSectionService.createDataForRegularBets.and.returnValue({
      '1': { },
      '2': {
        winnings: [{ value: '0.1' }]
      }
    });

    component.bets = [];
    component['loadHistory']();
    tick();

    component.bets = null;
    component.dialog = null;
    component['loadHistory']();
    tick();

    component.bets = null;
    component.dialog = {} as any;
    component['loadHistory']();
    tick();

    expect(betHistoryMainService.getHistoryByBetGroupId).toHaveBeenCalledTimes(2);
    expect(cashOutSectionService.createDataForRegularBets).toHaveBeenCalledTimes(2);
    expect(timeService.formatByPattern).toHaveBeenCalledTimes(4);
    expect(timeService.getLocalDateFromString).toHaveBeenCalledTimes(4);
    expect(localeService.getString).toHaveBeenCalledTimes(4);
  }));

  describe('loadHistory', () => {
    it('should expand history bet if edited once', () => {
      cashOutSectionService.createDataForRegularBets.and.returnValue({ '1': { } });
      component['loadHistory']();
      expect(component.bets[0].eventSource.accaHistory.isExpanded).toBeTruthy();
    });

    it('should not expand history bet if edited more than once)', fakeAsync(() => {
      cashOutSectionService.createDataForRegularBets.and.returnValue({ '1': { }, '21': { } });
      component['loadHistory']();
      expect(component.bets[0].eventSource.accaHistory.isExpanded).toBeFalsy();
    }));
  });
});
