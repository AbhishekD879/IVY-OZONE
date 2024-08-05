import { MarketDescriptionPopupComponent } from "@lazy-modules/luckyDip/components/market-description-popup/market-description-popup.component";
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';

describe('MarketDescriptionPopupComponent', () => {
    let component, deviceService, windowRef;

    let mockData, closeDialogSpy;

    beforeEach(() => {
        closeDialogSpy = spyOn(MarketDescriptionPopupComponent.prototype['__proto__'], 'closeDialog');
        deviceService = {
            close: jasmine.createSpy('close')
        };
        windowRef = {
            document: {
                body: {
                    classList: {
                        add: jasmine.createSpy('classList.add'),
                        remove: jasmine.createSpy('classList.remove')
                    }
                },
                querySelector: jasmine.createSpy('querySelector'),
            },
            nativeWindow: {
                location: {
                    href: '/promotions'
                }
            }
        };

        mockData = {
            dialogClass: 'splash-popup',
            data: {
                marketTitle: 'marketTitle',
                marketDescripton: 'marketDescripton',
                infoIconImgPath:'infoIconImgPath'
            }
        };


        component = new MarketDescriptionPopupComponent(deviceService, windowRef);
        component.dialog = { closeOnOutsideClick: true };

    });

    it(`should be instance of 'AbstractDialogComponent'`, () => {
        expect(AbstractDialogComponent).isPrototypeOf(component);
    });

    it('should create component instance', () => {
        expect(component).toBeTruthy();
    });

    describe('open', () => {
        it('should get data', () => {

            component.params = mockData;
            const openSpy = spyOn(MarketDescriptionPopupComponent.prototype['__proto__'], 'open');

            component.open();

            expect(openSpy).toHaveBeenCalled();

        });
    });

    describe('closeMarketDescriptionDialog', () => {
        it('should call closeDialog', () => {

            component.closeMarketDescriptionDialog();
            expect(closeDialogSpy).toHaveBeenCalled();
        });
    });
});
