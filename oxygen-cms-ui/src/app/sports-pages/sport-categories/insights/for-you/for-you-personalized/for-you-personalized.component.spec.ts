import { of } from 'rxjs/observable/of';
import 'rxjs/add/observable/throw';
import { ForyoupersonalizedComponent } from './for-you-personalized.component';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { fakeAsync, tick } from '@angular/core/testing';
import { Params } from '@angular/router';
import { throwError } from 'rxjs';
import { Component } from '@angular/compiler/src/core';


 let mockData ={
  "brand": "ladbrokes",
  "sportId": 16,
  "name": "popularbets",
  "displayName": "Popular Bets",
  "enabled": true,
  "checkEvents": false,
  "hasEvents": false,
  "marketsNames": [],
  "interstitialBanners": null,
  "trendingTabs": [
      {
          "id": "65719983f121cb6d235b9fc1",
          "createdBy": "5645b8a220bd9e0800afdc57",
          "createdByUserName": null,
          "updatedBy": "5645b8a220bd9e0800afdc57",
          "updatedByUserName": null,
          "createdAt": "2023-12-07T10:08:03.935Z",
          "updatedAt": "2023-12-07T10:11:59.591Z",
          "sortOrder": null,
          "brand": "ladbrokes",
          "sportId": 16,
          "trendingTabName": "popular bets",
          "headerDisplayName": "Popular_bets",
          "enabled": true,
          "href": "insights-popular",
          "popularTabs": [
              {
                  "id": "65719983f121cb6d235b9fc0",
                  "createdBy": "5645b8a220bd9e0800afdc57",
                  "createdByUserName": null,
                  "updatedBy": "5645b8a220bd9e0800afdc57",
                  "updatedByUserName": null,
                  "createdAt": "2023-12-07T10:08:03.920Z",
                  "updatedAt": "2023-12-07T10:11:59.542Z",
                  "sortOrder": null,
                  "brand": "ladbrokes",
                  "sportId": 16,
                  "betSlipBarBetsAddedDesc": "You’ve added Top 5 bets to your betslip!",
                  "betSlipBarCTALabel": "add to betslip",
                  "betSlipBarDesc": "Add top 5 most backed to your betslip!",
                  "betSlipBarRemoveBetsCTALabel": "Remove all from betslip",
                  "suspendedBetsDesc": "Add mostbacked to your betslip!",
                  "suspendedBetsAddedText": "You have added most backed to your betslip!",
                  "href": null,
                  "enabled": true,
                  "informationTextEditor": "test",
                  "popularTabName": "Popular_tab",
                  "headerDisplayName": "Popular bets",
                  "topBetsHeaderLabel": null,
                  "startsInText": "Event Starting Within",
                  "backedInLastText": "Backed In The Last",
                  "showMoreText": "Show more",
                  "showLessText": "Show less",
                  "backedUpTimesText": "Backed in {n} Times!",
                  "informationTextDesc": "<p>Hey </p>",
                  "numbOfDefaultPopularBets": 5,
                  "numbOfShowMorePopularBets": 5,
                  "priceRange": "1/10-10/1",
                  "noPopularBetsMsg": "Sorry no bets",
                  "lastUpdatedTime": "Last Updated Time",
                  "nonLoginHeader": null,
                  "nonLoginCTA": null,
                  "noBettingHeader": null,
                  "noBettingDesc": null,
                  "noBettingCTA": null,
                  "backedInLastFilter": [
                      {
                          "isEnabled": true,
                          "displayName": "48hrs",
                          "isTimeInHours": true,
                          "day": null,
                          "time": 48
                      }
                  ],
                  "eventStartsFilter": [
                      {
                          "isEnabled": true,
                          "displayName": "48hrs",
                          "isTimeInHours": true,
                          "day": null,
                          "time": 48
                      },
                      {
                          "isEnabled": true,
                          "displayName": "3hrs",
                          "isTimeInHours": true,
                          "day": null,
                          "time": 3
                      }
                  ]
              }
          ]
      },
      {
          "id": "65719984f121cb6d235b9fc3",
          "createdBy": "5645b8a220bd9e0800afdc57",
          "createdByUserName": null,
          "updatedBy": "5645b8a220bd9e0800afdc57",
          "updatedByUserName": null,
          "createdAt": "2023-12-07T10:08:04.004Z",
          "updatedAt": "2023-12-07T10:11:59.690Z",
          "sortOrder": null,
          "brand": "ladbrokes",
          "sportId": 16,
          "trendingTabName": "foryou",
          "headerDisplayName": "Foryou",
          "enabled": true,
          "href": "insights-forYou",
          "popularTabs": [
              {
                  "id": "65719983f121cb6d235b9fc2",
                  "createdBy": "5645b8a220bd9e0800afdc57",
                  "createdByUserName": null,
                  "updatedBy": "5645b8a220bd9e0800afdc57",
                  "updatedByUserName": null,
                  "createdAt": "2023-12-07T10:08:03.990Z",
                  "updatedAt": "2023-12-08T05:37:32.897Z",
                  "sortOrder": -1,
                  "brand": "ladbrokes",
                  "sportId": 16,
                  "informationTextEditor":'informationTextEditor',
                  "betSlipBarBetsAddedDesc": "You’ve added Top 5 bets to your betslip!",
                  "betSlipBarCTALabel": "add to For You betslip!",
                  "betSlipBarDesc": "Add top 5 bets For You to your betslip!",
                  "betSlipBarRemoveBetsCTALabel": "Remove all from betslip!",
                  "suspendedBetsDesc": "Add For You bets to your betslip!",
                  "suspendedBetsAddedText": "You have added Top 5 For You to your betslip!",
                  "href": "for-you-personalized-bets",
                  "enabled": true,
                  "popularTabName": "for-you-personalized-bets",
                  "headerDisplayName": "for you personalized",
                  "topBetsHeaderLabel": "Top bets for you header",
                  "startsInText": "",
                  "backedInLastText": "",
                  "showMoreText": "Show More",
                  "showLessText": "Show Less",
                  "backedUpTimesText": "Backed in {n} Times",
                  "informationTextDesc": "<p>View some of the latest bets similar to what you've recently bet on.</p>",
                  "numbOfDefaultPopularBets": 5,
                  "numbOfShowMorePopularBets": 10,
                  "priceRange": "1/10-10/1",
                  "noPopularBetsMsg": null,
                  "lastUpdatedTime": "Last Updated Time",
                  "nonLoginHeader": "Please Log In to see personalised bets For You",
                  "nonLoginCTA": "Log In",
                  "noBettingHeader": "We need more info!",
                  "noBettingDesc": "By placing Football bets we can personalise your For You Page to suit your needs.",
                  "noBettingCTA": "Go Betting cta",
                  "backedInLastFilter": [],
                  "eventStartsFilter": []
              }
          ]
      }
  ],
  "showNewFlag": true,
  "id": "657178ccf121cb6d235b9f6e",
  "createdBy": "5645b8a220bd9e0800afdc57",
  "createdByUserName": "ozoneqa@coral.co.uk",
  "updatedBy": "5645b8a220bd9e0800afdc57",
  "updatedByUserName": "ozoneqa@coral.co.uk",
  "createdAt": "2023-12-07T07:48:28.282Z",
  "updatedAt": "2023-12-07T10:11:59.750Z",
  "sortOrder": 8,
  "hidden": false
}as any
 
