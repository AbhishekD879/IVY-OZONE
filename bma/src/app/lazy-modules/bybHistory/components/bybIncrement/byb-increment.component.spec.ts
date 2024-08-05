import { BybIncrementComponent } from './byb-increment.component';

describe('BybIncrementComponent', () => {
    let component, marketService, dashBoardService;

    beforeEach(() => {
        marketService = {
            selectedSelectionsSet: new Set(),
            selectValue: jasmine.createSpy('selectValue').and.returnValue(1),
            markets: [{ groupName: 'Exact Total Goals', selections: [{ id: '0', relatedTeamType: 0 }, { id: '1', relatedTeamType: 1 }, { id: '2', relatedTeamType: 2 }] },
            {}],
            isSelected: jasmine.createSpy('isSelected').and.returnValue(1),
            loadSelectionData: jasmine.createSpy('loadSelectionData').and.returnValue(Promise.resolve(([{ selections: [{ title: 'arsenal', selections: [1,2] },
            { title: 'liverpool', selections: [1,2] }] }]))),
            seperate: jasmine.createSpy('seperate').and.returnValue(1),
        };
        component = new BybIncrementComponent(marketService);
    });

    describe('ngOnChanges', () => {
        it('should call ngOnChanges', () => {
            component.initial = -1;
            spyOn(component,'seperate');
            component.ngOnChanges({'market' : true});
            expect(marketService.loadSelectionData).toHaveBeenCalled();
        });
    });

    describe('ngOnInit', () => {
        it('should call ngoninit with initial 0', () => {
            component.initial = -1;
            spyOn(component,'callExactMarkets');
            spyOn(component,'seperate');
            component.ngOnInit();
            expect(component.callExactMarkets).toHaveBeenCalled();
        });
    });

    //seperate
    describe('seperate', () => {
        it('should call seperate over', () => {
            component.initial = -1;
            component.marketRespData = [{selections: [{title: 'OVER'}]}];
            component.seperate();
            expect(component.incrementenable).toBeFalsy();
        });

        it('should call seperate under', () => {
            component.initial = -1;
            component.marketRespData = [{selections: [{title: 'UNDER'}]}];
            component.seperate();
            expect(component.incrementenable).toBeFalsy();
        });

        it('no data', () => {
            component.incrementenable = true;
            component.seperate();
            expect(component.incrementenable).toBeTruthy();
        });
    });

    //displayIncrement
    describe('displayIncrement', () => {
        it('should call displayIncrement ', () => {
            component.buttonState = 'state1';
            component.marketRespData = [{selections: [{title: 'OVER'}]}];
            component.market = {groupName: 'Participant_1 Total Goals'};
            component.overMarketsMap = [{bettingValue1: 1}, {bettingValue1: 2}];
            component.overMarkets = component.overMarketsMap ;
            component.displayIncrement('over');
            expect(component.incrementenable).toBeTruthy();
        });

        it('should skip if  ', () => {
            component.buttonState = 'state1';
            component.marketRespData = [{selections: [{title: 'OVER'}]}];
            component.market = {groupName: 'Participant_1 Total Goals'};
            component.overMarketsMap = [{bettingValue1: 1}, {bettingValue1: 2}];
            component.displayIncrement('over');
            expect(component.incrementenable).toBeTruthy();
        });

        it('should call displayIncrement with state over', () => {
            component.buttonState = 'over';
            component.marketRespData = [{selections: [{title: 'OVER'}]}];
            component.market = {groupName: 'Participant_1 Total Goals'};
            component.overMarketsMap = [{bettingValue1: 1}, {bettingValue1: 2}];
            component.overMarkets = component.overMarketsMap ;
            component.displayIncrement('over');
            expect(component.incrementenable).toBeTruthy();
        });

        it('should call displayIncrement ', () => {
            component.buttonState = 'state1';
            component.marketRespData = [{selections: [{title: 'OVER'}]}];
            component.market = {groupName: 'Participant_1 Total Goals'};
            component.underMarketsMap = [{bettingValue1: 1}, {bettingValue1: 2}];
            component.overMarkets = component.overMarketsMap ;
            component.displayIncrement('under');
            expect(component.incrementenable).toBeTruthy();
        });
    });

    //rotate
    describe('rotate', () => {
        it('should call rotate', () => {
            component.initial = -1;
            component.showMarkets = [{bettingValue1: 1}, {bettingValue1: 2}];
            component.iterativeIndex = component.showMarkets.entries();
            component.incrementer = 0;
            component.rotate(1);
            expect(marketService.isSelected).toHaveBeenCalled();
        });

        it('should call rotate', () => {
            component.initial = -1;
            component.showMarkets = [{bettingValue1: 1}, {bettingValue1: 2}];
            component.iterativeIndex = component.showMarkets.entries();
            component.incrementer = -2;
            component.rotate(-1);
            expect(marketService.isSelected).toHaveBeenCalled();
        });
    });

    //selectValue
    describe('selectValue', () => {
        it('should call selectValue', () => {
            component.selectValue({selection: {id :1}, market: {}});
            expect(marketService.selectValue).toHaveBeenCalled();
        });
    });

    //callExactMarkets
    describe('callExactMarkets', () => {
        it('should call callExactMarkets', () => {
            component.market = {groupName: 'Total Goals'};
            component.callExactMarkets();
            expect(marketService.loadSelectionData).toHaveBeenCalled();
        });

        it('should call callExactMarkets', () => {
            marketService.markets = [{ groupName: 'Exact Total Goals1',
             selections: [{ id: '0', relatedTeamType: 0 }, { id: '1', relatedTeamType: 1 }, { id: '2', relatedTeamType: 2 }]}];
            component.market = {groupName: 'Total Goals1'};
            component.callExactMarkets();
            expect(marketService.loadSelectionData).not.toHaveBeenCalled();
        });

        it('should call callExactMarkets without component.market', () => {
            marketService.markets = [{ groupName: 'Exact Total Goals1',
             selections: [{ id: '0', relatedTeamType: 0 }, { id: '1', relatedTeamType: 1 }, { id: '2', relatedTeamType: 2 }]}];
            component.callExactMarkets();
            expect(marketService.loadSelectionData).not.toHaveBeenCalled();
        });
    });

    //exactMarkets
    describe('exactMarkets', () => {
        it('should call exactMarkets', () => {
            component.exactMapMarkets = [{bettingValue1: 1}, {bettingValue1: 2}];
            component.exactMarkets();
            expect(component.initial).toBe(0);
        });

        it('should call exactMarkets', () => {
            component.buttonState = 'exact';
            component.exactMapMarkets = [{bettingValue1: 1}];
            component.exactMarkets();
            expect(component.initial).toBe(0);
        });
    });

    //fncollapseLists
    describe('fncollapseLists', () => {
        it('should call fncollapseLists', () => {
            component.collapseLists.emit = jasmine.createSpy('emit');
            component.fncollapseLists();
            expect(component.collapseLists.emit).toHaveBeenCalled();
        });
    });

    //markets
    describe('get markets', () => {
        it('should call fncollapseLists', () => {
            component.market = {markets : {}};
            const retVal = component.markets as any;
            expect(retVal).toBe(component.market.markets);
        });
    });
});
