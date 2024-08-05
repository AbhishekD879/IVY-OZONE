
import { FreebetSignpostingComponent } from './freebet-signposting.component';

const signpostingConfig = [{
    id: '',
    createdBy: '',
    createdByUserName: '',
    updatedBy: '',
    updatedByUserName: '',
    createdAt: '',
    updatedAt: '',
    sortOrder: 0,
    brand: '',
    freeBetType: '',
    fromOffer: '',
    betConditions: '',
    sport: '',
    event: '',
    market: '',
    price: {
        priceType: 'decimal',
        priceNum: 5,
        priceDen: 1,
        priceDec: 5
    },
    signPost: 'This is signposting text',
    disabled: false,
    isActive: true,
    title: 'eachway',
}]

describe('FreebetSignpostingComponent', () => {
    let component: FreebetSignpostingComponent;
    let signpostingCmsService, gtmService, userService;

    beforeEach(() => {

        signpostingCmsService = {
            freeBetSignpostingArray: signpostingConfig,
            gtmLoadingStatus: {
                betslip: false,
                quickbet: false
            }
        };

        gtmService = {
            push: jasmine.createSpy('push')
        };

        userService = {
            oddsFormat:'frac'
        }

        component = new FreebetSignpostingComponent(
            signpostingCmsService,
            gtmService,
            userService
        );

    });

    it('should create component instance', () => {
        expect(component).toBeTruthy();
    });

    describe('#ngOnInit', () => {
        it('#ngOnInit on load should call onLoadSignpostingCheck', () => {
            spyOn(component as any, 'onLoadSignpostingCheck');
            component.ngOnInit();
            expect(component['onLoadSignpostingCheck']).toHaveBeenCalledWith(signpostingCmsService.freeBetSignpostingArray);
        });

        it('#ngOnInit on load should not call onLoadSignpostingCheck when signpostingconfig is null', () => {
            spyOn(component as any, 'onLoadSignpostingCheck');
            signpostingCmsService.freeBetSignpostingArray = null;
            component.ngOnInit();
            expect(component['onLoadSignpostingCheck']).not.toHaveBeenCalled();
        });

        it('onLoadSignpostingCheck should set isSignpostingEnabled to true in decimal', () => {
            component.betInfo = {
                price: {
                    priceNum: 1,
                    priceDen: 2,
                }
            }
           const myPrivateSpy = spyOn<any>(component, 'onLoadSignpostingCheck').and.callThrough();
            myPrivateSpy.call(component, signpostingCmsService.freeBetSignpostingArray);  
            expect(component.isSignpostingEnabled).toBeTrue();
        });

        it('onLoadSignpostingCheck should set isSignpostingEnabled to true in fractional', () => {
            component.betInfo = {
                price: {
                    priceNum: 1,
                    priceDen: 2,
                }
            }
            signpostingCmsService.freeBetSignpostingArray[0].price.priceType = 'fractional';
            const myPrivateSpy = spyOn<any>(component, 'onLoadSignpostingCheck').and.callThrough();
            myPrivateSpy.call(component, signpostingCmsService.freeBetSignpostingArray);  
            expect(component.isSignpostingEnabled).toBeTrue();
        });

        it('onLoadSignpostingCheck should set isSignpostingEnabled to true when user oddsformat is decimal', () => {
            userService = {
                oddsFormat: 'dec'
            }

            component = new FreebetSignpostingComponent(
                signpostingCmsService,
                gtmService,
                userService
            );

            component.betInfo = {
                price: {
                    priceNum: 1,
                    priceDen: 2,
                    priceDec: '0.5'
                }
            }

            signpostingCmsService.freeBetSignpostingArray[0].price.priceType = 'fractional';
            const myPrivateSpy = spyOn<any>(component, 'onLoadSignpostingCheck').and.callThrough();
            myPrivateSpy.call(component, signpostingCmsService.freeBetSignpostingArray);  
            expect(component.isSignpostingEnabled).toBeTrue();
        });


        it('onLoadSignpostingCheck should set signpostingMessage to value', () => {
            component.betInfo = {
                price: {
                    priceNum: 1,
                    priceDen: 2,
                }
            }
            const signpostText = signpostingCmsService.freeBetSignpostingArray[0].signPost;
            const myPrivateSpy = spyOn<any>(component, 'onLoadSignpostingCheck').and.callThrough();
            myPrivateSpy.call(component, signpostingCmsService.freeBetSignpostingArray);  
            expect(component.isSignpostingEnabled).toBeTrue();
            expect(component.signpostingMessage).toEqual(signpostText);
        });

        it('signpostingMessage to be undefined when signposting array is null', () => {
            component.betInfo = {
                price: {
                    priceNum: 1,
                    priceDen: 2,
                }
            }
            signpostingCmsService.freeBetSignpostingArray = null;
            component.ngOnInit();
            expect(component.isSignpostingEnabled).toBeFalse();
            expect(component.signpostingMessage).toBeUndefined();
        });

        it('GA tracking for betslip', () => {
            component.betInfo = {
                price: {
                    priceNum: 1,
                    priceDen: 2,
                },
                sportId: '21'
            }
            component.eventLocation = 'betslip';
            signpostingCmsService.gtmLoadingStatus.betslip = false;
            const myPrivateSpy = spyOn<any>(component, 'onLoadGATrackingCheck').and.callThrough();
            myPrivateSpy.call(component);  
            expect(signpostingCmsService.gtmLoadingStatus.betslip).toBeTrue();
        });


        it('GA tracking for quickbet', () => {
            component.betInfo = {
                price: {
                    priceNum: 1,
                    priceDen: 2,
                },
                sportId: '21',
                categoryId: '21'
            }
            component.eventLocation = 'quickbet';
            signpostingCmsService.gtmLoadingStatus.quickbet = false;
            const myPrivateSpy = spyOn<any>(component, 'onLoadGATrackingCheck').and.callThrough();
            myPrivateSpy.call(component);  
            expect(signpostingCmsService.gtmLoadingStatus.quickbet).toBeTrue();
        });
    });
});
