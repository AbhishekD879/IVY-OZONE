import { fakeAsync,tick } from '@angular/core/testing';
import { LinesummaryComponent } from './linesummary.component';
import { ILotto, ILottoDraw, ILottoLineSummary, ILottoPrice } from '../../models/lotto.model';
import { ILottoNumber } from '../../models/lotto-numbers.model';
import { of, throwError } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
 
describe('LinesummaryComponent', () => {
  let component: LinesummaryComponent,
   route,
   router,
   lottoService,
   storage,
   filterService,
   device,
   command,
   infoDialogService,
   user,
   fracToDecService,
   pubSubService,
   componentFactoryResolver,
   dialogService,
   segmentDataUpdateService,
   locale,
   changeDetectorRef,
   infoDialog,
   windowRef,
   timeService
 
  beforeEach(fakeAsync(() => {
    route = {
      params: of([])
    };
    router={
      navigate: jasmine.createSpy('navigate'),
      url: 'test_url',
    }
    lottoService ={
      getLotteryData : (key: string) => of({
        uri: 'http://test.com'
      }),
    
      getShutAtTime : (key: ILotto) => '',

      getLottoDialog: jasmine.createSpy('getLottoDialog').and.returnValue({singleData: 'lotto',infoMessage : 'test', nextLink :'WWW.abc.com', maxPayOut:1000})
    };
    storage = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set'),
      remove: jasmine.createSpy('remove'),
    }
    const currentDate = new Date();
    currentDate.setDate(currentDate.getDate() + 1);
    const currentDate1 = new Date();
    currentDate1.setDate(currentDate1.getDate() + 2);
    
    infoDialog = {
      openConnectionLostPopup: jasmine.createSpy()
    };

    filterService = {

      orderBy: (key1: any, key2: any) => [
        {
          checked: false,
          shutAtTime: currentDate.toDateString(),
          drawAtTime: currentDate.toDateString(),
        } as ILottoDraw,
        {
          checked: false,
          shutAtTime: currentDate.toDateString(),
          drawAtTime: currentDate.toDateString(),
        } as ILottoDraw,
        {
          checked: false,
          shutAtTime: currentDate1.toDateString(),
          drawAtTime: currentDate1.toDateString(),
        } as ILottoDraw
      ]
    };
    device= {
      isOnline :() => true
    };
    
    command={};
    
    infoDialogService= {
      openConnectionLostPopup : () => { }
    };
    
    user = {
      oddsFormat : 'frac'
    };

    changeDetectorRef = {
      detectChanges: () => {}
    }
    
    fracToDecService = {
      getDecimal: (key1: number, key2: number) => []
    };
    
    pubSubService = {
      API : {
        ADD_TO_BETSLIP_BY_SELECTION: "Beslipselection",
        
      },
       publish  : (key: string, value: any) => {},
       subscribe: (key, name, callback) => callback(),
     };
    
    componentFactoryResolver= {
      resolveComponentFactory : jasmine.createSpy()
    } ;
    
    dialogService={
      selectedBackup:1,
      API : {
        lottoNumberSelector: ''
      },
      openDialog :(...args) => {
        const obj = args[3];
        obj.selectNumbers(1,0);
        obj.luckyDip(1);
        obj.resetNumbers();
        obj.doneSelected();
        obj.onBeforeClose();
      }
    };
    
    windowRef = {
      document: {
        addEventListener: () => { },

        body: {
          scrollTop: 0
        },

        documentElement: {
          scrollTop: 1
        },
      }

    };

    locale = {
      getString: jasmine.createSpy().and.returnValue('Ladbrokes')
    };

    segmentDataUpdateService= {
      headerTime : {
        days: 12,
        hours: 20,
        minutes: 20,
      },
    
      changes : {
        next: jasmine.createSpy()
      }
    };
    createComp();
  }));

  function createComp() {
    component = new LinesummaryComponent(
      route,
      router,
      lottoService,
      storage,
      filterService,
      device,
      command,
      infoDialogService,
      user,
      fracToDecService,
      pubSubService,
      componentFactoryResolver,
      dialogService,
      segmentDataUpdateService,
      locale,
      changeDetectorRef,
      windowRef,
      timeService
    )
  }

  it('should create', () => {
    expect(component).toBeDefined();
  });

  it('should call nginit() method', fakeAsync(() => {
      spyOn(component,'init');
      component.linesSummary= [ { numbersData:[] , isBonusBall: false, isFavourite: false }]
      component.orderedDraws = [{checked : false}as ILottoDraw]
      component.ngOnInit();    
      tick();
      expect(component.lotteryData).toEqual({
        uri: 'http://test.com'
      } as ILotto)
  }));

  it('should call nginit() method with null', fakeAsync(() => {
    environment.brand = 'ladbrokes';
    spyOn(component,'init');
    spyOn(component['lottoService'],'getLotteryData').and.returnValue(of(null));
    component.orderedDraws = [{checked : false}as ILottoDraw];
    component.linesSummary= [ { numbersData:[] , isBonusBall: false, isFavourite: false }];
    component.ngOnInit();
    tick();
    expect(component.lotteryData).toBeUndefined();
    expect(component['locale'].getString).toHaveBeenCalled();
}));

  it('should call nginit() method with error', fakeAsync(() => {
    environment.brand = 'ladbrokes';
    spyOn(component,'init');
    spyOn(component['lottoService'],'getLotteryData').and.returnValue(throwError(() => "error"));
    component.orderedDraws = [{checked : false}as ILottoDraw];
    component.linesSummary= [ { numbersData:[] , isBonusBall: false, isFavourite: false }]
    component.ngOnInit();
    tick();
    expect(component.lotteryData).toBeUndefined();
    expect(component['locale'].getString).toHaveBeenCalled();
  }));

  describe('drawsShow', () => {
    it('drawsShow', fakeAsync(() => {
      component.currentLotto = { name: '49s' } as any;
      filterService.orderBy = jasmine.createSpy().and.returnValue([{ id: 1, shutAtTime: '10-10-2030' }]);
      createComp();
      component.currentLottery = <any>{
        draw: [{}, {}, {}],
        limits: 3
      };

      component.drawsShow(7);
      expect(component.limitValue).toBe(3);
      expect(filterService.orderBy).toHaveBeenCalledWith(component.currentLottery.draw, ['drawAtTime', 'description']);
    }));
  });

  it('it should call isWeeksSelected()',()=>{
     component['weeks'] = [
      { value: 1, selected: false },
      { value: 2, selected: true },
      { value: 3, selected: false },
      { value: 4, selected: false }];
    component.isWeeksSelected()
    expect(component.weeks[1].selected).toBeTruthy()
  })

  it('should call setHeaderData() method', fakeAsync(() => {
    component.singleData ={ label : 'test', maxPayOut:1000} as any;
    component.setHeaderData();
    expect(component.days).toEqual(12);
    expect(component.hours ).toEqual(20);
    expect(component.minutes ).toEqual(20);
    expect(component.singleData.label).toEqual('test');
   }));
   it('should call setHeaderData() method', fakeAsync(() => {
   component['segmentDataUpdateService'].headerTime = undefined;
   component.setHeaderData();
   expect(segmentDataUpdateService.headerTime).toBeUndefined();

   }));
  
 
  it('should call init() method with lottery data', fakeAsync(() => {
    component.lotteryData= { 
    shutAtTime: Date.now().toString(), normal: { name: 'test', lotteryPrice: [ {numberCorrect: '123'} as ILottoPrice], maxNumber: 100, draw: []} as any  ,  boosterBall: { name: 'test', lotteryPrice: [ {numberCorrect: '123'} as ILottoPrice], maxNumber: 100, draw: []} as unknown, maxNumber: "20" }  as ILotto;
    component.orderedDraws = [{ checked: true } as ILottoDraw];
    const spy = spyOn(component, 'setHeaderData');
    component.init();
    component['setHeaderData'] = jasmine.createSpy();
    expect(spy).toHaveBeenCalled();
  }));

  it('should call init() method with lottery data', fakeAsync(() => {
    component.lotteryData= { shutAtTime: Date.now().toString(),  boosterBall: { name: 'test', lotteryPrice: [ {numberCorrect: '123'} as ILottoPrice], maxNumber: 100, draw: []} as unknown, maxNumber: "20" }  as ILotto;
    component.orderedDraws = [{ checked: true } as ILottoDraw];
    const spy = spyOn(component, 'setHeaderData');
    expect(component.orderedDraws[0].checked).toBeTruthy();
   }));

  it('should call changeFavourite()',()=>{
    component.linesSummary = [{} as ILottoLineSummary , {} as ILottoLineSummary];
    component.changeFavourite(1,{ currentTarget: {checked:true}});
    expect(component.linesSummary[1].isFavourite).toBeTruthy();

  });

  it('should call createLine() method ', () => {
    component['linesSummary'] = [{ numbersData: {}, isBonusBall: false, isFavourite: false } as any];
    component['linesSummary'].length = 0;
    component.createLine();
    expect(component.maxLineWrapper).toEqual(undefined);
  });

  it('should call createLine() method linesummary length <= 19 ', () => {
    component.maxLineWrapper = true ;
    component['linesSummary'] = [];
    component['linesSummary'].length = 21;
    component.createLine();
    expect(component.maxLineWrapper).toBeTruthy();
  });

  it('should call resetSelected() method ', () => {
    component.resetSelected(10);
    expect(component.selected).toEqual(10)
  });

  it('openLottoInfoDialog: no internet', () => {
  
    component['device'].isOnline = jasmine.createSpy().and.returnValue(false);
    component.openLottoInfoDialog();
    expect(infoDialog.openConnectionLostPopup).toHaveBeenCalledTimes(0);
  });

  it('should return openInfoDialog', () => {
    component['device'].isIos= true;
    const spy = spyOn(component['dialogService'], 'openDialog');
    component['device'].isOnline = jasmine.createSpy().and.returnValue(true);
    const selectNumbersSpy = spyOn(component, 'selectNumbers');
    component.singleData ={singleData: 'lotto',infoMessage : 'test', nextLink :'WWW.abc.com', maxPayOut:1000} as any;
    component.openLottoInfoDialog();
    expect(infoDialog.openConnectionLostPopup).not.toHaveBeenCalled();
    expect(dialogService.openDialog).toHaveBeenCalled();
    expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalled();
  });

  it('should call doneSelectedCreateNewLine() method ', () => {
    component['selected'] = 1;
    component.currentLottery = { maxNumber : "10" } as ILotto;
    const spy1 = spyOn(component, 'createLine');
    component.doneSelectedCreateNewLine();
    expect(spy1).toHaveBeenCalled();
  });
  it('doneSelected', () => {
    component.numbersData = <any>[{}, { selected: true }];
    component.currentLotto = { maxNumber : "10" } as ILotto;
    component['setSelectedBallNumbers'] = jasmine.createSpy();
    component.linesSummary = [{} as ILottoLineSummary];
    const spy = spyOn(component['changeDetectorRef'], 'detectChanges');
    component.doneSelected(0);
    expect(component['setSelectedBallNumbers']).toHaveBeenCalledWith([]);
    expect(spy).toHaveBeenCalled();
    expect(storage.set).toHaveBeenCalledWith(component.currentLotto.name, []);

   });

  it('should call numDialog() method ', () => {
    component['selected'] = 1;
    component.currentLottery = { maxNumber : "10" } as ILotto;
    const spy1 = spyOn(component, 'openNumberDailog');
    component.numDialog();
    expect(spy1).toHaveBeenCalledWith(0);
  });

  it('should call luckyDip() method ', () => {
    component['selected'] = 1;
    component.currentLottery = { maxNumber : "10" } as ILotto;
    const spy1 = spyOn(component, 'disabledBalls');
    component.luckyDip(10);
    expect(spy1).toHaveBeenCalled();
  });

  it('should call luckyDip() method with id', () => {
    component['selected'] = 1;
    component.currentLottery = { maxNumber : "10" } as ILotto;
    component['numberData'] = [
      {
        value: 1,
        selected: true
      } as ILottoNumber
    ]
    const spy1 = spyOn(component, 'disabledBalls');
    component.luckyDip(10, 1);
    expect(spy1).toHaveBeenCalled();
  });

  it('should call luckyDip() method with id should return undefined', () => {
    component['selected'] = 5;
    component.currentLottery = { maxNumber : "10" } as ILotto;
    const spy1 = spyOn(component, 'disabledBalls');
    component.luckyDip(10, 1);
    expect(spy1).toHaveBeenCalled();
  });

  it('should call editLine() method ', () => {
    component.linesSummary = [{} as ILottoLineSummary , { numbersData: []} as ILottoLineSummary];
    component['selected'] = 1;
    const spy = spyOn(component, 'setBallNumbers');
    const spy1 = spyOn(component, 'openNumberDailog');
    
    component.editLine(1);
    expect(spy).toHaveBeenCalled();
    expect(spy1).toHaveBeenCalledWith(0, 1);
  });
  
    it('should call openNumberDailog() method with selectNumbers', () => {
      const selectNumbersSpy = spyOn(component, 'selectNumbers');
      component.currentLottery = { name: 'test', maxPicks: 20 } as ILotto;
      dialogService.openDialog = (...args) => {
        const obj = args[3];
        obj.selectNumbers(0);
      }
      component.linesSummary = [{} as ILottoLineSummary , { numbersData: [{value : 1}]} as ILottoLineSummary];
      component.openNumberDailog(0, 1);
      expect(selectNumbersSpy).toHaveBeenCalled();
    });

    it('should call openNumberDailog() method with luckyDip', () => {
      const luckyDipSpy = spyOn(component, 'luckyDip');
      component.currentLottery = { name: 'test', maxPicks: 20 } as ILotto;
      dialogService.openDialog = (...args) => {
        const obj = args[3];
        obj.luckyDip(0);
      }
      component.linesSummary = [{} as ILottoLineSummary , { numbersData: []} as ILottoLineSummary];
      component.openNumberDailog(0, 1);
      expect(luckyDipSpy).toHaveBeenCalled();
    });

    it('should call openNumberDailog() method with resetnumber', () => {
      const resetNumbersSpy = spyOn(component, 'resetNumbers');
      component.currentLottery = { name: 'test', maxPicks: 20 } as ILotto;
      dialogService.openDialog = (...args) => {
        const obj = args[3];
        obj.resetNumbers();
      }
      component.linesSummary = [{} as ILottoLineSummary , { numbersData: []} as ILottoLineSummary];
      component.openNumberDailog(0, 1);
      expect(resetNumbersSpy).toHaveBeenCalled();
    });

    it('should call openNumberDailog() method with done sleected', () => {
      const doneSelectedSpy = spyOn(component, 'doneSelected');
      component.currentLottery = { name: 'test', maxPicks: 20 } as ILotto;
      dialogService.openDialog = (...args) => {
        const obj = args[3];
        obj.doneSelected();
      }
      component.linesSummary = [{} as ILottoLineSummary , { numbersData: []} as ILottoLineSummary];
      component.openNumberDailog(0, 1);
      expect(doneSelectedSpy).toHaveBeenCalled();
    });

    it('should call openNumberDailog() method with done sleected with id undefined', () => {
      const doneSelectedSpy = spyOn(component, 'doneSelectedCreateNewLine');
      component.currentLottery = { name: 'test', maxPicks: 20 } as ILotto;
      dialogService.openDialog = (...args) => {
        const obj = args[3];
        obj.doneSelected();
      }
      component.linesSummary = [{} as ILottoLineSummary , { numbersData: []} as ILottoLineSummary];
      component.openNumberDailog(0);
      expect(doneSelectedSpy).toHaveBeenCalled();
    });
  
    it('should call openNumberDailog() method with id Undefined', () => {
      const resetSelectedSpy = spyOn(component, 'resetSelected'); 
      component.currentLottery = { name: 'test', maxPicks: 20 } as ILotto;
      component['isDone'] = false;
      dialogService.openDialog = (...args) => {
        const obj = args[3];
        obj.onBeforeClose();
      }
      component.linesSummary = [{} as ILottoLineSummary , { numbersData: [{value : 1}]} as ILottoLineSummary];
      component.openNumberDailog(0, undefined);
      expect(resetSelectedSpy).toHaveBeenCalled();
    });

    it('should call openNumberDailog() method with id', () => {
        const resetSelectedSpy = spyOn(component, 'resetSelected');
        component.numberDataList = [[{ selected: true , value : 1}],[{selected: false , value : 2}]as any]
        component.currentLottery = { name: 'test', maxPicks: 20 } as ILotto;
         component['isDone'] = false;
        dialogService.openDialog = (...args) => {
          const obj = args[3];
          obj.onBeforeClose();
        }
        component.linesSummary = [{ numbersData: [{value : 1}]} as ILottoLineSummary];
        component.openNumberDailog(0, 0);
        expect(resetSelectedSpy).toHaveBeenCalled();
       });
      it('should call openNumberDailog() method with id', () => {
        const resetSelectedSpy = spyOn(component, 'resetSelected');
        component.numberDataList = [[{ selected: true , value : 1}],[{selected: false , value : 2}]as any]
        component.currentLottery = { name: 'test', maxPicks: 20 } as ILotto;
        component['isDone'] = false;
        dialogService.openDialog = (...args) => {
          const obj = args[3];
          obj.onBeforeClose();
        }
        component.linesSummary = [{ numbersData: [{value : 10}]} as ILottoLineSummary];
        component.openNumberDailog(0, 0);
        expect(resetSelectedSpy).toHaveBeenCalled();
       });

      
  it('should call openNumberDailog() method with id', () => {
    const spy = spyOn(component['dialogService'], 'openDialog');
    component.currentLottery = { name: 'test', maxPicks: 20 } as ILotto;
    component['numberDataList'] = [[{ value: 1, selected: true}]];
    component.linesSummary = [{} as ILottoLineSummary , { numbersData: []} as ILottoLineSummary];

    component.openNumberDailog(0, 1);
    expect(spy).toHaveBeenCalled();

  });

  it('should call doneSelected() method ', () => {
    component['numberData'] = [
      {
        selected: true
      } as ILottoNumber
    ]
    component.lotteryData = { maxNumber : "10" } as ILotto;
    component.currentLotto = { maxNumber : "10" } as ILotto;
    component.currentLottery = { name: 'test', maxPicks: 20 } as ILotto;
    component.linesSummary = [{} as ILottoLineSummary];
    component.doneSelected(0);
   });

  it('should call selectNumbers() method ', () => {
    component['numberData'] = [
      {
        selected: true
      } as ILottoNumber
    ]
    const spy = spyOn(component, 'disabledBalls');
    component.selectNumbers({ index: 0}, 0);
    expect(spy).toHaveBeenCalled();
  });

  it('should call selectNumbers() method with equal max picks', () => {
    component['numberData'] = [
      {
        selected: false
      } as ILottoNumber
    ]
    const spy = spyOn(component, 'disabledBalls');
    component.selected = 20
    component.currentLottery = { name: 'test', maxPicks: 20 } as ILotto;
    component.selectNumbers({ index: 0}, 0);
    expect(spy).not.toHaveBeenCalled();
  });

  it('should call selectNumbers() method with less than max picks', () => {
    component['numberData'] = [
      {
        selected: false
      } as ILottoNumber
    ]
    const spy = spyOn(component, 'disabledBalls');
    component.selected = 10
    component.currentLottery = { name: 'test', maxPicks: 20 } as ILotto;
    component.selectNumbers({ index: 0}, 0);
    expect(spy).toHaveBeenCalled();
  });


  it('should call resetNumbers() method with id undefined ', () => {
    component.currentLottery = { name: 'test' } as ILotto;
    component.currentLotto = { maxNumber : "10" } as ILotto;
    spyOn(component, 'setBallNumbers');

    component.resetNumbers(undefined);

    expect(component.ballSelected).toEqual([]);
    expect(component.selected).toBeFalsy();
    expect(storage.remove).toHaveBeenCalledWith(component.currentLotto.name);
    expect(component.setBallNumbers).toHaveBeenCalled();
     expect(segmentDataUpdateService.changes.next).toHaveBeenCalledWith({
      numbersSelected: component.numbersSelected,
      numbersData: component.numbersData,
      selected: component.selected
    });
  });

  it("should call resetNumbers() method ", () => {
    component.currentLottery = { maxPicks: 5} as ILotto;
    component.currentLotto = { maxNumber: "5" } as ILotto;
    component.selected = 5;
    component.numberDataList = [
      [{ value: 1, selected: true, disabled: true }],
    ] as any;
    component.resetNumbers(0);

    expect(segmentDataUpdateService.changes.next).toHaveBeenCalledWith({
      numbersSelected: component.numbersSelected,
      numbersData: component.numbersData,
      selected: component.selected,
    });
  });

  it('should call selectDraw() method', () => {
    const spy = spyOn(component, 'updateDraws');
    component.selectDraw({} as ILottoDraw);
    expect(spy).toHaveBeenCalled();
  });

  it('should call selectDraw() method with checked true', () => {
    const spy = spyOn(component, 'updateDraws');
    component.selectDraw({ checked: true } as ILottoDraw);
    expect(spy).toHaveBeenCalled();
  });

  it('should call removeLine() method with line summary', () => {
    component.linesSummary = [{} as ILottoLineSummary];
    component.removeLine(0);
    expect(component.maxLineWrapper).toEqual(false);
  });


  it('should call removeLine() method with out line summary', () => {
     component.linesSummary=[];
    component.linesSummary.length = 90;
    component.removeLine(0);
    expect(component.maxLineWrapper).toEqual(true);
  });


  it('should call selectWeek() method', () => {
    component['weeks'] = [
      { value: 1, selected: false },
      { value: 2, selected: true },
      { value: 3, selected: false },
      { value: 4, selected: false }];
    const date = component.selectWeek(0);
    expect(component['weeks'][0]['selected']).toEqual(true);
  });

  it('should call addToBetslip() method with values', fakeAsync(() => {
    component.lotteryPrice = [
      {
        numberPicks: "1",
        numberCorrect: "1",
        priceDen:1,
        priceNum: 1,
      } as ILottoPrice
    ];
    component.linesSummary = [{
      numbersData: [{
        value: 1,
        selected: false,
      }, {
        value: 2,
        selected: true,
      }]
    } as ILottoLineSummary];
    component['weeks'] = [
      { value: 1, selected: false },
      { value: 2, selected: true },
      { value: 3, selected: false },
      { value: 4, selected: false }];
    component.currentLotto = { maxPicks : 0, normal: { name: 'test'} } as ILotto;
    component.boosterBall = undefined;
    component.currentLottery = { } as ILotto;
    component.draws =[{"id":"53346","drawAtTime":"2023-04-22T20:00:00Z","checked":true},{}as any]
    const list ={ draws : [{"id":"53346","drawAtTime":"2023-04-22T20:00:00Z","checked":true}],"drawAtTime":"2023-04-22T20:00:00Z","checked":true}
    spyOn(component, 'getBetObject').and.returnValue(list);
    const spy = spyOn(component, 'scrollToTop');
    const spy1 = spyOn(component, 'drawsFromSelectedWeeks').and.returnValue(list.draws as any);
    component.addToBetslip();
    tick();
    expect(spy).toHaveBeenCalled();
    expect(spy1).toHaveBeenCalled();

  }));
  it('should call addToBetslip() method with values', fakeAsync(() => {
    component.lotteryPrice = [
      {
        numberPicks: "1",
        numberCorrect: "1",
        priceDen:1,
        priceNum: 1,
      } as ILottoPrice
    ];
    component.linesSummary = [{
      numbersData: [{
        value: 1,
        selected: false,
      }, {
        value: 2,
        selected: true,
      }]
    } as ILottoLineSummary];
    component['weeks'] = [
      { value: 1, selected: false },
      { value: 2, selected: true },
      { value: 3, selected: false },
      { value: 4, selected: false }];
    component.currentLotto = { maxPicks : 0, normal: { name: 'test'} } as ILotto;
    component.boosterBall = undefined;
    component.currentLottery = { } as ILotto;
    component.draws =[{"id":"53346","drawAtTime":"2023-04-22T20:00:00Z","checked":true},{}as any]
    const list ={ draws : [{"id":"53346","drawAtTime":"2023-04-22T20:00:00Z","checked":true}],"drawAtTime":"2023-04-22T20:00:00Z","checked":true}
    spyOn(component, 'getBetObject').and.returnValue(list);
    const spy1 = spyOn(component, 'drawsFromSelectedWeeks').and.returnValue(list.draws as any);
    component['device'].isOnline = jasmine.createSpy().and.returnValue(false);
    component.addToBetslip();
    tick();
    expect(spy1).toHaveBeenCalled();
    expect(infoDialog.openConnectionLostPopup).toHaveBeenCalledTimes(0);

  }));
  it('should call addToBetslip() method with values', fakeAsync(() => {
    component.lotteryPrice = [
      {
        numberPicks: "1",
        numberCorrect: "1",
        priceDen:1,
        priceNum: 1,
      } as ILottoPrice
    ];
    component.linesSummary = [{
      numbersData: [{
        value: 1,
        selected: false,
      }, {
        value: 2,
        selected: true,
      }]
    } as ILottoLineSummary];
    component['weeks'] = [
      { value: 1, selected: false },
      { value: 2, selected: true },
      { value: 3, selected: false },
      { value: 4, selected: false }];
    component.currentLotto = { maxPicks : 0, normal: { name: 'test'} } as ILotto;
    component.boosterBall = undefined;
    component.currentLottery = { } as ILotto;
    component.draws =[{"id":"53346","drawAtTime":"2023-04-22T20:00:00Z","checked":true},{}as any]
    const list ={ draws : {undefined}};
    spyOn(component, 'getBetObject').and.returnValue(list);
    const spy1 = spyOn(component, 'drawsFromSelectedWeeks').and.returnValue(list.draws as any);
    component['device'].isOnline = jasmine.createSpy().and.returnValue(false);
    component.addToBetslip();
    tick();
    expect(spy1).toHaveBeenCalled();
    expect(infoDialog.openConnectionLostPopup).toHaveBeenCalledTimes(0);

  }))


   it ('it should call scrollToTop()', ()=>{
    component.scrollToTop();
    expect(windowRef.document.body.scrollTop).toEqual(0);
    expect(windowRef.document.documentElement.scrollTop).toBe(0);
   });

  it('should call getBetObject() method with booster data', () => {
    
    component.singleData ={ label : 'test', maxPayOut:1000} as any;
    const boosterball= true; 
    const drawData = {
      maxPicks: 0,
      description: "49's Lottery Draw",
      boosterBall: { sort: '49s', lotteryPrice: [{ numberCorrect: '1234' }] },
      normal: { sort: '49s', lotteryPrice: [{ numberCorrect: '1234' }] }
    } as any;
    component.weeks = [
      { value: 1, selected: false },
      { value: 2, selected: true },
      { value: 3, selected: false },
      { value: 4, selected: false }];

    component.lotteryPrice = [
      {
        numberPicks: "1",
        numberCorrect: "1",
        priceDen:1,
        priceNum: 1,
      } as ILottoPrice
    ];
    component.linesSummary = [{
      numbersData: [{
        value: 1,
        selected: false,
      }, {
        value: 2,
        selected: true,
      }]
    } as ILottoLineSummary];
    spyOn(component,'replaceDrawWithBoosterDraw').and.returnValue(drawData as any);
    component.currentLotto = drawData;
    const draw = drawData;
    component.getBetObject(0, draw , boosterball);
    component.draws=[];
    expect(component.weeks[0].selected).toBeFalsy();
    expect(component.weeks[1].selected).toBeTruthy();
    expect(component.weeks[2].selected).toBeFalsy();
  });

  it('should call getBetObject() method with normal data', () => {
    
    component.singleData ={ label : 'test', maxPayOut:1000} as any;
    const boosterball= false; 
    const drawData = {
      maxPicks: 0,
      description: "49's Lottery Draw",
      normal: { sort: '49s', lotteryPrice: [{ numberCorrect: '1234' }] }
    } as any;
    component.weeks = [
      { value: 1, selected: false },
      { value: 2, selected: true },
      { value: 3, selected: false },
      { value: 4, selected: false }];

    component.lotteryPrice = [
      {
        numberPicks: "1",
        numberCorrect: "1",
        priceDen:1,
        priceNum: 1,
      } as ILottoPrice
    ];
    component.linesSummary = [{
      numbersData: [{
        value: 1,
        selected: false,
      }, {
        value: 2,
        selected: true,
      }]
    } as ILottoLineSummary];
    spyOn(component,'replaceDrawWithBoosterDraw').and.returnValue(null);
    component.currentLotto = drawData;
    const draw = drawData;
    component.getBetObject(0, draw , boosterball);
    component.draws=[];
    expect(component.weeks[0].selected).toBeFalsy();
    expect(component.weeks[1].selected).toBeTruthy();
    expect(component.weeks[2].selected).toBeFalsy();
  });


  it('it should call drawsFromSelectedWeeks()',()=>{
    const draw ={drawAtTime: "2023-04-19T11:50:00Z", description: 'Irish Lottery'}as any;
    component.currentLottery = {
    draw: [{drawAtTime: "2023-04-19T11:50:00Z", description: 'Irish Lottery'}], 
     
  } as any;
   expect(component.drawsFromSelectedWeeks(1,draw)).toEqual(component.currentLottery.draw as any);
  });

  it(' should called addLinesToBetSlip()',()=>{
    const bets = [{
      "isLotto": true,
      "data": {
      },
      "goToBetslip": true,
      "type": "SGL"
    }]
    const spy = spyOn(component['pubSubService'], 'publish');
    component.addLinesToBetSlip(bets);
    expect(spy).toHaveBeenCalled();
  });

  it('should call getBetObject() method with values', () => {
    
    component.singleData ={ label : 'test', maxPayOut:1000} as any;
    const boosterball= false;
    const draw = { maxPicks : 0, boosterBall: {
      description: "49's Lottery Draw", sort: '49s', lotteryPrice: [{ numberCorrect: '1234' }]}, normal: { sort: '49s', lotteryPrice: [{ numberCorrect: '1234' }]}} as any;
    component.weeks = [
      { value: 1, selected: false },
      { value: 2, selected: true },
      { value: 3, selected: false },
      { value: 4, selected: false }];

    component.lotteryPrice = [
      {
        numberPicks: "1",
        numberCorrect: "1",
        priceDen:1,
        priceNum: 1,
      } as ILottoPrice
    ];
    component.linesSummary = [{
      numbersData: [{
        value: 1,
        selected: false,
      }, {
        value: 2,
        selected: true,
      }]
    } as ILottoLineSummary];
    spyOn(component,'replaceDrawWithBoosterDraw').and.returnValue(draw as any);
    component.currentLotto = draw;
    component.getBetObject(0, draw , boosterball);
    expect(component.weeks[0].selected).toBeFalsy();
    expect(component.weeks[1].selected).toBeTruthy();
    expect(component.weeks[2].selected).toBeFalsy();
  });

  it('it should call replaceDrawWithBoosterDraw() with draw',()=>{
    component.currentLotto = {
        boosterBall: {draw: [{drawAtTime: "2023-04-19T11:50:00Z", description: 'Irish Lottery'}]}, 
        maxNumber: "20"
    } as any;
   const value = component.replaceDrawWithBoosterDraw({drawAtTime :"2023-04-19T11:50:00Z", description: 'Irish Lottery'} as any);
   expect(value.drawAtTime).toEqual("2023-04-19T11:50:00Z");
  });

  it('should call setAccumulatorPrices() method with boosterball values', () => {
    component.currentLotto = {
      shutAtTime: Date.now().toString(),
      normal: { 
        name: 'test',
        lotteryPrice: [{ numberCorrect: '123' } as ILottoPrice],
        maxNumber: 100, draw: [] 
      } as any,
        boosterBall: { name: 'test', lotteryPrice: [{ numberCorrect: '1234' } as ILottoPrice],
        maxNumber: 100, draw: [] 
      }as any, 
        maxNumber: "20"
    } as ILotto;
    component.prices ={
      "id": "29",
      "lotteryId": "3",
      "numberCorrect": "4",
      "numberPicks": "4",
      "priceNum": 800,
      "priceDen": 1
  };
    const isBoosterBall = true;
    component.currentLottery = { maxPicks : 0 } as ILotto;
    component.setAccumulatorPrices(isBoosterBall);
    expect(component.prices.id).toEqual("29");
    expect(component.prices.lotteryId).toEqual("3");
    expect(component.prices.numberCorrect).toEqual("4");
    expect(component.prices.numberPicks).toEqual("4");
    expect(component.prices.priceNum).toEqual(800);
    expect(component.prices.priceDen).toEqual(1);
    expect(isBoosterBall).toBeTruthy();
   })

  it('should call setAccumulatorPrices() method with boosterball false statement', () => {
    component.currentLotto = {
      shutAtTime: Date.now().toString(),
      normal: { 
        name: 'test',
        lotteryPrice: [{ numberCorrect: '123' } as ILottoPrice],
        maxNumber: 100, draw: [] 
      } as any,
        boosterBall: { name: 'test', lotteryPrice: [{ numberCorrect: '1234' } as ILottoPrice],
        maxNumber: 100, draw: [] 
      }as any, 
        maxNumber: "20"
    } as ILotto;
    const isBoosterBall = false;
    const value = component.setAccumulatorPrices(isBoosterBall);
    expect(isBoosterBall).toBeFalsy();
    expect(value).toEqual({ prices: [ ] });
  });
  
  it('should call setAccumulatorPrices() method  with lotteryPrice length 0', () => {
    component.currentLotto = {
      shutAtTime: Date.now().toString(),
      normal: { 
        name: 'test',
        lotteryPrice: [ ],
        maxNumber: 100, draw: [] 
      } as any,
        boosterBall: { name: 'test', lotteryPrice: [{ numberCorrect: '1234' } as ILottoPrice],
        maxNumber: 100, draw: [] 
      }as any, 
        maxNumber: "20"
    } as ILotto;
    const isBoosterBall = false;
    const value = component.setAccumulatorPrices(isBoosterBall);
      
  });

  it('should call setBallNumbers() method', () => {
    component.linesSummary = [{
      numbersData: [{
        value: 1,
        selected: 1,
      }, {
        value: 2,
        selected: true,
      }]
    } as ILottoLineSummary];
    component.currentLottery = {maxPicks : 1, maxNumber: '100' } as ILotto;
    component.lotteryData = { name: 'test' } as ILotto;
    component.currentLotto={name:'test'}as ILotto
    storage.get.and.returnValue([{} as ILottoNumber]);

    component.setBallNumbers(0);
    expect(component.ballSelected.length).toEqual(1);
    expect(component.selected).toEqual(0);
  })

  it('should call closeMaxLinesWrapper() method', () => {
    component.closeMaxLinesWrapper();
    expect(component.maxLineWrapper).toBeFalse();
  });

  it('should call selectAll() method method with checked true and return status as true', () => {
    component.dateWiseDraws ={
      "11/12/2022": {
        draws : [{checked: true } as any]  
      }
    };
    component.selectAll;
    expect(component.selectAll).toBeTruthy();
  });

  it('should call handleSelectAll() method with checked false and return status as false', () => {
    component.dateWiseDraws ={
      "11/12/2022": {
        draws : [{checked: false } as any]  
      }
    };
    const spy = spyOn(component, 'updateDraws');
    
    component.handleSelectAll();
    expect(component.selectAll).toBeTruthy();
    expect(spy).toHaveBeenCalled();

  });

  it('it should call getUTCHoursAndMinutes()',()=>{
    const datestr = new Date("11/12/2022");
    component.getUTCHoursAndMinutes(datestr);
    spyOn(component,'prependZero');
  });
  
  it('it should call prependZero()',()=>{
    const val = ["11/12/2022","11/12/2022","11/12/2022"];
    component.prependZero(val);
    
  });

  it('it should call prependZero()',()=>{
    const val = [];
    component.prependZero(val);
    expect(val).toEqual([]);
  });

  it('should convert text to capitalized text', () => {
    const textString = "irish lotto 6 Ball";
    expect(component.capitalizeText(textString)).toEqual("Irish Lotto 6 Ball");
  });

  it('should convert text to capitalized text with prepend special characters', () => {
    const textString = "irish Lotto 6 ball (main)";
    expect(component.capitalizeText(textString)).toEqual("Irish Lotto 6 Ball (Main)");
  });

  it('should convert text to capitalized text with prepend special characters', () => {
    const textString = "49's 6 ball";
    expect(component.capitalizeText(textString)).toEqual("49's 6 Ball");
  });

  it('should return drawData from lineSummaryDrawHandler', () => {
    const lottoObj = {description: 'irish lotto'} as any;
    expect(component.lineSummaryDrawHandler(null, lottoObj) as any).toEqual({ description: 'Irish Lotto' });
  })
  
});
