import { fakeAsync } from '@angular/core/testing';
import { of } from 'rxjs';
import { FanzoneAppGamesComponent } from '@app/fanzone/components/fanzoneGames/fanzone-games.component';
import { FANZONE_GAMES } from '@lazy-modules/fanzone/fanzone.constant';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { FANZONECONFIG } from '@app/fanzone/guards/mockdata/fanzone-auth-guardservice.mock';

describe('FanzoneAppGamesComponent', () => {
  let component: FanzoneAppGamesComponent;

  let windowRefService,
    page,
    deviceService,
    casinoGamesConfig,
    user,
    userService,
    fanzoneGamesService,
    fanzoneSharedService,
    gtmService,
    fanzoneStorageService,
    pubsub,
    fanzoneHelperService;

  beforeEach(() => {
    windowRefService = {
      nativeWindow: {
        location: {
          href: ''
        },
        open: jasmine.createSpy('open'),
        clientConfig: {
          bmaCasinoGamesConfig: {
            miniGamesHost: 'https://casinogames.ladbrokes.com'
          },
          vnUser: {
            lang: 'en'
          },
          vnAppInfo: {
            brand: 'CORAL',
            frontend: 'cl'
          },
          vnClaims: {
            'http://api.bwin.com/v3/user/usertoken': 'asdasd',
            'http://api.bwin.com/v3/user/sessiontoken': '121212',
            'http://api.bwin.com/v3/user/currency': 'GBP'
          },
          vnProductHomepages: {
            sports: 'http://qa22.sports.com'
          }
        }
      }
    };
    page = {
      culture: {
        replace: jasmine.createSpy('replace').and.returnValue('en-us')
      }
    };
    deviceService = {};
    casinoGamesConfig = {
      miniGamesHost: 'https://casinogames.ladbrokes.com',
      userHostAddress: '12.3.4.5',
      fzGmImgDsUrl: '/htmllobby/images/newlmticons/fanzonelarge/$GAMENAME$.jpg',
      fzGmImgMbUrl: '/htmllobby/images/newlmticons/fanzonesmall/$GAMENAME$.jpg',
      fzGmLaDsUrl : '/fcasino/$casinogamelang$/gamelaunch.html?gamename=$GAMENAME$&langId=$LANGID$&invokerProduct=BETTING&channelId=FC&brand=LADBROKEUK&frontend=ld&lobbyType=instantGames&conf=$ENV$&hostUrl=$HOSTURL$&mode=real&demo=FALSE&sessionKey=$SESSIONKEY$&userToken=$USERTOKEN$&sessionToken=$SESSIONTOKEN$&pLang=$pLANG$&clickTimeStamp=$TIMESTAMP$&launchSource=LCG_OZONE&catId=LMC_FANZONE&subcatId=LMC_FANZONE&rowNumber=1&colNumber=1&iconSize={}&gamePosition=1&pageNumber=1&lobbyRes=NORMAL&width=1024&height=770&currency=$CURRENCY$&ip=$USERIP$&keepAliveInterval=600000&fzTeamId=$TEAM_ID$&fzTeamName=$TEAM_NAME$',
      fzGmLaMbUrl :  '/fcasino/$casinogamelang$/fcgames/vendorgames/mobile.html?gameVariantName=$GAMENAME$&langId=$LANGID$&invokerProduct=BETTING&channelId=$CHANNELID$&brandId=LADBROKEUK&frontend=ld&lobbyType=instantGames&conf=$ENV$&lobbyURL=$LOBBYURL$&mode=real&demo=FALSE&ssoKey=$SESSIONKEY$&userToken=$USERTOKEN$&sessionToken=$SESSIONTOKEN$&pLang=$pLANG$&clickTimeStamp=$TIMESTAMP$&launchSource=LCG_OZONE&catId=LMC_FANZONE&subcatId= LMC_FANZONE&rowNumber=1&colNumber=1&iconSize={}&gamePosition=1&pageNumber=1&ip=$USERIP$&fzTeamId=$TEAM_ID$&fzTeamName=$TEAM_NAME$'
    };
    user = {
      claims: {
        get: () => { }
      }
    };
    userService = {};
    fanzoneGamesService = {
      setNewSignPostingSeenDate: jasmine.createSpy('setNewSignPostingSeenDate')
    };
    fanzoneSharedService = {
      getFanzoneNewSignPosting: jasmine.createSpy('getFanzoneNewSignPosting'),
      showGameLaunchPopup: jasmine.createSpy('showGameLaunchPopup')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    fanzoneStorageService = {
      get: jasmine.createSpy('get').and.returnValue({ teamId:'FZ001', teamName: 'Manchester' }),
      set: jasmine.createSpy('set')
    };
    pubsub = {
      cbMap: {},
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((name, method, cb) => pubsub.cbMap[method] = cb),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    fanzoneHelperService = {};
    component = new FanzoneAppGamesComponent(windowRefService,
      page,
      deviceService,
      casinoGamesConfig,
      user,
      userService,
      fanzoneGamesService,
      fanzoneSharedService,
      gtmService,
      fanzoneStorageService,
      pubsub,
      fanzoneHelperService
    );
  });

  describe('ngOnInit', () => {
    it('should invoke on load', () => {
      fanzoneHelperService.selectedFanzone = FANZONECONFIG as any;
      spyOn(component, 'getNewSignPostingData');
      spyOn(component, 'getFanzoneGamesHost');
      spyOn(component, 'buildFanzoneGamesData');
      component.ngOnInit();
      expect(component.getNewSignPostingData).toHaveBeenCalled();
      expect(component.getFanzoneGamesHost).toHaveBeenCalled();
      expect(component.buildFanzoneGamesData).toHaveBeenCalled();
    });

    it('should get fanzone details data ', fakeAsync(() => {
      spyOn(component, 'getNewSignPostingData');
      spyOn(component, 'getFanzoneGamesHost');
      spyOn(component, 'buildFanzoneGamesData');
      pubsub.subscribe = jasmine.createSpy('pubSubService.subscribe')
          .and.callFake((filename: string, eventName: string, callback: Function) => {
              if (eventName === 'FANZONE_DATA') {
                  callback(FANZONECONFIG);

                  expect(component.fanzoneDetails).toBeDefined();
                  expect(component.buildFanzoneGamesData).toHaveBeenCalled();
              }
          });
      component.ngOnInit();
    }));
  });

  it('should make fanzone fanzoneGames data  empty', fakeAsync(() => {
    spyOn(component, 'getNewSignPostingData');
    spyOn(component, 'getFanzoneGamesHost');
    spyOn(component, 'buildFanzoneGamesData');
    pubsub.subscribe = jasmine.createSpy('pubSubService.subscribe')
        .and.callFake((filename: string, eventName: string, callback: Function) => {
          callback();
          expect(component.fanzoneGames).toEqual([]);
        });
    component.ngOnInit();
  }));

  describe('getNewSignPostingData', () => {
    it('should get the new Signposting data', () => {
      fanzoneSharedService.getFanzoneNewSignPosting.and.returnValue(of([{ startDate: '', endDate: '' }]));
      component.getNewSignPostingData();
      expect(component.newSignPostingData).toBeDefined();
    });
  });

  describe('getFanzoneGamesHost', () => {
    it('should get host url from clientconfig', () => {
      component.getFanzoneGamesHost();
      expect(component.clientConfig).toBeDefined();
    });

    it('should host be undefined if clientconfig is not available', () => {
      windowRefService.nativeWindow.clientconfig = undefined;
      component.getFanzoneGamesHost();
      expect(component.clientConfig).toBeDefined();
    });

    it('should host be undefined if nativeWindow is not available', () => {
      windowRefService.nativeWindow = undefined;
      component.getFanzoneGamesHost();
      expect(component.clientConfig).toBeDefined();
    });
  });

  describe('buildFanzoneGamesData', () => {
    it('should build fanzone games array', () => {
      component.fanzoneDetails = FANZONECONFIG as any;
      spyOn(component, 'getThumbnailAndGameUrls').and.returnValue({} as any);
      component.buildFanzoneGamesData();
      expect(component.getThumbnailAndGameUrls).toHaveBeenCalledTimes(FANZONE_GAMES.SUPPORTED_GAMES.length * 2);
      expect(component.fanzoneGames.length).toBe(FANZONE_GAMES.SUPPORTED_GAMES.length);
    });
  });

  describe('getThumbnailAndGameUrls', () => {
    it('should build game thumbnail and launch url for mobile', () => {
      deviceService.isMobileOnly = true;
      const storage = { teamId:'FZ001', teamName: 'Manchester' };
      spyOn(component, 'buildFanzoneGameImageUrl');
      spyOn(component, 'buildFanzoneGameLaunchUrl');
      const urls = component.getThumbnailAndGameUrls('test');
      expect(component.buildFanzoneGameImageUrl).toHaveBeenCalledOnceWith(casinoGamesConfig.fzGmImgMbUrl, 'test', storage);
      expect(component.buildFanzoneGameLaunchUrl).toHaveBeenCalledOnceWith(casinoGamesConfig.fzGmLaMbUrl, 'test', storage);
    });

    it('should build game thumbnail and launch url for desktop', () => {
      deviceService.isMobileOnly = false;
      const storage = { teamId:'FZ001', teamName: 'Manchester' };
      spyOn(component, 'buildFanzoneGameImageUrl');
      spyOn(component, 'buildFanzoneGameLaunchUrl');
      component.getThumbnailAndGameUrls('test');
      expect(component.buildFanzoneGameImageUrl).toHaveBeenCalledOnceWith(casinoGamesConfig.fzGmImgDsUrl, 'test', storage );
      expect(component.buildFanzoneGameLaunchUrl).toHaveBeenCalledOnceWith(casinoGamesConfig.fzGmLaDsUrl, 'test', storage);
    });
  });

  describe('buildFanzoneGameImageUrl', () => {
    it('should prepare dynamic game image url', () => {
      const storage = { teamId:'FZ001', teamName: 'Manchester' };
      const gameVariantName = 'test';
      component.fanzoneGamesHost = 'https://casinogames.ladbrokes.com';
      const gameThumbnailUrl = component.buildFanzoneGameImageUrl(casinoGamesConfig.fzGmImgDsUrl, gameVariantName, storage);
      expect(gameThumbnailUrl).toBe(`${component.fanzoneGamesHost}/htmllobby/images/newlmticons/fanzonelarge/${gameVariantName}_${storage.teamId}.jpg`);
    });
  });

  describe('buildFanzoneGameLaunchUrl', () => {
    it('should prepare dynamic game launch url for ios device if wrapper', () => {
      component.clientConfig = windowRefService.nativeWindow.clientConfig;
      const storage = { teamId:'FZ001', teamName: 'Manchester' };
      const gameVariantName = 'test';
      component.fanzoneGamesHost = 'https://casinogames.ladbrokes.com';
      deviceService.isIos = true;
      deviceService.isWrapper = true;
      spyOn(component, <any>'getEnvironment').and.returnValue('test');
      const gameLaunchUrl = component.buildFanzoneGameLaunchUrl(casinoGamesConfig.fzGmImgMbUrl, gameVariantName, storage);
      expect(gameLaunchUrl).not.toBeUndefined();
    });

    it('should prepare dynamic game launch url for ios device if not wrapper', () => {
      component.clientConfig = windowRefService.nativeWindow.clientConfig;
      const storage = { teamId:'FZ001', teamName: 'Manchester' };
      const gameVariantName = 'test';
      component.fanzoneGamesHost = 'https://casinogames.ladbrokes.com';
      deviceService.isIos = true;
      deviceService.isWrapper = false;
      spyOn(component, <any>'getEnvironment').and.returnValue('test');
      const gameLaunchUrl = component.buildFanzoneGameLaunchUrl(casinoGamesConfig.fzGmImgMbUrl, gameVariantName, storage);
      expect(gameLaunchUrl).not.toBeUndefined();
    });

    it('should prepare dynamic game launch url for android device if wrapper', () => {
      component.clientConfig = windowRefService.nativeWindow.clientConfig;
      const storage = { teamId:'FZ001', teamName: 'Manchester' };
      const gameVariantName = 'test';
      component.fanzoneGamesHost = 'https://casinogames.ladbrokes.com';
      deviceService.isIos = false;
      deviceService.isWrapper = true;
      spyOn(component, <any>'getEnvironment').and.returnValue('test');
      const gameLaunchUrl = component.buildFanzoneGameLaunchUrl(casinoGamesConfig.fzGmImgMbUrl, gameVariantName, storage);
      expect(gameLaunchUrl).not.toBeUndefined();
    });

    it('should prepare dynamic game launch url for android device if not wrapper', () => {
      component.clientConfig = windowRefService.nativeWindow.clientConfig;
      const storage = { teamId:'FZ001', teamName: 'Manchester' };
      const gameVariantName = 'test';
      component.fanzoneGamesHost = 'https://casinogames.ladbrokes.com';
      deviceService.isIos = false;
      deviceService.isWrapper = false;
      spyOn(component, <any>'getEnvironment').and.returnValue('test');
      const gameLaunchUrl = component.buildFanzoneGameLaunchUrl(casinoGamesConfig.fzGmImgMbUrl, gameVariantName, storage);
      expect(gameLaunchUrl).not.toBeUndefined();
    });
  });

  describe('suppressGameForRGYUsers', () => {
    it('should hide slot rivals game for rgy users', () => {
      userService.bonusSuppression = true;
      expect(component.suppressGameForRGYUsers('SLOT_RIVALS')).toBeTruthy();
    });

    it('should not hide scratch card game for rgy users', () => {
      userService.bonusSuppression = true;
      expect(component.suppressGameForRGYUsers('SCRATCH_CARDS')).toBeFalsy();
    });
  });

  describe('ngOnDestroy', () => {
    it('should set the storage with new signposting seen data', () => {
      component.ngOnDestroy();
      expect(fanzoneGamesService.setNewSignPostingSeenDate).toHaveBeenCalled();
    });
  });

  describe('launchGame', () => {
    it('should launch game in same window for mobile', () => {
      deviceService.isMobileOnly = true;
      component.launchGame({gameLaunchUrl: 'testurl'} as any, 0);
      expect(windowRefService.nativeWindow.open).toHaveBeenCalledWith('testurl', '_self');
      expect(gtmService.push).toHaveBeenCalled();
    });

    it('should launch game in popup for desktop', () => {
      deviceService.isMobileOnly = false;
      component.launchGame({gameLaunchUrl: 'testurl'} as any,0);
      expect(fanzoneSharedService.showGameLaunchPopup).toHaveBeenCalled();
      expect(gtmService.push).toHaveBeenCalled();
    });
  });

  describe('playNow', () => {
    it('should launch game on click of Play Now button', () => {
      deviceService.isMobileOnly = false;
      const event: any = { stopPropagation: jasmine.createSpy() };
      component.playNow(event, {gameLaunchUrl: 'testurl'} as any ,0);
      expect(fanzoneSharedService.showGameLaunchPopup).toHaveBeenCalled();
      expect(gtmService.push).toHaveBeenCalled();
    });
  });

  describe('getPageCulture', () => {
    it('#getPageCulture', () => {
      component['getPageCulture']();
      expect(page.culture.replace).toHaveBeenCalled();
    });
  });

  describe('getEnvironment', () => {
    it('should return QA for qa env', () => {
      component.clientConfig = windowRefService.nativeWindow.clientConfig;
      expect(component['getEnvironment']()).toBe('QA');
    });

    it('should return FVT for stage env.', () => {
      component.clientConfig = windowRefService.nativeWindow.clientConfig;
      component.clientConfig.vnProductHomepages.sports = "http://test.sports.coral.co.uk/en"
      expect(component['getEnvironment']()).toBe('FVT');
    });

    it('should return BETA for beta envs', () => {
      component.clientConfig = windowRefService.nativeWindow.clientConfig;
      component.clientConfig.vnProductHomepages.sports = "http://beta2.sports.coral.co.uk/en"
      expect(component['getEnvironment']()).toBe('BETA');
    });

    it('should return PROD for production', () => {
      component.clientConfig = windowRefService.nativeWindow.clientConfig;
      component.clientConfig.vnProductHomepages.sports = "http://sports.coral.co.uk/en"
      expect(component['getEnvironment']()).toBe('PROD');
    });
  });
});
