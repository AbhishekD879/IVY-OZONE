import { of, throwError } from 'rxjs';
import { FanzoneAppClubComponent } from '@app/fanzone/components/fanzoneClub/fanzone-club.component';
import { FANZONETEASERDATA, FANZONETEASEREMPTYDATA } from '@app/fanzone/constants/fanzoneconstants';
import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { EVENTS_DATA } from '@app/promotions/constants/promotion-mock';

describe('FanzoneAppClubComponent', () => {
    let component: FanzoneAppClubComponent;
    let changeDetectorRef;
    let cmsService;
    let fanzoneModuleService;
    let siteServerService;
    let cacheEventsService;
    let updateEventService;
    let channelService;
    let pubSubService;
    let promotionsService;
    let eventsData;
    let promotionData;

    const clubs = [{
        title: 'CLUB',
        bannerLink: '{32ACDBCF-D0CD-4194-91EA-A49182D0473D}',
        description: 'description',
    }]

    beforeEach(() => {
        eventsData = EVENTS_DATA;
        changeDetectorRef = {
            detectChanges: jasmine.createSpy('detectChanges'),
        };
        cmsService = { getFanzoneClubs: jasmine.createSpy().and.returnValue(of(clubs)) } as any;

        fanzoneModuleService = {
            getFanzoneImagesFromSiteCore: jasmine.createSpy().and.returnValue(of(FANZONETEASERDATA))
        }
        siteServerService = {
            getEventsByOutcomeIds: jasmine.createSpy('getEventsByOutcomeIds').and.returnValue(Promise.resolve(eventsData))
        };
        cacheEventsService = {
            store: jasmine.createSpy('getLSChannelsFromArray').and.callThrough(),
            clearByName: jasmine.createSpy('clearByName').and.callThrough()
        };
        updateEventService = {
            init: jasmine.createSpy('init').and.callThrough()
        };
        channelService = {
            getLSChannelsFromArray: jasmine.createSpy('getLSChannelsFromArray').and.returnValue('1234'),
        };
        pubSubService = {
            subscribe: jasmine.createSpy('subscribe').and.callFake((p1, p2, callback) => {
                callback();
            }),
            unsubscribe: jasmine.createSpy('unsubscribe'),
            publish: jasmine.createSpy('publish'),
            API: pubSubApi
        };
        promotionsService = {
            isUserLoggedIn: jasmine.createSpy('isUserLoggedIn'),
            disableOptInButton: jasmine.createSpy('disableOptInButton'),
            decorateLinkAndTrust: jasmine.createSpy('decorateLinkAndTrust'),
            enableOptInButton: jasmine.createSpy('enableOptInButton'),
            changeBtnLabel: jasmine.createSpy('changeBtnLabel'),
            sendGTM: jasmine.createSpy('sendGTM'),
            preparePromotions: jasmine.createSpy('preparePromotions').and.callFake((p1) => {
                return p1;
            }),
            storeId: jasmine.createSpy('storeId').and.callFake((p1) => {
                return of({ fired: false });
            }),
            getPromotionsFromSiteCore: jasmine.createSpy('getPromotionsFromSiteCore').and.returnValue(of({}))
        };
        promotionData = {
            marketLevelFlag: 'marketLevelFlag',
            eventLevelFlag: 'eventLevelFlag',
            useDirectFileUrl: 'sport/football/matches/today',
            directFileUrl: 'sport/football/matches/today',
            overlayBetNowUrl: 'url',
            flagName: 'flags',
            iconId: 'icon/122'
        };

        component = new FanzoneAppClubComponent(changeDetectorRef, cmsService, fanzoneModuleService, siteServerService, cacheEventsService, updateEventService, channelService, pubSubService, promotionsService);
    });

    describe('#FanzoneAppClubComponent', () => {
        it('should get Fanzone clubs', () => {
            component.ngOnInit();
            expect(component.clubsData).toBeDefined();
        })
        it('should handle if teasers call return error response', () => {
            fanzoneModuleService.getFanzoneImagesFromSiteCore = jasmine.createSpy().and.returnValue(throwError({ status: 404 }));
            component.ngOnInit();

            expect(component.clubBannerLink).toEqual('');
            expect(component.state.error).toBeTrue;
        });
        it('should handle if teasers data is not present', () => {
            fanzoneModuleService.getFanzoneImagesFromSiteCore = jasmine.createSpy().and.returnValue(of(FANZONETEASEREMPTYDATA));
            component.ngOnInit();

            expect(component.clubBannerLink).toEqual('');
        });
        it('should call getDynamicButtonDetails', () => {
            spyOn(component as any, 'getDynamicButtonDetails');
      
            component['populatePromoData'](clubs[0] as any,'data');
            expect(component['getDynamicButtonDetails']).toHaveBeenCalled();
        });
        it('populate is called', () => {
            spyOn(component as any, 'populatePromoData');
            component.ngOnInit();
      
            expect(component['populatePromoData']).toHaveBeenCalled();
        });
        it('populate test cases is called', () => {
            const str = '<button id="dynamic-btn"> dasdasdadasdadads </button>';
            component.promoDescriptionContentArr = [{ htmlCont: 'content', selection: '1234', eventInfo: '' as any }] as any;
            spyOn(component as any, 'getDynamicButtonDetails');
            component.populatePromoData(clubs[0] as any,str);
            expect(component['getDynamicButtonDetails']).toHaveBeenCalled();
        });
        it('populate test cases is called with dynamicbtn', () => {
            const str = '<button id="dynamicbtn"> dasdasdadasdadads </button>';
            component.promoDescriptionContentArr = [{ htmlCont: 'content', selection: '1234', eventInfo: '' as any }] as any;
            spyOn(component as any, 'getDynamicButtonDetails');
            component.populatePromoData(clubs[0]as any,str);
            expect(component['getDynamicButtonDetails']).toHaveBeenCalled();
        });
        it('getDynamicButtonDetails is called', () => {
            const data = ['1234'];
            component.promoDescriptionContentArr = [{ htmlCont: 'content', selection: '1234', eventInfo: '' as any }] as any;
            spyOn(component as any, 'liveConnection');
            component.getDynamicButtonDetails(data);
            expect(component.promoDescriptionContentArr).not.toBeUndefined();
          });
          it('subscribe to be called', () => {
            component.promoDescriptionContentArr = [{
              htmlCont: 'content', selection: '1234', eventInfo: { event: { outcome: { id: '123' } } }
            }] as any;
            component.liveConnection();
      
            expect(pubSubService.publish).toHaveBeenCalled();
          });
    })
    describe('ngOnDestroy', () => {
        it('ngOnDestroy, init', () => {  
          component.ngOnDestroy();

          expect(pubSubService.unsubscribe).toHaveBeenCalledTimes(1);
        });
      });
})