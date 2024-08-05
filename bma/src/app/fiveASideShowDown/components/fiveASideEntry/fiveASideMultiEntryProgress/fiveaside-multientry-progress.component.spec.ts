import {
    FiveASideMultiEntryProgressComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideMultiEntryProgress/fiveaside-multientry-progress.component';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
describe('FiveASideMultiEntryProgressComponent', () => {
    let component: FiveASideMultiEntryProgressComponent;
    let pubsub, coreToolsService, gtmService,changeDetectorRef;

    beforeEach(() => {
        pubsub = {
            publish: jasmine.createSpy('publish'),
            publishSync: jasmine.createSpy('publishSync'),
            subscribe: jasmine.createSpy('subscribe'),
            unsubscribe: jasmine.createSpy('unsubscribe'),
            API: pubSubApi
        },
            coreToolsService = {
                uuid: jasmine.createSpy().and.returnValue('122344543')
            },
            gtmService = {
                push: jasmine.createSpy()
            },
            changeDetectorRef = {
                detectChanges: jasmine.createSpy('detectChanges'),
                markForCheck: jasmine.createSpy('markForCheck')
            },
            component = new FiveASideMultiEntryProgressComponent(pubsub, coreToolsService, gtmService,changeDetectorRef);
    });
    describe('ngAfterViewInit', () => {
        beforeEach(() => {
            component.contestInfo = { contestSize: 20 } as any;
            component.prize = {};
            component.isDisabled = false;
            component.inputElement = {
                nativeElement: {
                    style: {
                    }
                }
            };
        });
        it('when totalPrizess passed', () => {
            component.prize = { totalPrizes: 20 } as any;
            component.ngAfterViewInit();
            expect(component.inputElement).not.toBeUndefined();
        });

        it('when totalPrizes passed and contest size is 1', () => {
            component.contestInfo = { contestSize: 1 } as any;
            component.prize = { totalPrizes: 20 } as any;
            component.ngAfterViewInit();
            expect(component.inputElement).not.toBeUndefined();
        });
    });
    describe('#parserank', () => {
        it('should return first value in the string', () => {
            const result = component.parserank('1=');
            expect(result).toEqual('1');
        });
    });
    describe('#ngOnInit', () => {
        it('should call required methods', () => {
            spyOn(component, 'updateRankEntryProgress');
            component.myEntriesList = [];
            component.componentId = '123';
            component.ngOnInit();
            expect(component.updateRankEntryProgress).toHaveBeenCalled();
        });
    });
    describe('#ngOnChanges', () => {
        it('ngOnChanges', () => {
            spyOn(component, 'updateRankEntryProgress');
            component.ngOnChanges({ myEntriesList: { isFirstChange: () => false,previousValue:{value:1} } } as any);
            expect(component.updateRankEntryProgress).toHaveBeenCalled();
        });
        it('ngOnChanges', () => {
            spyOn(component, 'updateRankEntryProgress');
            component.ngOnChanges({ myEntriesList: { isFirstChange: () => true } } as any);
            expect(component.updateRankEntryProgress).not.toHaveBeenCalled();
        });
        it('ngOnChanges', () => {
            spyOn(component, 'updateRankEntryProgress');
            const changes = {} as any;
            component.ngOnChanges(changes);
            expect(component.updateRankEntryProgress).not.toHaveBeenCalled();
        });
    });
    describe('#updateRankEntryProgress', () => {
        it('should update for the entry', () => {
            const myEntriesList = [{ rank: '1=', rankProgress: '' }] as any;
            component.contestInfo = { contestSize: 5 } as any;
            component.updateRankEntryProgress(myEntriesList);
            expect(myEntriesList[0].rankProgress).toEqual(80);
        });
        it('should update for the entry', () => {
            const myEntriesList = [{ rank: '1=', rankProgress: '' }] as any;
            component.contestInfo = { contestSize: 250 } as any;
            component.updateRankEntryProgress(myEntriesList);
            expect(myEntriesList[0].rankProgress).toEqual(99);
        });
    });
    describe('widgetClick', () => {
        it('widgetClick', () => {
            component.openAllMyEntries = false;
            spyOn(component,'trackGTMEvent');
            component.myEntriesList = [{} as any, {} as any];
            component.widgetClick();
            expect(pubsub.publish).toHaveBeenCalled();
            expect(component.openAllMyEntries).toBe(true);
            expect(component.trackGTMEvent).toHaveBeenCalled();
        });
        it('widgetClick', () => {
            component.openAllMyEntries = false;
            spyOn(component,'trackGTMEvent');
            component.myEntriesList = undefined as any;
            component.widgetClick();
            expect(pubsub.publish).not.toHaveBeenCalled();
            expect(component.trackGTMEvent).not.toHaveBeenCalled();
        });
        it('widgetClick', () => {
            component.openAllMyEntries = false;
            spyOn(component,'trackGTMEvent');
            component.myEntriesList = [{} as any];
            component.widgetClick();
            expect(pubsub.publish).not.toHaveBeenCalled();
            expect(component.trackGTMEvent).not.toHaveBeenCalled();
        });
    });
    describe('trackGTMEvent', () => {
        it('trackGTMEvent', () => {
            component.trackGTMEvent('Open', 'ViewAllEntries', 'AllEntries');
            expect(gtmService.push).toHaveBeenCalled();
        });
    });
    describe('overlayClear', () => {
        it('overlayClear', () => {
            component.openAllMyEntries = true;
            component.overlayClear();
            expect(component.openAllMyEntries).toBe(false);
        });
    });

});
