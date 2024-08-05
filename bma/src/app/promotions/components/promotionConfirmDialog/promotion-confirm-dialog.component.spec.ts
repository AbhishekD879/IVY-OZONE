import { PromotionConfirmDialogComponent } from './promotion-confirm-dialog.component';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { of, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
describe('PromotionConfirmDialogComponent', () => {
    let component,
        promotionData,
        device,
        windowRef,
        promotionsService,
        betpromotionsService,
        pubSubService,
        router,
        quickDepositIframeService,
        localeService;
    beforeEach(() => {
        device = {};
        promotionData = {
            marketLevelFlag: 'marketLevelFlag',
            eventLevelFlag: 'eventLevelFlag',
            useDirectFileUrl: 'sport/football/matches/today',
            directFileUrl: 'sport/football/matches/today',
            overlayBetNowUrl: 'url',
            flagName: 'flags',
            iconId: 'icon/122',
            betPack: {
                isBetPack: true,
                bodyText: 'test_BetPack',
                congratsMsg: '<p>Congratulations</p>',
                offerId: '1234',
                triggerIds: '1234',
                betValue: '1',
                lowFundMessage: 'test low funds',
                notLoggedinMessage: 'Please Login to continue',
                errorMessage: 'Error_Cannot process',
            }
        };
        windowRef = {
            document: {
                body: {
                    classList: {
                        add: jasmine.createSpy('classList.add'),
                        remove: jasmine.createSpy('classList.remove')
                    }
                }
            },
            nativeWindow: {
                open: jasmine.createSpy('nativeWindow.open')
            }
        };
        pubSubService = {
            publish: jasmine.createSpy('publish'),
            subscribe: jasmine.createSpy('subscribe').and.callFake((file, methods, callback) => {
                callback();
            }),
            unsubscribe: jasmine.createSpy('unsubscribe'),
            API: pubSubApi
        };
        quickDepositIframeService = {
            redirectToDepositPage: jasmine.createSpy()
        };
        promotionsService = {
            isUserLoggedIn: jasmine.createSpy('isUserLoggedIn'),
        };
        betpromotionsService = {
            onBuyBetPack: jasmine.createSpy('onBuyBetPack').and.returnValue(of({})),
            sendGTM: jasmine.createSpy('sendGTM')
        };
        router = {
            navigateByUrl: jasmine.createSpy('navigateByUrl').and.returnValue(Promise.resolve()),
            navigate: jasmine.createSpy('navigate')
        };
        localeService = {
            getString: jasmine.createSpy('getString').and.returnValue('test')
        };
        component = new PromotionConfirmDialogComponent(
            device,
            windowRef,
            promotionsService,
            betpromotionsService,
            pubSubService,
            router,
            quickDepositIframeService,
            localeService
        );
        component.dialog = { changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') },
                             closeOnOutsideClick: true };
        component.isPending = false;
        component.promo = {
            promotionId: '123',
            betPack: {
                notLoggedinMessage: 'not logged in',
                lowFundMessage: 'low funds',
                offerId:'123'
            }
        };
    });
    it('should create', () => {
        expect(component).toBeTruthy();
    });
    it(`should be instance of 'AbstractDialog'`, () => {
        expect(AbstractDialogComponent).isPrototypeOf(component);
    });
    it('openThisDialog', () => {
        const params = { data: { promotion: promotionData } };
        AbstractDialogComponent.prototype.setParams(params);
        component.promo = params.data.promotion;
        component.buttonName = 'Confirm';
        component.errorMsg = null;
        const openSpy = spyOn(PromotionConfirmDialogComponent.prototype['__proto__'], 'open');
        component.open();
        expect(component.dialog.closeOnOutsideClick).toBeFalsy();
        expect(openSpy).toHaveBeenCalled();
        expect(component.promo).toEqual(promotionData);
        expect(windowRef.document.body.classList.add).toHaveBeenCalledWith('promotion-modal-open');
    });

    it('closeThisDialog should not push the error details in GA tracking  ', () => {
        const closeDialogSpy = spyOn(PromotionConfirmDialogComponent.prototype['__proto__'], 'closeDialog');
        component.errorMsg = undefined;
        
        component.closeThisDialog('exit');

        expect(betpromotionsService.sendGTM).toHaveBeenCalledWith('exit', 'purchase page', '123');
        expect(closeDialogSpy).toHaveBeenCalled();
        expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('promotion-modal-open');
    });
    it('closeThisDialog should push the error details in GA tracking', () => {
        const closeDialogSpy = spyOn(PromotionConfirmDialogComponent.prototype['__proto__'], 'closeDialog');
        component.errorMsg = { msg: 'error' };
        const sendDatatoGTMSpy = spyOn(component, 'sendDatatoGTM');

        component.closeThisDialog('exit');

        expect(sendDatatoGTMSpy).toHaveBeenCalled();
        expect(closeDialogSpy).toHaveBeenCalled();
        expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('promotion-modal-open');
    });
    it('closeThisDialog should not call sendDatatoGTMSpy if button is not exit', () => {
        const closeDialogSpy = spyOn(PromotionConfirmDialogComponent.prototype['__proto__'], 'closeDialog');
        component.errorMsg = { msg: 'error' };
        const sendDatatoGTMSpy = spyOn(component, 'sendDatatoGTM');

        component.closeThisDialog('deposit');

        expect(sendDatatoGTMSpy).not.toHaveBeenCalled();
        expect(closeDialogSpy).toHaveBeenCalled();
        expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('promotion-modal-open');
    });
    it('should call open login dialog', () => {
        component.buttonName = 'Login';
        component.confirmDialog();
        expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'betpack' });
    });
    it('should call open Deposit dialog', () => {
        component.buttonName = 'Deposit';
        const closeDialogSpy = spyOn(PromotionConfirmDialogComponent.prototype['__proto__'], 'closeDialog');
        component['confirmDialog']();
        expect(quickDepositIframeService.redirectToDepositPage).toHaveBeenCalled();
        expect(closeDialogSpy).toHaveBeenCalled();
    });
    it('should call login on confirm button', () => {
        component.buttonName = 'Confirm';
        const params = { data: { promotion: promotionData } };
        AbstractDialogComponent.prototype.setParams(params);
        component.promo = params.data.promotion;
        promotionsService['isUserLoggedIn'] = jasmine.createSpy().and.callFake(() => {
            return false;
        });
        component['confirmDialog']();
        expect(component.buttonName).toBe('Login');
        expect(component.errorMsg).toEqual(promotionData.betPack.notLoggedinMessage);
    });
    it('should call betpack on confirm button', () => {
        component.buttonName = 'Confirm';
        spyOn(component, 'buyBetPack');
        promotionsService['isUserLoggedIn'] = jasmine.createSpy().and.callFake(() => {
            return true;
        });
        component['confirmDialog']();
        expect(component['buyBetPack']).toHaveBeenCalled();
    });
    it('switch default', () => {
        component.buttonName = 'test';
        component.confirmDialog();
        expect(pubSubService.publish).not.toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'betpack' });
    });
    it('success scenario on buybetpack', fakeAsync(() => {
        component.isPending = true;
        component.promo = promotionData;
        component.params = { data: { callConfirm: jasmine.createSpy() } };
        component.buyBetPack();
        tick();
        expect(component.params.data.callConfirm).toHaveBeenCalledWith('<p>Congratulations</p>');
    }));
    it('error scenario low funds on buybetpack', () => {
        component['betpromotionsService'].onBuyBetPack = jasmine
            .createSpy('onBuyBetPack')
            .and.returnValue(throwError({ type: 'error', msg: 'INSUFFICIENT_FUNDS' }));
        component.promo = promotionData;
        component.buyBetPack();
        expect(component.buttonName).toEqual('Deposit');
        expect(component.errorMsg).toEqual(promotionData.betPack.lowFundMessage);
    });
    it('error scenario 2 low funds on buybetpack', () => {
        component['betpromotionsService'].onBuyBetPack = jasmine
            .createSpy('onBuyBetPack')
            .and.returnValue(throwError({ type: 'error', msg: 'INSUFFICIENT_FUNDS' }));
        component.promo = promotionData;
        component.promo.betPack.lowFundMessage = null;
        component.buyBetPack();
        expect(component.buttonName).toEqual('Deposit');
        expect(localeService.getString).toHaveBeenCalledWith('bs.SERVICE_ERROR');
    });
    it('error scenario 3 on buybetpack', () => {
        component['betpromotionsService'].onBuyBetPack = jasmine
            .createSpy('onBuyBetPack')
            .and.returnValue(throwError({ type: 'error', msg: 'Genric' }));
        component.promo = promotionData;
        component.buyBetPack();
        expect(component.errorMsg).toEqual(promotionData.betPack.errorMessage);
    });
    it('error scenario 4 on buybetpack', () => {
        component['betpromotionsService'].onBuyBetPack = jasmine
            .createSpy('onBuyBetPack')
            .and.returnValue(throwError({ type: 'error', msg: 'Genric' }));
        component.promo = promotionData;
        component.promo.betPack.errorMessage = null;
        component.buyBetPack();
        expect(localeService.getString).toHaveBeenCalledWith('bs.SERVICE_ERROR');
    });

    describe('sendDatatoGTM', () => {

        it('error message is notLoggedinMessage', () => {

            component.errorMsg = component.promo.betPack.notLoggedinMessage;

            component['sendDatatoGTM']();

            expect(betpromotionsService.sendGTM).toHaveBeenCalledWith('exit', 'not logged in', '123');
        });

        it('error message is lowFundMessage', () => {
            component.errorMsg = component.promo.betPack.lowFundMessage;

            component['sendDatatoGTM']();

            expect(betpromotionsService.sendGTM).toHaveBeenCalledWith('exit', 'low funds', '123');
        });

        it('error message is neither notLoggedIn nor lowFunds', () => {
            component.errorMsg = 'error';

            component['sendDatatoGTM']();

            expect(betpromotionsService.sendGTM).toHaveBeenCalledWith('exit', 'error message', '123');
        });
    });
});
