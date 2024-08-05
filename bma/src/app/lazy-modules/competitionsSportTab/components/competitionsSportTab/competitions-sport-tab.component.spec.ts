import { fakeAsync, flush } from '@angular/core/testing';
import { of as observableOf, throwError } from 'rxjs';
import {
  CompetitionsSportTabComponent
} from '@lazy-modules/competitionsSportTab/components/competitionsSportTab/competitions-sport-tab.component';

describe('#CompetitionsSportTabComponent', () => {
  let component: CompetitionsSportTabComponent;

  let currentMatchesService;
  let cmsService;
  let storageService;

  const cmsCompetitionsData = { 'A-ZClassIDs': '11,12', InitialClassIDs: '13' };
  const ssCompetitionsData = [
    {
      class: { id: '10', name: 'A' }
    }, {
      class: { id: '11', name: 'C' }
    }, {
      class: { id: '12', name: 'D' }
    }, {
      class: { id: '13', name: 'B' }
    }
  ] as any;

  beforeEach(() => {
    currentMatchesService = {
      getFootballClasses: jasmine.createSpy('getFootballClasses').and.returnValue(Promise.resolve(ssCompetitionsData)),
      getOtherClasses: jasmine.createSpy('getOtherClasses').and.returnValue(Promise.resolve(ssCompetitionsData))
    };
    cmsService = {
      getCompetitions: jasmine.createSpy('getCompetitions').and.returnValue(observableOf(cmsCompetitionsData))
    };
    storageService = {
      set: jasmine.createSpy('set'),
    };

    component = new CompetitionsSportTabComponent(currentMatchesService, cmsService, storageService);

    component.sport = {
      config: {
        name: 'football',
        request: {
          categoryId: '16'
        },
        tier: 1
      }
    } as any;
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it(`isLoading should be truthy`, () => {
    expect(component.isLoading).toBeTruthy();
  });

  describe('checkIsLoading', () => {
    describe('should return False if isLoaded', () => {
      beforeEach(() => {
        component.isLoaded = true;
      });

      afterEach(() => {
        component.checkIsLoading();

        expect(component.isLoading).toBeFalsy();
      });

      it(`and isTierOne equal false`, () => {
        component.isTierOne = false;
      });

      it(`and isResponseError equal true`, () => {
        component.isTierOne = true;
        component.isResponseError = true;
        component.isNoCategories = false;
        component.childComponentLoaded = false;
      });

      it(`and isNoCategories equal true`, () => {
        component.isTierOne = true;
        component.isResponseError = false;
        component.isNoCategories = true;
        component.childComponentLoaded = false;
      });

      it(`and childComponentLoaded equal true`, () => {
        component.isTierOne = true;
        component.isResponseError = false;
        component.isNoCategories = false;
        component.childComponentLoaded = true;
      });
    });

    describe('should return True', () => {
      afterEach(() => {
        component.checkIsLoading();

        expect(component.isLoading).toBeTruthy();
      });

      it(`if isLoaded equal False`, () => {
        component.isLoaded = false;
      });

      it(`if isLoaded equal True and childComponentLoaded`, () => {
        component.isLoaded = true;
        component.isTierOne = true;
        component.isResponseError = false;
        component.isNoCategories = false;
        component.childComponentLoaded = false;
      });
    });
  });

  describe('#ngOnInit', () => {
    it('#ngOnInit if tier 1 sport', () => {
      component.ngOnInit();

      expect(component.categoryName).toEqual('football');
      expect(component.categoryId).toEqual('16');
      expect(currentMatchesService.getFootballClasses).toHaveBeenCalledTimes(1);
    });

    it('should fetch current tab data', () => {
      const tabs =
        [
          { id: 'id1' },
          {
            id: 'competitions',
            interstitialBanners: {
              bannerEnabled: true,
              bannerPosition: '0',
              ctaButtonLabel: 'cta',
              desktopBannerId: '',
              mobileBannerId: '',
              redirectionUrl: ''
            }
          }
        ] as any;
      component.sportTabs = tabs;
      component.ngOnInit();
      expect(component.targetTab).toEqual
        ({
          id: 'competitions',
          interstitialBanners: {
            bannerEnabled: true,
            bannerPosition: '0',
            ctaButtonLabel: 'cta',
            desktopBannerId: '',
            mobileBannerId: '',
            redirectionUrl: ''
          }
        } as any)
    })

    it('#ngOnInit if not tier 1 sport', () => {
      component.sport.config.tier = 2;
      component.ngOnInit();
      expect(currentMatchesService.getFootballClasses).not.toHaveBeenCalled();
      expect(storageService.set).not.toHaveBeenCalled();
    });
  });

  it('#updateLoadingState', () => {
    spyOn(component, 'checkIsLoading');
    component.updateLoadingState({
      isLoaded: true,
      isResponseError: false,
      eventsBySectionsLength: 3
    });
    expect(component.isLoaded).toEqual(true);
    expect(component.isResponseError).toEqual(false);
    expect(component.eventsBySectionsLength).toEqual(3);
    expect(component.checkIsLoading).toHaveBeenCalled();
  });

  it('childComponentLoadedHandler should set childComponentLoaded prop to true', () => {
    spyOn(component, 'checkIsLoading');
    expect(component.childComponentLoaded).toBeFalsy();
    component.childComponentLoadedHandler();

    expect(component.childComponentLoaded).toBeTruthy();
    expect(component.checkIsLoading).toHaveBeenCalled();
  });

  describe('#loadCompetitionsData', () => {
    it('CASE 1 - should load Competitions Data', fakeAsync(() => {
      spyOn(component, 'checkIsLoading');
      cmsService.getCompetitions = jasmine.createSpy('getCompetitions').and.returnValue(observableOf(cmsCompetitionsData));
      component['loadCompetitionsData']('football');
      flush();
      expect(cmsService.getCompetitions).toHaveBeenCalled();
      expect(currentMatchesService.getFootballClasses).toHaveBeenCalledWith([ '13', '11', '12' ]);
      expect(component.allCategories).toEqual([
        {
          class: { id: '11', name: 'C' }
        }, {
          class: { id: '12', name: 'D' }
        }
      ] as any);
      expect(component.currentMatchCategories).toEqual([
        {
          class: { id: '13', name: 'B' }
        }
      ] as any);
      expect(component.isResponseError).toBe(false);
      expect(component.isLoaded).toBe(true);
      expect(storageService.set).toHaveBeenCalledTimes(2);
      expect(component.checkIsLoading).toHaveBeenCalled();
    }));

    it('CASE 2 - should load Competitions Data', fakeAsync(() => {
      cmsService.getCompetitions = jasmine.createSpy('getCompetitions').and.returnValue(observableOf(
        { InitialClassIDs: '12' }));
      component['loadCompetitionsData']('football');
      flush();
      expect(cmsService.getCompetitions).toHaveBeenCalled();
      expect(currentMatchesService.getFootballClasses).toHaveBeenCalledWith([ '12' ]);
      expect(component.allCategories).toEqual([] as any);
      expect(component.currentMatchCategories).toEqual([
        {
          class: { id: '12', name: 'D' }
        }
      ] as any);
      expect(component.isResponseError).toBe(false);
      expect(component.isLoaded).toBe(true);
      expect(storageService.set).toHaveBeenCalledTimes(2);
    }));

    it('CASE 3 - should load Competitions Data', fakeAsync(() => {
      cmsService.getCompetitions = jasmine.createSpy('getCompetitions').and.returnValue(observableOf(
        { 'A-ZClassIDs': '11' }));
      component['loadCompetitionsData']('football');
      flush();
      expect(cmsService.getCompetitions).toHaveBeenCalled();
      expect(currentMatchesService.getFootballClasses).toHaveBeenCalledWith([ '11' ]);
      expect(component.allCategories).toEqual([
        {
          class: { id: '11', name: 'C' }
        }
      ] as any);
      expect(component.currentMatchCategories).toEqual([] as any);
      expect(component.isResponseError).toBe(false);
      expect(component.isLoaded).toBe(true);
      expect(storageService.set).toHaveBeenCalledTimes(2);
    }));

    it('CASE 4 - should throw error getClasses', fakeAsync(() => {
      spyOn(component, 'checkIsLoading');
      (component.allCategories as any) = ssCompetitionsData;
      currentMatchesService.getFootballClasses.and.returnValue(Promise.reject({error: 'error'}));
      component['loadCompetitionsData']('football');
      flush();

      expect(currentMatchesService.getFootballClasses).toHaveBeenCalled();
      expect(component.isLoaded).toEqual(true);
      expect(component.isResponseError).toEqual(true);
      expect(component.checkIsLoading).toHaveBeenCalled();
    }));

    it('CASE 5 - should throw error cmsService.getCompetitions', fakeAsync(() => {
      cmsService.getCompetitions.and.returnValue(throwError({ error: 'error' }));
      component['loadCompetitionsData']('football');
      flush();

      expect(currentMatchesService.getFootballClasses).not.toHaveBeenCalled();
      expect(component.isLoaded).toEqual(true);
    }));

    describe('isNoCategories', () => {
      beforeEach(() => {
        cmsService.getCompetitions = jasmine.createSpy('getCompetitions').and.returnValue(observableOf(cmsCompetitionsData));
      });

      describe('should be false', () => {
        afterEach(() => {
          expect(component.isNoCategories).toBe(false);
        });

        it(`if allCategories and currentMatchCategories`, fakeAsync(() => {
          component['loadCompetitionsData']('football');
          flush();
        }));

        it(`if no allCategories but currentMatchCategories`, fakeAsync(() => {
          spyOn(component as any, 'mainCompetitions').and.returnValue([]);

          component['loadCompetitionsData']('football');
          flush();
        }));

        it(`if no currentMatchCategories but allCategories`, fakeAsync(() => {
          spyOn(component as any, 'azCompetitions').and.returnValue([]);

          component['loadCompetitionsData']('football');
          flush();
        }));
      });

      it(`should be true if no allCategories and currentMatchCategories`, fakeAsync(() => {
        spyOn(component as any, 'azCompetitions').and.returnValue([]);
        spyOn(component as any, 'mainCompetitions').and.returnValue([]);

        component['loadCompetitionsData']('football');
        flush();

        expect(component.isNoCategories).toBe(true);
      }));
    });
  });

  describe('#getClasses', () => {
    it('should call getClasses for football', fakeAsync(() => {
      component['getClasses'](['1'], 'football');
      flush();

      expect(currentMatchesService.getFootballClasses).toHaveBeenCalledWith(['1']);
    }));

    it('should call getClasses for other sports', fakeAsync(() => {
      component.categoryId = '2';
      component['getClasses'](['1'], 'tennis');
      flush();

      expect(currentMatchesService.getOtherClasses).toHaveBeenCalledWith(['1'], '2');
    }));
  });
});