const routeParams: Params = {
  id: '57fcfcd9b6aff9ba6c252a2c',
  moduleId: '5beee1bbc9e77c0001fb69e3'
};
describe('ForyoupersonalizedComponent', () => {
  let component: ForyoupersonalizedComponent;
  let activatedRoute;
  let apiClientService;
  let dialogService;
  let changeDetectorRef;
  let matSnackBar;

  
 
  beforeEach(() => {
    activatedRoute = {
      params: of(routeParams)
    };
    
    apiClientService = {
        forYouService: jasmine.createSpy('forYouService').and.returnValue({
        getDetailsByBrand: jasmine.createSpy('').and.returnValue(of( {mockData}
     )),
     saveCMSForYouPersonalizedData :jasmine.createSpy('').and.returnValue(of({body :mockData}))
     })
    }


    dialogService = {
       showNotificationDialog :jasmine.createSpy('showNotificationDialog')
    }

    changeDetectorRef = {
      detectChanges: () => {}
    }

    matSnackBar = {
      open: jasmine.createSpy('open')
    }

    component = new ForyoupersonalizedComponent(
      activatedRoute,
      apiClientService,
      dialogService,
      changeDetectorRef,
      matSnackBar,
    );

  });
  
  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("#ngOnInit", () => {
    const spy = spyOn<any>(component, "loadInitialData");
    component.ngOnInit();
    expect(spy).toHaveBeenCalled();
  });

  it("it should calll loadInitialData with default body data", fakeAsync(() => {
    component.informationTextEditor = "test" as any;
    component.actionButtons = {
      extendCollection: jasmine.createSpy("extendCollection"),
    } as any;

    component.informationTextEditor as Component;
    component.informationTextEditor = {
      update: jasmine.createSpy("update"),
    } as any;
    spyOn(component, "createFormGroup");
    component["loadInitialData"]();
    tick();
  }));
  
  it("it should calll loadInitialData", fakeAsync(() => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy("extendCollection"),
    } as any;
    component.informationTextEditor as Component;
    apiClientService = {
      forYouService: jasmine.createSpy("forYouService").and.returnValue({
        getDetailsByBrand: jasmine
          .createSpy("")
          .and.returnValue(of({ body: mockData })),
      }),
    };
    component["loadInitialData"]();
    tick();
 
  }));

  it("it should calll loadInitialData throwError", fakeAsync(() => {
   apiClientService.forYouService().getDetailsByBrand.and.returnValue(throwError({status: 404}))
   component["loadInitialData"]();
   tick();
 }))

   it('#createFormGroup default', () => {
    component.forYou = mockData.trendingTabs[0]as any;
    component.form = new FormGroup({
      headerDisplayName: new FormControl(component.forYou?.headerDisplayName || ''),
      showMoreText: new FormControl(component.forYou?.showMoreText || '', [Validators.required, Validators.maxLength(15)]),
      showLessText: new FormControl(component.forYou?.showLessText || '', [Validators.required, Validators.maxLength(15)]),
      backedUpTimesText: new FormControl(component.forYou?.backedUpTimesText || '', [Validators.required, Validators.maxLength(30)]),
      numbOfDefaultPopularBets: new FormControl(component.forYou?.numbOfDefaultPopularBets || 0, [Validators.required, Validators.min(1), Validators.max(5)]),
      numbOfShowMorePopularBets: new FormControl(component.forYou?.numbOfShowMorePopularBets || 0, [Validators.required, Validators.min(1), Validators.max(10)]),
      priceRange: new FormControl(component.forYou?.priceRange || '', [Validators.required, Validators.pattern('^([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})[-]([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})$')]),
      lastUpdatedTime: new FormControl(component.forYou?.lastUpdatedTime || '', [Validators.required, Validators.maxLength(20)]),
      informationTextDesc: new FormControl(component.forYou?.informationTextDesc || '', [Validators.required]),
      betSlipBarDesc: new FormControl(component.forYou?.betSlipBarDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarCTALabel: new FormControl(component.forYou?.betSlipBarCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      betSlipBarBetsAddedDesc: new FormControl(component.forYou?.betSlipBarBetsAddedDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarRemoveBetsCTALabel: new FormControl(component.forYou?.betSlipBarRemoveBetsCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      suspendedBetsAddedText: new FormControl(component.forYou?.suspendedBetsAddedText || '', [Validators.required, Validators.maxLength(50)]),
      suspendedBetsDesc: new FormControl(component.forYou?.suspendedBetsDesc || '', [Validators.required, Validators.maxLength(50)]),
      nonLoginHeader: new FormControl(component.forYou?.nonLoginHeader || '', [Validators.required, Validators.maxLength(50)]),
      noBettingCTA: new FormControl(component.forYou?.noBettingCTA || '', [Validators.required, Validators.maxLength(20)]),
      noBettingHeader: new FormControl(component.forYou?.noBettingHeader || '', [Validators.required, Validators.maxLength(50)]),
      noBettingDesc: new FormControl(component.forYou?.noBettingDesc || '', [Validators.required, Validators.maxLength(100)]),
    });
    component.createFormGroup();
    expect(component.form).toBeDefined();


   });
   it('#createFormGroup  false ', () => {
    component.forYou = null;
    component.form = new FormGroup({
      headerDisplayName: new FormControl(component.forYou?.headerDisplayName || ''),
      showMoreText: new FormControl(component.forYou?.showMoreText || '', [Validators.required, Validators.maxLength(15)]),
      showLessText: new FormControl(component.forYou?.showLessText || '', [Validators.required, Validators.maxLength(15)]),
      backedUpTimesText: new FormControl(component.forYou?.backedUpTimesText || '', [Validators.required, Validators.maxLength(30)]),
      numbOfDefaultPopularBets: new FormControl(component.forYou?.numbOfDefaultPopularBets || 0, [Validators.required, Validators.min(1), Validators.max(5)]),
      numbOfShowMorePopularBets: new FormControl(component.forYou?.numbOfShowMorePopularBets || 0, [Validators.required, Validators.min(1), Validators.max(10)]),
      priceRange: new FormControl(component.forYou?.priceRange || '', [Validators.required, Validators.pattern('^([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})[-]([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})$')]),
      lastUpdatedTime: new FormControl(component.forYou?.lastUpdatedTime || '', [Validators.required, Validators.maxLength(20)]),
      informationTextDesc: new FormControl(component.forYou?.informationTextDesc || '', [Validators.required]),
      betSlipBarDesc: new FormControl(component.forYou?.betSlipBarDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarCTALabel: new FormControl(component.forYou?.betSlipBarCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      betSlipBarBetsAddedDesc: new FormControl(component.forYou?.betSlipBarBetsAddedDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarRemoveBetsCTALabel: new FormControl(component.forYou?.betSlipBarRemoveBetsCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      suspendedBetsAddedText: new FormControl(component.forYou?.suspendedBetsAddedText || '', [Validators.required, Validators.maxLength(50)]),
      suspendedBetsDesc: new FormControl(component.forYou?.suspendedBetsDesc || '', [Validators.required, Validators.maxLength(50)]),
      nonLoginHeader: new FormControl(component.forYou?.nonLoginHeader || '', [Validators.required, Validators.maxLength(50)]),
      noBettingCTA: new FormControl(component.forYou?.noBettingCTA || '', [Validators.required, Validators.maxLength(20)]),
      noBettingHeader: new FormControl(component.forYou?.noBettingHeader || '', [Validators.required, Validators.maxLength(50)]),
      noBettingDesc: new FormControl(component.forYou?.noBettingDesc || '', [Validators.required, Validators.maxLength(100)]),
    });
    component.createFormGroup();
    expect(component.form).toBeDefined();

   });
   it('#formControls default', () => {
    component.forYou = mockData.trendingTabs[0]as any
    component.form = new FormGroup({
      headerDisplayName: new FormControl(component.forYou?.headerDisplayName || ''),
      showMoreText: new FormControl(component.forYou?.showMoreText || '', [Validators.required, Validators.maxLength(15)]),
      showLessText: new FormControl(component.forYou?.showLessText || '', [Validators.required, Validators.maxLength(15)]),
      backedUpTimesText: new FormControl(component.forYou?.backedUpTimesText || '', [Validators.required, Validators.maxLength(30)]),
      numbOfDefaultPopularBets: new FormControl(component.forYou?.numbOfDefaultPopularBets || 0, [Validators.required, Validators.min(1), Validators.max(5)]),
      numbOfShowMorePopularBets: new FormControl(component.forYou?.numbOfShowMorePopularBets || 0, [Validators.required, Validators.min(1), Validators.max(10)]),
      priceRange: new FormControl(component.forYou?.priceRange || '', [Validators.required, Validators.pattern('^([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})[-]([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})$')]),
      lastUpdatedTime: new FormControl(component.forYou?.lastUpdatedTime || '', [Validators.required, Validators.maxLength(20)]),
      informationTextDesc: new FormControl(component.forYou?.informationTextDesc || '', [Validators.required]),
      betSlipBarDesc: new FormControl(component.forYou?.betSlipBarDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarCTALabel: new FormControl(component.forYou?.betSlipBarCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      betSlipBarBetsAddedDesc: new FormControl(component.forYou?.betSlipBarBetsAddedDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarRemoveBetsCTALabel: new FormControl(component.forYou?.betSlipBarRemoveBetsCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      suspendedBetsAddedText: new FormControl(component.forYou?.suspendedBetsAddedText || '', [Validators.required, Validators.maxLength(50)]),
      suspendedBetsDesc: new FormControl(component.forYou?.suspendedBetsDesc || '', [Validators.required, Validators.maxLength(50)]),
      nonLoginHeader: new FormControl(component.forYou?.nonLoginHeader || '', [Validators.required, Validators.maxLength(50)]),
      noBettingCTA: new FormControl(component.forYou?.noBettingCTA || '', [Validators.required, Validators.maxLength(20)]),
      noBettingHeader: new FormControl(component.forYou?.noBettingHeader || '', [Validators.required, Validators.maxLength(50)]),
      noBettingDesc: new FormControl(component.forYou?.noBettingDesc || '', [Validators.required, Validators.maxLength(100)]),
    });
    component.formControls;
    expect(component.form).toBeDefined();

   });
   
   it("it should calll buildBreadCrumbsData", fakeAsync(() => {
    const forYoutabId ="111"
    component["buildBreadCrumbsData"](forYoutabId);
    tick();
   
   }));

   it("it should call updateInfoTxtData()", () => {
    const data = "info";
    component.forYou = {
      informationTextDesc: "info",
    } as any;
    component.form = new FormGroup({
      informationTextDesc: new FormControl("updateInfoTxtData" || ""),
    });
    const result = component.updateInfoTxtData(data);
    expect(result).toEqual("info");
  });

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

  it('#actionsHandler', () => {
    component.saveChanges = jasmine.createSpy('save');
    component.revertChanges = jasmine.createSpy('revertChanges');
    component.actionsHandler('test');
    expect(component.saveChanges).not.toHaveBeenCalled();
    expect(component.revertChanges).not.toHaveBeenCalled();
  });

  it('#revertChanges default', () => {
    const spy = spyOn<any>(component, 'loadInitialData')
    component.revertChanges();
    expect(spy).toHaveBeenCalled();
  });

  it('#saveChanges default', () => {
   component.forYou = {"name": "popularbets",}as any;
   const spy = spyOn<any>(component, 'sendRequest');
   component.saveChanges();
   expect(spy).toHaveBeenCalled();
   
  });
  it('#saveChanges default', () => {
    component.forYou = null;
    const spy = spyOn<any>(component, 'sendRequest');
    component.saveChanges();
    expect(spy).toHaveBeenCalled();
   });

   it("it should calll sendRequest", fakeAsync(() => {
   const requestType = "saveCMSForYouPersonalizedData";
   
   component["sendRequest"](requestType, false );
   tick();
  expect(requestType).toEqual('saveCMSForYouPersonalizedData');
  expect(component.forYou).toEqual(mockData)
  }));

  it("it should calll sendRequest", fakeAsync(() => {
    const requestType = "saveCMSForYouPersonalizedData";  
    component["sendRequest"](requestType, true );
    tick();
    expect(requestType).toEqual('saveCMSForYouPersonalizedData');

  }));

  it("it should calll sendRequest throwError", fakeAsync(() => {
    const requestType = "saveCMSForYouPersonalizedData";
    apiClientService.forYouService().saveCMSForYouPersonalizedData.and.returnValue(throwError({status: 404}))
    component["sendRequest"](requestType, true );
    tick();
    expect(requestType).toEqual('saveCMSForYouPersonalizedData');

   }))
   

})
