import { TestBed, getTestBed, fakeAsync } from '@angular/core/testing';
import { FanzonesAPIService } from "./fanzones.api.service";
import { of } from 'rxjs/observable/of';
import { HttpClientTestingModule } from "@angular/common/http/testing";
import { MatDialog } from '@angular/material/dialog';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../client/private/services/http/';
import { BrandService } from '../../client/private/services/brand.service';
import { TeamKitAPIService } from '@root/app/one-two-free/teamKit.api.service';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';
import { HttpErrorResponse } from '@angular/common/http';
import { throwError } from 'rxjs';




describe('FanzonesAPIService', () => {
  let injector: TestBed;
  let service: FanzonesAPIService;

  const mockedFaanzone = {
    name: 'test',
    active: false,
    launchBannerUrl: 'test',
    teamId: 'test',
    openBetID: 'test',
    fanzoneBanner: 'test',
    assetManagementLink: 'test',
    primaryCompetitionId: 'test',
    secondaryCompetitionId: 'test',
    clubIds: 'test',
    location: 'test',
    nextGamesLbl: 'test',
    outRightsLbl: 'test',
    premierLeagueLbl: 'test',
    id: 'test',
    brand: 'test',
    createdBy: 'test',
    createdAt: 'test',
    updatedBy: 'test',
    updatedAt: 'test',
    updatedByUserName: 'test',
    createdByUserName: 'test',
    universalSegment: true,
    exclusionList: ['test1', 'test2'],
    inclusionList: ['test1', 'test2'],
    title: 'test',
    bannerLink: 'test',
    description: 'test',
    validityPeriodStart: 'test',
    validityPeriodEnd: 'test',
  };
  const arrayMockedFaanzone = [{
    name: 'test',
    active: false,
    launchBannerUrl: 'test',
    teamId: 'test',
    openBetID: 'test',
    fanzoneBanner: 'test',
    assetManagementLink: 'test',
    primaryCompetitionId: 'test',
    secondaryCompetitionId: 'test',
    clubIds: 'test',
    location: 'test',
    nextGamesLbl: 'test',
    outRightsLbl: 'test',
    premierLeagueLbl: 'test',
    id: 'test',
    brand: 'test',
    createdBy: 'test',
    createdAt: 'test',
    updatedBy: 'test',
    updatedAt: 'test',
    updatedByUserName: 'test',
    createdByUserName: 'test',
    universalSegment: true,
    exclusionList: ['test1', 'test2'],
    inclusionList: ['test1', 'test2'],
    title: 'test',
    bannerLink: 'test',
    description: 'test',
    validityPeriodStart: 'test',
    validityPeriodEnd: 'test',
  }];

  const mockedClubs = {
    active: true,
    title: 'test',
    bannerLink: 'test',
    description: 'test',
    validityPeriodStart: 'test',
    validityPeriodEnd: 'test',
  };
  const mockPreferences = {
    active: true,
    pcDescription: 'test',
    pcKeys: [],
    ctaText: 'test',
    subscribeText: 'test',
    confirmText: 'test',
    confirmCTA: 'test',
    exitCTA: 'test',
    notificationPopupTitle: 'test',
    unsubscribeTitle: 'test',
    notificationDescriptionDesktop: 'test',
    unsubscribeDescription: 'test',
    noThanksCTA: 'test',
    optInCTA: 'test',
    pushPreferenceCentreTitle: 'test',
    id: 'test',
    brand: 'test',

    createdBy: 'test',
    createdAt: 'test',

    updatedBy: 'test',
    updatedAt: 'test',

    updatedByUserName: 'test',
    createdByUserName: 'test',

    universalSegment: true,
    exclusionList: ['1', '2'],
    inclusionList: ['1', '2']
  };
  const mockhttp = {
    "headers": {
      "normalizedNames": {},
      "lazyUpdate": null
    },
    "status": 200
  };

  const apiServiceStub = {
    fanzoneService: () => ({
      getAllFanzones: () => of(arrayMockedFaanzone),
      getFanzoneSyc: () => of(mockedFaanzone),
      getFanzonePreferences: () => of(mockedFaanzone),
      getAllFanzoneClubs: () => of(mockedFaanzone),
      deleteFanzone: (id) => of(id),
      getFanzoneClub: (id) => of(id),
      createFanzone: () => of(mockedFaanzone),
      getFanzoneDetails: (id) => of(mockedFaanzone),
      updateFanzoneDetails: (id, fanzone) => of(mockedFaanzone),
      saveFanzoneSyc: (method, id, fanzone) => of(mockedFaanzone),
      saveFanzonePreferences: (method, id, preferences) => of(mockedFaanzone),
      updateFanzoneClub: (id, clubs) => of(mockedClubs),
      saveFanzoneClub: (clubs) => of(mockedClubs),
      deleteFanzoneClub: (id) => of(mockedClubs),
    }),
  };
  const kitServiceStub = {};
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        FanzonesAPIService,
        GlobalLoaderService,
        { provide: ApiClientService, useValue: apiServiceStub },
        { provide: TeamKitAPIService, useValue: kitServiceStub },
        BrandService,
        MatDialog
      ]
    });
    injector = getTestBed();

    service = injector.get(FanzonesAPIService);
  });

  it('should createFanzone fanzone and call showLoader', () => {
    const spyOnLoader = spyOn(service['globalLoaderService'], 'showLoader');
    service.createFanzone(mockedFaanzone).subscribe(fanzone => {
      expect(spyOnLoader).toHaveBeenCalled();
      expect(fanzone).toEqual(mockedFaanzone);
    });
  });

  it('should return fanzone and call showLoader', () => {
    const spyOnLoader = spyOn(service['globalLoaderService'], 'showLoader');
    service.getAllFanzones().subscribe(fanzone => {
      expect(spyOnLoader).toHaveBeenCalled();
      expect(fanzone).toEqual(arrayMockedFaanzone);
    });
  });

  it('should call wrappedObservable and responce to be equal 1', () => {
    const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.callThrough();
    service.getFanzoneDetails('1').subscribe(data => {
      expect(data).toBe(mockedFaanzone);
      expect(spyOnWrappedObservable).toHaveBeenCalled();
    });
  });

  it('should call wrappedObservable and responce to be equal 2', () => {
    const spyOnLoader = spyOn(service['globalLoaderService'], 'showLoader');
    service.updateFanzoneDetails('1', mockedFaanzone).subscribe(data => {
      expect(spyOnLoader).toHaveBeenCalled();
      expect(data).toEqual(mockedFaanzone);
    });
  });

  it('should call deleteFanzone to delete particular fanzone with id', () => {
    const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.callThrough();
    service.deleteFanzone('1').subscribe(data => {
      expect(spyOnWrappedObservable).toHaveBeenCalled();
    });
  });

  it('should call saveFanzoneSyc to save the fanzone', () => {
    service.saveFanzoneSyc('post', mockedFaanzone, '1').subscribe(data => {
    });
  });

  it('should call getFanzoneSyc and call showLoader', () => {
    const spyOnLoader = spyOn(service['globalLoaderService'], 'showLoader');
    service.getFanzoneSyc().subscribe(fanzone => {
      expect(spyOnLoader).toHaveBeenCalled();
      expect(fanzone).toEqual(mockedFaanzone);
    });
  });

  it('should call getFanzoneClub to get fanzone clubs', () => {
    const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.callThrough();
    service.getFanzoneClub('1').subscribe(data => {
      expect(spyOnWrappedObservable).toHaveBeenCalled();
    });
  });

  it('should call getAllFanzoneClubs to get all fanzone clubs', () => {
    const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.callThrough();
    service.getAllFanzoneClubs().subscribe(data => {
      expect(spyOnWrappedObservable).toHaveBeenCalled();
    });
  });

  it('should call saveFanzoneClub to save fanzone club', () => {
    const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.callThrough();
    service.saveFanzoneClub(mockedFaanzone).subscribe(data => {
      expect(spyOnWrappedObservable).toHaveBeenCalled();
    });
  });

  it('should call updateFanzoneClub to update a fanzone club', () => {
    const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.callThrough();
    service.updateFanzoneClub('1', mockedFaanzone).subscribe(data => {
      expect(spyOnWrappedObservable).toHaveBeenCalled();
    });
  });

  it('should call deleteFanzoneClub a fanzone club', () => {
    const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.callThrough();
    service.deleteFanzoneClub('1').subscribe(data => {
      expect(spyOnWrappedObservable).toHaveBeenCalled();
    });
  });

  it('should call getFanzonePreferences to get all preferences', () => {
    const spyOnLoader = spyOn(service['globalLoaderService'], 'showLoader');
    service.getFanzonePreferences().subscribe(fanzone => {
      expect(spyOnLoader).toHaveBeenCalled();
    });
  });

  it('should call saveFanzonePreferences to save the preferences', () => {
    const spyOnLoader = spyOn(service['globalLoaderService'], 'showLoader');
    service.saveFanzonePreferences('post', mockPreferences, '1').subscribe(fanzone => {
      expect(spyOnLoader).toHaveBeenCalled();
    });
  });

  it('should call handleRequestError and call showLoader', () => {
    const spyOnLoader = spyOn(service['globalLoaderService'], 'hideLoader');
    service.handleRequestError('error');
    expect(spyOnLoader).toHaveBeenCalled();
  });

  it('should call hideloader', () => {
    const spyOnLoader = spyOn(service['globalLoaderService'], 'hideLoader');
    service.handleRequestError('error');
    expect(spyOnLoader).toHaveBeenCalled();
  });

  it('catch for wrappedObservable', fakeAsync(() => {
    let spyOnLoader = spyOn(service['globalLoaderService'], 'hideLoader');
    service.wrappedObservable(throwError(new HttpErrorResponse(<any>{ res: mockhttp }))).subscribe(
      data => fail('should have failed with the 404 error'),
      (error: HttpErrorResponse) => {
        expect(spyOnLoader).toHaveBeenCalled();
      });
  }));
});