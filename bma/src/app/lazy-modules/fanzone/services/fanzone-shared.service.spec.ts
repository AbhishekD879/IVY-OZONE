import { pubSubApi } from '@app/core/services/communication/pubsub/pubsub-api.constant';
import { of, of as observableOf, throwError } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';
import { FanzoneSharedService } from '@lazy-modules/fanzone/services/fanzone-shared.service';
import { alreadyResignedTeam, alreadySelectedTeam, communication, FANZONE_POS_GET, noTeamSelected, selectedTeam } from '@app/core/services/fanzone/constant/fanzone.constant';
import { gtmTackingKeys } from '@app/fanzone/constants/fanzonePreferenceConstants';
import { IFanzoneData } from '@root/app/fanzone/models/fanzone-preferences.model';
import { FANZONECONFIG } from '@app/fanzone/guards/mockdata/fanzone-auth-guardservice.mock';

describe('FanzoneSharedService', () => {
    let service: FanzoneSharedService,
        pubSubService,
        cmsToolsService,
        deviceService,
        httpClient,
        coreToolsService,
        fanzoneStorageService,
        casinoLinkService,
        nativeBridgeService,
        userService,
        segmentEventManagerService,
        segmentedCMSService,
        cmsInitConfigPromise,
        windowRefService,
        asyncScriptLoaderService,
        gtmService,
        router,
        dialogService,
        timeService,
        vanillaApiService,
        componentFactoryResolver,
        fanzoneHelperService,
        fanzoneGamesService;
    beforeEach(() => {
        windowRefService = {};
        asyncScriptLoaderService = {};

        pubSubService = {
            publish: jasmine.createSpy('publish'),
            subscribe: jasmine.createSpy('subscribe'),
            API: pubSubApi
        };

        cmsToolsService = {
            processResult: jasmine.createSpy('processResult').and.returnValue([])
        };

        deviceService = {
            strictViewType: 'mobile',
            requestPlatform: 'mobile',
            isAndroid: true,
            isIos: false,
            isWrapper: true
        };

        httpClient = {
            get: jasmine.createSpy('get').and.returnValue(of(
                {
                    body: []
                }))
        };

        coreToolsService = {
            deepClone: jasmine.createSpy('deepClone')
        };

        fanzoneStorageService = {
            get: jasmine.createSpy('get'),
            set: jasmine.createSpy('set'),
            remove: jasmine.createSpy('remove')
        };

        casinoLinkService = {
            filterGamingLinkForIOSWrapper: jasmine.createSpy('filterGamingLinkForIOSWrapper')
        };

        nativeBridgeService = {
            isRemovingGamingEnabled: false
        };

        userService = {
            currencySymbol: '$'
        };
        segmentEventManagerService = {
            getSegmentDetails: jasmine.createSpy('getSegmentDetails')
        };
        segmentedCMSService = {
            getCmsInitData: jasmine.createSpy('getCmsInitData')
        };
        cmsInitConfigPromise = undefined;
        vanillaApiService = {
            get: jasmine.createSpy('vanillaApiService.get').and.returnValue(of(FANZONE_POS_GET)),
            post: jasmine.createSpy('vanillaApiService.post').and.returnValue(of([]))
        };
        gtmService = {
            push: jasmine.createSpy('push')
        };
        timeService = {
            getSuspendAtTime: jasmine.createSpy().and.returnValue(new Date())
        };
        router = {
            navigate: jasmine.createSpy('navigate')
        };
        dialogService = {
            openDialog: jasmine.createSpy('openDialog')
        };
        fanzoneHelperService = {
            PublishFanzoneData: jasmine.createSpy(),
            checkIfTeamIsRelegated: jasmine.createSpy('checkIfTeamIsRelegated').and.returnValue(true),
            selectedFanzone: FANZONECONFIG
        };
        componentFactoryResolver = jasmine.createSpyObj('componentFactoryResolver', ['resolveComponentFactory']);
        fanzoneGamesService = {
            getNewFanzoneGamesPopupSeen: jasmine.createSpy('getNewFanzoneGamesPopupSeen').and.returnValue(false),
        };
        service = new FanzoneSharedService(
            fanzoneStorageService,
            pubSubService,
            cmsToolsService,
            deviceService,
            httpClient,
            coreToolsService,
            casinoLinkService,
            nativeBridgeService,
            userService,
            segmentEventManagerService,
            segmentedCMSService,
            windowRefService,
            asyncScriptLoaderService,
            cmsInitConfigPromise,
            gtmService,
            router,
            dialogService,
            timeService,
            vanillaApiService,
            componentFactoryResolver,
            fanzoneHelperService,
            fanzoneGamesService
        );
    });
    it('should create instance', () => {
        expect(service).toBeDefined();
    });
    describe('#getSpecialPagesDataCollection', () => {
        it('should call special-pages', () => {
            service.getSpecialPagesDataCollection().subscribe();
            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-syc`,
                { observe: 'response', params: {} }
            );
        });

        it('should saveTeamOnPlatformOne', () => {
            fanzoneStorageService.get.and.returnValue(selectedTeam);
            service.showNotifications = jasmine.createSpy();
            service.saveTeamOnPlatformOne(selectedTeam, communication);
            expect(selectedTeam).toBe(selectedTeam);
            expect(router.navigate).not.toHaveBeenCalled();
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        });

        it('should saveTeamOnPlatformOne and not call show notifications when its not a device', () => {
            fanzoneStorageService.get.and.returnValue(alreadySelectedTeam);
            deviceService.isWrapper = false;
            service.showNotifications = jasmine.createSpy();
            service.saveTeamOnPlatformOne(alreadySelectedTeam, communication, '');
            expect(service.showNotifications).toHaveBeenCalledWith(false);
        });

        it('should saveTeamOnPlatformOne and call show notifications for subscribed user', () => {
            fanzoneStorageService.get.and.returnValue(alreadySelectedTeam);
            deviceService.isWrapper = true;
            service.showNotifications = jasmine.createSpy();
            service.saveTeamOnPlatformOne(alreadySelectedTeam, communication, '');
            expect(service.showNotifications).toHaveBeenCalledWith(true);
        });

        it('should saveTeamOnPlatformOne and call show notifications for resigned user', () => {
            fanzoneStorageService.get.and.returnValue(alreadyResignedTeam);
            service.showNotifications = jasmine.createSpy();
            service.saveTeamOnPlatformOne(alreadySelectedTeam, communication, '');
            expect(service.showNotifications).toHaveBeenCalledWith(false);
        });

        it('should not saveTeamOnPlatformOne and call show notifications for new user', () => {
            fanzoneStorageService.get.and.returnValue({isFanzoneExists: false, isResignedUser: false});
            service.showNotifications = jasmine.createSpy();
            service.saveTeamOnPlatformOne(alreadySelectedTeam, communication, '');
            expect(service.showNotifications).toHaveBeenCalledWith(false);
        });

        it('saveEmailOptinData post api', () => {
            service.saveEmailOptinData({});
            expect(vanillaApiService.post).toHaveBeenCalled();
        });

        it('saveEmailOptinData post api', () => {
            service.getUserCommunicationSettings();
            expect(vanillaApiService.get).toHaveBeenCalled();
        });

        it('should call getFanzoneEmailOptin', async () => {
            service.getFanzoneEmailOptin().subscribe();
      
            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
              `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-optin-email`,
              { observe: 'response', params: {} }
            );
          })

        it('saveEmailOptinData post api', () => {
            service.saveEmailOptinData = jasmine.createSpy('saveEmailOptinData').and.returnValue(of({
                dontShowMeAgainPref: true,
                remindMeLaterPrefDate: '2023-07-14T15:53:47Z',
                remindMeLaterCount: 2
              }));
            service.postEmailOptinDetails({}, true);
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        })

        it('getEmailPayload', ()=>{
            const req = { dontShowMeAgainPref: true, remindMeLaterPrefDate: '2023-07-14T15:53:47Z', remindMeLaterCount: 2 }
            const res = service.getEmailPayload(req);
            expect(res).toEqual([{"key": "DONT_SHOW_ME_AGAIN_PREF", "value": true},
                {"key": "REMINDME_LATER_PREF_DATE", "value": "2023-07-14T15:53:47Z"},
                {"key": "REMINDME_LATER_COUNT", "value": 2}]);
        });

        it('should saveTeamOnPlatformOne navigateTo', () => {
            fanzoneStorageService.get.and.returnValue(selectedTeam);
            service.showNotifications = jasmine.createSpy();
            service.saveTeamOnPlatformOne(selectedTeam, communication, 'football/ArsenalFC/now-next');
            expect(router.navigate).toHaveBeenCalledWith(['football/ArsenalFC/now-next']);
            expect(service.showNotifications).not.toHaveBeenCalled();
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        });

        it('#resignFanzone error', () => {
            fanzoneStorageService.get.and.returnValue(selectedTeam);
            service.deleteFanzonePreferences = jasmine.createSpy('deleteFanzonePreferences').and.returnValue(throwError('error'));
            spyOn(console, 'error');
            service.resignFanzone();
            expect(console.error).toHaveBeenCalledWith('error');
        })

        it('#resignFanzone when storage is empty', () =>{
            service.deleteFanzonePreferences = jasmine.createSpy('deleteFanzonePreferences').and.returnValue(observableOf({}));
            fanzoneStorageService.get.and.returnValue({});
            service.pushCachedEvents = jasmine.createSpy('');
            service.resignFanzone();
            expect(fanzoneStorageService.set).toHaveBeenCalled();
            expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.FANZONE_DATA, {});
            expect(router.navigate).toHaveBeenCalledWith(['']);
            expect(service.pushCachedEvents).toHaveBeenCalled();
          });

          it('#resignFanzone when team in storage exists', () =>{
            service.deleteFanzonePreferences = jasmine.createSpy('deleteFanzonePreferences').and.returnValue(observableOf({}));
            fanzoneStorageService.get.and.returnValue(selectedTeam);
            service.pushCachedEvents = jasmine.createSpy('');
            service.resignFanzone();
            expect(fanzoneStorageService.set).toHaveBeenCalled();
            expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.FANZONE_DATA, {});
            expect(router.navigate).toHaveBeenCalledWith(['']);
            expect(service.pushCachedEvents).toHaveBeenCalled();
          });

        it('#getFanzoneInfo', () => {
            fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(selectedTeam);
            const res = service.getFanzoneInfo();
            expect(res).toEqual(selectedTeam);
        });

        it('#checkIfTeamIsRelegated', () => {
            service.checkIfTeamIsRelegated();
            expect(fanzoneHelperService.checkIfTeamIsRelegated).toHaveBeenCalled();
        });


        it('#getFanzoneInfo when storage key is not found', () => {
            fanzoneStorageService.get.and.returnValue(null);
            expect(service['getFanzoneInfo']()).toEqual({});
        });

        it('saveTeamOnPlatformOne remove showSYCPopupOn when saving a team', () => {
            const data = {showSYCPopupOn: '2022-05-07T13:20:00.834Z', teamId: '1c8m2ko0wxq1asfkuykurdr0y'};
            fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue(data);
            service.saveTeamOnPlatformOne(data);
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        })
        it('#getFanzoneInfo when storage is empty', () => {
            fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({});
            const res = service.getFanzoneInfo();
            expect(res).toEqual({});
        });

        it('#isTeamSelection team selection', () => {
            const res = service.isTeamSelection('avjdhiuf');
            expect(res).toBe(true);
        })

        it('#isTeamSelection custom selection', () => {
            const res = service.isTeamSelection('FZ001');
            expect(res).toBe(false);
        })

        it('#getSelectedTeam true', () => {
            const res = service.getSelectedTeam(selectedTeam);
            expect(res).toBe(selectedTeam);
        })

        it('#getSelectedTeam false when empty object is passed', () => {
            fanzoneStorageService.get = jasmine.createSpy('fanzone').and.returnValue({ teamId: '123', teamName: 'Arsenal' })
            service.getFanzoneInfo = jasmine.createSpy().and.returnValue({ teamId: '123', teamName: 'Arsenal' });
            const res = service.getSelectedTeam(<IFanzoneData>{});
            expect(res).toEqual({ teamId: '123', teamName: 'Arsenal' });
        })

        it('should call showNotifications return error when saveTeamOnPlatformOne called', () => {
            vanillaApiService.post = jasmine.createSpy().and.returnValue(throwError({ status: 404 }))
            service.saveTeamOnPlatformOne(selectedTeam, communication);
            expect(fanzoneStorageService.set).not.toHaveBeenCalledWith('fanzone', { 'teamId': 'ehd2iemqmschhj2ec0vayztzz', 'teamName': 'Everton FC', 'subscriptionDate': undefined });
        });

        it('should call showNotifications', () => {
            service.showNotifications = jasmine.createSpy('showNotifications');
            service.saveTeamOnPlatformOne(noTeamSelected, communication);
            expect(service.showNotifications).not.toHaveBeenCalled();
        });

        it('should navigate to preference center ', () => {
            deviceService.isWrapper = true;
            service.pushCachedEvents = jasmine.createSpy();
            service.showNotifications(false);
            expect(service.pushCachedEvents).toHaveBeenCalled();
            expect(router.navigate).toHaveBeenCalled();
        })

        it('should navigate to notifications ', () => {
            deviceService.isWrapper = false;
            service.pushCachedEvents = jasmine.createSpy();
            service.showNotifications(false);
            expect(service.pushCachedEvents).toHaveBeenCalled();
            expect(dialogService.openDialog).toHaveBeenCalled();
        })

        it('appendToStorage()', () => {
            fanzoneStorageService.get.and.returnValue({});
            service.appendToStorage({ isFanzoneExists: true });
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        })

        it('appendToStorage() with param', () => {
            fanzoneStorageService.get.and.returnValue({isCustomResignedUser: true});
            service.appendToStorage({ isFanzoneExists: true }, true);
            expect(fanzoneStorageService.set).toHaveBeenCalled();
        })

        it('addDaysToCurrentDate', () => {
            const future = new Date();
            future.setDate(future.getDate() + 1);
            const res = service.addDaysToCurrentDate(1);
            expect(res).toBeDefined();
            expect(future).toBeDefined();
        })

        it('should delete fanzone preferences', () => {
            vanillaApiService.post = jasmine.createSpy().and.returnValue(of({}));
            const res = service.deleteFanzonePreferences();
            expect(res).toBeDefined();
        });

        it('should call gtmService push', () => {
            const dataLayer = {
                event: gtmTackingKeys.trackEvent,
                eventAction: gtmTackingKeys.preferenceCentre,
                eventCategory: gtmTackingKeys.fanzone,
                eventLabel: 'eventLabel',
                eventDetails: 'eventDetails'
            }
            service.pushCachedEvents('eventLabel', 'eventDetails');
            expect(gtmService.push).toHaveBeenCalledWith(dataLayer.event, dataLayer);
        })

        it('should call gtmService push', () => {
            const dataLayer = {
                event: gtmTackingKeys.trackEvent,
                eventAction: gtmTackingKeys.preferenceCentre,
                eventCategory: 'eventCategory',
                eventLabel: 'eventLabel',
                eventDetails: 'eventDetails'
            }
            service.pushCachedEvents('eventLabel', 'eventDetails', 'eventCategory');
            expect(gtmService.push).toHaveBeenCalledWith(dataLayer.event, dataLayer);
        })

        it('should handle error in  getFanzonePreferences()', () => {
            httpClient.get.and.returnValue(throwError('error'));
            service.getFanzonePreferences().subscribe();

            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-preference-center`,
                { observe: 'response', params: {} }
            );
        });

        it('should call getFanzonePreferences()', () => {
            service.getFanzonePreferences().subscribe();

            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-preference-center`,
                { observe: 'response', params: {} }
            );
        });

        it('team selection payload', () => {
            const selectedTeamPayload = {
                category: "football",
                preferences: [
                    {
                        key: "TEAM_ID",
                        value: "27"
                    },
                    {
                        key: "TEAM_NAME",
                        value: "Arsenal"
                    }
                ]
            }
            const res = service.getPayload({ teamId: '27', teamName: 'Arsenal' });
            expect(res).toEqual(selectedTeamPayload);
        });
        
        it('addDaysToDate', () => {
            const future = new Date();
            future.setDate(future.getDate() + 1);
            const res = service.addDaysToDate(future.toString(), 1);
            expect(res).toBeDefined();
            expect(future).toBeDefined();
        });

        it('communication preferences payload', () => {
            const preferencePayload = {
                category: "football",
                preferences: [
                    { key: "COMM_PREFERENCES", value: JSON.stringify(["POST_MATCH"]) }
                ]
            }
            const res = service.getPayload({ teamId: '27', teamName: 'Arsenal' }, ["POST_MATCH"]);
            expect(res).toEqual(preferencePayload);
        });

        it('should show games popup', () => {
            service.getFanzoneNewGamePopupContent = jasmine.createSpy('getFanzoneNewGamePopupContent').and.returnValue(of([{}]));
            service.showGamesPopup();      
            expect(dialogService.openDialog).toHaveBeenCalled();
        });

        it('should show game launch popup', () => {
            service.showGameLaunchPopup({gameLaunchUrl: 'test-url'});        
            expect(dialogService.openDialog).toHaveBeenCalled();
        });

        it('should call getFanzoneNewSignPosting()', () => {
            service.getFanzoneNewSignPosting().subscribe();

            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-new-signposting`,
                { observe: 'response', params: {} }
            );
        });

        it('should handle error in  getFanzoneNewSignPosting()', () => {
            httpClient.get.and.returnValue(throwError('error'));
            service.getFanzoneNewSignPosting().subscribe();

            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-new-signposting`,
                { observe: 'response', params: {} }
            );
        });

        it('should call getFanzoneNewGamePopupContent()', () => {
            service.getFanzoneNewGamePopupContent().subscribe();

            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-new-gaming-pop-up`,
                { observe: 'response', params: {} }
            );
        });

        it('should handle error in  getFanzoneNewGamePopupContent()', () => {
            httpClient.get.and.returnValue(throwError('error'));
            service.getFanzoneNewGamePopupContent().subscribe();

            expect(httpClient.get).toHaveBeenCalled();
            expect(httpClient.get).toHaveBeenCalledWith(
                `${environment.CMS_ENDPOINT}/${environment.brand}/fanzone-new-gaming-pop-up`,
                { observe: 'response', params: {} }
            );
        });

        it('#getFanzoneBannerFromSiteCore', () => {
            service.getFanzoneBannerFromSiteCore();
            expect(vanillaApiService.get).toHaveBeenCalled();
        });

        it('#resignFanzone when 21st team in storage exists', () =>{
            service.saveUserFanzoneTeam = jasmine.createSpy('saveUserFanzoneTeam').and.returnValue(observableOf({}));
            fanzoneStorageService.get.and.returnValue(noTeamSelected);
            service.pushCachedEvents = jasmine.createSpy('');
            service.resignFanzone();
            expect(fanzoneStorageService.set).toHaveBeenCalled();
            expect(pubSubService.publish).toHaveBeenCalledWith(pubSubApi.FANZONE_DATA, {});
            expect(router.navigate).toHaveBeenCalledWith(['']);
            expect(service.pushCachedEvents).toHaveBeenCalled();
        });

        it('#isSubscribedToCustomTeam should return true if teamid is custom', () => {
            fanzoneStorageService.get.and.returnValue({teamId: 'FZ001'});
            expect(service.isSubscribedToCustomTeam()).toBeTruthy();
        });

        it('#isSubscribedToCustomTeam should return false if teamid is other valid team', () => {
            fanzoneStorageService.get.and.returnValue({teamId: 'test'});
            expect(service.isSubscribedToCustomTeam()).toBeFalsy();
        });

        it('#isSubscribedToCustomTeam should return false if teamid details are not available in storage', () => {
            fanzoneStorageService.get.and.returnValue(null);
            expect(service.isSubscribedToCustomTeam()).toBeFalsy();
        });
    });

    describe('showFanzoneGamesPopup', () => {
        beforeEach(()=>{
            service.showGamesPopup = jasmine.createSpy('showGamesPopup');
        });

        it('should see the fanzone games popup if user visited fanzone games first time', () => {
            service.isIosBlackListedDevice = jasmine.createSpy('isIosBlackListedDevice').and.returnValue(observableOf(false));
            service['showFanzoneGamesPopup'](fanzoneHelperService.selectedFanzone);
            expect(service.showGamesPopup).toHaveBeenCalled();
        });

        it('isIosBlackListedDevice', () => {
            service['device'].isWrapper=true;
            service['device'].isIos=true;
            service['fanzoneHelperService'].appBuildVersion='7.8-16';
            service.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({GamingEnabled:
                {
                    "iosVersionBlackList": [
                      "7.8-16"
                    ],
                  }
            }));
            service['isIosBlackListedDevice']().subscribe((res) =>expect(res).toBeTruthy());  
        });

        it('isIosBlackListedDevice when device is not wrapper', () => {
            service['device'].isWrapper=true;
            service['device'].isIos=true;
            service['fanzoneHelperService'].appBuildVersion='7.8-16';
            service.getSystemConfig = jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({GamingEnabled:
                {
                    "iosVersionBlackList": [
                      "7.8-1"
                    ],
                  }
            }));
            service['isIosBlackListedDevice']().subscribe((res) =>expect(res).toBeFalsy());  
        });
    
        it('should not see fanzone games popup if user already visited fanzone games tab', () => {
            fanzoneGamesService.getNewFanzoneGamesPopupSeen.and.returnValue(true);
            service['showFanzoneGamesPopup'](fanzoneHelperService.selectedFanzone);
            expect(service.showGamesPopup).not.toHaveBeenCalled();
        });
    
        it('should not see fanzone games popup if games tab is OFF', () => {
            fanzoneHelperService.selectedFanzone.fanzoneConfiguration.showGames = false;
            service['showFanzoneGamesPopup'](fanzoneHelperService.selectedFanzone);
            expect(service.showGamesPopup).not.toHaveBeenCalled();
        });
    });
});
