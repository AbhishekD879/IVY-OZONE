import { fakeAsync, tick } from '@angular/core/testing';
import { of } from 'rxjs';
import { RpgComponent } from './rpg.component';
import { clientConfigMock, rpgResponseMock, gymlResponseMock } from './rpg.component.mock';

describe('RpgComponent', () => {
  let component, windowRef, deviceService,
  page,
  gtmService,
  http,
  storageService,
  casinoGamesConfig,
  user,
  awsFirehoseService,
  changeDetectorRef;

  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        location: {
          href: ''
        },
        open: jasmine.createSpy('open'),
        clearTimeout: jasmine.createSpy('clearTimeout'),
        setTimeout: jasmine.createSpy().and.callFake((callback: Function) => {
          callback();
        }),
        clientConfig: {
          bmaCasinoGamesConfig: {
            miniGamesHost: 'www.coral.co.uk/en'
          },
          vnAppInfo: {
            brand: 'CORAL',
            frontend: 'cl',
            vnClaims: {
              'http://api.bwin.com/v3/user/usertoken': 'asdasd',
              'http://api.bwin.com/v3/user/sessiontoken': '121212'
            }
          }
        }
      }
    };
    page = {
      culture: {
        replace: jasmine.createSpy('replace')
      }
    };
    deviceService = {};
    gtmService = {
      push: jasmine.createSpy('push')
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges')
    };

    http = {
      get: () => {},
      post: () => {}
    };

    storageService = {
      get: () => {},
      set: () => {}
    };

    awsFirehoseService = {
      addAction: jasmine.createSpy()
    };

    user = {
      claims: {
        get: () => { }
      }
    };

    casinoGamesConfig = {
      gameLaunchUrl: `/fcasino/en_GB/fcgames/vendorgames/mobile.html?gameVariantName=$GAMENAME$&langId=$LANGID$&invokerProduct=BETTING&channelId=$CHANNELID$&brandId=LADBROKEUK&lobbyType=instantGames&conf=$ENV$&ip=$USERIP$&keepAliveInterval=600000&mode=real&demo=FALSE&ssoKey=$SESSIONKEY$&lobbyURL=$LOBBYURL$&pLang=$pLANG$&frontend=ld&userToken=$USERTOKEN$&sessionToken=$SESSIONTOKEN$&clickTimeStamp=$TIMESTAMP$&launchSource=SPORTS_GYML&catId=LMC_HOME&subcatId=LMC_HOME_TOPGAMES&rowNumber=1&colNumber=$COLNUMBER$&iconSize=1`,
      gymlUrl: 'https://scmedia.itsfogo.com/$-$/aecf2c358b6d45cd8b191dd0590d06bf.json',
      gameImageUrl: 'https://casinogames.ladbrokes.com/htmllobby/images/newlmticons/supersquare/{0}.jpg',
      recentlyPlayedGamesUrl: "/games/casinowidget/recentgameswidget?.box=1&invokerProduct=betting&_disableFeature=GlobalSearch",
      rpgUrl: 'https://lcg-feeds.itsbogo.com/api/rest/casino/feeds/v2/getUserRecentlyPlayedGames&sessionKey=$SESSIONKEY$',
      miniGamesHost: 'https://casinogames.ladbrokes.com',
      userHostAddress: '12.3.4.5',
      rpgCacheExpiry: 1,
      rpgPayload: {
        "accountName": "$ACCOUNTNAME$",
        "productId": "CASINO",
        "brandId": "CORAL",
        "feId": "cl",
        "channelId": "$CHANNELID$",
        "lang": "en_US",
        "noofgames": 10,
        "lobbyType": "instantCasino",
        "reqSource": "LCG_SPORTS"
      }
    };

    component = new RpgComponent(
      windowRef,
      deviceService,
      page,
      gtmService,
      http,
      storageService,
      casinoGamesConfig,
      user,
      changeDetectorRef,
      awsFirehoseService
    );
  });

  it('should create a component', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('clientConfig data is available', () => {
      component['getCasinoData'] = jasmine.createSpy('getCasinoData');
      spyOn(component, 'setGATracking');
      const getSpy = spyOn(storageService, 'get').and.returnValue({filteredRpg: null, timestamp: new Date().getTime() - 100*1000, username: 'abc'});
      component.ngOnInit();
      expect(component['getCasinoData']).toHaveBeenCalled();
    });

    it('clientConfig data is available, but rpgPayload data is NOT there', () => {
      component['getCasinoData'] = jasmine.createSpy('getCasinoData');
      spyOn(component, 'setGATracking');
      component.casinoGamesConfig.rpgPayload = null;
      const getSpy = spyOn(storageService, 'get').and.returnValue({filteredRpg: null, timestamp: new Date().getTime() - 100*1000, username: 'abc'});
      component.ngOnInit();
      expect(component['getCasinoData']).not.toHaveBeenCalled();
    });

    it('clientConfig data is available, userName mismatch', () => {
      component['getCasinoData'] = jasmine.createSpy('getCasinoData');
      spyOn(component, 'setGATracking');
      const getSpy = spyOn(storageService, 'get').and.returnValue({filteredRpg: null, timestamp: new Date().getTime() - 3*1000, username: 'abc'});
      component.userName = '123';
      component.ngOnInit();
      expect(component['getCasinoData']).toHaveBeenCalled();
    });

    it('clientConfig data is available, using stored rpg data', () => {
      component['getCasinoData'] = jasmine.createSpy('getCasinoData');
      const rpgData = [
        {
          "displayname": "Crypto Cash",
          "gamevariant": "ivycryptocash",
          "imageUrl": "https://casinogames.coral.co.uk/htmllobby/images/newlmticons/supersquare/ivycryptocash.jpg"
        },
        {
          "displayname": "Eye of Horus",
          "gamevariant": "blueprinteyeofhorus",
          "imageUrl": "https://casinogames.coral.co.uk/htmllobby/images/newlmticons/supersquare/blueprinteyeofhorus.jpg"
        }
      ];
      spyOn(component, 'setGATracking');
      const getSpy = spyOn(storageService, 'get').and.returnValue({filteredRpg: rpgData, timestamp: new Date().getTime() - 3*1000, username: 'abc'});
      const setCarouselScrollTrackSpy = spyOn(component, 'setCarouselScrollTrack');
      component.userName = 'abc';
      component.ngOnInit();
      expect(component['getCasinoData']).not.toHaveBeenCalled();
    });

    it('clientConfig data is NOT available', () => {
      component['getCasinoData'] = jasmine.createSpy('getCasinoData');
      spyOn(component, 'setGATracking');
      const getSpy = spyOn(storageService, 'get').and.returnValue({filteredRpg: null, timestamp: new Date().getTime() - 100*1000, username: 'abc'});
      windowRef.nativeWindow = {};
      component.ngOnInit();
      expect(component['getCasinoData']).toHaveBeenCalled();
    });
  });
  
  it('#seeMoreClick', () => {
    component['setGATracking'] = jasmine.createSpy('setGATracking');
    component.seeMoreClick();
    expect(component['setGATracking']).toHaveBeenCalled();
  });

  it('#getPageCulture', () => {
    component.getPageCulture();
    expect(page.culture.replace).toHaveBeenCalled();
  });

  it('#setGATracking', () => {
    component.setGATracking('contentView', 'load', 'not applicable', 'not applicable', 'not applicable');
    expect(gtmService.push).toHaveBeenCalled();
  });

  describe('#setCarouselScrollTrack', () => {
    it('when element is there in html', () => {
      const elem = document.createElement('div');
     spyOn(document, 'querySelector').and.returnValue(elem);
     const addEventListenerSpy = spyOn(elem, 'addEventListener');
      component.setCarouselScrollTrack();
      expect(addEventListenerSpy).toHaveBeenCalled();
    });
  });
  

  it('#scrollEventCallback', () => {
    component.scrollEventCallback();
    expect(windowRef.nativeWindow.setTimeout).toHaveBeenCalledWith(jasmine.any(Function), 66);
  });

  it('#ngOnDestroy', () => {
    const elem = document.createElement('div');
   spyOn(document, 'querySelector').and.returnValue(elem);
   const removeEventListenerSpy = spyOn(elem, 'removeEventListener');
    component.ngOnDestroy();
    expect(removeEventListenerSpy).toHaveBeenCalled();
  });

  it('#getCasinoData with data in rpg and gyml calls', fakeAsync(() => {
    spyOn(component, 'getRpgData').and.returnValue(of(rpgResponseMock));
    spyOn(component, 'getGymlData').and.returnValue(of(gymlResponseMock));
    spyOn(component, 'setGATracking');
    component.rpgModule = {gamesAmount: 10};
    component.rpgUrl = 'https://lcg-feeds.itsbogo.com/api/rest/casino/feeds/v2/getUserRecentlyPlayedGames&sessionKey=$SESSIONKEY$';
    component.gymlUrl = 'https://scmedia.itsfogo.com/$-$/aecf2c358b6d45cd8b191dd0590d06bf.json';
    const setCarouselScrollTrackSpy = spyOn(component, 'setCarouselScrollTrack');
    component.getCasinoData();
    tick(100);
    expect(setCarouselScrollTrackSpy).toHaveBeenCalled();
  }));

  it('#getCasinoData with data in rpg call and Dont have to use gyml call', fakeAsync(() => {
    spyOn(component, 'getRpgData').and.returnValue(of(rpgResponseMock));
    spyOn(component, 'getGymlData').and.returnValue(of(gymlResponseMock));
    spyOn(component, 'setGATracking');
    component.rpgModule = {gamesAmount: 6};
    component.rpgUrl = 'https://lcg-feeds.itsbogo.com/api/rest/casino/feeds/v2/getUserRecentlyPlayedGames&sessionKey=$SESSIONKEY$';
    component.gymlUrl = 'https://scmedia.itsfogo.com/$-$/aecf2c358b6d45cd8b191dd0590d06bf.json';
    const setCarouselScrollTrackSpy = spyOn(component, 'setCarouselScrollTrack');
    component.getCasinoData();
    tick(100);
    expect(setCarouselScrollTrackSpy).toHaveBeenCalled();
  }));

  it('#getCasinoData with NO data in rpg call', fakeAsync(() => {
    spyOn(component, 'getRpgData').and.returnValue(of({}));
    spyOn(component, 'setGATracking');
    const setCarouselScrollTrackSpy = spyOn(component, 'setCarouselScrollTrack');
    component.getCasinoData();
    tick(100);
    expect(setCarouselScrollTrackSpy).not.toHaveBeenCalled();
  }));

  it('#getRpgData, android web, for CORAL, with NO sessionKey in rpgUrl', () => {
    const getSpy = spyOn(http, 'post');
    component.rpgPayload = clientConfigMock.bmaCasinoGamesConfig.rpgPayload;
    component.brand = 'CORAL';
    component.userName = 'abc';
    component.rpgUrl = 'https://lcg-feeds.itsbogo.com/api/rest/casino/feeds/v2/getUserRecentlyPlayedGames';
    component.getRpgData();
    expect(getSpy).toHaveBeenCalled();
  });

  it('#getRpgData, android web, for LADBROKEUK, with NO sessionKey in rpgUrl', () => {
    const getSpy = spyOn(http, 'post');
    component.rpgPayload = clientConfigMock.bmaCasinoGamesConfig.rpgPayload;
    component.brand = 'LADBROKEUK';
    component.userName = 'abc';
    component.rpgUrl = 'https://lcg-feeds.itsbogo.com/api/rest/casino/feeds/v2/getUserRecentlyPlayedGames';
    component.getRpgData();
    expect(getSpy).toHaveBeenCalled();
  });


  it('#getRpgData, android web, for CORAL', () => {
    const getSpy = spyOn(http, 'post');
    component.rpgPayload = clientConfigMock.bmaCasinoGamesConfig.rpgPayload;
    component.brand = 'CORAL';
    component.userName = 'abc';
    component.rpgUrl = 'https://lcg-feeds.itsbogo.com/api/rest/casino/feeds/v2/getUserRecentlyPlayedGames&sessionKey=$SESSIONKEY$';
    component.getRpgData();
    expect(getSpy).toHaveBeenCalled();
  });

  it('#getRpgData, android web', () => {
    const getSpy = spyOn(http, 'post');
    component.rpgPayload = clientConfigMock.bmaCasinoGamesConfig.rpgPayload;
    component.userName = 'abc';
    component.rpgUrl = 'https://lcg-feeds.itsbogo.com/api/rest/casino/feeds/v2/getUserRecentlyPlayedGames&sessionKey=$SESSIONKEY$';
    component.getRpgData();
    expect(getSpy).toHaveBeenCalled();
  });

  it('#getRpgData, android Native', () => {
    const getSpy = spyOn(http, 'post');
    component.rpgPayload = clientConfigMock.bmaCasinoGamesConfig.rpgPayload;
    component.deviceService.isWrapper = true;
    component.userName = 'abc';
    component.rpgUrl = 'https://lcg-feeds.itsbogo.com/api/rest/casino/feeds/v2/getUserRecentlyPlayedGames&sessionKey=$SESSIONKEY$';
    component.getRpgData();
    expect(getSpy).toHaveBeenCalled();
  });

  it('#getRpgData, IOS Native', () => {
    const getSpy = spyOn(http, 'post');
    component.rpgPayload = clientConfigMock.bmaCasinoGamesConfig.rpgPayload;
    component.userName = 'abc';
    component.deviceService.isIos = true;
    component.deviceService.isWrapper = true;
    component.rpgUrl = 'https://lcg-feeds.itsbogo.com/api/rest/casino/feeds/v2/getUserRecentlyPlayedGames&sessionKey=$SESSIONKEY$';
    component.getRpgData();
    expect(getSpy).toHaveBeenCalled();
  });

  it('#getRpgData, IOS web', () => {
    const getSpy = spyOn(http, 'post');
    component.rpgPayload = clientConfigMock.bmaCasinoGamesConfig.rpgPayload;
    component.userName = 'abc';
    component.deviceService.isIos = true;
    component.deviceService.isWrapper = false;
    component.rpgUrl = 'https://lcg-feeds.itsbogo.com/api/rest/casino/feeds/v2/getUserRecentlyPlayedGames&sessionKey=$SESSIONKEY$';
    component.getRpgData();
    expect(getSpy).toHaveBeenCalled();
  });

  it('#getGymlData - Android Non-wrapper', () => {
    const getSpy = spyOn(http, 'get');
    component.getGymlData();
    expect(getSpy).toHaveBeenCalled();
  });

  describe('#rpgCarouselClick', () => {
    it('device is IN', () => {
      component.clientConfig = clientConfigMock;
      const setGATrackingSpy = spyOn(component, 'setGATracking');
      spyOn(component, 'getPageCulture').and.returnValue('en_gb');
      spyOn(component, 'getEnvironment').and.returnValue('BETA');
      deviceService.isIos = true;
      deviceService.isWrapper = true;
      component.rpgCarouselClick('playtechlivespinawin', 2);
      expect(setGATrackingSpy).toHaveBeenCalled();
    });

    it('device is IOS', () => {
      component.clientConfig = clientConfigMock;
      const setGATrackingSpy = spyOn(component, 'setGATracking');
      spyOn(component, 'getPageCulture').and.returnValue('en_gb');
      spyOn(component, 'getEnvironment').and.returnValue('BETA');
      deviceService.isIos = true;
      deviceService.isWrapper = false;
      component.rpgCarouselClick('playtechlivespinawin', 2);
      expect(setGATrackingSpy).toHaveBeenCalled();
    });

    it('device is AN', () => {
      component.clientConfig = clientConfigMock;
      const setGATrackingSpy = spyOn(component, 'setGATracking');
      spyOn(component, 'getPageCulture').and.returnValue('en_gb');
      spyOn(component, 'getEnvironment').and.returnValue('BETA');
      deviceService.isIos = false;
      deviceService.isWrapper = true;
      component.rpgCarouselClick('playtechlivespinawin', 2);
      expect(setGATrackingSpy).toHaveBeenCalled();
    });

    it('device is AW', () => {
      component.clientConfig = clientConfigMock;
      const setGATrackingSpy = spyOn(component, 'setGATracking');
      spyOn(component, 'getPageCulture').and.returnValue('en_gb');
      spyOn(component, 'getEnvironment').and.returnValue('BETA');
      deviceService.isIos = false;
      deviceService.isWrapper = false;
      component.rpgCarouselClick('playtechlivespinawin', 2);
      expect(setGATrackingSpy).toHaveBeenCalled();
    });
  });


  describe('#getEnvironment', () => {
    it('should return QA', () => {
      component.clientConfig = clientConfigMock;
      expect(component.getEnvironment()).toBe('QA');
    });

    it('should return FVT for stage env.', () => {
      component.clientConfig = clientConfigMock;
      component.clientConfig.vnProductHomepages.sports = "http://test.sports.coral.co.uk/en"
      expect(component.getEnvironment()).toBe('FVT');
    });

    it('should return PROD', () => {
      component.clientConfig = clientConfigMock;
      component.clientConfig.vnProductHomepages.sports = "http://sports.coral.co.uk/en"
      expect(component.getEnvironment()).toBe('PROD');
    });
  });
});
