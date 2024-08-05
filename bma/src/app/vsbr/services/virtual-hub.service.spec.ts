import { VirtualHubService } from './virtual-hub.service';
import { of } from 'rxjs/internal/observable/of';
import { fakeAsync, flush, tick } from '@angular/core/testing';

describe('VirtualHubService', () => {
    let vanillaApiService, service: VirtualHubService, gtmService, storageService


    beforeEach(() => {
        vanillaApiService = {
            post: jasmine.createSpy('post').and.returnValue(of([{type: ['test']}])),
        }
        gtmService = {
            push: jasmine.createSpy('push')
        }
        storageService = new Map();
        service = new VirtualHubService(vanillaApiService, gtmService, storageService);
    })

    describe('fetchVirtualImagesFromSiteCore', () => {
        it('fetchVirtualImagesFromSiteCore', () => {
            spyOn(service, 'getSiteCoreData' as any);
            service.fetchVirtualImagesFromSiteCore({} as any, {} as any, {'topSports': true} as any)
            expect(service['getSiteCoreData']).toHaveBeenCalled();
        })
    })

    describe('mergeCmsAndSitecoreData', () => {
        it('mergeCmsAndSitecoreData', () => {
            service['_settings'] = { channel: 'mobile' } as any;
            spyOn(service, 'getSiteCoreData' as any);
            const sportConfigs = [{ mobileImageId: 1, imgURL: 0, altText: 0 }]
            const retVal = service['mergeCmsAndSitecoreData']([{ Id: 1, imgUrl: 1, altText: 1 }] as any, sportConfigs as any) as any;
            expect(retVal[0].imgURL).toBe(1);
        })

        it('mergeCmsAndSitecoreData desktop', () => {
            service['_settings'] = { channel: 'desktop' } as any;
            spyOn(service, 'getSiteCoreData' as any);
            const sportConfigs = [{ desktopImageId: 1, imgURL: 0, altText: 0 }]
            const retVal = service['mergeCmsAndSitecoreData']([{ Id: 1, imgUrl: 1, altText: 1 }] as any, sportConfigs as any) as any;
            expect(retVal[0].imgURL).toBe(1);
        })
    })


    describe('groupAndFormatOffers', () => {

        it('groupAndFormatOffers without length', () => {
            spyOn(service, 'formatOfferResponse' as any);
            const retVal = service['groupAndFormatOffers']([] as any);
            expect(retVal.length).toBe(0);
        })
        it('groupAndFormatOffers with length', () => {
            spyOn(service, 'formatOfferResponse' as any).and.returnValue([{ data: 1 }]);
            const retVal = service['groupAndFormatOffers']([{ data: 1 }] as any);
            expect(retVal.length).toBe(1);
        })
    })

    describe('groupAndFormatOffers', () => {
        it('groupAndFormatOffers', () => {
            service['_settings'] = { brand: 'lads' } as any;
            spyOn(service, 'getObjectKeyValue' as any).and.returnValue('test');
            const retVal = service['formatOfferResponse']({ test: 1 } as any, 1 as any);
            expect(retVal.index).toBe(1);
        })

        it('groupAndFormatOffers with bannerlink', () => {
            service['_settings'] = { brand: 'lads' } as any;
            spyOn(service, 'getObjectKeyValue' as any).and.returnValue('test');
            const retVal = service['formatOfferResponse']({ bannerLink: { attributes: "test" } } as any, 1 as any);
            expect(retVal.index).toBe(1);
        })

        it('groupAndFormatOffers with bannerlink', () => {
            service['_settings'] = undefined;
            spyOn(service, 'getObjectKeyValue' as any).and.returnValue('test');
            const retVal = service['formatOfferResponse']({ bannerLink: { attributes: "test" } } as any, 1 as any);
            expect(retVal.index).toBe(1);
        })
    })

    describe('getObjectKeyValue', () => {
        it('getObjectKeyValue', () => {
            const retVal = service['getObjectKeyValue']({ test: '1' } as any, 'test' as any);
            expect(retVal).toBe('1')
        })

        it('getObjectKeyValue with empty obj', () => {
            const retVal = service['getObjectKeyValue']({} as any, 'test' as any);
            expect(retVal).toBe('')
        })
    })

    
    describe('partition', () => {
        it('partition', () => {
            const retVal = service['partition']([{ filterString: 'test' }] as any, {} as any) as any;
            expect(retVal[1].length).toBe(1)
        })
        
        it('partition', () => {
            const retVal = service['partition']([] as any, {} as any) as any;
            expect(retVal[1].length).toBe(0)
        })

        it('partition', () => {
            const retVal = service['partition']([{ filterString: 'test' }] as any, 'filterString') as any;
            expect(retVal[0].length).toBe(1)
        })
    })
    
    describe('setOrUpdateCmsConfig', () => {
        it('setOrUpdateCmsConfig', () => {
            service.cmsData = { next: () => true } as any;
            const retVal = service.setOrUpdateCmsConfig({});
        })
    })
    
    describe('getCmsData', () => {
        it('getCmsData', () => {
            service.cmsData = { asObservable: () => true } as any;
            const retVal = service.getCmsData();
        })
    })

    describe('getSiteCoreData', () => {
        it('getSiteCoreData', fakeAsync(() => {
            spyOn(service, ['groupAndFormatOffers'] as any) as any;
            spyOn(service, ['mergeCmsAndSitecoreData'] as any) as any;
            spyOn(service, ['partition'] as any).and.returnValue([[{topSportsIndex: 1}, {topSportsIndex: 2}], []] );
            const retVal = service['getSiteCoreData']({} as any, {'topSports': true} as any) as any;
            // tick(6000);
            retVal.subscribe([{type: ['test']}])
            flush()
        }))

        it('getSiteCoreData', fakeAsync(() => {
            vanillaApiService.post = jasmine.createSpy('post').and.returnValue(of([{type: []}])),
            spyOn(service, ['groupAndFormatOffers'] as any) as any;
            spyOn(service, ['mergeCmsAndSitecoreData'] as any) as any;
            spyOn(service, ['partition'] as any).and.returnValue([[{topSportsIndex: 1}, {topSportsIndex: 2}], []] );
            const retVal = service['getSiteCoreData']({} as any,{'topSports': true} as any) as any;
            retVal.subscribe([{type: ['test']}])
            flush()
        }))

        it('getSiteCoreData', fakeAsync(() => {
            vanillaApiService.post = jasmine.createSpy('post').and.returnValue(of([{type: []}])),
            spyOn(service, ['groupAndFormatOffers'] as any) as any;
            spyOn(service, ['mergeCmsAndSitecoreData'] as any) as any;
            spyOn(service, ['partition'] as any).and.returnValue([undefined, []] );
            const retVal = service['getSiteCoreData']({} as any, {'topSports': true} as any) as any;
            retVal.subscribe([{type: ['test']}])
            flush()
        }))

        it('getSiteCoreData', fakeAsync(() => {
            vanillaApiService.post = jasmine.createSpy('post').and.returnValue(of([{type: []}])),
            spyOn(service, ['groupAndFormatOffers'] as any) as any;
            spyOn(service, ['mergeCmsAndSitecoreData'] as any) as any;
            spyOn(service, ['partition'] as any).and.returnValue([undefined, [{title: 'a'}, {title: 'c'},  {title: 'b'},  {title: 'b'}]] );
            const retVal = service['getSiteCoreData']({} as any, {'topSports': true} as any) as any;
            retVal.subscribe([{type: ['test']}])
            flush()
        }))
        
        it('getSiteCoreData 4', fakeAsync(() => {
            vanillaApiService.post = jasmine.createSpy('post').and.returnValue(of([{type: 'TopSports', teasers: ['a']}])),
            spyOn(service, ['groupAndFormatOffers'] as any) as any;
            spyOn(service, ['mergeCmsAndSitecoreData'] as any) as any;
            spyOn(service, ['partition'] as any).and.returnValue([undefined, [{title: 'a'}, {title: 'c'},  {title: 'b'},  {title: 'b'}]] );
            const retVal = service['getSiteCoreData']({} as any, {'topSports': true} as any) as any;
            retVal.subscribe([{type: ['test']}])
            flush()
        }))
    })

    describe('getLibraryOffers', () => {
        it('getLibraryOffers', fakeAsync(() => {
            service['sitecoreVRRootFolder'] = 'sitecoreVRRootFolder';
            const retVal = service['getLibraryOffers']('page' as any);
            retVal.subscribe()
            tick();
        }))

        it('getLibraryOffers without page', fakeAsync(() => {
            service['sitecoreVRRootFolder'] = 'sitecoreVRRootFolder';
            const retVal = service['getLibraryOffers']('' as any);
            retVal.subscribe();
            tick();
        }))

        it('getLibraryOffers without page', fakeAsync(() => {
            service['sitecoreVRRootFolder'] = 'sitecoreVRRootFolder';
            const retVal = service['getLibraryOffers']('virtuals' as any);
            retVal.subscribe();
            tick();
        }))
    })

    describe('getSiteCoreImages', () => {
        it('getSiteCoreImages', fakeAsync(() => {
            spyOn(service,'groupAndFormatOffers' as any)
            spyOn(service, 'getLibraryOffers' as any).and.returnValue(of([{teasers: 'teasers'}]));
            const retVal = service['getSiteCoreImages']('page' as any);
            retVal.subscribe()
            tick();
        }))

        it('getSiteCoreImages qithout teasers', fakeAsync(() => {
            spyOn(service, 'getLibraryOffers' as any).and.returnValue(of([{others: 'teasers'}]));
            const retVal = service['getSiteCoreImages']('page' as any);
            retVal.subscribe()
            tick();
        }))

        it('getSiteCoreImages qithout teasers undefined', fakeAsync(() => {
            spyOn(service, 'getLibraryOffers' as any).and.returnValue(of([]));
            const retVal = service['getSiteCoreImages']('page' as any);
            retVal.subscribe()
            tick();
        }))
    })

    describe('bannerInit', () => {
        it('bannerInit', fakeAsync(() => {
            service['getLibraryOffers'] = jasmine.createSpy('getLibraryOffers').and.returnValue(of(true))
            const retVal = service.bannerInit();
        }))
    })

    describe('triggerGTATracking', () => {
        it('triggerGTATracking', () => {
            service['trackOtherSportsClickGTMEvent'] = jasmine.createSpy('trackOtherSportsClickGTMEvent');
            service.onClickNavigationDetails = {id: 'other sports'} as any;
            const retVal = service.triggerGTATracking('url');
        })

        it('triggerGTATracking', () => {
            // spyOn(service, 'trackTopSportsClickGTMEvent');
            service['trackTopSportsClickGTMEvent'] = jasmine.createSpy('trackTopSportsClickGTMEvent');
            service.onClickNavigationDetails = {id: 'top sports'} as any;
            const retVal = service.triggerGTATracking('url');
        })
    })

    describe('trackOtherSportsClickGTMEvent', () => {
        it('trackOtherSportsClickGTMEvent', () => {
            service['trackOtherSportsClickGTMEvent']({title: 'title'} as any, 'url');
            expect(service.onClickNavigationDetails.id).toBeNull();
        })
    })

    describe('trackTopSportsClickGTMEvent', () => {
        it('trackTopSportsClickGTMEvent', () => {
            service['trackTopSportsClickGTMEvent']({title: 'title'} as any, 'url');
            expect(service.onClickNavigationDetails.id).toBeNull();
        })
    })
});
