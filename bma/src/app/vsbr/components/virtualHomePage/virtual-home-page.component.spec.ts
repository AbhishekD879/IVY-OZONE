import { of } from 'rxjs/internal/observable/of';
import { VirtualHomePageComponent } from './virtual-home-page.component';
import { fakeAsync, tick } from '@angular/core/testing';
import { throwError } from 'rxjs';

describe('VirtualHomePageComponent', () => {
    let pubsub, cmsService, featuredModuleService, virtualHubService, deviceService,
        inPlayConnectionService, inPlayMainService, changeDetectorRef, pubsubService
    let component: VirtualHomePageComponent;


    beforeEach(() => {
        pubsub = {
            publish: jasmine.createSpy('publish'),
            subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb: Function) => {
                cb(true)
            }),
            API: {
                FEATURED_CONNECT_STATUS: 'FEATURED_CONNECT_STATUS',
                VIRTUAL_EVENT_COUNT_UPDATE: 'VIRTUAL_EVENT_COUNT_UPDATE'
            }
        },
            cmsService = {
                getFSC:  jasmine.createSpy('getFSC').and.returnValue(of({modules: [{'@type' : 'VirtualRaceModule'}]})),
            },
            featuredModuleService = {
                addEventListener: jasmine.createSpy('addEventListener'),
                startConnection: jasmine.createSpy('startConnection'),
                trackDataReceived: jasmine.createSpy('trackDataReceived'),
            }
        virtualHubService = {
            getCmsData: jasmine.createSpy('getCmsData').and.returnValue(of({
                cmsVirtualSportsData: 'data',
                cmsConfig: { UseFSCCached: {enabled: false}, VirtualHubHomePage: { topSports: 'topSports' }, VirtualSports: { virtual: 'virtual-horse-racing' } }
            })),
            fetchVirtualImagesFromSiteCore: jasmine.createSpy('getCmsData').and.returnValue(of(
                {
                    topSports: 'topSports',
                    otherSports: 'otherSports',
                    featureZoneOffers: 'featureZoneOffers'
                }
            ))
        },

            deviceService = {
                getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue({mobile: true}),
            },
            inPlayConnectionService = {
                connectComponent: jasmine.createSpy('connectComponent').and.returnValue(of({ data: 'connectComponent' })),
            },
            inPlayMainService = {
                getVirtualsData: jasmine.createSpy('getVirtualsData').and.returnValue(of({ data: 'getVirtualsData' })),
                unsubscribeForVRUpdates: jasmine.createSpy('unsubscribeForVRUpdates'),
            },
            changeDetectorRef = {
                detectChanges: jasmine.createSpy('detectChanges').and.callThrough(),
            },
            pubsubService = {
                subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb: Function) => {
                    cb(true)
                }),
                API: {
                    FEATURED_CONNECT_STATUS: 'FEATURED_CONNECT_STATUS',
                    VIRTUAL_EVENT_COUNT_UPDATE: 'VIRTUAL_EVENT_COUNT_UPDATE'
                }
            },
            component = new VirtualHomePageComponent(pubsub, cmsService, featuredModuleService, virtualHubService, deviceService,
                inPlayConnectionService, inPlayMainService, changeDetectorRef, pubsubService);
    })

    describe('ngOnInit', () => {
        it('ngOnInit', () => {
            spyOn(component, 'showSpinner');
            spyOn(component, 'hideSpinner');
            spyOn(component, 'loadCmsAndSiteCoreImageConfig' as any);
            spyOn(component, 'loadNumberIndicator' as any);
            spyOn(component, 'loadNextEvents' as any);
            component.ngOnInit();

        })

        it('ngOnInit', () => {
            virtualHubService.getCmsData = jasmine.createSpy('getCmsData').and.returnValue(of({
                cmsVirtualSportsData: 'data',
                cmsConfig: { VirtualHubHomePage: { topSports: false, nextEvents: true }, VirtualSports: { 'virtual-horse-racing': 'virtual-horse-racing' } }
            })),
            spyOn(component, 'showSpinner');
            spyOn(component, 'hideSpinner');
            spyOn(component, 'loadCmsAndSiteCoreImageConfig' as any);
            spyOn(component, 'loadNumberIndicator' as any);
            spyOn(component, 'loadNextEvents' as any);
            component.ngOnInit();

        })

        it('ngOnInit', () => {
            virtualHubService.getCmsData = jasmine.createSpy('getCmsData').and.returnValue(of({
                cmsVirtualSportsData: 'data',
                cmsConfig: { VirtualHubHomePage: { topSports: false, nextEvents: true } }
            })),
            spyOn(component, 'showSpinner');
            spyOn(component, 'hideSpinner');
            spyOn(component, 'loadCmsAndSiteCoreImageConfig' as any);
            spyOn(component, 'loadNumberIndicator' as any);
            spyOn(component, 'loadNextEvents' as any);
            component.ngOnInit();

        })

        it('ngOnInit thow error', () =>{
            virtualHubService.getCmsData =() => throwError('err');
            component.ngOnInit();
        });
    })

    describe('loadCmsAndSiteCoreImageConfig', () => {
        it('loadCmsAndSiteCoreImageConfig 1', fakeAsync(() => {
            spyOn(component, 'getBGImageUrl');
            component['loadCmsAndSiteCoreImageConfig']({} as any);
            tick(1000);
            expect(component.showLoader).toBeFalsy()
        }))

        it('loadCmsAndSiteCoreImageConfig 2', fakeAsync(() => {
            deviceService.getDeviceViewType = () => {mobile: false},
            deviceService = {
                getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue({mobile: true}),
            },
            virtualHubService.fetchVirtualImagesFromSiteCore = jasmine.createSpy('getCmsData').and.returnValue(of(null)),
                spyOn(component, 'getBGImageUrl');
            component['loadCmsAndSiteCoreImageConfig']({} as any);
            tick(1000);
            expect(component.showLoader).toBeFalsy()
        }))

        it('loadCmsAndSiteCoreImageConfig undefined', fakeAsync(() => {
            deviceService.getDeviceViewType = () => {mobile: false},
            deviceService = {
                getDeviceViewType: jasmine.createSpy('getDeviceViewType').and.returnValue(undefined),
            },
            virtualHubService.fetchVirtualImagesFromSiteCore = jasmine.createSpy('getCmsData').and.returnValue(of(null)),
                spyOn(component, 'getBGImageUrl');
            component['loadCmsAndSiteCoreImageConfig']({} as any);
            tick(1000);
            expect(component.showLoader).toBeFalsy()
        }))

        it('loadCmsAndSiteCoreImageConfig is failed', fakeAsync(() => {
                virtualHubService.fetchVirtualImagesFromSiteCore =() => throwError('err');
                component['loadCmsAndSiteCoreImageConfig']({} as any);
            tick(1000);
        }));
    })

    describe('loadNextEvents', () => {
        it('loadNextEvents', fakeAsync(() => {
            spyOn(component, 'getBGImageUrl');
            const featured = {
                modules: [{
                    '@type': 'VirtualRaceModule'
                }]
            } as any;

            component['featuredModuleService'].addEventListener = jasmine.createSpy('addEventListener')
                .and.callFake((messageText, callbackFn) => {
                    if (messageText === 'FEATURED_STRUCTURE_CHANGED') {
                        callbackFn(Object.assign({}, featured));
                        expect(component.virtualShowLoader).toBeFalsy()
                    }
                });
            component['loadNextEvents']();
            tick(1000);
            expect(featuredModuleService.startConnection).toHaveBeenCalled();
            component['pubsub'].subscribe = jasmine.createSpy('subscribe').and.callFake((a, b, cb: Function) => {
                cb(false);
                expect(component.virtualShowLoader).toBeFalsy()
            });

            //virtualHubService.getCmsData =() => throwError('err');
            component['loadNextEvents']();
            tick(1000);
            expect(featuredModuleService.startConnection).toHaveBeenCalled();


            component.readFSCFromCF = false;
            component['loadNextEvents']();
            tick(1000);
            component['pubsub'].subscribe = jasmine.createSpy('subscribe').and.callFake((a, b, cb: Function) => {
                cb(true);
                expect(component.virtualShowLoader).toBeFalsy()
            });
            expect(featuredModuleService.startConnection).toHaveBeenCalled();

            component['loadNextEvents']();
            tick(1000);
            component['pubsub'].subscribe = jasmine.createSpy('subscribe').and.callFake((a, b, cb: Function) => {
                cb(false);
                expect(component.virtualShowLoader).toBeFalsy()
            });
            expect(featuredModuleService.startConnection).toHaveBeenCalled();
        }))

        it('loadNextEvents error case', fakeAsync(() => {
            spyOn(component, 'getBGImageUrl');
            const featured = {
                modules: [{
                    '@type': 'VirtualRaceModule'
                }]
            } as any;

            component['featuredModuleService'].addEventListener = jasmine.createSpy('addEventListener')
                .and.callFake((messageText, callbackFn) => {
                    if (messageText === 'FEATURED_STRUCTURE_CHANGED') {
                        callbackFn(Object.assign({}, featured));
                        expect(component.virtualShowLoader).toBeFalsy()
                    }
                });
            cmsService.getFSC =() => throwError('err');
            component['loadNextEvents']();
            tick(1000);
            expect(featuredModuleService.startConnection).toHaveBeenCalled();
            component['pubsub'].subscribe = jasmine.createSpy('subscribe').and.callFake((a, b, cb: Function) => {
                cb(false);
                expect(component.virtualShowLoader).toBeFalsy()
            });

        }))

    })

    describe('loadNumberIndicator', () => {
        it('loadNumberIndicator', fakeAsync(() => {
            component['loadNumberIndicator']();
            tick(1000);
        }))

    })

    describe('validateNextEventEnabled', () => {
        it('validateNextEventEnabled', () => {
            component.virtualHubSystemConfig = {
                'nextEvents': true,
                'topSports': false,
                'otherSports': false,
                'featureZone': false,
                'headerBanner': false
            }
            const retvalue = component['validateNextEventEnabled']();
            expect(retvalue).toBeTruthy();
            component.virtualHubSystemConfig = {
                'nextEvents': false,
                'topSports': false,
                'otherSports': false,
                'featureZone': false,
                'headerBanner': true
            }
            const nextRetvalue = component['validateNextEventEnabled']();
            expect(nextRetvalue).toBeFalsy();
        })
    })

    describe('ngOnDestroy', () => {
        it('ngOnDestroy: should unsubscribe from connectSubscription', function () {
            component['connectSubscription'] = {
                unsubscribe: jasmine.createSpy('unsubscribe')
            } as any;
            component['virtualhubSubscription'] = {
                unsubscribe: jasmine.createSpy('virtualhubSubscription')
            } as any;
            component.ngOnDestroy();
            expect(component['connectSubscription'].unsubscribe).toHaveBeenCalled();
            expect(inPlayMainService.unsubscribeForVRUpdates).toHaveBeenCalled();
        })

        it('ngOnDestroy: with undefined case', function () {
            component.ngOnDestroy();
            expect(component['connectSubscription']).toBeUndefined();
        })
    })

    describe('getBGImageUrl', () => {
        it('ngOnDestroy: should unsubscribe from connectSubscription', () => {
            component.virtualHubSystemConfig = {
                'topSportsBackgroundID': '1'
            }
            component['virtualHubService'] = {
                siteCoreOffers: [
                    {
                        'Id' : '1',
                        'imgUrl': 'text'
                    }
                ]
            } as any;
            const retValue = component.getBGImageUrl();
            expect(retValue).toBe('text');
            component.virtualHubSystemConfig = {
                'topSportsBackgroundID': '2'
            }
            component['virtualHubService'] = {
                siteCoreOffers: [
                    {
                        'Id' : '1',
                    }
                ]
            } as any;
            const nextretValue = component.getBGImageUrl();
        })
    })
});