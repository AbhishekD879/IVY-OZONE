
import { of, throwError } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { LuckyDipService } from './lucky-dip.service';
import { fakeAsync, tick } from '@angular/core/testing';

describe('luckyDipService', () => {
    let service, http: HttpClient, domain, brand;
    let mockLuckyDipData =
    {
        id: ' 63ecd2a079768e6cf926a83b',
        luckyDipBannerConfig: {
            animationImgPath: 'https:/animation.com',
            bannerImgPath: 'https:/ banner.com',
            infoIconImgPath: 'https:/ info.com'
        },
        luckyDipFieldsConfig: {
            title: 'Lucky DIp test 1',
            desc: 'Here u can play',
            welcomeMessage: 'Welcome to COntest',
            betPlacementTitle: 'First title',
            betPlacementStep1: 'Step 1',
            betPlacementStep2: 'Step 2',
            betPlacementStep3: 'Step 3',
            termsAndConditionsURL: 'http:/ url.com',
            playerCardDesc: 'Player 1',
            potentialReturnsDesc: 'Win Money'
        }, playerPageBoxImgPath: ' https: /path1.com'
    }
    beforeEach(() => {
        service = new LuckyDipService(http, domain, brand);
    });

    it('wrappedObservable', fakeAsync(() => {
        const observableDate = {
        map: jasmine.createSpy('map').and.callFake(({ title, message, closeCallback }) => {
            closeCallback();
        }).and.returnValue({ catch: jasmine.createSpy('catch').and.returnValue(throwError({ error: 'error' })) })
        }

        const sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({ body: mockLuckyDipData }));
        service.wrappedObservable(observableDate);
        tick();
        tick();

        expect(sendRequestSpy).not.toHaveBeenCalled();

    }));


    it('should call getLuckyDipData', fakeAsync(() => {
        const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.returnValue({
            observableDate: jasmine.createSpy('observableDate').and.returnValue(of({
                map: jasmine.createSpy('map').and.callFake(({ title, message, closeCallback }) => {
                    closeCallback();
                }).and.returnValue({ catch: jasmine.createSpy('catch').and.returnValue(throwError({ error: 'error' })) })
            })),
        })

        const sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({ body: mockLuckyDipData }));
        service.getLuckyDipData();
        tick();
        tick();

        expect(sendRequestSpy).toHaveBeenCalled();
        expect(spyOnWrappedObservable).toHaveBeenCalled();
    }));

    describe('luckyDipData', () => {
        it('luckyDipData if Id is given', fakeAsync(() => {
            const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.returnValue({
                observableDate: jasmine.createSpy('observableDate').and.returnValue(of({
                    map: jasmine.createSpy('map').and.callFake(({ title, message, closeCallback }) => {
                        closeCallback();
                    }).and.returnValue({ catch: jasmine.createSpy('catch').and.returnValue(throwError({ error: 'error' })) })
                })),
            })

            const updateSplashDataSpy = spyOn(service as any, 'updateSplashData').and.returnValue(of({}));
            spyOn(service as any, 'sendRequest');
            service.luckyDipData(mockLuckyDipData, '1234');
            tick();
            tick();

            expect(updateSplashDataSpy).toHaveBeenCalled();
            expect(spyOnWrappedObservable).toHaveBeenCalled();
        }));
        it('luckyDipData if Id is not given', fakeAsync(() => {
            const spyOnWrappedObservable = spyOn(service, 'wrappedObservable').and.returnValue({
                observableDate: jasmine.createSpy('observableDate').and.returnValue(of({
                    map: jasmine.createSpy('map').and.callFake(({ title, message, closeCallback }) => {
                        closeCallback();
                    }).and.returnValue({ catch: jasmine.createSpy('catch').and.returnValue(throwError({ error: 'error' })) })
                })),
            })

            const postSplashDataSpy = spyOn(service as any, 'postSplashData').and.returnValue(of({}));
            spyOn(service as any, 'sendRequest');
            service.luckyDipData(mockLuckyDipData);
            tick();
            tick();

            expect(postSplashDataSpy).toHaveBeenCalled();
            expect(spyOnWrappedObservable).toHaveBeenCalled();
        }));
    });

    describe('postSplashData', () => {
        it('postSplashData', fakeAsync(() => {
            const sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));

            service.postSplashData(mockLuckyDipData);
            tick();
            tick();

            expect(sendRequestSpy).toHaveBeenCalled();
        }));
    });

    describe('updateSplashData', () => {
        it('updateSplashData if Id is given', fakeAsync(() => {
            const sendRequestSpy = spyOn(service as any, 'sendRequest').and.returnValue(of({}));

            service.updateSplashData(mockLuckyDipData);
            tick();
            tick();

            expect(sendRequestSpy).toHaveBeenCalled();
        }));
    });
});
