import { BetpackInfoPageComponent } from '@lazy-modules/betpackPage/components/betpackInfoPage/betpack-info-page.component';
import { of } from 'rxjs/internal/observable/of';
import { fakeAsync, tick, flush,discardPeriodicTasks }from '@angular/core/testing';
import { throwError } from 'rxjs';
describe('BetpackInfopageComponent', () => {
    let device,
        windowRef,
        betpromotionsService,
        userService,
        pubSubService,
        quickDepositIframeService,
        timeService,
        freeBetsService,
        router,
        changeDetectorRef,
        component,
        gtmService,
        domSanitizer,
        betpackCmsService,
        dialogService,
        platformLocation,
        sessionStorage;

    beforeEach(() => {
        const event =[ { scrollIntoView:jasmine.createSpy('scrollIntoView') }] as any;
        device = {};
        windowRef = {
            document: {
                body: {
                    classList: {
                        add: jasmine.createSpy('add'),
                        remove: jasmine.createSpy('remove')
                    }
                },
                
                querySelector: jasmine.createSpy('querySelector').and.returnValue(
                    {
                        scroll: jasmine.createSpy(),            
                    })

            }
        };
        router = {
            navigateByUrl: jasmine.createSpy(),
            routeReuseStrategy: {
                shouldReuseRoute: function () { }
            }
        };
        changeDetectorRef = {
            detectChanges: jasmine.createSpy('detectChanges')
        };
        freeBetsService = {
            getFreeBets: jasmine.createSpy('getFreeBets').and.returnValue(of([{}])),
        };
        userService = {
            status: true, maxStakeScale: '0.2', bppToken: true, username: 'test',
            isInShopUser: jasmine.createSpy('isInShopUser').and.returnValue(true),
        } as any;
        pubSubService = {
            subscribe: jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn()).and.returnValue({ signPost: '', signPostTooltip: '' }),
            publish: jasmine.createSpy('publish'),
            unsubscribe: jasmine.createSpy('unsubscribe'),
            API: {
                SESSION_LOGIN: 'SESSION_LOGIN',
                OPEN_LOGIN_DIALOG: 'OPEN_LOGIN_DIALOG'
            }
        };
        betpromotionsService = {
            onBuyBetPack: jasmine.createSpy('onBuyBetPack').and.returnValue(of({}))
        };

        timeService = {
            formatByPattern: jasmine.createSpy('formatByPattern').and.returnValue('15:10')
        };
        quickDepositIframeService = {
            isEnabled: jasmine.createSpy('isEnabled').and.returnValue(of(false)),
            redirectToDepositPage: jasmine.createSpy('redirectToDepositPage'),
        };
        gtmService = {
            push: jasmine.createSpy('push')
        };
        domSanitizer = {
            sanitize: jasmine.createSpy().and.returnValue('test'),
            bypassSecurityTrustHtml: () => { }
        };
        dialogService = {
            closeDialog: jasmine.createSpy('closeDialog'),
            API: {
                betpackInfoDialog: 'betpackInfoDialog'
            }
        };
        betpackCmsService = {};
        platformLocation = {
            onPopState: jasmine.createSpy('onPopState')
        };
        sessionStorage = {
            set: jasmine.createSpy('set'),
            remove: jasmine.createSpy('remove')
        };
        createComponentInstance();
        component.params = {
            data: {
                bp: {
                    betPackId: 1,
                    purchased: false,
                    betPackPurchaseAmount: '4',
                    betPackTokenList: [{ tokenTitle: 'accumulator' }, { tokenTitle: '£3 pound offer' }]
                },
                betpackLabels: {
                    betPackAlreadyPurchasedPerDayBannerLabel: 'Daily Limit Exceeded. Only 1 Bet Pack can be purchased per day',
                    buyButtonLabel: 'Buy',
                    buyNowLabel: 'Buy Now',
                    maxBetPackPerDayBannerLabel: 'Only 1 Bet Pack can be purchased per day.',
                    moreInfoLabel: 'MORE INFO',
                    maxPurchasedLabel: "MAX PURCHASED",
                    limitedLabel: 'Limited Availability',
                    soldOutLabel: 'SOLD OUT',
                    endingSoonLabel: 'ENDING SOON',
                    expiresInLabel: 'EXPRES IN',
                    endedLabel: 'ENDED',
                    gotoMyBetPacksLabel: 'Go To My Bet Packs',
                    lessInfoLabel: 'LESS INFO',
                    betPackInfoLabel: 'Bet Packs Info',
                    serviceError: 'This bet bundle is not available to purchase',
                    kycArcGenericMessage: 'Your account is not enabled to buy Bet Bundles',
                    emptyLabel :' '
                },
                isBuyInfoClicked: false,
                clicked: true,
                reviewPage: {},
                signPostingMsg: 'Only 1 Bet Pack can be purchased per day.'
            }
        };
        component.dialog = {
            open: jasmine.createSpy('open'),
            close: jasmine.createSpy('close'),
            changeDetectorRef: { detectChanges: jasmine.createSpy('detectChanges') }
        };
    });

    const createComponentInstance = () => {
        component = new BetpackInfoPageComponent(
            device,
            windowRef,
            betpromotionsService,
            userService,
            pubSubService,
            quickDepositIframeService,
            timeService,
            router,
            changeDetectorRef,
            gtmService,
            domSanitizer,
            betpackCmsService,
            dialogService,
            sessionStorage,
            platformLocation
        );
    };

    describe('constructor', () => {
        it('constructor called', fakeAsync(() => {
            component = new BetpackInfoPageComponent(
                device,
                windowRef,
                betpromotionsService,
                userService,
                pubSubService,
                quickDepositIframeService,
                timeService,
                router,
                changeDetectorRef,
                gtmService,
                domSanitizer,
                betpackCmsService,
                dialogService,
                sessionStorage,
                platformLocation
            );
            spyOn(component, 'closeThisDialog');
            expect(platformLocation.onPopState).toHaveBeenCalled();
        }));
    });

    describe('ngOnInit', () => {
        it('should call on load', fakeAsync(() => {
            const parentNgOnInit = spyOn(BetpackInfoPageComponent.prototype['__proto__'], 'ngOnInit');
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({}));
            component.bp = component.params.data.bp;
            betpackCmsService.kycVerified = true;
            spyOn(component, 'scrollTodescription');
            spyOn(component, 'afterBPLoginHandler');
            userService.isInShopUser = jasmine.createSpy('isInShopUser').and.returnValue(false);
            component.ngOnInit();
            expect(parentNgOnInit).toHaveBeenCalled();
            expect(pubSubService.subscribe).toHaveBeenCalled();
            expect(component.scrollTodescription).toHaveBeenCalled();
        }));

        it('should listen in case of user balance changed for quick deposit user', fakeAsync(() => {
            const parentNgOnInit = spyOn(BetpackInfoPageComponent.prototype['__proto__'], 'ngOnInit');
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({}));
            component.bp = component.params.data.bp;
            component.isQuickDepositEnabled = true;
            component.betpackLabels = component.params.data.betpackLabels;
            spyOn(component, 'checkKYC');
            spyOn(component, 'scrollTodescription');
            spyOn(component, 'afterBPLoginHandler');
            component.ngOnInit();
            expect(pubSubService.subscribe).toHaveBeenCalled();
            expect(component.disableBuyBtn).toBeFalsy();
            expect(component.depositWarn).toBeFalsy();
            expect(component.buyNowBtn).toBe(component.betpackLabels.buyButtonLabel + ' - ' + component.bp.betPackPurchaseAmount);
            expect(sessionStorage.remove).toHaveBeenCalled();
            expect(component.isQuickDepositEnabled).toEqual(null);
        }));

        it('should listen in case of user balance changed for regular user', fakeAsync(() => {
            const parentNgOnInit = spyOn(BetpackInfoPageComponent.prototype['__proto__'], 'ngOnInit');
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({}));
            component.bp = component.params.data.bp;
            component.betpackLabels = component.params.data.betpackLabels;
            spyOn(component, 'checkKYC');
            spyOn(component, 'scrollTodescription');
            spyOn(component, 'afterBPLoginHandler');
            component.ngOnInit();
            expect(sessionStorage.remove).not.toHaveBeenCalled();
        }));
    });

    describe('open', () => {
        beforeEach(() => {
            spyOn(component, 'checkKYC');
        });
        it('bet pack popup open in case of less info button clicked', fakeAsync(() => {
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({ signPost: 'max1', signPostTooltip: 'maximum one can be purchased', betpackId: 1 }));
            component.open();
            expect(windowRef.document.body.classList.add).toHaveBeenCalledWith('betpack-modal-open');
            expect(component.buyNowBtn).toBe(component.betpackLabels.buyNowLabel + ' - ' + component.bp.betPackPurchaseAmount);
            expect(component.header).toBe(component.betpackLabels.betPackInfoLabel);
            expect(component.params.data.reviewPage).toBe(component.params.data.reviewPage);
            expect(component.moreInfoBtn).toBe(component.params.data.betpackLabels.lessInfoLabel);
        }));

        it('should show more info button in case of less info button clicked in popup', fakeAsync(() => {
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({ signPost: 'max1', signPostTooltip: 'maximum one can be purchased', betpackId: 1 }));
            component.buyNowBtn = component.params.data.betpackLabels.gotoMyBetPacksLabel;
            component.open();
            expect(component.params.data.clicked).toBe(false);
            expect(component.moreInfoBtn).toBe(component.params.data.betpackLabels.moreInfoLabel);
        }));

        it('bet pack popup open in case of Buy button clicked', fakeAsync(() => {
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({ signPost: 'max1', signPostTooltip: 'maximum one can be purchased', betpackId: 2 }));
            component.params.data.isBuyInfoClicked = true;
            component.open();
            expect(component.buyNowBtn).toBe(component.betpackLabels.buyButtonLabel + ' - ' + component.bp.betPackPurchaseAmount);
            expect(component.header).toBe(component.betpackLabels.buyBetPackLabel);
        }));

        it('bet pack popup open in case of more info button clicked', fakeAsync(() => {
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({ signPost: 'max1', signPostTooltip: 'maximum one can be purchased', betpackId: 2 }));
            component.params.data.clicked = true;
            component.open();
            expect(component.buyNowBtn).toBe(component.betpackLabels.buyNowLabel + ' - ' + component.bp.betPackPurchaseAmount);
            expect(component.header).toBe(component.betpackLabels.betPackInfoLabel);
            expect(component.params.data.reviewPage).toBe(component.params.data.reviewPage);
            expect(component.moreInfoBtn).toBe(component.params.data.betpackLabels.lessInfoLabel);
        }));

        it('bet pack popup open in case of Buy button clicked', fakeAsync(() => {
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({ signPost: 'max1', signPostTooltip: 'maximum one can be purchased', betpackId: 1 }));
            component.params.data.isBuyInfoClicked = true;
            component.open();
            expect(component.buyNowBtn).toBe(component.betpackLabels.buyButtonLabel + ' - ' + component.bp.betPackPurchaseAmount);
            expect(component.header).toBe(component.betpackLabels.buyBetPackLabel);
        }));

        it('should disable buy button in popup incase of maxPurchasedLabel sign posting', fakeAsync(() => {
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({ signPost: 'max1', signPostTooltip: 'maximum one can be purchased', betpackId: 1 }));
            component.params.data.signPostingMsg = component.params.data.betpackLabels.maxPurchasedLabel;
            component.open();
            expect(component.params.data.isBuyInfoClicked).toBeFalsy();
        }));

        it('should disable buy button in popup incase of maxPurchasedLabel sign posting', fakeAsync(() => {
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({ signPost: 'max1', signPostTooltip: 'maximum one can be purchased', betpackId: 1 }));
            component.params.data.signPostingMsg = component.params.data.betpackLabels.endedLabel;
            component.open();
            expect(component.params.data.isBuyInfoClicked).toBeFalsy();
        }));

        it('should disable buy button in popup incase of maxPurchasedLabel sign posting', fakeAsync(() => {
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({ signPost: 'max1', signPostTooltip: 'maximum one can be purchased', betpackId: 1 }));
            component.params.data.signPostingMsg = component.params.data.betpackLabels.soldOutLabel;
            component.open();
            expect(component.params.data.isBuyInfoClicked).toBeFalsy();
        }));

        it('should show timer in case of for expiresInLabel is available', fakeAsync(() => {
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({ signPost: 'max1', signPostTooltip: 'maximum one can be purchased', betpackId: 1 }));
            component.params.data.signPostingMsg = "EXPIRES IN";
            component.params.data.bp.expiresIntimer = new Date().getTime();
            spyOn(component, 'buttonState');
            component.open();
            expect(component.buttonState).toHaveBeenCalled();
        }));

        it('should not show timer in case of no expiresInLabel is available', fakeAsync(() => {
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({ signPost: 'max1', signPostTooltip: 'maximum one can be purchased', betpackId: 1 }));
            component.params.data.signPostingMsg = component.params.data.betpackLabels.soldOutLabel;
            spyOn(component, 'buttonState');
            component.open();
            expect(component.buttonState).toHaveBeenCalled();
        }));

        it('should show timer after betpack time is updated', fakeAsync(() => {
            pubSubService.subscribe = jasmine.createSpy('subscribe').and.callFake((arg0, arg2, fn) => fn({ signPost: 'max1', signPostTooltip: 'maximum one can be purchased', betpackId: 1, expiresIntimer: new Date().getTime() }));
            component.params.data.signPostingMsg = "Ending Soon";
            spyOn(component, 'buttonState');
            component.open();
            expect(component.params.data.bp.expiresIntimer).toBeDefined();
            expect(component.buttonState).toHaveBeenCalled();
        }));
    });

    describe('closeThisDialog', () => {
        it('should close dialog', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.isQuickDepositEnabled = true;
            component.closeThisDialog();
            tick(1000);
            expect(component.moreInfoBtn).toBe(component.betpackLabels.moreInfoLabel);
            expect(pubSubService.publish).toHaveBeenCalledWith('CLOSE_DIALOG', true);
            expect(dialogService.closeDialog).toHaveBeenCalledWith(dialogService.API.betpackInfoDialog);
            expect(sessionStorage.remove).toHaveBeenCalled();
            flush();
        }));

        it('should close dialog in case of min deposit', fakeAsync(() => {
            component.depositWarn = true;
            component.bp = component.params.data.bp;
            component.betpackLabels = component.params.data.betpackLabels;
            component.isQuickDepositEnabled = false;
            component.closeThisDialog();
            tick(1000);
            expect(component.moreInfoBtn).toBe(component.betpackLabels.moreInfoLabel);
            expect(pubSubService.publish).toHaveBeenCalledWith('CLOSE_DIALOG', true);
            expect(dialogService.closeDialog).toHaveBeenCalledWith(dialogService.API.betpackInfoDialog);
            expect(sessionStorage.remove).not.toHaveBeenCalled();
            flush()
        }));

        it('should close dialog in case of kyc error', fakeAsync(() => {
            component.kycEnable = true;
            component.bp = component.params.data.bp;
            component.betpackLabels = component.params.data.betpackLabels;
            component.closeThisDialog();
            tick(1000);
            expect(component.moreInfoBtn).toBe(component.betpackLabels.moreInfoLabel);
            expect(pubSubService.publish).toHaveBeenCalledWith('CLOSE_DIALOG', true);
            expect(dialogService.closeDialog).toHaveBeenCalledWith(dialogService.API.betpackInfoDialog);
            flush();
        }));

        it('should close dialog in case of suspended error', fakeAsync(() => {
            component.suspendedBanner = true;
            component.bp = component.params.data.bp;
            component.betpackLabels = component.params.data.betpackLabels;
            component.closeThisDialog();
            tick(1000);
            expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('betpack-modal-open');
            expect(component.moreInfoBtn).toBe(component.betpackLabels.moreInfoLabel);
            expect(pubSubService.publish).toHaveBeenCalledWith('CLOSE_DIALOG', true);
            expect(dialogService.closeDialog).toHaveBeenCalledWith(dialogService.API.betpackInfoDialog);
            flush();
        }));
    });

    describe('moreInfoClickEvent', () => {
        it('should show less info text when more info button clicked false', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.bp = component.params.data.bp;
            component.params.data.clicked = false;
            spyOn(component, 'sendGtmData');
            spyOn(component, 'scrollTodescription');
            component.moreInfoClickEvent();
            expect(component.moreInfoBtn).toBe(component.params.data.betpackLabels.lessInfoLabel);
            expect(component.scrollTodescription).toHaveBeenCalled();

        }));

        it('should show less info text when more info button clicked true', fakeAsync(() => {
            component.bp = component.params.data.bp;
            component.params.data.clicked = true;
            component.betpackLabels = component.params.data.betpackLabels;
            spyOn(component, 'sendGtmData');
            spyOn(component, 'scrollTodescription');
            component.moreInfoClickEvent();
            expect(component.moreInfoBtn).toBe(component.params.data.betpackLabels.moreInfoLabel);
            expect(component.scrollTodescription).toHaveBeenCalled();
        }));
    });

    describe('buyNowClickEvent', () => {
        it('should show Buy now popup on click of buy button in feature betpack section', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.bp = component.params.data.bp;
            component.params.data.isBuyInfoClicked = true;
            component.params.data.clicked = false;
            spyOn(component, 'dailogButton');
            spyOn(component, 'sendGtmData');
            component.buyNowClickEvent();
            expect(component.dailogButton).toHaveBeenCalled();
        }));

        it('should show Buy now popup on click of buy button in betpack info popup page', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.params.data.isBuyInfoClicked = false;
            component.params.data.clicked = true;
            component.bp = component.params.data.bp;
            spyOn(component, 'sendGtmData');
            component.buyNowClickEvent();
            expect(component.buyNowBtn).toBe(component.betpackLabels.buyButtonLabel + ' - ' + component.params.data.bp.betPackPurchaseAmount);
            expect(component.header).toBe(component.betpackLabels.buyBetPackLabel);
        }));

        it('should navigate to betpack review', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.params.data.isBuyInfoClicked = true;
            component.params.data.clicked = false;
            component.buyNowBtn = component.betpackLabels.gotoMyBetPacksLabel;
            component.bp = component.params.data.bp;
            spyOn(component, 'closeThisDialog');
            spyOn(component, 'sendGtmData');
            component.buyNowClickEvent();
            expect(component['router'].navigateByUrl).toHaveBeenCalledWith('betbundle-review');
            expect(component.closeThisDialog).toHaveBeenCalled();
        }));
    });

    describe('buyNowBetTrigger', () => {
        it('should invoke onBuyBetPack successfully', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            spyOn(component, 'sendGtmData');
            spyOn(component, 'sendGtmDataError');
            component.buyNowBetTrigger();
            expect(component.reviewFlag).toBeTruthy();
            expect(component.buyNowBtn).toBe(component.betpackLabels.gotoMyBetPacksLabel);
            expect(component.errorMsg).toBe(component.betpackLabels.betPackSuccessMessage);
            expect(component.quickDepositPanel).toBeFalsy();
            expect(component.review).toBeFalsy();
            expect(component.params.data.isBuyInfoClicked).toBe(true);
            flush()
        }));

        it('should invoke onBuyBetPack faiure case', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels; component.bp = component.params.data.bp;
            component.betpromotionsService.onBuyBetPack = jasmine.createSpy().and.returnValue(throwError({
                msg: 'INSUFFICIENT_FUNDS'
            }));
            component.reviewPage = true;
            spyOn(component, 'sendGtmData');
            spyOn(component, 'sendGtmDataError');
            component.buyNowBetTrigger();
            expect(component.reviewFlag).toBeFalsy();
            expect(component.depositWarn).toBeTruthy();
            expect(component.errorMsg).toBe(component.betpackLabels.depositMessage);
            expect(component.buyNowBtn).toBe('MAKE A DEPOSIT');
            flush()
        }));

        it('should invoke onBuyBetPack faiure case', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.bp = component.params.data.bp;
            component.betpromotionsService.onBuyBetPack = jasmine.createSpy().and.returnValue(throwError({
                msg: 'FAILED_TO_AWARD_TOKEN'
            }));
            component.reviewPage = false;
            spyOn(component, 'sendGtmData');
            spyOn(component, 'sendGtmDataError');
            component.buyNowBetTrigger();
            expect(component.reviewFlag).toBeFalsy();
            expect(component.suspendedBanner).toBeTruthy();
            expect(component.errorMsg).toBe(component.betpackLabels.serviceError);
            flush()
        }));
    });

    describe('betPlaced', () => {
        it('should show the timer when bet pack is placed', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.betPlaced(component.betpackLabels.gotoMyBetPacksLabel);
            expect(component.betDate).toBeDefined();
            expect(component.betTime).toBeDefined();
        }));

        it('should not show the timer when bet pack is placed', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.betPlaced(component.betpackLabels.buyButtonLabel);
            expect(component.betDate).toBeUndefined();
            expect(component.betTime).toBeUndefined();
        }));
    });

    describe('dailogButton', () => {
        it('should show error message in dialog bor for in-shop customer', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.bp = component.params.data.bp;
            component.buyNowBtn = component.betpackLabels.buyButtonLabel + " - " + component.bp.betPackPurchaseAmount;
            component.userService.status = false;
            component.dailogButton();
            expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'betpack' });
        }));

        it('should show error message in dialog in case of kyc not verified', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.bp = component.params.data.bp;
            component.buyNowBtn = component.betpackLabels.buyButtonLabel + " - " + component.bp.betPackPurchaseAmount;
            component.userService.status = true;
            betpackCmsService.kycVerified = false;
            component.dailogButton();
            expect(component.errorMsg).toBe(component.betpackLabels.kycArcGenericMessage);
            expect(component.kycEnable).toBeTruthy();
        }));

        it('should show error message in dialog in case of kyc verification is pending', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.bp = component.params.data.bp;
            component.buyNowBtn = component.betpackLabels.buyButtonLabel + " - " + component.bp.betPackPurchaseAmount;
            component.userService.status = true;
            betpackCmsService.kycVerified = true;
            betpackCmsService.verificationStatus = 'Pending';
            component.dailogButton();
            expect(component.errorMsg).toBe(component.betpackLabels.kycArcGenericMessage);
            expect(component.kycEnable).toBeTruthy();
        }));

        it('should not show error message in dialog bor for other customers', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.bp = component.params.data.bp;
            betpackCmsService.kycVerified = true;
            betpackCmsService.verificationStatus = 'completed';
            component.buyNowBtn = component.betpackLabels.buyButtonLabel + " - " + component.bp.betPackPurchaseAmount;
            component.userService.isInShopUser = jasmine.createSpy('isInShopUser').and.returnValue(false);
            component.userService.status = false;
            component.dailogButton();
            expect(component.errorMsg).toBe(undefined);
            expect(component.kycEnable).toBeFalsy();
        }));

        it('should invoke buyNowBetTrigger', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.bp = component.params.data.bp;
            component.buyNowBtn = component.betpackLabels.buyButtonLabel + " - " + component.bp.betPackPurchaseAmount;
            component.userService.status = true;
            betpackCmsService.kycVerified = true;
            userService.isInShopUser = jasmine.createSpy('isInShopUser').and.returnValue(false);
            spyOn(component, 'buyNowBetTrigger');
            component.dailogButton();
            expect(component.buyNowBetTrigger).toHaveBeenCalled();
        }));

        it('should redirect to deposit page in case of regular user', fakeAsync(() => {
            component.buyNowBtn = 'MAKE A DEPOSIT';
            component.betpackLabels = component.params.data.betpackLabels;
            component.bp = component.params.data.bp;
            spyOn(component, 'closeThisDialog');
            component.dailogButton();
            expect(quickDepositIframeService.redirectToDepositPage).toHaveBeenCalled();
            expect(component.closeThisDialog).toHaveBeenCalled();
        }));

        it('should show card details in iframe without closing betpack popup for quick deposit user', fakeAsync(() => {
            component.buyNowBtn = 'MAKE A DEPOSIT';
            component.betpackLabels = component.params.data.betpackLabels;
            component.bp = component.params.data.bp;
            quickDepositIframeService.isEnabled = jasmine.createSpy('isEnabled').and.returnValue(of(true));
            spyOn(component, 'closeThisDialog');
            component.dailogButton();
            expect(quickDepositIframeService.redirectToDepositPage).toHaveBeenCalled();
            expect(component.closeThisDialog).not.toHaveBeenCalled();
        }));

        it('should redirect to deposit page in case of quickDepositIframeService throws error', fakeAsync(() => {
            component.buyNowBtn = 'MAKE A DEPOSIT';
            component.betpackLabels = component.params.data.betpackLabels;
            component.bp = component.params.data.bp;
            quickDepositIframeService.isEnabled = jasmine.createSpy('isEnabled').and.returnValue(throwError('error'));
            spyOn(component, 'closeThisDialog');
            component.dailogButton();
            expect(quickDepositIframeService.redirectToDepositPage).toHaveBeenCalled();
            expect(component.closeThisDialog).toHaveBeenCalled();
        }));

        it('should close', fakeAsync(() => {
            component.buyNowBtn = 'CLOSE';
            component.betpackLabels = component.params.data.betpackLabels;
            component.bp = component.params.data.bp;
            spyOn(component, 'closeThisDialog');
            component.dailogButton();
            expect(component.closeThisDialog).toHaveBeenCalled();
        }));
    });

    describe('signPostingBkg', () => {
        it('should apply warning style for maxPurchasedLabel signposting-1', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.params.data.signPostingMsg = component.params.data.betpackLabels.maxPurchasedLabel;
            component.signPostingBkg(component.params.data.signPostingMsg);
            expect(component.params.data.isBuyInfoClicked).toBe(null);
            expect(component.disableBuyBtn).toBeTruthy();
        }));

        it('should apply warning style for ended label signposting', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.params.data.signPostingMsg = component.params.data.betpackLabels.endedLabel;
            component.signPostingBkg(component.params.data.signPostingMsg);
            expect(component.params.data.isBuyInfoClicked).toBe(null);
            expect(component.disableBuyBtn).toBeTruthy();
        }));

        it('should apply warning style for soldout label signposting', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.params.data.signPostingMsg = component.params.data.betpackLabels.soldOutLabel;
            component.signPostingBkg(component.params.data.signPostingMsg);
            expect(component.params.data.isBuyInfoClicked).toBe(null);
            expect(component.disableBuyBtn).toBeTruthy();
        }));
        it('should apply for empty label signposting', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.params.data.signPostingMsg = component.params.data.betpackLabels.emptyLabel;
            component.signPostingBkg(component.params.data.signPostingMsg);
            const style = component.signPostingBkg(component.params.data.signPostingMsg);
            expect(style).toEqual({ 'background-color': '#FFFFFF', 'color': '#FFFFFF' });
        }));

        it('should not apply warning style for maxPurchasedLabel signposting', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.disableBuyBtn = false;
            component.params.data.signPostingMsg = component.params.data.betpackLabels.limitedLabel;
            const style = component.signPostingBkg(component.params.data.signPostingMsg);
            expect(style).toEqual({ 'background-color': '#FFF270', 'color': '#07294B' });
        }));
        it('should not apply warning style for comingsoon signposting', fakeAsync(() => {
            component.betpackLabels = component.params.data.betpackLabels;
            component.disableBuyBtn = false;
            component.params.data.signPostingMsg = component.params.data.betpackLabels.comingSoon;
            const style = component.signPostingBkg(component.params.data.signPostingMsg);
            expect(style).toEqual({ 'background-color': '#8D5BA1', 'color': '#FFFFFF' });
        }));
    });


    describe('sendGtmData', () => {
        it('sendGtmDataCalled form review page', () => {
            component.reviewPage=true
            component.reviewFlag =false
            component.bp = {
                betPackId: 1,
                purchased: false,
                betPackPurchaseAmount: '4'
            } as any;
            component['sendGtmData']('less info');
            expect(gtmService.push).toHaveBeenCalledWith('trackEvent',{ event: 'trackEvent', eventAction: 'my bet bundles', eventCategory: 'bet bundles marketplace', eventLabel: 'less info', promoType: 'bet bundles-1' });
        });
        it('sendGtmDataCalled form review page', () => {
            component.reviewPage=false
            component.reviewFlag =true
            component.bp = {
                betPackId: 1,
                purchased: false,
                betPackPurchaseAmount: '4'
            } as any;
            component['sendGtmData']('less info');
            expect(gtmService.push).toHaveBeenCalledWith('trackEvent', { event: 'trackEvent', eventAction: 'bundle receipt', eventCategory: 'bet bundles marketplace', eventLabel: 'less info', promoType: 'bet bundles-1' });
        });
        it('sendGtmDataCalled form review page', () => {
            component.reviewPage=false
            component.reviewFlag =false
            component.bp = {
                betPackId: 1,
                purchased: false,
                betPackPurchaseAmount: '4'
            } as any;
            component['sendGtmData']('less info');
            expect(gtmService.push).toHaveBeenCalledWith('trackEvent',{ event: 'trackEvent', eventAction: 'bet bundles', eventCategory: 'bet bundles marketplace', eventLabel: 'less info', promoType: 'bet bundles-1' });
        });
    });

    describe('sendGtmDataError', () => {
        it('sendGtmDataErrorCalled', () => {
            component.bp = {
                betPackId: 1,
                purchased: false,
                betPackPurchaseAmount: '4'
            } as any;
            component.reviewPage = true;
            component['sendGtmDataError']('less info')
            expect(gtmService.push).toHaveBeenCalled();
        });

        it('sendGtmDataErrorCalled in case of betpack', () => {
            component.bp = {
                betPackId: 1,
                purchased: false,
                betPackPurchaseAmount: '4'
            } as any;
            component.reviewPage = false;
            component['sendGtmDataError']('less info')
            expect(gtmService.push).toHaveBeenCalled();
        });
    });

    describe('useNow', () => {
        it('should navigate to deeplink url in case of url doesn\'t start with /', () => {
            router.url = '/sport/basketball/matches';
            spyOn(component, 'sendGtmData');
            spyOn(component, 'closeThisDialog');
            component.useNow('use now', 'sport/basketball/matches');
            component[router.routeReuseStrategy.shouldReuseRoute()];
            expect(router.navigateByUrl).toHaveBeenCalledWith('/sport/basketball/matches');
            expect(component.sendGtmData).toHaveBeenCalled();
            expect(component.closeThisDialog).toHaveBeenCalled();
        });

        it('should navigate to deeplink url in case of url start with /', () => {
            spyOn(component, 'sendGtmData');
            spyOn(component, 'closeThisDialog');
            component.useNow('use now', '/sport/basketball/matches');
            component[router.routeReuseStrategy.shouldReuseRoute()];
            expect(router.navigateByUrl).toHaveBeenCalledWith('/sport/basketball/matches');
            expect(component.sendGtmData).toHaveBeenCalled();
            expect(component.closeThisDialog).toHaveBeenCalled();
        });
    });

    describe('sendGMTWhileClose', () => {
        it('should invoke GA event in case of min deposit', () => {
            component.depositWarn = true;
            spyOn(component, 'sendGtmData');
            component.sendGMTWhileClose();
            expect(component.sendGtmData).toHaveBeenCalledWith('fail - exit');
        });

        it('should invoke GA event in case of kyc error', () => {
            component.kycEnable = true;
            spyOn(component, 'sendGtmData');
            component.sendGMTWhileClose();
            expect(component.sendGtmData).toHaveBeenCalledWith('fail - exit');
        });

        it('should invoke GA event in case of suspended error', () => {
            component.suspendedBanner = true;
            spyOn(component, 'sendGtmData');
            component.sendGMTWhileClose();
            expect(component.sendGtmData).toHaveBeenCalledWith('fail - exit');
        });

        it('should invoke GA event in case of no error', () => {
            component.suspendedBanner = false;
            component.kycEnable = false;
            component.depositWarn = false;
            spyOn(component, 'sendGtmData');
            component.sendGMTWhileClose();
            expect(component.sendGtmData).toHaveBeenCalledWith('exit');
        });
    });

    describe('ontimerEmits', () => {
        it('should call on ontimerEmits', fakeAsync(() => {
            component.betpackLabels = { endedLabel: 'Ended' };
            component.ontimerEmits(false);
            expect(component.isExpiresIn).toBeFalse();
            expect(component.disableBuyBtn).toBeTruthy();
            expect(component.params.data.signPostingMsg).toBe(component.betpackLabels.endedLabel);
            expect(component.signPostingToolTip).toBe(component.betpackLabels.endedTooltip);

        }));
    });

    describe('ngOnDestroy', () => {
        it('should call on ngOnDestroy', fakeAsync(() => {
            component.ngOnDestroy();
            expect(windowRef.document.body.classList.remove).toHaveBeenCalledWith('betpack-modal-open');
            expect(component.isExpiresIn).toBeFalse();
        }));
    });

    describe('buttonState', () => {
        it('if signPosting msg is max purchased && buyNowBtn notEqual to gotoMyBetPacksLabel  ', fakeAsync(() => {
            component.betpackLabels = { maxPurchasedLabel: 'maxPurchasedLabel' };
            component.reviewFlag = false;
            component.buttonState();
            expect(component.disableBuyBtn).toBeTruthy();
            expect(component.params.data.isBuyInfoClicked ).toBeUndefined();
        }));

        it('if signPosting msg is ended Label && buyNowBtn notEqual to gotoMyBetPacksLabel  ', fakeAsync(() => {
            component.betpackLabels = { endedLabel : 'ENDED' };
            component.reviewFlag = false;
            component.buttonState();
            expect(component.disableBuyBtn).toBeTruthy();
            expect(component.params.data.isBuyInfoClicked ).toBeUndefined();
        }));

        it('if signPosting msg is soldOut Label && buyNowBtn notEqual to gotoMyBetPacksLabel  ', fakeAsync(() => {
            component.betpackLabels = { soldOutLabel : 'SOLD OUT' };
            component.reviewFlag = false;
            component.buttonState();
            expect(component.disableBuyBtn).toBeTruthy();
            expect(component.params.data.isBuyInfoClicked ).toBeUndefined();
        }));

        it('if no signPosting msg', fakeAsync(() => {
            component.betpackLabels = { gotoMyBetPacksLabel : 'Go to my betpack', soldOutLabel : 'SOLD OUT' };
            component.buyNowBtn = component.betpackLabels.gotoMyBetPacksLabel;
            component.reviewFlag= false;
            component.buttonState();
            expect(component.disableBuyBtn).toBeTruthy();
            expect(component.params.data.isBuyInfoClicked ).toBeUndefined();
        }));
    });

    describe('afterLoginHandler', () => {
        it('should close the dialog after login', fakeAsync(() => {
            spyOn(component, 'closeThisDialog');
            component.afterBPLoginHandler();
            expect(sessionStorage.set).toHaveBeenCalledWith('betpackData', component.params.data);
            expect(component.closeThisDialog).toHaveBeenCalled();
        }));
    });

    describe('scrollTodescription', () => {
        it('scrollTodescription if condition', fakeAsync(() => {
            component.scrollTodescription();
            tick(0);
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('.betpack-info-desc');
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('.betpack-more-info');

            discardPeriodicTasks();
        }));

        it('scrollTodescription else if condition', fakeAsync(() => {
            component.params.data.clicked = false;
            component.scrollTodescription();
            tick(0);
            expect(windowRef.document.querySelector).toHaveBeenCalledWith('.betpack-more-info');
            discardPeriodicTasks();
        }));

        it('scrollTodescription if no betpack params', fakeAsync(() => {
            component.params.data = null;
            component.scrollTodescription();
            tick(0);
            expect(windowRef.document.querySelector).not.toHaveBeenCalled();
            discardPeriodicTasks();
        }));
    });

    describe('checkStatus', () => {
        it('checkStatus called', fakeAsync(() => {
            component.betpackLabels = { comingSoon: 'ComingSoon' }
            expect(component.checkStatus("ComingSoon")).toBeTrue();
            discardPeriodicTasks();
        }));
        it('checkStatus called', fakeAsync(() => {
            component.betpackLabels = { comingSoon: 'ComingSoon' }
            expect(component.checkStatus("test")).toBeFalse();
            discardPeriodicTasks();
        }));
    });
});