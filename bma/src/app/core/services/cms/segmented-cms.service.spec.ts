import {  of, ReplaySubject, throwError } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { fakeAsync, tick } from '@angular/core/testing';
import { SegmentedCMSService } from './segmented-cms.service';
import { pubSubApi } from '../communication/pubsub/pubsub-api.constant';
import { IInitialData } from '@app/core/services/cms/models';

describe('SegmentedCMSService', () => {
    const initialDataMock = {
        systemConfiguration: { systemConfiguration: {} },
        navigationPoints: [{ a: 1, b: 2 }],
    } as any;

    let service;
    let httpClient;
    let segmentCacheManagerService;
    let pubSubService;
    let segmentedCMSEndPointService;

    beforeEach(() => {
        httpClient = {
            get: jasmine.createSpy('get').and.returnValue(of({ body: [] }))
        };

        segmentCacheManagerService = jasmine.createSpy();

        segmentedCMSEndPointService = {
            getInitialDataEndPoint: jasmine.createSpy('getInitialDataEndPoint')
        };
        pubSubService = {
            publish: jasmine.createSpy('publish'),
            subscribe: jasmine.createSpy('subscribe').and.callFake((fileName: string, method: string, callback: Function) => {
                callback();
            }),
            API: pubSubApi
          };
        service = new SegmentedCMSService(
            httpClient,
            segmentedCMSEndPointService,
            pubSubService
        );

        service['initialData$'] = new ReplaySubject<any>(1);
        service['initialData$'].next(initialDataMock as any);
    });

    describe('SegmentedCMSService', () => {
        it('should create instance', () => {
            spyOn(service, 'getCmsInitData').and.callThrough();
            expect(service instanceof SegmentedCMSService).toBeTruthy();
            expect(service).toBeDefined();
            expect(pubSubService.subscribe).toHaveBeenCalled();
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake(
                (fileName: string, method: string, callback: Function) => {
                    if (method === pubSubService.API.SEGMENT_RECEIVED) {
                        callback();
                        expect(service.getCmsInitData).toHaveBeenCalled();
                    }
                });
        });
    });

    describe('ngOnDestroy', () => {
        it('should unsubscribe ReplaySubject', () => {
            service['initialData$'] = new ReplaySubject<any>(1);
            service.ngOnDestroy();
            expect(service['initialData$']).toBeDefined();
        });

        it('should not unsubscribe', function () {
            service['initialData$'] = null;
            service.ngOnDestroy();
            expect(service['initialData$']).toBe(null);
        });
    });

    describe('getCmsCSPInitData', () => {
        beforeEach(() => {
            service['initialData$'] = undefined;
            service['getData'] = jasmine.createSpy('getData').and.returnValue(of({ body: initialDataMock }));
            service['releaseSubject'] = jasmine.createSpy('releaseSubject');
        });

        it('should throw error', fakeAsync(() => {
            segmentCacheManagerService['isChanged'] = false;
            service['windowRef'] = { nativeWindow: {} } as any;
            service['getData'] = jasmine.createSpy('getData').and.returnValue(throwError(''));
            service['getCmsInitData']().subscribe();
            tick();
            expect(pubSubService.publish).toHaveBeenCalled();
        }));
        it('should resolve if data present in observable and segment not changed', fakeAsync(() => {
            segmentCacheManagerService['isChanged'] = false;
            service['windowRef'] = { nativeWindow: {} } as any;
            service['getCmsInitData']().subscribe();
            tick();
            expect(service['releaseSubject']).toHaveBeenCalledWith(initialDataMock);
        }));
        it('should resolve if data present in observable and segment not changed and refresh true', fakeAsync(() => {
            segmentCacheManagerService['isChanged'] = false;
            service['windowRef'] = { nativeWindow: {} } as any;
            service['getCmsInitData'](true).subscribe();
            tick();
            expect(service['releaseSubject']).toHaveBeenCalledWith(initialDataMock);
        }));
        it('should resolve if data present in observable and segment not changed and refresh true', fakeAsync(() => {
            segmentCacheManagerService['isChanged'] = false;
            service['windowRef'] = { nativeWindow: {} } as any;
            service['initialData$'] = new ReplaySubject<IInitialData>(1);
            service['getCmsInitData'](true).subscribe();
            tick();
            expect(service['releaseSubject']).toHaveBeenCalledWith(initialDataMock);
        }));
        it('should do init call if no data in observable', fakeAsync(() => {
            segmentedCMSEndPointService.getInitialDataEndPoint = jasmine.createSpy().and.returnValue('initial-data/mobile');
            service['getCmsInitData']().subscribe();
            tick();
            expect(service['releaseSubject']).toHaveBeenCalledWith(initialDataMock);
            expect(service['getData']).toHaveBeenCalledWith('initial-data/mobile');
        }));
        it('should return stored data', () => {
            service['initialData$'] = new ReplaySubject<any>(1);
            service['initialData$'].next(initialDataMock);
            service['getCmsInitData'](false).subscribe((data) => {
                expect(data).toBe(initialDataMock);
            });
            expect(service['releaseSubject']).not.toHaveBeenCalled();
            expect(service['getData']).not.toHaveBeenCalled();
        });
    });

    describe('releaseSubject', () => {
        it('calls', fakeAsync(() => {
            service['initialData$'] = new ReplaySubject<any>(1);
            service['initialDataAvailable'] = false;
            service['initialData$'].subscribe((data) => { expect(data).toBe(initialDataMock); });
            service['releaseSubject'](initialDataMock);
            tick();
            expect(service['initialDataAvailable']).toBe(true);
        }));
    });

    describe('getData', () => {
        it('should call getData() with params', () => {
            const url = 'test-link', options = { option: 'option' };
            service['getData'](url, options);
            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/${url}`,
                { observe: 'response', params: options }
            );
        });
        it('should call getData() without params', () => {
            const url = 'test-link';
            service['getData'](url);
            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/${url}`,
                { observe: 'response', params: {} }
            );
        });
    });

    describe('isInitialDataAvailable', () => {
        it('isInitialDataAvailable returns false', () => {
            service.initialDataAvailable = false;
            service['isInitialDataAvailable'](); 
            expect(service['isInitialDataAvailable']()).toBe(false);
        });
        it('isInitialDataAvailable returns true', () => {
            service.initialDataAvailable = true;
            service['isInitialDataAvailable'](); 
            expect(service['isInitialDataAvailable']()).toBe(true);
        });
    });

    describe('getActiveExtraNavPoints', () => {
        const initialDataMock = {
            extraNavigationPoints: [{
                categoryId: [16],
                competitionId: [123, 234],
                homeTabs: ['/featured', '/inplay'],
                enabled: true,
                targetUri: '/12free',
                title: 'Football',
                description: 'werthjk',
                validityPeriodEnd: '2026-02-24T09:48:20.917Z',
                validityPeriodStart: '2018-12-24T09:48:20.917Z',
                featureTag: '12F'
              }]
          } as any;
          
        it('getActiveExtraNavPoints should call  checkForModule ', () => {
          spyOn(service, 'checkForModule').and.returnValue(true);
          spyOn(Date, 'now').and.returnValue(1588539600000);
          service.getActiveExtraNavPoints(initialDataMock,['/inplay'],'homeTabs');
          expect(service.checkForModule).toHaveBeenCalled();
        })
        it('getActiveExtraNavPoints with no data  ', () => {
            spyOn(service, 'checkForModule').and.returnValue(true);
            spyOn(Date, 'now').and.returnValue(1588539600000);
            service.getActiveExtraNavPoints(undefined,['/inplay'],'homeTabs');
            expect(service.getActiveExtraNavPoints.length).toBe(3);
          })
    })
    describe('checkForModule',()=>
    {
      const   point= {
            categoryId: [16],
            competitionId: [123, 234],
            homeTabs: ['/featured', '/inplay'],
            enabled: true,
            targetUri: '/12free',
            title: 'Football',
            description: 'werthjk',
            validityPeriodEnd: '2026-02-24T09:48:20.917Z',
            validityPeriodStart: '2018-12-24T09:48:20.917Z',
            featureTag: '12F'
      }
        it('should return true for homepage inplay tab configured in cms',()=>
        {
          expect(service.checkForModule(['/inplay'],point,'homeTabs')).toBeTruthy();
        })
        it('should return true for bigcompetition configured in cms',()=>
        {
          expect(service.checkForModule(['/football',123,16],point,'bigCompetition')).toBeTruthy();
        })
        it('should return true for sports category configured in cms',()=>
        {
          expect(service.checkForModule(['/football',11689,16],point,'sports')).toBeTruthy();
        })
    })   

    describe('showOtfBtn',()=>
    {
      it('should return base url',()=>
      {
        expect(service.showOtfBtn('/home/featured?abcd')).toEqual('/home/featured');
        expect(service.showOtfBtn('/home/inplay?abcd')).toEqual('/home/inplay');
      })  
    })
});
