import { fakeAsync,tick } from '@angular/core/testing';
import { foryoumainComponent } from './for-you-main.component';
import { Params } from '@angular/router';
import { of } from 'rxjs';

let mockdata = {
  trendingTabName: "foryou",
  headerDisplayName: "Foryou",
  enabled: true,
  href: "insights-forYou",
  popularTabs: [
    {
      href: "for-you-personalized-bets",
      enabled: true,
      popularTabName: "for-you-personalized-bets",
    },
  ],
} as any;

let popularBetsData = {
  name: "popularbets",
  displayName: "Popular bets",
  enabled: true,
  trendingTabs: [
    {
      id: "654d0ed741f8421450717fd1",
      trendingTabName: "popular bets",
      headerDisplayName: "Popular_bets",
      enabled: true,
      href: "insights-popular",
      popularTabs: [
        {
          id: "654d0ed741f8421450717fd0",
          href: null,
          enabled: true,
          popularTabName: "Popular_tab",
        },
      ],
    },
  ],
  href: "insights-forYou",
} as any;

const routeParams: Params = {
  id: '57fcfcd9b6aff9ba6c252a2c',
  moduleId: '5beee1bbc9e77c0001fb69e3'
};
describe('foryoumain', () => {
  let component: foryoumainComponent;
  let globalLoaderService;
  let activatedRoute;
  let apiClientService;
  let matSnackBar;
  let insightsService;
  let dialogService;

beforeEach(() => {
  globalLoaderService = {
    showLoader: jasmine.createSpy('showLoader'),
    hideLoader: jasmine.createSpy('hideLoader')
  };

  activatedRoute = {
    params: of(routeParams),
  };
  
  apiClientService = {
    sportTabService: jasmine.createSpy('sportTabService').and.returnValue({
      edit : jasmine.createSpy('edit').and.returnValue(of({body : popularBetsData}))
    })
  }

  matSnackBar = {
    open: jasmine.createSpy('open')
  }

  insightsService = {
    getSportTabById: jasmine.createSpy('getSportTabById ').and.returnValue(of(popularBetsData)),
    getSportCategoryById: jasmine.createSpy('getSportCategoryById').and.returnValue(of(popularBetsData)),
  }
  component = new foryoumainComponent(
     globalLoaderService,
     activatedRoute,
     apiClientService,
     matSnackBar,
     insightsService,
     dialogService,
  );
  component.forYouBets = mockdata;
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
    component.actionButtons = {
      extendCollection: jasmine.createSpy("extendCollection"),
    } as any;
    component.sportTab = popularBetsData;
    const spy = spyOn<any>(component, "buildBreadCrumbsData");
    const spy1 = spyOn<any>(component, "createForyouSportTable");

    component["loadInitialData"]();
    tick();
    expect(spy).toHaveBeenCalled();
    expect(spy1).toHaveBeenCalled();
  }));

  it("it should calll loadInitialData without body data", fakeAsync(() => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy("extendCollection"),
    } as any;
    
    component.sportTab = null;
    const spy = spyOn<any>(component, "buildBreadCrumbsData");
    const spy1 = spyOn<any>(component, "createForyouSportTable");

    component["loadInitialData"]();
    tick();
    expect(spy).toHaveBeenCalled();
    expect(spy1).toHaveBeenCalled();
  }));

  it("it should call buildBreadCrumbsData", fakeAsync(() => {
    component["buildBreadCrumbsData"](popularBetsData, "12345" as any);
    tick();
  }));

  it('should call isValidForm',()=>{
    const data = popularBetsData;
  component.isValidForm(data);
  })

  it('should sportTabReorderHandler', () => {
    component.sportTabReorderHandler('test');
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
    const spy = spyOn<any>(component, 'loadInitialData');
    component.revertChanges();
    expect(spy).toHaveBeenCalled();
  });

  it('#saveChanges default', () => {
    const spy = spyOn<any>(component, 'submitChanges');
    component.saveChanges();
    expect(spy).toHaveBeenCalled();
  });

  it("it should calll createForyouSportTable", fakeAsync(() => {
    component.sportTab = mockdata;
    component["createForyouSportTable"]();
    tick();
  }));

  it("it should calll sendRequest", fakeAsync(() => {
    component.actionButtons = {
      extendCollection: jasmine.createSpy("extendCollection"),
    } as any;
    const message = "save changes";
    component.sportTab = popularBetsData;
    component["submitChanges"](message);
    tick();
    expect(message).toEqual("save changes");
  }));
  

});

