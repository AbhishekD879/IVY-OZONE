import { ExtraPlaceSignpostingComponent } from "./extra-place-signposting.component";
import { of } from 'rxjs';

describe('ExtraPlaceSignpostingComponent', () => {
    let component: ExtraPlaceSignpostingComponent;
    let cmsService;

    beforeEach(() => {
        cmsService = {
            getCmsInitData: jasmine.createSpy('getCmsInitData').and.returnValue(of({ sportCategories: [{ imageTitle: 'Horse Racing', messageLabel: 'HORSE MESSAGE' }, { imageTitle: 'Golf', messageLabel: 'Golf' }] }))
        };
        createComponent();
        component.betSlipData={
            drilldownTagNames: 'MKTFLAG_EPR',
            eachWayPlaces:'5',
            previousOfferedPlaces:'4'
        } as any;
        component.marketData = {
            drilldownTagNames: 'MKTFLAG_EPR',
            referenceEachWayTerms: {
                id: '1',
                places: '4'
            },
            eachWayPlaces: '5',
            markets: [
                {
                }
            ]
        } as any;

        component.eventData = {
            categoryName: 'Horse Racing'
        } as any;

        component.origin = 'openbets';
        component.isBetHistory=true;

    });

    function createComponent() {
        component = new ExtraPlaceSignpostingComponent(cmsService);
    }
    it('ngOnInit', () => {
        component.marketData.eachWayPlaces = '4';
        const openSpy = spyOn(ExtraPlaceSignpostingComponent.prototype as any, 'buildNonRunnerMessage');
        component.ngOnInit();
        expect(openSpy).toHaveBeenCalled();
    });

    it('ngOnInit for array of referenceEachWayTerms', () => {
          component.marketData = {
            drilldownTagNames: 'MKTFLAG_EPR',
            referenceEachWayTerms:[{
                id: '1',
                places: '4'
            }],
            eachWayPlaces: '4',
            markets: [
                {
                }
            ]
        } as any;
        const openSpy = spyOn(ExtraPlaceSignpostingComponent.prototype as any, 'extraPlaceSignposting');
        component.ngOnInit();
        expect(openSpy).toHaveBeenCalled();
    });

    it('ngOnInit with signposting build', () => {
        component.origin='betslip';
       const openSpy = spyOn(ExtraPlaceSignpostingComponent.prototype as any, 'extraPlaceSignposting');
        component.ngOnInit();
        expect(openSpy).toHaveBeenCalled();
    });
    it('ngOnInit with signposting with referenceeachway', () => {
       const openSpy = spyOn(ExtraPlaceSignpostingComponent.prototype as any, 'extraPlaceSignposting');
        component.ngOnInit();
        expect(openSpy).toHaveBeenCalled();
    });

    it('isNonRunnerEvent for falsy condition', () => {
        component.isNonRunnerEvent();
        expect(component.isNonRunnerEvent()).toBeFalsy();
    });

    it('isNonRunnerEvent for true condition', () => {
        component.marketData.eachWayPlaces = '4'
        component.isNonRunnerEvent();
        expect(component.isNonRunnerEvent()).toBeTruthy();
    });

    it('getOrigin', () => {
        component['getOrigin']();
        expect(component['getOrigin']()).toEqual('OPENBETS');
    });

    it('isExtraPlaceOfferedEvent', () => {
        component.origin = 'betslip';
        component['extraPlaceSignposting'](2, 4);
        expect(component.extraPlaceName).toEqual('2 places instead of 4');
    });

    it('getExtraPlaceName when origin is betslip', ()=> {
        component.origin = 'betslip';
        const result = component['getExtraPlaceName'](2, 4);
        expect(result).toBe(' 2 places instead of 4');
    })

    it('getExtraPlaceName when origin is not betslip', ()=> {
        component.origin = 'bet';
        const result = component['getExtraPlaceName'](2, 4);
        expect(result).toBe('Paying 2 places instead of 4');
    })


    it('isMyBetsPage with toBeTruthy condition', () => {
        component['isMyBetsPage']();
        expect(component['isMyBetsPage']()).toBeTruthy();
    });


    it('isMyBetsPage with toBeFalsy condition', () => {
        component.origin = 'bets'
        component['isMyBetsPage']();
        expect(component['isMyBetsPage']()).toBeFalsy();
    });


    it('extraPlaceSignposting constructing the signposting message with places', () => {
        component.origin = 'bets'
        const market={
            eachWayPlaces:'5',
           places:'4'
        }
        component['extraPlaceSignposting']( market.eachWayPlaces,  market.places);
        expect(component['extraPlaceName']).toEqual('Paying 5 places instead of 4');
    });

    it('isExtraPlaceOfferedEvent', () => {
        component['isExtraPlaceOfferedEvent']();
        expect(component['isExtraPlaceOfferedEvent']()).toBeTruthy();
    });


    it('isExtraPlaceOfferedEvent for falsy event', () => {
        component.marketData.drilldownTagNames = 'EPR'
        component['isExtraPlaceOfferedEvent']();
        expect(component['isExtraPlaceOfferedEvent']()).toBeFalse();
    });


    it('buildNonRunnerMessage ', () => {
        component['buildNonRunnerMessage']();
        expect(component['nonRunnerMessage']).toEqual('HORSE MESSAGE');
    });


    it('buildNonRunnerMessage ', () => {
        component.eventData.categoryName = 'Golf'
        cmsService.getCmsInitData = jasmine.createSpy('getCmsInitData').and.returnValue(of({ sportCategories: [{ imageTitle: 'Golf', messageLabel: 'Golf' }] }));
        component['buildNonRunnerMessage']();
        expect(component['nonRunnerMessage']).toEqual('Golf');
    });
 
    it('isMyBetsEpr ', () => {
        component['isMyBetsEpr']();
        expect(component['isMyBetsEpr']()).toBeTruthy();
    });
    it('isMyBetsEpr witout bethistory', () => {
        component.isBetHistory=false;
        component['isMyBetsEpr']();
        expect(component['isMyBetsEpr']()).toBeFalsy();
    });
});