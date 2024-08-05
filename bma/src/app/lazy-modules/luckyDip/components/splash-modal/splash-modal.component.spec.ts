import { SplashModalComponent } from "@lazy-modules/luckyDip/components/splash-modal/splash-modal.component";
import { pubSubApi } from "@app/core/services/communication/pubsub/pubsub-api.constant";
import { of } from "rxjs";
import { LUCKY_DIP_CONSTANTS } from '@lazy-modules/luckyDip/constants/lucky-dip-constants';

describe('SplashModalComponent', () => {
    let component, deviceService, windowRef, pubsub,
        gtmTrackingService,
        domToolsService,
        quickBetService, serviceClosureService, ldCmsService, storage, changeDetectorRef,domSanitizer;

    let mockData, closeDialogSpy;
    const eventEntity = {
        categoryId: '',
        typeId: '',
        id: '',
        eventIsLive: true,
        typeName: '',
    } as any;
    const market = { rawHandicapValue: '10' }, outcome = {
        id: '',
        modifiedPrice: '',
        outcomeMeaningMajorCode: '',
        prices: [{
            priceType: '',
            handicapValueDec: 'a,bcd'
        }, {
            priceType: ''
        }]
    };

    beforeEach(() => {
        closeDialogSpy = spyOn(SplashModalComponent.prototype['__proto__'], 'closeDialog'),
            deviceService = {
                close: jasmine.createSpy('close')

            },
            windowRef = {
                document: {
                    body: {
                        classList: {
                            add: jasmine.createSpy('classList.add'),
                            remove: jasmine.createSpy('classList.remove')
                        }
                    },
                    getElementsByClassName: jasmine.createSpy('getElementsByClassName').and.returnValue([{
                        style: {
                          display: ''
                        }
                      }]),
                    querySelector: jasmine.createSpy('querySelector'),
                },
                nativeWindow: {
                    location: {
                        href: '/promotions'
                    },
                    screen: {
                        height: 720
                    }
                }
            },
            domSanitizer = {
                sanitize: jasmine.createSpy().and.returnValue('test'),
                bypassSecurityTrustHtml: () => { },
                bypassSecurityTrustStyle: () => { },
                bypassSecurityTrustScript: () => { },
                bypassSecurityTrustUrl: () => { },
                bypassSecurityTrustResourceUrl: () => { }
              },
            domToolsService = {
                toggleVisibility: jasmine.createSpy('toggleVisibility')
            },
            pubsub = {
                publish: jasmine.createSpy('publish'),
                subscribe: jasmine.createSpy('subscribe').and.callFake((name, method, cb) => pubsub.cbMap[method] = cb),
                unsubscribe: jasmine.createSpy('unsubscribe'),
                API: pubSubApi
            };

        storage = {
            get: jasmine.createSpy('get'),
            set: jasmine.createSpy('set'),
            remove: jasmine.createSpy('remove')
        };

        quickBetService = {
            removeSelection: jasmine.createSpy('removeSelection')
        }

        mockData = {
            dialogClass: 'splash-popup',
            data: {
                marketTitle: 'marketTitle',
                marketDescripton: 'marketDescripton',
                callConfirm: jasmine.createSpy('callConfirm')
            }
        };
        gtmTrackingService = {
            detectTracking: jasmine.createSpy('detectTracking').and.returnValue({})
        },
            ldCmsService = {
                isLuckyDipReceipt: {
                    next: jasmine.createSpy('next').and.returnValue(of())
                },
                getLuckyDipCMSAnimationData : jasmine.createSpy('getLuckyDipCMSAnimationData').and.returnValue(of('<svg></svg>'))
            };
        changeDetectorRef = {

            detectChanges: jasmine.createSpy('detectChanges')

        };

        component = new SplashModalComponent(deviceService, windowRef, storage, pubsub,
            gtmTrackingService,
            domToolsService,
            quickBetService, ldCmsService, serviceClosureService, changeDetectorRef,domSanitizer);
        component.dialog = { closeOnOutsideClick: true };

    });

    it('should create component instance', () => {
        expect(component).toBeTruthy();
    });

    describe('ngOnInit', () => {
        it('should call ngonint', () => {
            spyOn(component, 'createMarketObj');
            component.cmsConfig = {
                luckyDipFieldsConfig: {
                    playerCardDesc: '',
                    gotItCTAButton: '',
                    potentialReturnsDesc: ''
                },
                playerPageBoxImgPath: '',
            };
            component['pubsub'].subscribe = jasmine.createSpy('subscribe').and.callFake((namespace, message, callback) => {
                if (namespace === 'Lucky dip keypad') {
                    windowRef.nativeWindow.screen.height = 700;
                    callback(true);
                    windowRef.nativeWindow.screen.height = 800;
                    callback(true);
                    expect(component.isKeyPadClosed).toBeTruthy()
                }
            })
            component.ngOnInit();
            ldCmsService.getLuckyDipCMSAnimationData().subscribe()
        })
    })
    describe('open', () => {
        it('should get data', () => {
            spyOn(component, 'createMarketObj');
            component.params = mockData;
            const openSpy = spyOn(SplashModalComponent.prototype['__proto__'], 'open');

            component.open();

            expect(openSpy).toHaveBeenCalled();

        });
    });

    describe('createMarketObj', () => {
        it('should call detectTracking', () => {

            component.eventEntity = eventEntity;
            component.market = market;
            component.outcome = outcome;
            component.createMarketObj();
            outcome.prices = [];
            component.createMarketObj();
            expect(gtmTrackingService.detectTracking).toHaveBeenCalled();
        });
    });
    describe('betPlaced', () => {
        it('should call queryselector', () => {
            component.params = mockData;
            spyOn(component, 'startAnimation');
            const elementMock = document.createElement('div');
            windowRef.document.querySelector = jasmine.createSpy('querySelector').and.returnValue(elementMock);
            component.betPlaced('');
            expect(windowRef.document.querySelector).toHaveBeenCalled();
        });
    });

    describe('startAnimation', () => {
        it('should call startAnimation', (done) => {

            const value = {
                legParts: [{
                    eventDesc: 'Man City v Watford"',
                    marketDesc: 'Handicap Match Result - Man City +2.0 goals',
                    outcomeDesc: 'tie',
                    outcomeId: '955100247',
                    handicap: '+2.0'
                }],
                payout: {
                    potential: ''
                },
                price: {
                    priceDen: ''
                }
            };
            const cmsConfig = {
                luckyDipFieldsConfig: {
                    playerCardDesc: '',
                    gotItCTAButton: '',
                    potentialReturnsDesc: ''
                },
                playerPageBoxImgPath: '',

            }
            const d = {
                cmsConfig: {
                  playerPageBoxImgPath: '',
                  playerCardDesc: '',
                  potentialReturnsDesc: '',
                  gotItCTAButton: ''
                },
                playerData: {
                  playerName: '',
                  odds: '',
                  amount: ''
                },
                svg: '<svg></svg'
              }
            component.animationData = d;
            component.cmsConfig = cmsConfig;
            component.params = mockData;

            component.startAnimation(value);
        
            setTimeout(() => {
                done();
            }, 1000);
            expect(component.params).toEqual(mockData);
        });
    });

    describe('closeSplashDialog', () => {
        it('should not call queryselector', done => {
            component.selectionDataQb = {} as any;
            component.outcome = { id: '123' } as any;
            component.params = mockData;
            spyOn(component, 'startAnimation');
            const elementMock = document.createElement('div');
            windowRef.document.querySelector = jasmine.createSpy('querySelector').and.returnValue(elementMock);
            deviceService.isIos = true;
            deviceService.isWrapper = true;
            component.closeSplashDialog();

            expect(windowRef.document.querySelector).not.toHaveBeenCalled();
            setTimeout(() => {
                done();
            }, 250);
        });

        
        it('should call queryselector', done => {
            component.selectionDataQb = {} as any;
            component.outcome = { id: '123' } as any;
            component.params = mockData;
            spyOn(component, 'startAnimation');
            const elementMock = document.createElement('div');
            windowRef.document.getElementsByClassName = jasmine.createSpy('querySelector').and.returnValue([])
            windowRef.document.querySelector = jasmine.createSpy('querySelector').and.returnValue(elementMock);
            deviceService.isIos = true;
            deviceService.isWrapper = true;
            component.closeSplashDialog();

            expect(windowRef.document.querySelector).not.toHaveBeenCalled();
            setTimeout(() => {
                done();
            }, 250);
    
        });
    });

    describe('ngOnDestroy', () => {
        it('should call ngOnDestroy', () => {
            component.ngOnDestroy();
            expect(pubsub.unsubscribe).toHaveBeenCalledWith(LUCKY_DIP_CONSTANTS.LUCKY_DIP_KEYPAD);
        })
    })
});
