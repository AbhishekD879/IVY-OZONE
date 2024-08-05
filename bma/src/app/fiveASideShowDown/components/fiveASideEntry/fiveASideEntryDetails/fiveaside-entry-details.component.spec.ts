import { MY_ENTRIES_LIST } from '@app/fiveASideShowDown/mockdata/entryinfo.mock';
import {
    FiveASideEntryDetailsComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryDetails/fiveaside-entry-details.component';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';

describe('FiveASideEntryDetailsComponent', () => {
    let component: FiveASideEntryDetailsComponent;
    let fiveASideEntryInfoService, fiveAsideLiveServeUpdatesSubscribeService,
        pubSubService, coreToolsService, changeDetectorRef, gtmService, windowRef,deviceService;

    beforeEach((() => {
        fiveASideEntryInfoService = {
            outComesFormation: jasmine.createSpy('outComesFormation').and.returnValue(MY_ENTRIES_LIST[0].legs)
        };
        fiveAsideLiveServeUpdatesSubscribeService = {
            legsUpdateSubscribe: jasmine.createSpy('legsUpdateSubscribe'),
            unSubscribeShowDownChannels: jasmine.createSpy('unSubscribeShowDownChannels'),
        };
        pubSubService = {
            API: pubSubApi,
            subscribe: jasmine.createSpy('subscribe'),
            publish: jasmine.createSpy('publish'),
            unsubscribe: jasmine.createSpy('unsubscribe')
        },
            coreToolsService = {
                uuid: jasmine.createSpy().and.returnValue('122344543')
            },
            changeDetectorRef = {
                detectChanges: jasmine.createSpy('detectChanges')
            },
            gtmService = {
                push: jasmine.createSpy('push')
            },
            windowRef = {
            nativeWindow: {
                scrollTo: jasmine.createSpy(),
                scroll:jasmine.createSpy(),
                scrollY: 5
            },
                document: {
                  querySelector: jasmine.createSpy('querySelector').and.returnValue({
                    getBoundingClientRect:jasmine.createSpy('getBoundingClientRect').and.returnValue({height:10})
                  })
                }
              };
            deviceService = {
                isDesktop :true
            };
        component = new FiveASideEntryDetailsComponent(fiveASideEntryInfoService,
            pubSubService, coreToolsService,
            fiveAsideLiveServeUpdatesSubscribeService, changeDetectorRef, gtmService, windowRef, deviceService);
    }));

    describe('ngOnInit', () => {
        it('ngOnInit for live', () => {
            component.outComes = MY_ENTRIES_LIST[0].legs as any;
            spyOn(component, 'getOutcomeIds');
            spyOn(component as any, 'myEntryListenerForEntryExpansion');
            component.eventStatus = 'live';
            component.ngOnInit();
            expect(component.data[0].outcomeId).toBe('1276513011');
        });
        it('ngOnInit for pre', () => {
            component.outComes = MY_ENTRIES_LIST[0].legs as any;
            spyOn(component, 'getOutcomeIds');
            spyOn(component as any, 'myEntryListenerForEntryExpansion');
            component.eventStatus = 'pre';
            component.ngOnInit();
            expect(component.data[0].outcomeId).toBe('1276513011');
            expect(component.getOutcomeIds).not.toHaveBeenCalled();
        });
    });
    describe('outComeChangeUpdate', () => {
        it('outComeChangeUpdate', () => {
            component.outComeChangeUpdate({ previous: ['123456', '45678', '98765'], current: ['456788', '876555', '6554435'] });
            expect(component.outcomeIds.length).toEqual(3);
        });
    });
    describe('ngOnChnages', () => {
        it('ngOnChanges', () => {
            component.ngOnChanges({ outComes: [{ outcomeId: '1234' }, { outcomeId: '4556' }] } as any);
            expect(fiveASideEntryInfoService.outComesFormation).toHaveBeenCalled();
        });
        it('ngOnChnages', () => {
            component.ngOnChanges({} as any);
            expect(fiveASideEntryInfoService.outComesFormation).not.toHaveBeenCalled();
        });
    });
    describe('ngOnDestory', () => {
        it('ngOnDestory', () => {
            component.outComes = [{} as any];
            component.outcomeIds = ['123545'];
            component.eventStatus = 'live';
            component.ngOnDestroy();
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).not.toHaveBeenCalled();
        });
        it('ngOnDestory', () => {
            component.outComes = [{} as any];
            component.outcomeIds = ['123545'];
            component.eventStatus = 'pre';
            component.ngOnDestroy();
            expect(component.outcomeIds.length).toBe(0);
        });
    });
    describe('getOutcomeIds', () => {
        it('getOutcomeIds', () => {
            component.outComes = MY_ENTRIES_LIST[0].legs as any;
            component.getOutcomeIds();
            expect(component.outcomeIds.length).not.toBe(0);
        });
    });
    describe('jumpToEntry', () => {
        it('jumpToEntry isTopEntry as true', () => {
            spyOn(component, 'trackGTMEvent');
            component.isTopEntry = true;
            component.closeDetails.emit = jasmine.createSpy('emit');
            spyOn(component, 'desktopScroll');
            spyOn(component, 'hideEntryDetails');
            component.jumpToEntry();
            expect(pubSubService.publish).toHaveBeenCalled();
            expect(component.trackGTMEvent).toHaveBeenCalled();
        });
        it('hideEntryDetails', () => {
            windowRef.document.querySelector.and.returnValue({ style: { display: {} } });
            component.hideEntryDetails();
        });
        it('hideEntryDetails', () => {
            windowRef.document.querySelector.and.returnValue(undefined);
            component.hideEntryDetails();
        });
        it('jumpToEntry isTopEntry as false', () => {
            spyOn(component, 'trackGTMEvent');
            component.isTopEntry = false;
            component.closeDetails.emit = jasmine.createSpy('emit');
            spyOn(component, 'desktopScroll');
            component.jumpToEntry();
            expect(pubSubService.publish).toHaveBeenCalled();
            expect(component.trackGTMEvent).toHaveBeenCalled();
        });
        it('jumpToEntry isTopEntry as false', () => {
            spyOn(component, 'trackGTMEvent');
            component.isTopEntry = false;
            component.closeDetails.emit = jasmine.createSpy('emit');
            deviceService.isDesktop=false;
            spyOn(component, 'desktopScroll');
            component.jumpToEntry();
            expect(pubSubService.publish).toHaveBeenCalled();
            expect(component.trackGTMEvent).toHaveBeenCalled();
        });
    });
    describe('desktopScroll', () => {
        it('desktopScroll', () => {
            const event = { scrollIntoView:jasmine.createSpy('scrollIntoView') } as any;
            component.desktopScroll(event,10);
            expect(windowRef.nativeWindow.scrollTo).toHaveBeenCalled();
        });
        it('desktopScroll', () => {
            component.desktopScroll(undefined as any,10);
            expect(windowRef.nativeWindow.scrollTo).toHaveBeenCalled();
        });
        it('desktopScroll', () => {
            const event = { scrollIntoView:jasmine.createSpy('scrollIntoView') } as any;
            windowRef.nativeWindow.scrollY = 0;
            component.desktopScroll(event,10);
            expect(windowRef.nativeWindow.scrollTo).not.toHaveBeenCalled();
        });
    });
    describe('trackGTMEvent', () => {
        it('trackGTMEvent', () => {
            component.trackGTMEvent('MyEntry', 'Click', 'JumpToEntry');
            expect(gtmService.push).toHaveBeenCalled();
        });
    });

    describe('#myEntryListenerForEntryExpansion', () => {
        it('should publish ENTRY_OPENED_TUTORIAL_OVERLAY', () => {
            component.isLeaderboard = false;
            component['myEntryListenerForEntryExpansion']();
            expect(pubSubService.publish).toHaveBeenCalled();
        });
        it('should not publish ENTRY_OPENED_TUTORIAL_OVERLAY', () => {
            component.isLeaderboard = true;
            component['myEntryListenerForEntryExpansion']();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
    });
});
