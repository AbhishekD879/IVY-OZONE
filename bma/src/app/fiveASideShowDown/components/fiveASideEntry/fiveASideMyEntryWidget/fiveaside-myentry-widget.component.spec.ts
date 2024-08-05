import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { MY_ENTRIES_LIST } from '@app/fiveASideShowDown/mockdata/entryinfo.mock';
import {
    USER_SHOWDOWN_DATA_NO_DISPLAY
  } from '@app/fiveASideShowDown/components/fiveASideLiveLeaderBoard/fiveaside-live-leader-board.mock';
import {
    FiveASideEntryWidgetComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideMyEntryWidget/fiveaside-myentry-widget.component';
import {
    of as observableOf
} from 'rxjs';

describe('FiveASideEntryWidgetComponent', () => {
    let component: FiveASideEntryWidgetComponent;
    let fiveAsideLiveServeUpdatesSubscribeService, userService,pubSubService,fiveasideLeaderBoardService,changeDetectorRef,
    awsService, coreToolsService;

    beforeEach(() => {
        fiveAsideLiveServeUpdatesSubscribeService = {
            userEntryUpdates: jasmine.createSpy('userEntryUpdates').and.callFake((arg0, fn, arg2) => fn()),
            unSubscribeShowDownChannels: jasmine.createSpy('unSubscribeShowDownChannels')
        };
        userService = {
            username: 'test_gvc'
        };
        fiveasideLeaderBoardService = {
            getContestPrizeById: jasmine.createSpy('getContestPrizeById').and.returnValue(observableOf({} as any))
        };
        coreToolsService = {
            uuid: jasmine.createSpy('uuid').and.returnValue('123abc')
        };
        awsService = {
            addAction: jasmine.createSpy('addAction')
        };
        pubSubService = {
            API: pubSubApi,
            subscribe: jasmine.createSpy('subscribe'),
            publish: jasmine.createSpy('publish'),
            unsubscribe: jasmine.createSpy('unsubscribe')
        };
        changeDetectorRef = {
            detectChanges: jasmine.createSpy('detectChanges'),
            markForCheck: jasmine.createSpy('markForCheck')
        };
        component = new FiveASideEntryWidgetComponent(fiveAsideLiveServeUpdatesSubscribeService, userService,
            coreToolsService, fiveasideLeaderBoardService, changeDetectorRef, pubSubService, awsService);
    });

    describe('ngOnInit', () => {
        it('ngOninit', () => {
            const myEntries = { update: MY_ENTRIES_LIST};
            pubSubService.subscribe.and.callFake((a, method, cb) => {
                cb(myEntries);
              });
            spyOn(component, 'updateHandler');
            component.contestId = '123434';
            component.myEntriesList = MY_ENTRIES_LIST as any;
            component.leaderboardData = USER_SHOWDOWN_DATA_NO_DISPLAY;
            component.prize = USER_SHOWDOWN_DATA_NO_DISPLAY.prizeMap;
            component.ngOnInit();
            expect(component['updateHandler']).toHaveBeenCalled();
        });
    });
    describe('#updateHandler', () => {
        it('should not publish data, if update throws empty entry summary', () => {
            component.updateHandler(null as any);
            expect(pubSubService.publish).not.toHaveBeenCalled();
        });
        it('should publish data and not log aws action if data is valid', () => {
            component.myEntriesList = MY_ENTRIES_LIST as any;
            component.updateHandler(MY_ENTRIES_LIST as any);
            expect(component.myEntriesList.length).not.toBe(0);
            expect(pubSubService.publish).toHaveBeenCalled();
        });
        it('should publish data and log aws action if data is not valid', () => {
            component.myEntriesList = MY_ENTRIES_LIST as any;
            component.updateHandler([]);
            expect(awsService.addAction).toHaveBeenCalled();
        });
    });

    describe('ngOnDestroy', () => {
        it('ngOnDestroy', () => {
            spyOn(component, 'updateHandler');
            component.ngOnDestroy();
            expect(fiveAsideLiveServeUpdatesSubscribeService.unSubscribeShowDownChannels).toHaveBeenCalled();
        });
    });
});
