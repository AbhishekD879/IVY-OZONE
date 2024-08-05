import { SbSingleDropDoubleOddItemComponent } from './sb-single-drop-double-odd-item.component';

describe('SbSingleDropDoubleOddItemComponent', () => {
    let component: SbSingleDropDoubleOddItemComponent;

    beforeEach(() => {
        component = new SbSingleDropDoubleOddItemComponent();
    });
    describe('ngOnInit', () => {
        it('should initialize marketNames and mktNameToOutcome correctly', () => {
            const market = {
                outcomes: [
                    { name: 'Team A and Over 3.5' },
                    { name: 'Team A and Over 2.5' },
                    { name: 'Team B and Under 1.5' },
                    { name: 'Team A and Under 3.5' },
                ]
            };
            component.market = market as any;

            component.ngOnInit();

            expect(component.marketNames).toEqual(['Team A ', 'Team B ']);
            expect(component.mktNameToOutcome[component.marketNames[0]]).toEqual([
                { name: 'Team A and Over 2.5' },
                { name: 'Team A and Over 3.5' },
                { name: 'Team A and Under 3.5' },
            ]);
            expect(component.mktNameToOutcome[component.marketNames[1]]).toEqual([
                { name: 'Team B and Under 1.5' },
            ]);
        });

        it('should set currOutcomes to outcomes of the first market name', () => {
            const market = {
                outcomes: [
                    { name: 'Team A and Over 2.5' },
                    { name: 'Team A and Under 1.5' },
                    { name: 'Team B and Under 3.5' },
                ]
            };
            component.market = market as any;

            component.ngOnInit();

            expect(component.currOutcomes).toEqual([
                { name: 'Team A and Over 2.5' },
                { name: 'Team A and Under 1.5' },
            ]);
        });

        it('should handle empty outcomes correctly', () => {
            const market = {
                outcomes: []
            };
            component.market = market as any;

            component.ngOnInit();

            expect(component.marketNames).toEqual([]);
            expect(component.mktNameToOutcome).toEqual({});
            expect(component.currOutcomes).toEqual(undefined);
        });
    });

    describe('OnValuechange', () => {
        it('should assign to currentOutcome', () => {
            component.mktNameToOutcome = { 1: { name: 'teamA' } }
            component.onValueChange(1);
            expect(component.currOutcomes as any).toEqual({ name: 'teamA' })
        });
    });

    describe('handleSelectionClick', () => {
        it('should emit the market', () => {
            component.selectionClickEmit.emit = jasmine.createSpy('selectionClickEmit.emit');
            component.handleSelectionClick({ name: 'Team A and Over 2.5' } as any);
            expect(component.selectionClickEmit.emit).toHaveBeenCalledOnceWith({ name: 'Team A and Over 2.5' } as any);
        });
    });
});
