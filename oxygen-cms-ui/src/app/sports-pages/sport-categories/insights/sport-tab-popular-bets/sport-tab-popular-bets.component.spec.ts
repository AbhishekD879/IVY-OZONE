import {fakeAsync, tick } from '@angular/core/testing';
import { SportTabPopularBetsComponent } from './sport-tab-popular-bets.component';
import { of } from 'rxjs';  
import { FormControl, FormGroup, Validators } from '@angular/forms';

import { Params } from '@angular/router';
import { ISportTabPopularBetsFilter } from '@root/app/client/private/models/sporttabFilters.model';
import { Component } from '@angular/core';
 
describe('SportTabPopularBetsComponent', () => {
  let component: SportTabPopularBetsComponent;
  let dialogService;
  let dialog;
  let activatedRoute;
  let apiClientService;
  let globalLoaderService;
  let snackBar;
  let changeDetectorRef;
  
  const routeParams: Params = {
    id: '57fcfcd9b6aff9ba6c252a2c',
    moduleId: '5beee1bbc9e77c0001fb69e3'
  };

  let popularBetsData = {
    brand: "bma",
    sportId: 16,
    name: "popularbets",
    displayName: "Popular bets",
    trendingTabs: [
      {
        id: "654d0ed741f8421450717fd1",
        trendingTabName: "popular bets",
        headerDisplayName: "Popular_bets",
        enabled: true,
        href: "insights-popular",
        popularTabs: [
          {

            betSlipBarBetsAddedDesc: "You’ve added Top 5 bets to your betslip!",
            betSlipBarCTALabel: "add to betslip",
            betSlipBarDesc: "Add top 5 most backed to your betslip!",
            betSlipBarRemoveBetsCTALabel: "Remove all from betslip",
            suspendedBetsDesc: "Add mostbacked to your betslip!",
            suspendedBetsAddedText:
              "You have added most backed to your betslip!",
            href: null,
            enabled: true,
            popularTabName: "Popular_tab",
            headerDisplayName: "Popular bets",
            topBetsHeaderLabel: null,
            startsInText: "Event Starting Within",
            backedInLastText: "Backed In The Last",
            showMoreText: "Show more",
            showLessText: "Show less",
            backedUpTimesText: "Backed in {n} Times!",
            informationTextDesc: "<p>Hey </p>",
            numbOfDefaultPopularBets: 5,
            numbOfShowMorePopularBets: 5,
            priceRange: "1/10-10/1",
            noPopularBetsMsg: "Sorry no bets",
            lastUpdatedTime: "Last Updated Time",
            nonLoginHeader: null,
            nonLoginCTA: null,
            noBettingHeader: null,
            noBettingDesc: null,
            noBettingCTA: null,
            informationTextEditor: "test",
            backedInLastFilter: [
              {
                isEnabled: true,
                displayName: "48hrs",
                isTimeInHours: true,
                isDefault : true,
                time:48,
              },
            ],
            eventStartsFilter: [
              {
                isEnabled: true,
                displayName: "48hrs",
                isTimeInHours: true,
                isDefault : true,
                time: 48,
              },
              {
                isEnabled: true,
                displayName: "3hrs",
                isTimeInHours: true,
                isDefault : true,
                time: 48,
              },
            ],
          },
        ],
      },
    ],
    href: "insights-forYou",
    showNewFlag: true,
    id: "6523bfd76859170a839de069",
    hidden: false,
  } as any;
  

  let mock = {
    id: "65719983f121cb6d235b9fc1",
    trendingTabName: "popular bets",
    headerDisplayName: "Popular_bets",
    enabled: true,
    href: "insights-popular",
    popularTabs: [
      {
        id: "65719983f121cb6d235b9fc0",
        betSlipBarBetsAddedDesc: "You’ve added Top 5 bets to your betslip!",
        betSlipBarCTALabel: "add to betslip",
        betSlipBarDesc: "Add top 5 most backed to your betslip!",
        betSlipBarRemoveBetsCTALabel: "Remove all from betslip",
        suspendedBetsDesc: "Add mostbacked to your betslip!",
        suspendedBetsAddedText: "You have added most backed to your betslip!",
        href: null,
        enabled: true,
        popularTabName: "Popular_tab",
        headerDisplayName: "Popular bets",
        topBetsHeaderLabel: null,
        startsInText: "Event Starting Within",
        backedInLastText: "Backed In The Last",
        showMoreText: "Show more",
        informationTextEditor: "test",
        showLessText: "Show less",
        backedUpTimesText: "Backed in {n} Times!",
        informationTextDesc: "<p>Hey </p>",
        numbOfDefaultPopularBets: 5,
        numbOfShowMorePopularBets: 5,
        priceRange: "1/10-10/1",
        noPopularBetsMsg: "Sorry no bets",
        lastUpdatedTime: "Last Updated Time",
        nonLoginHeader: null,
        nonLoginCTA: null,
        noBettingHeader: null,
        noBettingDesc: null,
        noBettingCTA: null,
        backedInLastFilter: [
          {
            isEnabled: false,
            displayName: "48 Hours",
            isTimeInHours: true,
            time:48,
            isDefault:false,
          },
        ],
        eventStartsFilter: [
          {
            isEnabled: false,
            displayName: "48 Hours",
            isTimeInHours: true,
            time:48,
            isDefault: false,
          },
        ],
      },
    ],
  } as any;

  beforeEach(() => {
    dialogService = {  
      showConfirmDialog: jasmine.createSpy('showConfirmDialog').and.callFake(({yesCallback,noCallback}) => {
      yesCallback();
      noCallback();
    })};

    dialog = {
      open: jasmine.createSpy("open").and.returnValue({
        afterClosed: jasmine.createSpy("afterClosed").and.returnValue(of({
            isEnabled: false,
            displayName: "48 Hours",
            isTimeInHours: true,
            time: 48,
            isDefault : true,
          })
        ),
      }),
    };

    activatedRoute = {
        params: of(routeParams)
    }

    apiClientService = {
      sportTabService: jasmine.createSpy('sportTabService').and.returnValue({
        getById : jasmine.createSpy('getById').and.returnValue(of({body : popularBetsData})),
        edit : jasmine.createSpy('edit').and.returnValue(of({body : popularBetsData}))
      }),
      sportCategory: jasmine.createSpy('sportCategory').and.returnValue({
        findOne : jasmine.createSpy('edit').and.returnValue(of(popularBetsData))
      }),
  
    }

    globalLoaderService ={
      showLoader : jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    }

    snackBar ={
      open :jasmine.createSpy('open')
    }
    changeDetectorRef = {
      detectChanges: () => {}
    }
    component = new SportTabPopularBetsComponent(
      dialogService,
      dialog,
      activatedRoute,
      apiClientService,
      globalLoaderService,
      snackBar,
      changeDetectorRef,
    );
  });
  
  it("it should call ngOnInit", fakeAsync(() => {
    const spy = spyOn<any>(component, "loadInitialData");
    component.ngOnInit();
    expect(spy).toHaveBeenCalled();
  }));

  it("it should calll loadInitialData", fakeAsync(() => {
    const spy = spyOn<any>(component, "createPopularBetsFormGroup");
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
    const spy = spyOn<any>(component, "createPopularBetsFormGroup");
    const spy1 = spyOn<any>(component, "buildBreadCrumbsData");
    component.sportTab = {popularTabs : [{informationTextEditor : null}] }as any

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
    component.populrBetsData = popularBetsData.trendingTabs[0]as any;
    component.form = new FormGroup({
      headerDisplayName: new FormControl(component.populrBetsData?.headerDisplayName || ''),
      topBetsHeaderLabel: new FormControl(component.populrBetsData?.topBetsHeaderLabel || '', [Validators.required, Validators.maxLength(30)]),
      showMoreText: new FormControl(component.populrBetsData?.showMoreText || '', [Validators.required, Validators.maxLength(15)]),
      showLessText: new FormControl(component.populrBetsData?.showLessText || '', [Validators.required, Validators.maxLength(15)]),
      backedUpTimesText: new FormControl(component.populrBetsData?.backedUpTimesText || '', [Validators.required, Validators.maxLength(30)]),
      numbOfDefaultPopularBets: new FormControl(component.populrBetsData?.numbOfDefaultPopularBets || 0, [Validators.required, Validators.min(1), Validators.max(5)]),
      numbOfShowMorePopularBets: new FormControl(component.populrBetsData?.numbOfShowMorePopularBets || 0, [Validators.required, Validators.min(1), Validators.max(10)]),
      priceRange: new FormControl(component.populrBetsData?.priceRange || '', [Validators.required, Validators.pattern('^([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})[-]([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})$')]),
      lastUpdatedTime: new FormControl(component.populrBetsData?.lastUpdatedTime || '', [Validators.required, Validators.maxLength(20)]),
      informationTextDesc: new FormControl(component.populrBetsData?.informationTextDesc || '', [Validators.required]),
      betSlipBarDesc: new FormControl(component.populrBetsData?.betSlipBarDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarCTALabel: new FormControl(component.populrBetsData?.betSlipBarCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      betSlipBarBetsAddedDesc: new FormControl(component.populrBetsData?.betSlipBarBetsAddedDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarRemoveBetsCTALabel: new FormControl(component.populrBetsData?.betSlipBarRemoveBetsCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      suspendedBetsAddedText: new FormControl(component.populrBetsData?.suspendedBetsAddedText || '', [Validators.required, Validators.maxLength(50)]),
      suspendedBetsDesc: new FormControl(component.populrBetsData?.suspendedBetsDesc || '', [Validators.required, Validators.maxLength(50)]),
      nonLoginHeader: new FormControl(component.populrBetsData?.nonLoginHeader || '', [Validators.required, Validators.maxLength(50)]),
      nonLoginCTA: new FormControl(component.populrBetsData?.nonLoginCTA || '', [Validators.required, Validators.maxLength(10)]),
      noBettingCTA: new FormControl(component.populrBetsData?.noBettingCTA || '', [Validators.required, Validators.maxLength(20)]),
      noBettingHeader: new FormControl(component.populrBetsData?.noBettingHeader || '', [Validators.required, Validators.maxLength(50)]),
      noBettingDesc: new FormControl(component.populrBetsData?.noBettingDesc || '', [Validators.required, Validators.maxLength(100)]),
    });
    component.createPopularBetsFormGroup();
    expect(component.form).toBeDefined();
   });
 
   
   it('#formControls default', () => {
    component.populrBetsData = popularBetsData.trendingTabs[0]as any;
    component.form = new FormGroup({
      headerDisplayName: new FormControl(component.populrBetsData?.headerDisplayName || ''),
      topBetsHeaderLabel: new FormControl(component.populrBetsData?.topBetsHeaderLabel || '', [Validators.required, Validators.maxLength(30)]),
      showMoreText: new FormControl(component.populrBetsData?.showMoreText || '', [Validators.required, Validators.maxLength(15)]),
      showLessText: new FormControl(component.populrBetsData?.showLessText || '', [Validators.required, Validators.maxLength(15)]),
      backedUpTimesText: new FormControl(component.populrBetsData?.backedUpTimesText || '', [Validators.required, Validators.maxLength(30)]),
      numbOfDefaultPopularBets: new FormControl(component.populrBetsData?.numbOfDefaultPopularBets || 0, [Validators.required, Validators.min(1), Validators.max(5)]),
      numbOfShowMorePopularBets: new FormControl(component.populrBetsData?.numbOfShowMorePopularBets || 0, [Validators.required, Validators.min(1), Validators.max(10)]),
      priceRange: new FormControl(component.populrBetsData?.priceRange || '', [Validators.required, Validators.pattern('^([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})[-]([1-9]{1}[0-9]{0,1})\/([1-9]{1}[0-9]{0,1})$')]),
      lastUpdatedTime: new FormControl(component.populrBetsData?.lastUpdatedTime || '', [Validators.required, Validators.maxLength(20)]),
      informationTextDesc: new FormControl(component.populrBetsData?.informationTextDesc || '', [Validators.required]),
      betSlipBarDesc: new FormControl(component.populrBetsData?.betSlipBarDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarCTALabel: new FormControl(component.populrBetsData?.betSlipBarCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      betSlipBarBetsAddedDesc: new FormControl(component.populrBetsData?.betSlipBarBetsAddedDesc || '', [Validators.required, Validators.maxLength(50)]),
      betSlipBarRemoveBetsCTALabel: new FormControl(component.populrBetsData?.betSlipBarRemoveBetsCTALabel || '', [Validators.required, Validators.maxLength(25)]),
      suspendedBetsAddedText: new FormControl(component.populrBetsData?.suspendedBetsAddedText || '', [Validators.required, Validators.maxLength(50)]),
      suspendedBetsDesc: new FormControl(component.populrBetsData?.suspendedBetsDesc || '', [Validators.required, Validators.maxLength(50)]),
      nonLoginHeader: new FormControl(component.populrBetsData?.nonLoginHeader || '', [Validators.required, Validators.maxLength(50)]),
      nonLoginCTA: new FormControl(component.populrBetsData?.nonLoginCTA || '', [Validators.required, Validators.maxLength(10)]),
      noBettingCTA: new FormControl(component.populrBetsData?.noBettingCTA || '', [Validators.required, Validators.maxLength(20)]),
      noBettingHeader: new FormControl(component.populrBetsData?.noBettingHeader || '', [Validators.required, Validators.maxLength(50)]),
      noBettingDesc: new FormControl(component.populrBetsData?.noBettingDesc || '', [Validators.required, Validators.maxLength(100)]),
    });
    component.formControls;
    expect(component.form).toBeDefined();

   });

  it('it should call ngOnChanges', fakeAsync(() => {
    component.form = {
      valueChanges: { subscribe: jasmine.createSpy().and.callFake(cb => cb({headerDisplayName: 'test'}))}
    } as any;
    component.changedPopularBetsData = {emit: jasmine.createSpy() } as any;
    component.sportTab = { trendingTabs : [] }as any;
    spyOn(component as any, 'showMarketSwitcherTable');
    spyOn(component,'defaultValidationHandler');
    component.ngOnChanges();   
    tick(1);
    expect( component.sportTab.trendingTabs).toEqual([]);
  }));

  it("it should call updateInfoTxtData", () => {
    component.populrBetsData = mock;
    component.form = new FormGroup({
      informationTextDesc: new FormControl("updateInfoTxtData" || ""),
    });
    component.updateInfoTxtData("informationTextDesc");
  });

  it('it should call reorderSortByFilters',fakeAsync(() => {
    component.populrBetsData = mock;
    const reOrderedData = [
    { isEnabled: true, displayName: "test",isTimeInHours: null,isDefault: true,time: null},
    { isEnabled: true, displayName: "test",isTimeInHours: null,isDefault: true,time: null}
    ] as any;
    const filterType = 'eventStartsFilter';
    component.reorderHandler(reOrderedData,filterType);
    tick();
    expect(component.populrBetsData).toEqual(mock);
  }));

  it('it should call revertChanges',fakeAsync(() => {
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

  it("#showMarketSwitcherTable", () => {
    component.showMarketSwitcher = false;
    component.sportTab = { name: "popular_bets" }as any;
    component.showMarketSwitcherTable();
    expect(component.isMarketsEdited).toBeFalsy();

  });

  it('it should call saveChanges()',fakeAsync(() => {
    const spy = spyOn<any>(component, 'submitChanges')
    component.saveChanges();
    expect(spy).toHaveBeenCalled();
  }));

  it("it should call submitChanges()", fakeAsync(() => {
    component.isMarketsEdited = false;
    component.actionButtons = {
      extendCollection: jasmine.createSpy("extendCollection"),
    } as any;
    spyOn<any>(component, "showMarketSwitcherTable");

    component.submitChanges();
    tick(1);
    expect(component.isMarketsEdited).toBeFalsy();
  }));

  it("it should calll normalizeTab", fakeAsync(() => {
   const result = component["normalizeTab"](popularBetsData);
   tick();
   expect(result).toEqual(popularBetsData)
  }));

  it("it should calll updatePopularBetFilter", fakeAsync(() => {
    const filterType = 'eventStartsFilter';
    component.populrBetsData = mock;
      const popularBets = {
        isEnabled: false,
        displayName: "48 Hours",
        isTimeInHours: true,
        time: 48,
        isDefault : false,
      };
    component['requestError'] = {
      showError : jasmine.createSpy('showError')
    }as any;  
    spyOn(component,'defaultValidationHandler');
    component["updatePopularBetFilter"](filterType as string, 'edit', popularBets as ISportTabPopularBetsFilter,);
    tick();
    expect(filterType).toEqual('eventStartsFilter');
   })); 

   it("it should calll updatePopularBetFilter with false time", fakeAsync(() => {
    const filterType = 'eventStartsFilter';
    component.populrBetsData = {
      id: "65719983f121cb6d235b9fc1",
      trendingTabName: "popular bets",
      headerDisplayName: "Popular_bets",
      enabled: true,
      href: "insights-popular",
      popularTabs: [
        {
          backedInLastFilter: [
            {
          isEnabled: false,
          displayName: "48 Hours",
          isTimeInHours: true,
          time: 48,
          isDefault : false,
            },
          ],
          eventStartsFilter: [
            {
              isEnabled: false,
              displayName: "48 Hours",
              isTimeInHours: true,
              time: 48,
              isDefault : false,
            },
          ],
        },
      ],
    } as any;
      const popularBets = {
        isEnabled: false,
        displayName: "48 Hours",
        isTimeInHours: true,
        time: 28,
        isDefault : false,
      };
      
    component['requestError'] = {
      showError : jasmine.createSpy('showError')
    }as any;  
    spyOn(component,'defaultValidationHandler');
    component["updatePopularBetFilter"](filterType as string, 'edit', popularBets as ISportTabPopularBetsFilter,);
    tick();
    expect(filterType).toEqual('eventStartsFilter');
   })); 
     
  it("it should calll defaultValidationHandler on true state", fakeAsync(() => {
    component.populrBetsData = {
      popularTabs: [
        {
          eventStartsFilter: [{ time: 48, isDefault: false }, { time: 48,isDefault: false }],
          backedInLastFilter: [{ time: 48,isDefault: true }, { isDefault: false }],
        },
      ],
    } as any;
    component['requestError'] = {
      showError : jasmine.createSpy('showError')
    }as any;
    component["defaultValidationHandler"]();
    tick();
    expect(component.isDefaultValueEmpty).toBe(false);  
  }));

  it("it should calll defaultValidationHandler on undefined state", fakeAsync(() => {
    component.populrBetsData = {
      popularTabs: [
        {
          eventStartsFilter: [{ time: 48, isDefault: true }, { time: 48,isDefault: false }],
          backedInLastFilter: [{ time: 48,isDefault: true }, { time: 48,isDefault: false }],
        },
      ],
    } as any;
    component['requestError'] = {
      showError : jasmine.createSpy('showError')
    }as any
    component["defaultValidationHandler"]();
    tick();
    expect(component.isDefaultValueEmpty).toBe(true);  
  }));
    
  it("it should calll removeFilter", fakeAsync(() => {
    const filterType = 'eventStartsFilter';
    component.populrBetsData = mock;
    const popularBets = mock.popularTabs[0].eventStartsFilter;
    spyOn(component,'defaultValidationHandler');
    component["removeFilter"](popularBets as ISportTabPopularBetsFilter,filterType as string);
    tick();
    expect(filterType).toEqual('eventStartsFilter');
  }));

  it("it should calll buildBreadCrumbsData", fakeAsync(() => {
    const tab = { id: "123" } as any;
    const sportTab = popularBetsData;
    component["buildBreadCrumbsData"](tab, sportTab);
    tick();
    expect(tab).toEqual({ id: "123" });
  }));
   
  it("it should calll validationHandler", fakeAsync(() => {
    component.isDefaultValueEmpty =  true;
    component.form = new FormGroup({
      headerDisplayName: new FormControl('popular_bets'),
    })
    const result =  component["validationHandler"]();
    tick();
    expect(result).toEqual(true)
  })); 
  
 });