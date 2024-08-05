import {
    FiveASideEntrySummaryComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideEntrySummary/fiveaside-entry-summary.component';
import { MY_ENTRIES_LIST, LEGS } from '@app/fiveASideShowDown/mockdata/entryinfo.mock';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { of } from 'rxjs';

describe('FiveASideEntrySummaryComponent', () => {
    let component: FiveASideEntrySummaryComponent;
    let fiveAsideLiveServeUpdatesSubscribeService, pubSubService, coreToolsService, changeDetectorRef, fiveasideLeaderBoardService,
        gtmService, userService;

    beforeEach(() => {
        fiveAsideLiveServeUpdatesSubscribeService = {
            getInitialLegs: jasmine.createSpy('getInitialLegs'),
            unSubscribeShowDownChannels: jasmine.createSpy('unSubscribeShowDownChannels'),
            addEventListneres: jasmine.createSpy('addEventListneres').and.callFake((arg0, fn) => fn()),
            removeAllEventListneres: jasmine.createSpy('removeAllEventListneres'),
            legsUpdateSubscribe: jasmine.createSpy('legsUpdateSubscribe')
        },
            pubSubService = {
                API: pubSubApi,
                subscribe: jasmine.createSpy('subscribe'),
                publish: jasmine.createSpy('publish'),
                unsubscribe: jasmine.createSpy('unsubscribe')
            },
            coreToolsService = {
                uuid: jasmine.createSpy().and.returnValue('122344543')
            },
            fiveasideLeaderBoardService = {
                getDynamicClass: jasmine.createSpy('getDynamicClass').and.returnValue('digitThree'),
                getLegsForEntryId: jasmine.createSpy('getLegsForEntryId').and.returnValue(of(LEGS))
            },
            changeDetectorRef = {
                detectChanges: jasmine.createSpy('detectChanges'),
                markForCheck: jasmine.createSpy('markForCheck')
            },
            gtmService = { push: jasmine.createSpy('push') },
            userService = {
                username: 'Test User'
            },
            component = new FiveASideEntrySummaryComponent(fiveAsideLiveServeUpdatesSubscribeService, pubSubService,
                coreToolsService, changeDetectorRef, fiveasideLeaderBoardService, gtmService, userService);
    });
    it('should create s', () => {
        expect(component).toBeTruthy();
    });

    it('should be an active user', () => {
        component.entryIdList = ['1', '2'];
        component.entryInfo = {} as any;
        component.eventStatus = 'live';
        component['checkActiveUser']();
        expect(component.isActiveUser).toBeFalsy();
    });
    it('should be an active user', () => {
        component.entryIdList = ['1', '2'];
        component.entryInfo = {} as any;
        component.eventStatus = 'pre';
        component['checkActiveUser']();
        expect(component.isActiveUser).toBeFalsy();
    });
    it('should be an active user', () => {
        component.entryInfo = {
            'userId': 'Test User',
            'voided': false,
            'priceNum': '',
            'priceDen': '',
            'overallProgressPct': 0,
            'id': '1',
            'userEntry': true
        };
        component.eventStatus = 'live';
        component['checkActiveUser']();
        expect(component.isActiveUser).toBeTruthy();
    });
    it('should be an active user', () => {
        component.entryInfo = {
            'userId': 'Test User',
            'voided': false,
            'priceNum': '',
            'priceDen': '',
            'overallProgressPct': 0,
            'id': '1',
            'userEntry': true
        };
        component.eventStatus = 'pre';
        component['checkActiveUser']();
        expect(component.isActiveUser).toBeFalsy();
    });

    it('should be an active user', () => {
        component.entryInfo = {
            'userId': 'Test User',
            'voided': false,
            'priceNum': '',
            'priceDen': '',
            'overallProgressPct': 0,
            'id': '1',
            'userEntry': true
        };
        component.eventStatus = 'live';
        component['checkActiveUser']();
        expect(component.isActiveUser).toBeTruthy();
    });
    it('should be an non active user', () => {
        component.entryIdList = ['1', '2'];
        component.entryInfo = {
            'userId': 'Test',
            'voided': false,
            'priceNum': '',
            'priceDen': '',
            'overallProgressPct': 0,
            'id': '6',
            'userEntry': true
        };
        component['checkActiveUser']();
        component.eventStatus = 'pre';
        expect(component.isActiveUser).toBeFalsy();
    });

    it('should be an active user with empty array', () => {
        component.entryIdList = [];
        component.entryInfo = {
            'userId': '1',
            'voided': false,
            'priceNum': '',
            'priceDen': '',
            'overallProgressPct': 0,
            'id': '1',
            'userEntry': true
        };
        component.ngOnInit();
    });
    it('getuserNameMask when username is present', () => {
        expect(component.getuserNameMask('ukgmicti')).toBe('ukgmi***');
    });
    it('getuserNameMask when username is present', () => {
        expect(component.getuserNameMask('ukgmi')).toBe('uk***');
    });
    it('getuserNameMask when username is present', () => {
        expect(component.getuserNameMask('ukgmic')).toBe('ukg***');
    });
    it('getuserNameMask when username is present', () => {
        expect(component.getuserNameMask('ukgmict_ipo')).toBe('ukgmi***');
    });
    it('getuserNameMask when username is not present', () => {
        expect(component.getuserNameMask('')).toBe('');
    });
    it('getuserNameMask when username is undefined', () => {
        expect(component.getuserNameMask(undefined as any)).toBe('');
    });

    it('should be an active user undefined', () => {
        component.entryIdList = ['1', '2'];
        component.entryInfo = {
            'userId': '1',
            'voided': false,
            'priceNum': '',
            'priceDen': '',
            'overallProgressPct': 0,
            'id': '1'
        };
        component.ngOnInit();
    });
    it('should return class based on rank', () => {
        component.entryInfo = { rank: 123 } as any;
        expect(component.getClass()).toEqual('digitThree');
    });
    describe('ngOninit', () => {
        it('ngOninit with isOverlay true', () => {
            component.isOverlay = true;
            component.entryIdList = ['1', '2'];
            spyOn(component as any, 'checkActiveUser');
            spyOn(component as any, 'myEntryUpdate');
            component.eventStatus = 'live';
            component.entryInfo = {
                'userId': '1',
                'voided': false,
                'priceNum': '',
                'priceDen': '',
                'overallProgressPct': 0,
                'id': '1'
            };
            component.ngOnInit();
            expect(component['checkActiveUser']).toHaveBeenCalled();
            expect(pubSubService.subscribe).toHaveBeenCalled();
        });
        it('ngOninit with isOverlay true', () => {
            component.entryIdList = ['1', '2'];
            component.isOverlay = true;
            component.isLeaderboard = true;
            spyOn(component as any, 'myEntryUpdate');
            component.eventStatus = 'live';
            component.entryInfo = {
                'userId': '1',
                'voided': false,
                'priceNum': '',
                'priceDen': '',
                'overallProgressPct': 0,
                'id': '1'
            };
            component.ngOnInit();
            expect(pubSubService.subscribe).toHaveBeenCalled();
        });
        it('ngOninit with isOverlay true', () => {
            component.entryIdList = ['1', '2'];
            component.isOverlay = true;
            component.isLeaderboard = false;
            spyOn(component as any, 'myEntryUpdate');
            component.eventStatus = 'live';
            component.entryInfo = {
                'userId': '1',
                'voided': false,
                'priceNum': '',
                'priceDen': '',
                'overallProgressPct': 0,
                'id': '1'
            };
            component.ngOnInit();
            expect(pubSubService.subscribe).toHaveBeenCalled();
        });
        it('ngOninit with isOverlay false', () => {
            component.entryIdList = ['1', '2'];
            component.isOverlay = false;
            component.isLeaderboard = false;
            spyOn(component as any, 'myEntryUpdate');
            component.eventStatus = 'pre';
            component.entryInfo = {
                'userId': '1',
                'voided': false,
                'priceNum': '',
                'priceDen': '',
                'overallProgressPct': 0,
                'id': '1'
            };
            component.ngOnInit();
            expect(pubSubService.subscribe).toHaveBeenCalled();
        });
        it('ngOninit with isOverlay true', () => {
            component.entryIdList = ['1', '2'];
            component.isOverlay = true;
            component.isLeaderboard = true;
            spyOn(component as any, 'myEntryUpdate');
            component.eventStatus = 'live';
            component.entryInfo = {
                'userId': '1',
                'voided': false,
                'priceNum': '',
                'priceDen': '',
                'overallProgressPct': 0,
                'id': '1'
            };
            component.ngOnInit();
            expect(pubSubService.subscribe).toHaveBeenCalled();
        });
        it('ngOninit with isOverlay true', () => {
            component.entryIdList = ['1', '2'];
            component.isOverlay = true;
            component.isLeaderboard = false;
            spyOn(component as any, 'myEntryUpdate');
            component.eventStatus = 'live';
            component.entryInfo = {
                'userId': '1',
                'voided': false,
                'priceNum': '',
                'priceDen': '',
                'overallProgressPct': 0,
                'id': '1'
            };
            component.ngOnInit();
            expect(pubSubService.subscribe).toHaveBeenCalled();
        });
        it('ngOninit with isOverlay false', () => {
            component.entryIdList = ['1', '2'];
            component.isOverlay = false;
            component.isLeaderboard = false;
            spyOn(component as any, 'myEntryUpdate');
            component.eventStatus = 'pre';
            component.entryInfo = {
                'userId': '1',
                'voided': false,
                'priceNum': '',
                'priceDen': '',
                'overallProgressPct': 0,
                'id': '1'
            };
            component.ngOnInit();
            expect(pubSubService.subscribe).toHaveBeenCalled();
        });
        it('ngOninit with isOverlay false', () => {
            component.entryIdList = ['1', '2'];
            component.isOverlay = false;
            component.isLeaderboard = true;
            spyOn(component as any, 'myEntryUpdate');
            spyOn(component as any, 'checkActiveUser');
            component.eventStatus = 'pre';
            component.entryInfo = {
                'userId': '1',
                'voided': false,
                'priceNum': '',
                'priceDen': '',
                'overallProgressPct': 0,
                'id': '1'
            };
            component.ngOnInit();
            expect(component['checkActiveUser']).toHaveBeenCalled();
            expect(pubSubService.subscribe).toHaveBeenCalled();
        });
        it('ngOninit with isOverlay true', () => {
            component.entryIdList = ['1', '2'];
            component.isOverlay = true;
            spyOn(component as any, 'myEntryUpdate');
            spyOn(component as any, 'checkActiveUser');
            component.eventStatus = 'live';
            component.ngOnInit();
            expect(component['checkActiveUser']).toHaveBeenCalled();
            expect(pubSubService.subscribe).toHaveBeenCalled();
        });
        it('ngOninit with isOverlay false', () => {
            component.entryIdList = ['1', '2'];
            component.isOverlay = false;
            spyOn(component as any, 'myEntryUpdate');
            spyOn(component as any, 'checkActiveUser');
            component.eventStatus = 'pre';
            component.ngOnInit();
            expect(component['checkActiveUser']).toHaveBeenCalled();
            expect(pubSubService.subscribe).toHaveBeenCalled();
        });
    });
    describe('closeAllEntries', () => {
        it('closeAllEntries with isOpened true', () => {
            component.entryInfo = { isOpened: true, isOverlayOpend: false } as any;
            component.componentId = '1234';
            component.closeAllEntryDetails(undefined as any);
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
        });
        it('closeAllEntries with isOverlayOpend true', () => {
            component.entryInfo = { isOpened: false, isOverlayOpend: true } as any;
            component.componentId = '1234';
            component.closeAllEntryDetails(undefined as any);
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
        });
        it('closeAllEntries with isOverlayOpend true', () => {
            component.entryInfo = { isOpened: false, isOverlayOpend: true } as any;
            component.componentId = '56789';
            component.closeAllEntryDetails('56789');
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
        });
        it('closeAllEntries with isOverlayOpend true', () => {
            component.entryInfo = { isOpened: true, isOverlayOpend: true } as any;
            component.componentId = '567899';
            component.closeAllEntryDetails('56789');
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
        });
    });
    describe('#myEntryUpdate', () => {
        it('myEntryUpdate with isOverlayOpened case 0', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 1;
            const myEntries = { update: myentrylist };
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.isOverlay = true;
            component.isLeaderboard = false;
            component.entryInfo.isOverlayOpend = true;
            component.entryInfo.currentIndex = 0;
            component.index = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
        });
        it('myEntryUpdate with isOverlayOpened Case 1', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 1;
            const myEntries = { update: [] };
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOverlayOpend = true;
            component.entryInfo.currentIndex = 0;
            component.index = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
        it('myEntryUpdate with isOverlayOpened Case 2', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 0;
            const myEntries = { update: myentrylist };
            component.index = 0;
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOverlayOpend = true;
            component.entryInfo.currentIndex = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
        it('myEntryUpdate  with isOpened true  Case 3', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 1;
            const myEntries = { update: myentrylist };
            component.index = 0;
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOpened = true;
            component.isLeaderboard = true;
            component.entryInfo.currentIndex = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).toHaveBeenCalled();
        });
        it('myEntryUpdate  with isOpened true', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 0;
            const myEntries = { update: myentrylist };
            component.index = 0;
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOpened = true;
            component.entryInfo.currentIndex = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
        it('myEntryUpdate  with isOpened true with index doesnot match', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 1;
            const myEntries = { update: myentrylist };
            component.index = 10;
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOpened = true;
            component.entryInfo.currentIndex = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
        it('myEntryUpdate  with isOverlayOpened false', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 1;
            const myEntries = { update: myentrylist };
            component.index = 0;
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOverlayOpend = false;
            component.entryInfo.currentIndex = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
        it('myEntryUpdate  with isOpened false', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 1;
            const myEntries = { update: myentrylist };
            component.index = 0;
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOpened = false;
            component.entryInfo.currentIndex = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
    });

    describe('openCloseHandleOverlay', () => {
        it('openCloseHandleOverlay with isOverlayOpend true and entryMatch', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '123434';
            const entryInfo = { componentId: '123434', entryId: '1232434234' };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with isOverlayOpend true and entryMatch with auto true', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '123434';
            component.index = 0;
            const entryInfo = { componentId: '123434', entryId: '1232434234', auto: true };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with isOverlayOpend true and entryMatch with auto true', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '123434';
            component.index = 1;
            const entryInfo = { componentId: '123434', entryId: '1232434234', auto: true };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).not.toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(true);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with isOverlayOpend true and entryMatch with auto true', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '123434';
            component.index = 0;
            const entryInfo = { componentId: '123434', entryId: '1232434234', auto: false };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with isOverlayOpend true and entryMatch with auto false', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '123434';
            const entryInfo = { componentId: '123434', entryId: '1232434234', auto: false };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with is OverlayOpend false and ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = false;
            component.componentId = '123434';
            const entryInfo = { componentId: '123434', entryId: '1232434234' };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.getInitialLegs).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(true);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with is OverlayOpend false and componentId & entryId Mismatch ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '1234345';
            const entryInfo = { componentId: '123434', entryId: '123243423' };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with is OverlayOpend false and entryId mismatch ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '1234345';
            const entryInfo = { componentId: '1234345', entryId: '123243423' };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with is OverlayOpend false and entryId match ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '1234345';
            const entryInfo = { componentId: '123434', entryId: '1232434234' };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
    });
    describe('openCloseHandler', () => {
        it('openCloseHandler with isOverlayOpend true and entryMatch', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = true;
            component.componentId = '123434';
            component.eventStatus = 'live';
            const entryInfo = { componentId: '123434', entryId: '1232434234' };
            component.openCloseHandler(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with isOverlayOpend true and entryMatch', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = true;
            component.componentId = '1234345';
            component.eventStatus = 'live';
            const entryInfo = { componentId: '123434', entryId: '1232434234' };
            component.openCloseHandler(entryInfo);
            expect(component.entryInfo.isOpened).toBe(true);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with isOverlayOpend true and entryMatch', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = true;
            component.componentId = '1234345';
            component.eventStatus = 'live';
            const entryInfo = { componentId: '1234345', entryId: '12324342346' };
            component.openCloseHandler(entryInfo);
            expect(component.entryInfo.isOpened).toBe(true);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });

        it('openCloseHandler with isOverlayOpend true and entryMatch isLeaderboard, isOpened is false', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.componentId = '123434';
            component.eventStatus = 'live';
            component.isLeaderboard = false;
            component.entryInfo.isOpened = false;
            const entryInfo = { componentId: '123434', entryId: '1232434234' };
            component.openCloseHandler(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOpened).toBe(true);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with isOverlayOpend true and entryMatch isLeaderboard is false and isOpened true', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.componentId = '123434';
            component.eventStatus = 'live';
            component.isLeaderboard = false;
            component.entryInfo.isOpened = true;
            const entryInfo = { componentId: '123434', entryId: '1232434234' };
            component.openCloseHandler(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with isOverlayOpend true and entryMatch isLeaderboard, isOpened is true', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.componentId = '123434';
            component.eventStatus = 'live';
            component.isLeaderboard = true;
            component.entryInfo.isOpened = true;
            const entryInfo = { componentId: '123434', entryId: '1232434234' };
            component.openCloseHandler(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });

        it('openCloseHandler with isOverlayOpend true and entryMatch', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = true;
            component.componentId = '123434';
            component.eventStatus = 'live';
            const entryInfo = { componentId: '123434', entryId: '1232434234', auto: true };
            component.openCloseHandler(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).not.toHaveBeenCalled();
            expect(component.entryInfo.isOpened).toBe(true);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with isOverlayOpend true and entryMatch', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = true;
            component.componentId = '123434';
            component.eventStatus = 'live';
            const entryInfo = { componentId: '123434', entryId: '1232434234', auto: false };
            component.openCloseHandler(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with is OverlayOpend false and ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = false;
            component.componentId = '123434';
            component.eventStatus = 'live';
            const entryInfo = { componentId: '123434', entryId: '1232434234' };
            component.openCloseHandler(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.getInitialLegs).toHaveBeenCalled();
            expect(component.entryInfo.isOpened).toBe(true);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with is OverlayOpend false and entryId mismatch ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = true;
            component.componentId = '1234345';
            component.eventStatus = 'pre';
            const entryInfo = { componentId: '1234345', entryId: '1232434234' };
            component.openCloseHandler(entryInfo);
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with is OverlayOpend false and entryId mismatch ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = true;
            component.componentId = '1234345';
            component.eventStatus = 'pre';
            const entryInfo = { componentId: '1234345', entryId: '12324342346' };
            component.openCloseHandler(entryInfo);
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with is OverlayOpend false and entryId mismatch ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = false;
            component.componentId = '1234345';
            component.eventStatus = 'pre';
            const entryInfo = { componentId: '1234345', entryId: '1232434234' };
            component.openCloseHandler(entryInfo);
            expect(component.entryInfo.isOpened).toBe(true);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
    });
    describe('onCLick', () => {
        it('onClick with isOverlay true', () => {
            component.isOverlay = true;
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.componentId = '123445';
            component.onClick();
            expect(pubSubService.publish).
                toHaveBeenCalledWith('CLOSE_ALL_ENTRIES_OVERLAY', { componentId: '123445', entryId: MY_ENTRIES_LIST[0].id });
        });
        it('onClick with isOverlay false', () => {
            component.isOverlay = false;
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.componentId = '123445';
            component.onClick();
            expect(pubSubService.publish).
                toHaveBeenCalledWith('CLOSE_ALL_ENTRIES', { componentId: '123445', entryId: MY_ENTRIES_LIST[0].id });
        });
    });

    describe('ngDestroy', () => {
        it('ngDestroy', () => {
            component.componentId = '1234';
            component.legDetails = [{} as any, {} as any, {} as any, {} as any, {} as any];
            component.outcomeIds = ['123455', '345455'];
            component.entryInfo = { isOverlayOpend: true, isOpened: true } as any;
            component.eventStatus = 'live';
            component.ngOnDestroy();
            expect(pubSubService.unsubscribe).toHaveBeenCalledWith('1234');
            expect(component.outcomeIds.length).toBe(0);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
        });
        it('ngDestroy when event is in preplay state', () => {
            component.componentId = '1234';
            component.legDetails = [{} as any, {} as any, {} as any, {} as any, {} as any];
            component.outcomeIds = ['123455', '345455'];
            component.entryInfo = { isOverlayOpend: true, isOpened: true } as any;
            component.eventStatus = 'pre';
            component.ngOnDestroy();
            expect(pubSubService.unsubscribe).toHaveBeenCalledWith('1234');
            expect(component.outcomeIds.length).toBe(0);
        });
    });
    describe('legsInitialHandlers', () => {
        it('legsInitialHandlers', () => {
            component.entryInfo = { legs: [] } as any;
            component.legsInitialHandlers(MY_ENTRIES_LIST[0].legs as any);
            expect(component.legDetails).not.toBeUndefined();
        });
    });

    it('#entryOpenCloseTrack should call gtm service(LeaderBoard)', () => {
        component.entryInfo = { id: 123 } as any;
        component.isLeaderboard = true;
        component['entryOpenCloseTrack' as any]('1abcd2', 'open');
        expect(gtmService.push).toHaveBeenCalled();
    });
    it('#entryOpenCloseTrack should call gtm service(MyEntries)', () => {
        component.entryInfo = { id: 123 } as any;
        component.isLeaderboard = false;
        component['entryOpenCloseTrack' as any]('1abcd2', 'open');
        expect(gtmService.push).toHaveBeenCalled();
    });

    describe('closeAllEntries', () => {
        it('closeAllEntries with isOpened true', () => {
            component.entryInfo = { isOpened: true, isOverlayOpend: false } as any;
            component.componentId = '1234';
            component.closeAllEntryDetails(undefined as any);
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
        });
        it('closeAllEntries with isOpened true', () => {
            component.entryInfo = { isOpened: true, isOverlayOpend: true } as any;
            component.componentId = '1234';
            component.closeAllEntryDetails(undefined as any);
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
        });
        it('closeAllEntries with isOpened true', () => {
            component.entryInfo = { isOpened: false, isOverlayOpend: false } as any;
            component.componentId = '1234';
            component.closeAllEntryDetails(undefined as any);
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).not.toHaveBeenCalled();
        });
        it('closeAllEntries with isOverlayOpend true', () => {
            component.entryInfo = { isOpened: false, isOverlayOpend: true } as any;
            component.componentId = '1234';
            component.closeAllEntryDetails(undefined as any);
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
        });
    });
    describe('#myEntryUpdate', () => {
        it('myEntryUpdate with isOverlayOpened case 0', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 1;
            const myEntries = { update: myentrylist };
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOverlayOpend = true;
            component.entryInfo.currentIndex = 0;
            component.index = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
        it('myEntryUpdate with isOverlayOpened Case 1', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 1;
            const myEntries = { update: [] };
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOverlayOpend = true;
            component.entryInfo.currentIndex = 0;
            component.index = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
        it('myEntryUpdate with isOverlayOpened Case 2', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 0;
            const myEntries = { update: myentrylist };
            component.index = 0;
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOverlayOpend = true;
            component.entryInfo.currentIndex = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
        it('myEntryUpdate  with isOpened true  Case 3', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 1;
            const myEntries = { update: myentrylist };
            component.index = 0;
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOpened = true;
            component.isLeaderboard = true;
            component.entryInfo.currentIndex = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).toHaveBeenCalled();
        });
        it('myEntryUpdate  with isOpened true', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 0;
            const myEntries = { update: myentrylist };
            component.index = 0;
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOpened = true;
            component.entryInfo.currentIndex = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
        it('myEntryUpdate  with isOpened true with index doesnot match', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 1;
            const myEntries = { update: myentrylist };
            component.index = 10;
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOpened = true;
            component.entryInfo.currentIndex = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
        it('myEntryUpdate  with isOverlayOpened false', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 1;
            const myEntries = { update: myentrylist };
            component.index = 0;
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOverlayOpend = false;
            component.entryInfo.currentIndex = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
        it('myEntryUpdate  with isOpened false', () => {
            const myentrylist = MY_ENTRIES_LIST as any;
            myentrylist[0].previousIndex = 1;
            const myEntries = { update: myentrylist };
            component.index = 0;
            component.entryInfo = {} as any;
            component.prizePoolData = {} as any;
            component.entryInfo.isOpened = false;
            component.entryInfo.currentIndex = 0;
            pubSubService.subscribe.and.callFake((sb, ch, fn) => {
                fn(myEntries);
            });
            component.myEntryUpdate();
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
    });

    describe('openCloseHandleOverlay', () => {
        it('openCloseHandleOverlay with isOverlayOpend true and entryMatch', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '123434';
            const entryInfo = { componentId: '123434', entryId: '1232434234' };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with isOverlayOpend true and entryMatch with auto true', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '123434';
            component.index = 0;
            const entryInfo = { componentId: '123434', entryId: '1232434234', auto: true };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with isOverlayOpend true and entryMatch with auto true', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '123434';
            component.index = 1;
            const entryInfo = { componentId: '123434', entryId: '1232434234', auto: true };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).not.toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(true);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with isOverlayOpend true and entryMatch with auto true', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '123434';
            component.index = 0;
            const entryInfo = { componentId: '123434', entryId: '1232434234', auto: false };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with isOverlayOpend true and entryMatch with auto false', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '123434';
            const entryInfo = { componentId: '123434', entryId: '1232434234', auto: false };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with is OverlayOpend false and ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = false;
            component.componentId = '123434';
            const entryInfo = { componentId: '123434', entryId: '1232434234' };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.getInitialLegs).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(true);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with is OverlayOpend false and componentId & entryId Mismatch ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '1234345';
            const entryInfo = { componentId: '123434', entryId: '123243423' };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandleOverlay with is OverlayOpend false and entryId mismatch ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOverlayOpend = true;
            component.componentId = '1234345';
            const entryInfo = { componentId: '1234345', entryId: '123243423' };
            component.openCloseHandleOverlay(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOverlayOpend).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
    });
    describe('openCloseHandler', () => {
        it('openCloseHandler with isOverlayOpend true and entryMatch', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = true;
            component.componentId = '123434';
            component.eventStatus = 'live';
            const entryInfo = { componentId: '123434', entryId: '1232434234' };
            component.openCloseHandler(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with isOverlayOpend true and entryMatch', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = true;
            component.componentId = '123434';
            component.eventStatus = 'live';
            const entryInfo = { componentId: '123434', entryId: '1232434234', auto: true };
            component.openCloseHandler(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).not.toHaveBeenCalled();
            expect(component.entryInfo.isOpened).toBe(true);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with isOverlayOpend true and entryMatch', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = true;
            component.componentId = '123434';
            component.eventStatus = 'live';
            const entryInfo = { componentId: '123434', entryId: '1232434234', auto: false };
            component.openCloseHandler(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with is OverlayOpend false and ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = false;
            component.componentId = '123434';
            component.eventStatus = 'live';
            const entryInfo = { componentId: '123434', entryId: '1232434234' };
            component.openCloseHandler(entryInfo);
            expect(fiveAsideLiveServeUpdatesSubscribeService.getInitialLegs).toHaveBeenCalled();
            expect(component.entryInfo.isOpened).toBe(true);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with is OverlayOpend false and entryId mismatch ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = true;
            component.componentId = '1234345';
            component.eventStatus = 'pre';
            const entryInfo = { componentId: '1234345', entryId: '1232434234' };
            component.openCloseHandler(entryInfo);
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with is OverlayOpend false and entryId mismatch ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = true;
            component.componentId = '1234345';
            component.eventStatus = 'pre';
            const entryInfo = { componentId: '1234345', entryId: '12324342346' };
            component.openCloseHandler(entryInfo);
            expect(component.entryInfo.isOpened).toBe(false);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
        it('openCloseHandler with is OverlayOpend false and entryId mismatch ', () => {
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.entryInfo.isOpened = false;
            component.componentId = '1234345';
            component.eventStatus = 'pre';
            const entryInfo = { componentId: '1234345', entryId: '1232434234' };
            component.openCloseHandler(entryInfo);
            expect(component.entryInfo.isOpened).toBe(true);
            expect(component.channel).toBe(`ENTRYINFO::${component.entryInfo.id}`);
        });
    });
    describe('onCLick', () => {
        it('onClick with isOverlay true', () => {
            component.isOverlay = true;
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.componentId = '123445';
            component.onClick();
            expect(pubSubService.publish).
                toHaveBeenCalledWith('CLOSE_ALL_ENTRIES_OVERLAY', { componentId: '123445', entryId: MY_ENTRIES_LIST[0].id });
        });
        it('onClick with isOverlay false', () => {
            component.isOverlay = false;
            component.entryInfo = MY_ENTRIES_LIST[0] as any;
            component.componentId = '123445';
            component.onClick();
            expect(pubSubService.publish).
                toHaveBeenCalledWith('CLOSE_ALL_ENTRIES', { componentId: '123445', entryId: MY_ENTRIES_LIST[0].id });
        });
    });

    describe('ngDestroy', () => {
        it('ngDestroy', () => {
            component.componentId = '1234';
            component.legDetails = [{} as any, {} as any, {} as any, {} as any, {} as any];
            component.outcomeIds = ['123455', '345455'];
            component.entryInfo = { isOverlayOpend: true, isOpened: true } as any;
            component.eventStatus = 'live';
            component.ngOnDestroy();
            expect(pubSubService.unsubscribe).toHaveBeenCalledWith('1234');
            expect(component.outcomeIds.length).toBe(0);
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
        });
        it('ngDestroy when event is in preplay state', () => {
            component.componentId = '1234';
            component.legDetails = [{} as any, {} as any, {} as any, {} as any, {} as any];
            component.outcomeIds = ['123455', '345455'];
            component.entryInfo = { isOverlayOpend: true, isOpened: true } as any;
            component.eventStatus = 'pre';
            component.ngOnDestroy();
            expect(pubSubService.unsubscribe).toHaveBeenCalledWith('1234');
            expect(component.outcomeIds.length).toBe(0);
        });
    });
    describe('legsInitialHandlers', () => {
        it('legsInitialHandlers', () => {
            component.entryInfo = { legs: [] } as any;
            component.legsInitialHandlers(MY_ENTRIES_LIST[0].legs as any);
            expect(component.legDetails).not.toBeUndefined();
        });
    });

    it('#entryOpenCloseTrack should call gtm service', () => {
        component.entryInfo = { id: 123 } as any;
        component['entryOpenCloseTrack' as any]('1abcd2', 'open');
        expect(gtmService.push).toHaveBeenCalled();
    });

    it('#postOnClick when isOverlay is false', () => {
        component.entryInfo = MY_ENTRIES_LIST[0] as any;
        component.entryInfo.outcomeIds = ['1276513011', '1276142011', '1276524684', '1276312971', '1276524685'];
        component.isOverlay = false;
        spyOn(component as any, 'legsInitialHandlers');
        spyOn(component as any, 'handleEntryUpdate');
        component.postOnClick();
        expect(fiveasideLeaderBoardService.getLegsForEntryId)
        .toHaveBeenCalledWith('1276513011,1276142011,1276524684,1276312971,1276524685');
        expect(component.legsInitialHandlers).toHaveBeenCalledWith(LEGS);
        expect(component.entryInfo.legs).toEqual(LEGS);
        expect(component['handleEntryUpdate']).toHaveBeenCalled();
    });
    it('#postOnClick when isOverlay is true', () => {
        component.entryInfo = MY_ENTRIES_LIST[0] as any;
        component.entryInfo.outcomeIds
            = ['1276513011', '1276142011', '1276524684', '1276312971', '1276524685'];
        component.isOverlay = true;
        spyOn(component as any, 'legsInitialHandlers');
        spyOn(component as any, 'handleEntryUpdate');
        component.postOnClick();
        expect(component.legsInitialHandlers).not.toHaveBeenCalledWith(LEGS);
    });
    describe('checkActiveUser', () => {
        it('checkActiveUser positive scenario', () => {
            component['entryIdList'] = ['1', '2'];
            component.eventStatus = 'live';
            component.entryInfo = { userId: 'Test User', id: '1'} as any;
            component.legsInitialHandlers(MY_ENTRIES_LIST[0].legs as any);
            expect(component.legDetails).not.toBeUndefined();
        });
        it('checkActiveUser positive scenario', () => {
            component['entryIdList'] = ['3', '4'];
            component.eventStatus = 'pre';
            component.entryInfo = { userId: 'Test User1', id: '1'} as any;
            component.legsInitialHandlers(MY_ENTRIES_LIST[0].legs as any);
            expect(component.legDetails).not.toBeUndefined();
        });
        it('checkActiveUser positive scenario 1p 1n', () => {
            component['entryIdList'] = ['3', '4'];
            component.eventStatus = 'live';
            component.entryInfo = { userId: 'Test User', id: '1'} as any;
            component.legsInitialHandlers(MY_ENTRIES_LIST[0].legs as any);
            expect(component.legDetails).not.toBeUndefined();
        });
        it('checkActiveUser positive scenario 1n 1p', () => {
            component['entryIdList'] = ['1', '2'];
            component.eventStatus = 'live';
            component.entryInfo = { userId: 'Test User1', id: '1'} as any;
            component.legsInitialHandlers(MY_ENTRIES_LIST[0].legs as any);
            expect(component.legDetails).not.toBeUndefined();
        });
        it('checkActiveUser incase of error', () => {
            component['entryIdList'] = undefined;
            component.eventStatus = 'live';
            component.entryInfo = { userId: 'Test User1', id: '1'} as any;
            spyOn(console,'warn');
            component['checkActiveUser']();
            expect(console.warn).toHaveBeenCalled();
        });
    });

    describe('legsInitialHandlers', () => {
        it('legsInitialHandlers', () => {
            component.entryInfo = { legs: [] } as any;
            component.legsInitialHandlers(MY_ENTRIES_LIST[0].legs as any);
            expect(component.legDetails).not.toBeUndefined();
        });
    });

    it('#entryOpenCloseTrack should call gtm service', () => {
        component.entryInfo = { id: 123 } as any;
        component['entryOpenCloseTrack' as any]('1abcd2', 'open');
        expect(gtmService.push).toHaveBeenCalled();
    });

    it('#postOnClick when isOverlay is false', () => {
        component.entryInfo = MY_ENTRIES_LIST[0] as any;
        component.entryInfo.outcomeIds = ['1276513011', '1276142011', '1276524684', '1276312971', '1276524685'];
        component.isOverlay = false;
        spyOn(component as any, 'legsInitialHandlers');
        spyOn(component as any, 'handleEntryUpdate');
        component.postOnClick();
        expect(fiveasideLeaderBoardService.getLegsForEntryId)
        .toHaveBeenCalledWith('1276513011,1276142011,1276524684,1276312971,1276524685');
        expect(component.legsInitialHandlers).toHaveBeenCalledWith(LEGS);
        expect(component.entryInfo.legs).toEqual(LEGS);
        expect(component['handleEntryUpdate']).toHaveBeenCalled();
    });
    it('#postOnClick when isOverlay is true', () => {
        component.entryInfo = MY_ENTRIES_LIST[0] as any;
        component.entryInfo.outcomeIds
            = ['1276513011', '1276142011', '1276524684', '1276312971', '1276524685'];
        component.isOverlay = true;
        spyOn(component as any, 'legsInitialHandlers');
        spyOn(component as any, 'handleEntryUpdate');
        component.postOnClick();
        expect(component.legsInitialHandlers).not.toHaveBeenCalledWith(LEGS);
    });
});
