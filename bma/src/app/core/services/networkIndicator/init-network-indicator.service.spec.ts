import { InitNetworkIndicatorService } from './init-network-indicator.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import environment from '@environment/oxygenEnvConfig';

describe('InitNetworkIndicatorService', () => {
    let service: InitNetworkIndicatorService;
    let windowRef;
    let pubSubService;
    let rendererService;

    beforeEach(() => {
        windowRef = {
            nativeWindow: {
                setTimeout: jasmine.createSpy('setTimeout').and.callFake(fn => fn()),
                clearTimeout: jasmine.createSpy('clearTimeout')
            },
            document: {
                querySelector: jasmine.createSpy()
            }
        } as any;
        pubSubService = {
            subscribe: jasmine.createSpy().and.callFake((sb, ch, fn) => {
                fn();
            }),
            cbMap: {},
            publish: jasmine.createSpy(),
            unsubscribe: jasmine.createSpy('unsubscribe'),
            API: pubSubApi
        } as any;
        rendererService = {
            renderer: {
                listen: jasmine.createSpy(),
                removeClass: jasmine.createSpy(),
                addClass: jasmine.createSpy()
            }
        };
        service = new InitNetworkIndicatorService(
            pubSubService, rendererService, windowRef
        );
    });

    describe('#subscribeToNetworkIndicatorEvents', () => {
        it('should init pubsub listeners and call addclass if element is present', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue({});
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === pubSubService.API['show-slide-out-betslip-true']) {
                    fn(true);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.addClass).toHaveBeenCalled();
        });

        it('should init pubsub listeners and call addclass if element is not present', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue(null);
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === pubSubService.API['show-slide-out-betslip-true']) {
                    fn(true);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.addClass).not.toHaveBeenCalled();
        });

        it('should init pubsub listeners and call addclass if element is present for show-slide-out-betslip-false', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue({});
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === pubSubService.API['show-slide-out-betslip-false']) {
                    fn(true);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.removeClass).toHaveBeenCalled();
        });

        it('should init pubsub listeners and call addclass if element is not present for show-slide-out-betslip-false', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue(null);
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === pubSubService.API['show-slide-out-betslip-false']) {
                    fn(true);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.removeClass).not.toHaveBeenCalled();
        });

        it('should init pubsub listeners and call addclass if element is present for QUICKBET_OPENED', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue({});
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === pubSubService.API.QUICKBET_OPENED) {
                    fn(true);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.addClass).toHaveBeenCalled();
        });

        it('should init pubsub listeners and call addclass if element is not present for QUICKBET_OPENED', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue(null);
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === pubSubService.API.QUICKBET_OPENED) {
                    fn(true);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.addClass).not.toHaveBeenCalled();
        });

        it('should init pubsub listeners and call addclass if element is present for QUICKBET_PANEL_CLOSE', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue({});
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === pubSubService.API.QUICKBET_PANEL_CLOSE) {
                    fn(true);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.removeClass).toHaveBeenCalled();
        });

        it('should init pubsub listeners and call addclass if element is not present for QUICKBET_PANEL_CLOSE', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue(null);
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === pubSubService.API.QUICKBET_PANEL_CLOSE) {
                    fn(true);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.removeClass).not.toHaveBeenCalled();
        });


        it('should init pubsub listeners and not call addclass if element is not present', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue(null);
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.addClass).not.toHaveBeenCalled();
            expect(rendererService.renderer.removeClass).not.toHaveBeenCalled();
        });

        it('should init pubsub listeners for NETWORK_INDICATOR_BOTTOM and displayStatus is true', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue({});
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === 'NETWORK_INDICATOR_BOTTOM') {
                    fn(true);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.addClass).toHaveBeenCalled();
        });

        it('should init pubsub listeners for NETWORK_INDICATOR_BOTTOM and displayStatus is false', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue({});
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === 'NETWORK_INDICATOR_BOTTOM') {
                    fn(false);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.removeClass).toHaveBeenCalled();
        });

        it('should init pubsub listeners for NETWORK_INDICATOR_BOTTOM_INDEX and displayStatus is true', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue({});
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === 'NETWORK_INDICATOR_BOTTOM_INDEX') {
                    fn(true);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.addClass).toHaveBeenCalled();
        });

        it('should init pubsub listeners for NETWORK_INDICATOR_BOTTOM_INDEX and displayStatus is false', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue({});
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === 'NETWORK_INDICATOR_BOTTOM_INDEX') {
                    fn(false);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.removeClass).toHaveBeenCalled();
        });

        it('should init pubsub listeners for NETWORK_INDICATOR_INDEX_HIDE and displayStatus is true', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue({});
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === 'NETWORK_INDICATOR_INDEX_HIDE') {
                    fn(true);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.addClass).toHaveBeenCalled();
        });

        it('should init pubsub listeners for NETWORK_INDICATOR_INDEX_HIDE and displayStatus is false', () => {
            service['getNetworkIndicatorEl'] = jasmine.createSpy('getNetworkIndicatorEl').and.returnValue({});
            service['pubSubService'].subscribe = jasmine.createSpy().and.callFake((sb, ch, fn) => {
                if (ch === 'NETWORK_INDICATOR_INDEX_HIDE') {
                    fn(false);
                }
            });
            service['subscribeToNetworkIndicatorEvents']();
            expect(rendererService.renderer.removeClass).toHaveBeenCalled();
        });
    });

    describe('#getNetworkIndicatorEl', () => {
        it('should return the element based on brand for coral', () => {
            environment.brand = 'bma';
            service['isCoral'] = true;
            windowRef.document.querySelector = jasmine.createSpy('querySelector').and.returnValue({});
            expect(service['getNetworkIndicatorEl']()).toEqual({} as any);
        });
        it('should return null if element not found for coral', () => {
            environment.brand = 'bma';
            windowRef.document.querySelector = jasmine.createSpy('querySelector').and.returnValue(null);
            expect(service['getNetworkIndicatorEl']()).toEqual(null);
        });
        it('should return the element based on brand for ladbrokes', () => {
            environment.brand = 'ladbrokes';
            windowRef.document.querySelector = jasmine.createSpy('querySelector').and.returnValue({});
            expect(service['getNetworkIndicatorEl']()).toEqual({} as any);
        });
        it('should return null if element not found for ladbrokes', () => {
            environment.brand = 'ladbrokes';
            windowRef.document.querySelector = jasmine.createSpy('querySelector').and.returnValue(null);
            expect(service['getNetworkIndicatorEl']()).toEqual(null);
        });
    });

    it('should call subscribeToNetworkIndicatorEvents on init', () => {
        service['subscribeToNetworkIndicatorEvents'] = jasmine.createSpy('subscribeToNetworkIndicatorEvents');
        service['init']();
        expect(service['subscribeToNetworkIndicatorEvents']).toHaveBeenCalled();
    });
});