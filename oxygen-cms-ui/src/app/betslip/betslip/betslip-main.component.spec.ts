import { fakeAsync, tick } from '@angular/core/testing';
import { BetslipMainComponent } from './betslip-main.component';
import { of } from 'rxjs';

let betslipcAccaMock = {
  "brand": "ExampleBrand",
  "accInsMsgEnabled": true,
  "svgId": "exampleSvgId",
  "bsAddToQualifyMsg": "Add to qualify message",
  "bsQualifiedMsg": "Qualified message",
  "bsqInfoIcon": true,
  "avlblInscCountIndi": "5",
  "obAccaCount": 3,
  "betslipSp": {
    "bsSp": "exampleBsSp",
    "enabled": true,
    "progressBar": true,
    "infoIcon": false
  },
  "accabarSp": {
    "absp": "exampleAbsp",
    "enabled": false,
    "progressBar": true
  },
  "betreceiptSp": {
    "brsp": "exampleBrsp",
    "enabled": true
  },
  "mybetsSp": {
    "mbsp": "exampleMbsp",
    "enabled": false
  },
  "profitIndi": "exampleProfitIndi",
  "profitIndiUrl": "http://example.com/profitIndiUrl"
  ,
  "popUpDetails": {
    "popUpTitle": "Example Popup Title",
    "popUpMessage": "Example Popup Message",
    "popUpUrl": "http://example.com/popup"
  }
} as any

describe('BetslipMainComponent', () => {
  let component: BetslipMainComponent;
  let apiClientService;
  let globalLoaderService;
  let dialogService;

  beforeEach(() => {
    apiClientService = {
      betslipService: jasmine.createSpy('betslipService').and.returnValue({
        getBetSlip: jasmine.createSpy('getBetSlip').and.returnValue(of({ body: betslipcAccaMock })),
        edit: jasmine.createSpy('edit').and.returnValue(of({ body: betslipcAccaMock }))
      }),
    }
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };

    component = new BetslipMainComponent(
      apiClientService,
      globalLoaderService,
      dialogService,
    );
    component.betSlipAccaResp = betslipcAccaMock;
  })

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("#ngOnInit", () => {
    const spy = spyOn<any>(component, "loadInitialData");
    component.ngOnInit();
    expect(spy).toHaveBeenCalled();
  });

  it("it should calll loadInitialData with default body data", fakeAsync(() => {
    component.betSlipAccaResp = betslipcAccaMock;
    const spy1 = spyOn<any>(component, "createBetslipTable");

    component["loadInitialData"]();
    tick();
    expect(spy1).toHaveBeenCalled();
  }));

  it("it should calll loadInitialData without body data", fakeAsync(() => {
    const spy1 = spyOn<any>(component, "createBetslipTable");
    component["loadInitialData"]();
    tick();
    expect(spy1).toHaveBeenCalled();
  }));

  it("it should call buildBreadCrumbsData", fakeAsync(() => {
    component["buildBreadCrumbsData"](betslipcAccaMock, "12345" as any);
    tick();
  }));

});