import { MatchRewardsMainComponent } from '@app/euro/components/matchRewardsMain/match-rewards-main.component';
import { dialogIdentifierDictionary } from '@core/constants/dialog-identifier-dictionary.constant';
import { MATCHDAY_REWARDS_MOCK } from '@app/euro/constants/matchday-rewards-data';
import { of, throwError } from 'rxjs';
import { fakeAsync, tick } from '@angular/core/testing';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { EURO_MESSAGES } from '@app/euro/constants/euro-constants';

describe('MatchRewardsMain', () => {
    let component, userService, pubSubService, componentFactoryResolver, dialogService, resolvedDialogComponent,
    deviceService, euroService, ngZone;

    beforeEach(() => {

        userService = {
            status: true,
            bppToken: '123'
        };
        pubSubService = {};
        pubSubService = new PubSubService(ngZone);
        spyOn(pubSubService, 'publish').and.callThrough();
        spyOn(pubSubService, 'subscribe').and.callThrough();
        spyOn(pubSubService, 'unsubscribe').and.callThrough();
        dialogService = {
            API: dialogIdentifierDictionary,
            openDialog: jasmine.createSpy('openDialog')
        };
        resolvedDialogComponent = {
            name: dialogService.API.howItWorksDialog
        };
        componentFactoryResolver = {
            resolveComponentFactory: jasmine.createSpy('resolveComponentFactory').and.returnValue(resolvedDialogComponent)
        };
        deviceService = {
            isMobile: true,
            isDesktop: false
        };
        ngZone = {
            runOutsideAngular: jasmine.createSpy('runOutsideAngular').and.callFake((fn) => fn())
        };
        euroService = {
            getMatchRewardsBadges: jasmine.createSpy('getMatchRewardsBadges').and.returnValue(Promise.resolve(MATCHDAY_REWARDS_MOCK)),
            getHowItWorksData: jasmine.createSpy('getHowItWorksData').and.
            returnValue(Promise.resolve({howItWorks: '<p>test1</p>'}))
        },
        component = new MatchRewardsMainComponent
        (userService, pubSubService, deviceService, euroService, componentFactoryResolver, dialogService);
    });

    describe('openPopUp', () => {
        it(`open dialog`, () => {
          (euroService['getHowItWorksData']as any).and.returnValue(of({howItWorks: '<p>test1</p>'}));
          component.openPopUp();
          expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
          expect(dialogService.openDialog).toHaveBeenCalledWith(
            'howItWorksDialog', resolvedDialogComponent, true, jasmine.any(Object)
          );
        });

        it(`open dialog with response data`, () => {
            component.euroRespData = MATCHDAY_REWARDS_MOCK;
            (euroService['getHowItWorksData'] as any).and.returnValue(of({ howItWorks: '<p>test1</p>' }));
            component.openPopUp();
            expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
            expect(dialogService.openDialog).toHaveBeenCalledWith(
                'howItWorksDialog', resolvedDialogComponent, true, jasmine.any(Object)
            );
        });

        it(`open dialog with response data with undefined`, () => {
            component.euroRespData = {};
            (euroService['getHowItWorksData'] as any).and.returnValue(of({}));
            component.openPopUp();
            expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
            expect(dialogService.openDialog).toHaveBeenCalledWith(
                'howItWorksDialog', resolvedDialogComponent, true, jasmine.any(Object)
            );
        });

        it(`open dialog with error case`, () => {
          (euroService['getHowItWorksData']as any).and.returnValue(throwError('some error'));
          component.euroRespData = MATCHDAY_REWARDS_MOCK;
          component.openPopUp();
          expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
          expect(dialogService.openDialog).toHaveBeenCalledWith(
            'howItWorksDialog', resolvedDialogComponent, true, jasmine.any(Object)
          );
        });

        it(`open dialog with error case without fullTermsURI`, () => {
            (euroService['getHowItWorksData'] as any).and.returnValue(throwError('some error'));
            component.euroRespData = {};
            component.openPopUp();
            expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
            expect(dialogService.openDialog).toHaveBeenCalledWith(
                'howItWorksDialog', resolvedDialogComponent, true, jasmine.any(Object)
            );
        });

        it(`open dialog with error case without fullTermsURI without response`, () => {
            (euroService['getHowItWorksData'] as any).and.returnValue(throwError('some error'));
            component.openPopUp();
            expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
            expect(dialogService.openDialog).toHaveBeenCalledWith(
                'howItWorksDialog', resolvedDialogComponent, true, jasmine.any(Object)
            );
        });

        it(`open dialog with response data with undefined without response`, () => {
            (euroService['getHowItWorksData'] as any).and.returnValue(of({}));
            component.openPopUp();
            expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
            expect(dialogService.openDialog).toHaveBeenCalledWith(
                'howItWorksDialog', resolvedDialogComponent, true, jasmine.any(Object)
            );
        });
    });

    describe('onInit', () => {
        it(`should call sessionStatusChange`, () => {
            spyOn(component, 'sessionStatusChange');
            (euroService['getMatchRewardsBadges']as any).and.returnValue(of(MATCHDAY_REWARDS_MOCK));
            component.ngOnInit();

            expect(component.sessionStatusChange).toHaveBeenCalledTimes(1);
        });
        it('should reject and not call sessionStatusChange', fakeAsync(() => {
            spyOn(component, 'sessionStatusChange');
            (euroService['getMatchRewardsBadges']as any).and.returnValue(throwError(null));
            component.euroResponse();
            expect(component.sessionStatusChange).not.toHaveBeenCalled();
        }));
        it('should reject and not call sessionStatusChange', fakeAsync(() => {
            spyOn(component, 'sessionStatusChange');
            (euroService['getMatchRewardsBadges']as any).and.returnValue(throwError('some error'));
            component.euroResponse();

            expect(component.sessionStatusChange).not.toHaveBeenCalled();
          }));

        it('should reject with error 1500', fakeAsync(() => {
            const err = { error: { proxyError: { code: 1500 } } };
            spyOn(component, 'sessionStatusChange');
            (euroService['getMatchRewardsBadges'] as any).and.returnValue(throwError(err));
            component.euroResponse();
            expect(component.errorMessage).toBe(EURO_MESSAGES.ERROR_USER_MESSAGE);
        }));

        it('should reject with error with 1400', fakeAsync(() => {
            const err = { error: { proxyError: { code: 1400 } } };
            spyOn(component, 'sessionStatusChange');
            (euroService['getMatchRewardsBadges'] as any).and.returnValue(throwError(err));
            component.euroResponse();
            expect(component.errorMessage).toBe(EURO_MESSAGES.ERROR_MESSAGE);
        }));

        it('should reject with out code', fakeAsync(() => {
            const err = { error: { proxyError: {} } };
            spyOn(component, 'sessionStatusChange');
            (euroService['getMatchRewardsBadges'] as any).and.returnValue(throwError(err));
            component.euroResponse();
            expect(component.errorMessage).toBe(EURO_MESSAGES.ERROR_MESSAGE);
        }));

        it('should reject with out proxy', fakeAsync(() => {
            const err = { error: {} };
            spyOn(component, 'sessionStatusChange');
            (euroService['getMatchRewardsBadges'] as any).and.returnValue(throwError(err));
            component.euroResponse();
            expect(component.errorMessage).toBe(EURO_MESSAGES.ERROR_MESSAGE);
        }));

        it('should reject with out error', fakeAsync(() => {
            const err = {};
            spyOn(component, 'sessionStatusChange');
            (euroService['getMatchRewardsBadges'] as any).and.returnValue(throwError(err));
            component.euroResponse();
            expect(component.errorMessage).toBe(EURO_MESSAGES.ERROR_MESSAGE);
        }));

        it(`should call unsubscribe`, () => {
            component.ngOnDestroy();

            expect(pubSubService.unsubscribe).toHaveBeenCalled();
        });

        it(`should  call sessionStatusChange`, () => {
            spyOn(component, 'euroResponse');
            component.sessionStatusChange();

            expect(component.euroResponse).toHaveBeenCalled();
        });

        it('SUCCESSFUL_LOGIN, SESSION_LOGIN', fakeAsync(() => {
            spyOn(component, 'sessionStatusChange');
            spyOn(component, 'euroResponse');
            component.ngOnInit();
            pubSubService.publish('SESSION_LOGIN', 1);
            tick();

            expect(component.sessionStatusChange).toHaveBeenCalled();
        }));

        it('SUCCESSFUL_LOGIN, SESSION_LOGIN withut token', fakeAsync(() => {
            spyOn(component, 'sessionStatusChange');
            spyOn(component, 'euroResponse');
            userService.bppToken = '';
            component.ngOnInit();
            pubSubService.publish('SESSION_LOGIN', 1);
            tick();

            expect(component.sessionStatusChange).toHaveBeenCalled();
        }));

        it(`should call return on euroApiDataResponse`, () => {
            spyOn(component, 'statusRender');
            component.euroApiDataResponse(null);
            expect(component.statusRender).not.toHaveBeenCalled();
        });

        it(`should call through`, () => {
            spyOn(component, 'statusRender');
            component.euroApiDataResponse(MATCHDAY_REWARDS_MOCK);
            expect(component.statusRender).toHaveBeenCalled();
        });

        it(`should call through for mocks`, () => {
            spyOn(component, 'statusRender');
            MATCHDAY_REWARDS_MOCK.placedBetToday = true;
            component.euroApiDataResponse(MATCHDAY_REWARDS_MOCK);
            expect(component.statusRender).toHaveBeenCalled();
        });

        it(`should not call through`, () => {
            spyOn(component, 'statusRender');
            MATCHDAY_REWARDS_MOCK.currentBadgeLocation = undefined;
            component.euroApiDataResponse(MATCHDAY_REWARDS_MOCK);
            expect(component.statusRender).not.toHaveBeenCalled();
        });

        it(`should not call through for desktop`, () => {
            spyOn(component, 'statusRender');
            deviceService.isDesktop = true;
            component.euroApiDataResponse(MATCHDAY_REWARDS_MOCK);
            expect(component.statusRender).not.toHaveBeenCalled();
        });

        it('should resolve and call euroApiDataResponse', fakeAsync(() => {
            spyOn(component, 'euroApiDataResponse');
            spyOn(component, 'hideSpinner');
            (euroService['getMatchRewardsBadges'] as any).and.returnValue(of(MATCHDAY_REWARDS_MOCK));
            component.euroResponse();

            expect(component.euroApiDataResponse).toHaveBeenCalled();
        }));

        it('should resolve and call euroApiDataResponse without placedBetToday', fakeAsync(() => {
            spyOn(component, 'euroApiDataResponse');
            spyOn(component, 'hideSpinner');
            MATCHDAY_REWARDS_MOCK.placedBetToday = false;
            (euroService['getMatchRewardsBadges'] as any).and.returnValue(of(MATCHDAY_REWARDS_MOCK));
            component.euroResponse();

            expect(component.euroApiDataResponse).toHaveBeenCalled();
        }));

        it(`should call statusRender with Mobile`, () => {
            component['statusrenderIndex'] = 0;
            deviceService.isMobile = true;
            component.statusRender(10);

            expect(component['statusrenderIndex']).toBe(11);
        });

        it(`should call statusRender with Desktop`, () => {
            component['statusrenderIndex'] = 0;
            deviceService.isMobile = false;
            component.statusRender(10);

            expect(component['statusrenderIndex']).toBe(11);
        });

        it(`should call statusRender with Desktop with 0`, () => {
            component['statusrenderIndex'] = 0;
            deviceService.isMobile = false;
            component.statusRender(0);

            expect(component['statusrenderIndex']).toBe(5);
        });

        it(`should statusrenderIndex greater than badges`, () => {
            component['statusrenderIndex'] = 0;
            component.totalNoOfBadges = 20;
            deviceService.isMobile = false;
            component.statusRender(20);

            expect(component['statusrenderIndex']).toBe(19);
        });

        it(`showConfetti`, () => {
            component.showConfetti('event');
            expect(componentFactoryResolver.resolveComponentFactory).toHaveBeenCalledWith(jasmine.any(Function));
            expect(dialogService.openDialog).toHaveBeenCalledWith(
              'euroCongratsDialog', resolvedDialogComponent, true, jasmine.any(Object)
            );
        });
    });
});

