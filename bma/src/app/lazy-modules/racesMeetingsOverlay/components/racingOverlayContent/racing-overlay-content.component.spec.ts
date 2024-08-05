
import { RacingOverlayContentComponent } from './racing-overlay-content.component';
import { overlayContentDataMock, sportEventsData as eventsData} from './mocks/overlay-sport-data.mock';

describe('RacingOverlayContentComponent ', () => {
    let component, horseRacingService, command,
        liveServeHandleUpdatesService, gtmService, locale, windowRef,deviceService; 
    const querySelector = true;


    beforeEach(() => {
        liveServeHandleUpdatesService = {
            subscribe: jasmine.createSpy('subscribe').and.callFake((a,b)=>{b();}),
            unsubscribe: jasmine.createSpy('unsubscribe')
        };
        command = {
            API: { HR_ENHANCED_MULTIPLES_EVENTS: 'HR_ENHANCED_MULTIPLES_EVENTS' }
        };
        horseRacingService = {
          
            groupByFlagCodesAndClassesTypeNames: jasmine.createSpy('groupByFlagCodesAndClassesTypeNames').and.returnValue({groupedRacing: eventsData})
        };
        locale = {
            getString: jasmine.createSpy('getString').and.returnValue('tomorrow')
        };
        gtmService = {
            push: jasmine.createSpy('push')
        }

        windowRef = {
            nativeWindow: {
              setTimeout: jasmine.createSpy().and.callFake(cb => {
                cb();
              })       
            }

        }
        deviceService = { isDesktop: false };
        const el2: HTMLElement = { scrollIntoView: () => { } } as any;
        spyOn(document, 'querySelector').and.returnValue(el2);

        component = new RacingOverlayContentComponent(
            horseRacingService,
            command,
            liveServeHandleUpdatesService,
            gtmService,
            locale,
            windowRef,
            deviceService);
            
        component.overlayContentData= overlayContentDataMock;
        component.eventEntity = overlayContentDataMock[0];
    });

    describe('ngOnChanges', () => {
      

        it('should check showMenu to be true/false', () => {
            let changes = { showMenu: { previousValue: '', currentValue: true } };
            component.liveServeChannels = ['sEvent21290128402'];
            component.sportModule = 'horseracing';
            component.eventEntity = {correctedDayValue:'racing.tomorrow'};
            component.isEntityChanged = true;
            component.ngOnChanges(changes);
            expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 100);
            changes = { showMenu: { previousValue: '', currentValue: false } };
            component.ngOnChanges(changes);
            expect( component.noEvents).toBe(true);
            expect(liveServeHandleUpdatesService.unsubscribe).toHaveBeenCalled();
        });

        it('should call ngOnInit method if showMenu not available', () => {
            component.showMenu = null;       
            component.isEntityChanged = true;
            component.sportModule = 'horseracing';
            component.eventEntity = {correctedDayValue:'racing.tomorrow'};
            const changes = { showMenu: { previousValue: '', currentValue: 'racing.tomorrow' } };
            component.ngOnChanges(changes);
            expect(liveServeHandleUpdatesService.subscribe).toHaveBeenCalled();
            expect( component.noEvents).toBe(true);
        });

        it('should call ngOnInit method if showMenu not available and all events null', () => {
            component.showMenu = null;       
            component.overlayContentData = null;
            component.isEntityChanged = true;
            component.sportModule = 'horseracing';
            component.eventEntity = {correctedDayValue:'racing.tomorrow'};
            const changes = { showMenu: { previousValue: '', currentValue: 'racing.tomorrow' } };
            component.ngOnChanges(changes);
            expect(liveServeHandleUpdatesService.subscribe).toHaveBeenCalled();
            expect( component.noEvents).toBe(true);
        });

        it('should call ngOnInit method if showMenu not available and changes object is null', () => {
            component.showMenu = null;       
            component.overlayContentData = null;
            component.isEntityChanged = true;
            component.sportModule = 'horseracing';
            component.eventEntity = {correctedDayValue:'racing.tomorrow'};
            const changes = { showMenu: null };
            component.ngOnChanges(changes);
            expect(liveServeHandleUpdatesService.subscribe).not.toHaveBeenCalled();
            expect( component.noEvents).toBe(false);
        });

        it('should call ngOnInit method if showMenu not available and overlayContentData data', () => {
            component.showMenu = null;
            component.isEntityChanged = true;
            component.eventEntity = {correctedDayValue:''};
            component.sportModule = 'horseracing';
            const changes = { showMenu: { previousValue: '', currentValue: 'racing.tomorrow' } };
            component.ngOnChanges(changes);
            expect(liveServeHandleUpdatesService.subscribe).toHaveBeenCalled();
            expect( component.noEvents).toBe(true);
        });

        it('should check for groupByFlagCodesAndClassesTypeNames empty data', async () => {
            const changes = { showMenu: { previousValue: '', currentValue: true } };
            component.liveServeChannels = ['sEvent21290128402'];
            component.sportModule = 'horseracing';
            component.eventEntity = {correctedDayValue:'racing.tomorrow'};
            component.isEntityChanged = true;
            component.isDesktop = false;
            horseRacingService.groupByFlagCodesAndClassesTypeNames.and.returnValue(null)
            await component.ngOnChanges(changes);
            expect( component.noEvents).toBe(true);
        });

        it('should check showMenu to be true/false for GH', () => {
            let changes = { showMenu: { previousValue: '', currentValue: true } };
            component.liveServeChannels = ['sEvent21290128402'];
            component.sportModule = 'greyhound';
            component.eventEntity = {correctedDay:'racing.tomorrow'};
            component.isEntityChanged = true;
            component.ngOnChanges(changes);
            expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 100);
            changes = { showMenu: { previousValue: '', currentValue: false } };
            component.ngOnChanges(changes);
            expect( component.noEvents).toBe(true);
            expect(liveServeHandleUpdatesService.unsubscribe).toHaveBeenCalled();
        });
    });

    describe('should call switchers onClick method', () => {
        it('should call selectDay on onClick method HR', () => {
            spyOn(component as any, 'selectDay').and.callThrough();
            component.sportModule = 'horseracing';
            component.dayValueText = 'correctedDayValue';
            component['createSwitchers']();
            component.switchers[0].onClick();
            
            expect(component['selectDay']).toHaveBeenCalledWith('racing.today');
          });

          it('should call selectDay on onClick method GH', () => {
            spyOn(component as any, 'selectDay').and.callThrough();
            component.sportModule = '';
            component.dayValueText = 'correctedDay';
            component.overlayContentData= overlayContentDataMock;
            component['createSwitchers']();
            component.switchers[0].onClick();
            
            expect(component['selectDay']).toHaveBeenCalledWith('racing.today');
          });
    });

    describe('#nextRacesLoaded', () => {
        it('nextracesLoaded flag to be true', () => {
           component.nextRacesLoaded();
           expect(component.nextRacesDataLoaded).toBeTruthy();
        });
    });

    describe('#ngOnDestroy', () => {
        it('should check if liveServechannels availabe and unsubscribe', () => {
            component.liveServeChannels = ['sEvent23432445'];
            component.ngOnDestroy();
            expect(liveServeHandleUpdatesService.unsubscribe).toHaveBeenCalled();
        });

        it('should check not unsubscribe if channels list is empty', () => {
            component.liveServeChannels = [];
            component.ngOnDestroy();
            expect(liveServeHandleUpdatesService.unsubscribe).not.toHaveBeenCalled();
        });
    });

    describe('#trackModule', () => {
        it('should call trackModule', () => {
           component.trackModule('horse racing', {'uk': true}, 'uk', {'uk': 'uk races'});
           expect(gtmService.push).toHaveBeenCalled();
        });
        it('should call trackModule with collapse status', () => {
            component.trackModule('horse racing', {'uk': false}, 'uk', {'uk': 'uk races'});
            expect(gtmService.push).toHaveBeenCalled();
         });
    });
});
