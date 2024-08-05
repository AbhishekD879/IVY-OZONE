import { fakeAsync, tick } from '@angular/core/testing';
import { BetslipAccaInsuranceEditComponent } from './betslip-acca-insurance-edit.component';
import { of, throwError } from 'rxjs';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Component } from '@angular/core';

describe('BetslipAccaInsuranceEditComponent', () => {
  let component: BetslipAccaInsuranceEditComponent;
  let brandService;
  let apiClientService;
  let globalLoaderService;
  let matSnackBar;
  let changeDetectorRef;
  let dialogService;


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

 

  beforeEach(() => {
    dialogService = {
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({ yesCallback, noCallback }) => {
        yesCallback();
        noCallback();
      })
    };

    apiClientService = {
      betslipService: jasmine.createSpy('betslipService').and.returnValue({
        getBetSlip: jasmine.createSpy('getBetSlip').and.returnValue(of({ body: betslipcAccaMock })),
        edit: jasmine.createSpy('edit').and.returnValue(of({ body: betslipcAccaMock }))
      }),
    }

    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    }

    matSnackBar = {
      open: jasmine.createSpy('open')
    }
    changeDetectorRef = {
      detectChanges: () => { }
    }
    component = new BetslipAccaInsuranceEditComponent(
      brandService,
      apiClientService,
      globalLoaderService,
      matSnackBar,
      changeDetectorRef,
      dialogService,
    );
  });

  it("it should call ngOnInit", fakeAsync(() => {
    const spy = spyOn<any>(component, "loadInitialData");
    component.ngOnInit();
    expect(spy).toHaveBeenCalled();
  }));

  it("it should calll loadInitialData", fakeAsync(() => {
    const spy = spyOn<any>(component, "createBetSlipAccaFormGroup");
    const spy1 = spyOn<any>(component, "buildBreadCrumbsData");
    component.informationTextEditor = "test" as any;

    component.informationTextEditor as Component;
    component.informationTextEditor = {
      update: jasmine.createSpy("update"),
    } as any;
    component["loadInitialData"]();
    tick(1);
    expect(spy).toHaveBeenCalled();
    expect(spy1).toHaveBeenCalled();

  }));
  it("it should calll loadInitialData empty data", fakeAsync(() => {
    const spy = spyOn<any>(component, "createBetSlipAccaFormGroup");
    const spy1 = spyOn<any>(component, "buildBreadCrumbsData");
    component.betSlipAcca = { popUpDetails: [{ popUpMessage: null }] } as any

    component.informationTextEditor as Component;
    component.informationTextEditor = {
      update: jasmine.createSpy("update"),
    } as any;
    component["loadInitialData"]();
    tick(1);
    expect(spy).toHaveBeenCalled();
    expect(spy1).toHaveBeenCalled();

  }));
  it('#createFormGroup default', () => {
    component.form = new FormGroup({
      accInsMsgEnabled: new FormControl(component.betSlipAcca.accInsMsgEnabled || false),
      svgId: new FormControl(component.betSlipAcca.svgId || ''),
      bsAddToQualifyMsg: new FormControl(component.betSlipAcca.bsAddToQualifyMsg || '', [Validators.required, Validators.maxLength(67)]),
      avlblInscCountIndi: new FormControl(component.betSlipAcca.avlblInscCountIndi || '', [Validators.required, Validators.maxLength(25)]),
      obAccaCount: new FormControl(component.betSlipAcca.obAccaCount || 0, [Validators.required, Validators.max(10)]),
      bsQualifiedMsg: new FormControl(component.betSlipAcca.bsQualifiedMsg || '', [Validators.required, Validators.maxLength(67)]),
      bsSp: new FormControl(component.betSlipAcca.betslipSp.bsSp || '', [Validators.required, Validators.maxLength(21)]),
      bsspEnabled: new FormControl(component.betSlipAcca.betslipSp.enabled || false),
      bsProgressBar: new FormControl(component.betSlipAcca.betslipSp.progressBar || false),
      bsInfoIcon: new FormControl(component.betSlipAcca.betslipSp.infoIcon || false),
      absp: new FormControl(component.betSlipAcca.accabarSp.absp || '', [Validators.required, Validators.maxLength(21)]),
      abspEnabled: new FormControl(component.betSlipAcca.accabarSp.enabled || false),
      abProgressBar: new FormControl(component.betSlipAcca.accabarSp.progressBar || true),
      brsp: new FormControl(component.betSlipAcca.betreceiptSp.brsp || '', [Validators.required, Validators.maxLength(21)]),
      brspEnabled: new FormControl(component.betSlipAcca.betreceiptSp.enabled || true),
      mbspEnabled: new FormControl(component.betSlipAcca.mybetsSp.enabled || true),
      mbsp: new FormControl(component.betSlipAcca.mybetsSp.mbsp || '', [Validators.required, Validators.maxLength(21)]),
      profitIndi: new FormControl(component.betSlipAcca.profitIndi || '', [Validators.required, Validators.maxLength(67)]),
      profitIndiUrl: new FormControl(component.betSlipAcca.profitIndiUrl || ''),
      popUpTitle: new FormControl(component.betSlipAcca.popUpDetails.popUpTitle || '', [Validators.required, Validators.maxLength(10)]),
      popUpMessage: new FormControl(component.betSlipAcca.popUpDetails.popUpMessage || '', [Validators.required]),
      priCtaLabel: new FormControl(component.betSlipAcca.popUpDetails.priCtaLabel || '', [Validators.required]),
      priCtaUrl: new FormControl(component.betSlipAcca.popUpDetails.priCtaUrl || '',),
      secCtaLabel: new FormControl(component.betSlipAcca.popUpDetails.secCtaLabel || '',),
      secCtaUrl: new FormControl(component.betSlipAcca.popUpDetails.secCtaUrl || ''),
    });
    component.createBetSlipAccaFormGroup();
    expect(component.form).toBeDefined();
  });


  it('#formControls default', () => {
    component.form = new FormGroup({
      accInsMsgEnabled: new FormControl(component.betSlipAcca.accInsMsgEnabled || false),
      svgId: new FormControl(component.betSlipAcca.svgId || ''),
      bsAddToQualifyMsg: new FormControl(component.betSlipAcca.bsAddToQualifyMsg || '', [Validators.required, Validators.maxLength(67)]),
      avlblInscCountIndi: new FormControl(component.betSlipAcca.avlblInscCountIndi || '', [Validators.required, Validators.maxLength(25)]),
      obAccaCount: new FormControl(component.betSlipAcca.obAccaCount || 0, [Validators.required, Validators.max(10)]),
      bsQualifiedMsg: new FormControl(component.betSlipAcca.bsQualifiedMsg || '', [Validators.required, Validators.maxLength(67)]),
      bsSp: new FormControl(component.betSlipAcca.betslipSp.bsSp || '', [Validators.required, Validators.maxLength(21)]),
      bsspEnabled: new FormControl(component.betSlipAcca.betslipSp.enabled || false),
      bsProgressBar: new FormControl(component.betSlipAcca.betslipSp.progressBar || false),
      bsInfoIcon: new FormControl(component.betSlipAcca.betslipSp.infoIcon || false),
      absp: new FormControl(component.betSlipAcca.accabarSp.absp || '', [Validators.required, Validators.maxLength(21)]),
      abspEnabled: new FormControl(component.betSlipAcca.accabarSp.enabled || false),
      abProgressBar: new FormControl(component.betSlipAcca.accabarSp.progressBar || true),
      brsp: new FormControl(component.betSlipAcca.betreceiptSp.brsp || '', [Validators.required, Validators.maxLength(21)]),
      brspEnabled: new FormControl(component.betSlipAcca.betreceiptSp.enabled || true),
      mbspEnabled: new FormControl(component.betSlipAcca.mybetsSp.enabled || true),
      mbsp: new FormControl(component.betSlipAcca.mybetsSp.mbsp || '', [Validators.required, Validators.maxLength(21)]),
      profitIndi: new FormControl(component.betSlipAcca.profitIndi || '', [Validators.required, Validators.maxLength(67)]),
      profitIndiUrl: new FormControl(component.betSlipAcca.profitIndiUrl || ''),
      popUpTitle: new FormControl(component.betSlipAcca.popUpDetails.popUpTitle || '', [Validators.required, Validators.maxLength(10)]),
      popUpMessage: new FormControl(component.betSlipAcca.popUpDetails.popUpMessage || '', [Validators.required]),
      priCtaLabel: new FormControl(component.betSlipAcca.popUpDetails.priCtaLabel || '', [Validators.required]),
      priCtaUrl: new FormControl(component.betSlipAcca.popUpDetails.priCtaUrl || '',),
      secCtaLabel: new FormControl(component.betSlipAcca.popUpDetails.secCtaLabel || '',),
      secCtaUrl: new FormControl(component.betSlipAcca.popUpDetails.secCtaUrl || ''),
    });
    component.formControls;
    expect(component.form).toBeDefined();

  });


  it("it should call updateInfoTxtData", () => {
    component.betSlipAcca = betslipcAccaMock;
    component.form = new FormGroup({
      informationTextDesc: new FormControl("popupMessage" || ""),
    });
    component.updateInfoTxtData("popupMessage");
  });


  it('it should call revertChanges', fakeAsync(() => {
    const spy = spyOn<any>(component, 'loadInitialData')
    component.revertChanges();
    expect(spy).toHaveBeenCalled();
  }));

  it('#actionsHandler call save', () => {
    component.saveChanges = jasmine.createSpy('save');
    component.actionsHandler('save');
    expect(component.saveChanges).toHaveBeenCalled();
  });

  it('#actionsHandler call revert', () => {
    component.revertChanges = jasmine.createSpy('revertChanges');
    component.actionsHandler('revert');
    expect(component.revertChanges).toHaveBeenCalled();
  });

  it('#actionsHandler do nothing', () => {
    component.saveChanges = jasmine.createSpy('save');
    component.revertChanges = jasmine.createSpy('revertChanges');
    component.actionsHandler('test');
    expect(component.saveChanges).not.toHaveBeenCalled();
    expect(component.revertChanges).not.toHaveBeenCalled();
  });

  it('it should call saveChanges()', fakeAsync(() => {
    const spy = spyOn<any>(component, 'submitChanges')
    component.saveChanges();
    expect(spy).toHaveBeenCalled();
  }));

  it("it should call submitChanges()", fakeAsync(() => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy("extendCollection"),
    } as any;
    component.submitChanges('edit');
    tick(1);
   }));

  it("it should calll buildBreadCrumbsData", () => {
    component.breadcrumbsData = [{ label: `Betslip`, url: `/betslip` },
    { label: 'Betslip Acca Insurance', url: `/betslip/betslip-acca-insurance` },];
    component["buildBreadCrumbsData"]();

    expect(component.breadcrumbsData[0].label).toEqual('Betslip')
  });

  describe('uploadSvgHandler', () => {
    it('should handle image uploading', () => {
      component.betSlipAcca = {
        svgId: '1'
      } as any;
      const setErrorsSpy = jasmine.createSpy('setErrors');
      component.form = {
        controls: {
          originalname: {
            setErrors: setErrorsSpy
          }
        }
      } as any;
      component.uploadSvgHandler({file: 'file'});
    })
    it('should throw error', () => {
      component.betSlipAcca = {
        svgId: '1'
      } as any;
      apiClientService.lottosService().uploadSvg.and.returnValue(throwError({ status: '401' }));
      component.uploadSvgHandler({ file: 'file' });
      expect(globalLoaderService.showLoader).toHaveBeenCalled();
    })
  })

  it("it should calll validationHandler", fakeAsync(() => {
    component.form = new FormGroup({
      bsQualifiedMsg: new FormControl('Qualified message'),
    })
    const result = component["validationHandler"]();
    tick();
    expect(result).toEqual(true)
  }));

});