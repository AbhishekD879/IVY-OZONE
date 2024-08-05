import { AuthService } from '@authModule/services/auth/auth.service';
import {
    of as observableOf,
    throwError as observableThrowError,
    Observable
} from 'rxjs';
import { ITempToken } from '@authModule/services/auth/auth.model';
import { fakeAsync, tick } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('AuthService', () => {
    let service: AuthService;
    let tempTokenService;
    let userService;
    let storage;
    let device;
    let bppAuthService;
    let proxyHeadersService;
    let getCookie;
    let sessionService;
    let commandService;
    let pubsub;
    let cmsService;
    let awsService;
    let upmsService;

    const temporaryTokenResponse = { sessionToken: 'temporarySessionToken' };
    let bppValidationResult = {
        freeBets: [''],
        privateMarkets: [''],
        token: 'token'
    };

    const createSpyWithReturnedObservable = (spyName: string, observableOf1?: any) => {
        return jasmine.createSpy(spyName)
            .and.returnValue(observableOf(observableOf1 ? observableOf1 : null));
    };

    beforeEach(() => {
        userService = {
            logout: jasmine.createSpy(),
            login: jasmine.createSpy(),
            set: jasmine.createSpy(),
            initProxyAuth: jasmine.createSpy(),
            resolveProxyAuth: jasmine.createSpy(),
            rejectProxyAuth: jasmine.createSpy(),
            isInShopUser: jasmine.createSpy().and.returnValue(false),
            proxyPromiseResolved: jasmine.createSpy().and.returnValue(true),
            username: 'username',
            bppToken: 'Aoz_dshfdfefnfE20--e'
        };
        storage = {
            set: jasmine.createSpy()
        };
        proxyHeadersService = {
            generateBppAuthHeaders: jasmine.createSpy()
        };
        bppAuthService = {
            validate: jasmine.createSpy()
        };
        tempTokenService = {
            fetchTemporaryToken: jasmine.createSpy()
        };
        device = {
            freeBetChannel: 'Mz'
        };

        getCookie = jasmine.createSpy('getCookie');
        storage = {
            getCookie,
            remove: jasmine.createSpy('remove'),
            get: jasmine.createSpy('get'),
            set: jasmine.createSpy('set')
        };

        awsService = {
            addAction: jasmine.createSpy('addAction')
        };

        device = {
            freeBetChannel: 'M'
        };

        bppAuthService = {
            validate: createSpyWithReturnedObservable('validate'),
        };

        proxyHeadersService = {
            generateBppAuthHeaders: jasmine.createSpy('generateBppAuthHeaders')
        };
        sessionService = {
          whenProxySession: jasmine.createSpy('whenProxySession').and.returnValue(Promise.resolve({}))
        };
        commandService = {
          register: jasmine.createSpy('register'),
          API: {
            BPP_AUTH_SEQUENCE: 'auth/bppAuthSequence',
            ODDS_BOOST_INIT: 'INIT_ODDS_BOOST',
            GET_ODDS_BOOST_TOKENS: 'GET_ODDS_BOOST_TOKENS'
          },
          executeAsync: jasmine.createSpy('executeAsync').and.returnValue(Promise.resolve(null))
        };
        pubsub = {
          publish: jasmine.createSpy('publish'),
          publishSync: jasmine.createSpy('publishSync'),
          subscribe: jasmine.createSpy('subscribe'),
          API: pubSubApi
        };
        cmsService = {
          getOddsBoost: jasmine.createSpy('getOddsBoost').and.returnValue(observableOf({}))
        };
        upmsService = {
            getOddsPreference: jasmine.createSpy('getOddsPreference').and.returnValue(observableOf({preferences:{oddPreference:'frac'}}))
        }

        service = new AuthService(
            tempTokenService,
            userService,
            bppAuthService,
            storage,
            proxyHeadersService,
            device,
            sessionService,
            commandService,
            pubsub,
            cmsService,
            awsService,
            upmsService
        );
    });

    describe('bppAuthSequence', () => {
        it('#bppAuthSequence should call correct methods', () => {
            const tokenData = {} as any;
            service.getTempToken = jasmine.createSpy().and.returnValue(observableOf(tokenData));
            service.bppLogin = jasmine.createSpy().and.returnValue(observableOf({}));
            service.bppAuthSequence().subscribe(() => {
                expect(service['bppLogin']).toHaveBeenCalledWith(tokenData as any);
            });
            expect(userService.initProxyAuth).toHaveBeenCalled();
            expect(service.getTempToken).toHaveBeenCalled();
        });

        it('#bppAuthSequence should not call bppLogin in case if there is no tokenData', () => {
            service.getTempToken = jasmine.createSpy().and.returnValue(observableOf(null));
            service.bppLogin = jasmine.createSpy().and.returnValue(observableOf({}));
            service.bppAuthSequence().subscribe(() => { }, () => {
                expect(service.bppLogin).not.toHaveBeenCalled();
            });
            expect(userService.initProxyAuth).toHaveBeenCalled();
            expect(service.getTempToken).toHaveBeenCalled();
        });
    });

    describe('getTempToken', () => {
        it('#getTempToken should call correct method and return correct result', () => {
            service['tempTokenService']['fetchTemporaryToken'] = jasmine.createSpy().and.returnValue(observableOf(temporaryTokenResponse));
            service.getTempToken().subscribe((data) => {
                expect(data).toEqual(jasmine.objectContaining({
                    username: userService.username,
                    tempToken: temporaryTokenResponse.sessionToken
                }));
            });
            expect(tempTokenService.fetchTemporaryToken).toHaveBeenCalled();
        });

        it('#getTempToken should return null in case there is no sessionToken in response', () => {
            service['tempTokenService']['fetchTemporaryToken'] = jasmine.createSpy().and.returnValue(observableOf({}));
            service.getTempToken().subscribe((data) => {
                expect(data).toBeUndefined();
            });
            expect(tempTokenService.fetchTemporaryToken).toHaveBeenCalled();
        });

        it('#getTempToken should return null in case of error in response', () => {
            service['tempTokenService']['fetchTemporaryToken'] = jasmine.createSpy().and.returnValue(observableThrowError(null));
            service.getTempToken().subscribe((data) => {
                expect(data).toBeNull();
            });
            expect(tempTokenService.fetchTemporaryToken).toHaveBeenCalled();
        });
    });

    describe('bppLogin', () => {
      it('call correct methiods after execution', fakeAsync(() => {
        const userResponseMock = {
          freeBets: 'freeBets',
          privateMarkets: {
            data: []
          },
          betBoosts: {
            data: []
          },
          token: 'token'
        };

        bppAuthService.validate = jasmine.createSpy().and.returnValue(
          observableOf(userResponseMock)
        );
        const testToken = {
          username: 'username',
          tempToken: 'sessionToken'
        };

        service['bppLogin'](testToken).subscribe(
          () => {
            expect(storage.set).toHaveBeenCalledWith('previousBppUsername', userService.username);
            expect(service['userService'].set).toHaveBeenCalled();
            expect(proxyHeadersService.generateBppAuthHeaders).toHaveBeenCalled();
            expect(userService.resolveProxyAuth).toHaveBeenCalled();
            expect(pubsub.publishSync.calls.argsFor(0)).toEqual(['STORE_PRIVATE_MARKETS', [userResponseMock.privateMarkets.data]]);
          },
          () => {
            expect(userService.rejectProxyAuth).toHaveBeenCalled();
          });
        tick();
      }));

        it('#bppLogin should call handleBppLoginError', () => {
            const params = { tempToken: 'sessionToken', username: userService.username };
            bppValidationResult = { error: 'error' } as any;
            service['handleBppLoginError'] = jasmine.createSpy();
            service['bppAuthService']['validate'] = jasmine.createSpy().and.returnValue(observableOf(bppValidationResult));
            service['bppLogin'](params as ITempToken).subscribe(() => {
                expect(storage.set).not.toHaveBeenCalledWith('previousBppUsername', userService.username);
                expect(pubsub.publish).not.toHaveBeenCalledWith('STORE_FREEBETS', bppValidationResult.freeBets);
                expect(pubsub.publish).not.toHaveBeenCalledWith('STORE_FREEBETS', bppValidationResult.privateMarkets);
                expect(userService.set).not.toHaveBeenCalledWith(jasmine.objectContaining({ bppToken: bppValidationResult.token }));
                expect(proxyHeadersService.generateBppAuthHeaders).not.toHaveBeenCalled();
                expect(userService.resolveProxyAuth).not.toHaveBeenCalled();
            });
            expect(bppAuthService.validate).toHaveBeenCalledWith(jasmine.objectContaining({
                username: userService.username,
                token: params.tempToken,
                channel: device.freeBetChannel
            }));
            expect(service['handleBppLoginError']).toHaveBeenCalled();
        });

      it('should store private markets as empty array', fakeAsync(() => {
        const testToken = {
          username: 'username',
          tempToken: 'sessionToken'
        };

        bppAuthService.validate.and.returnValue(observableOf({
          token: 'sadasdasfsd',
          freeBets: {
            data: [
              {
                freebetOfferType: 'SGL',
                freebetOfferCategories: {
                  freebetOfferCategory: 'Bet Pack'
                },
                tokenPossibleBet: {
                  inPlay: 'N',
                  betLevel: "ANY_POOLS"
                },
                tokenPossibleBets: []
              },{
                freebetOfferType: '',
                freebetOfferCategories: {
                  freebetOfferCategory: 'Bet Pack'
                },
                tokenPossibleBet: {
                  inPlay: 'N',
                  betLevel: "ANY"
                },
                tokenPossibleBets: []
              },
              {
                freebetOfferType: '',
                freebetOfferCategories: {
                  freebetOfferCategory: 'Bet Pack1'
                },
                tokenPossibleBet: {
                  inPlay: 'N',
                  betLevel: "ANY_POOLS"
                },
                tokenPossibleBets: []
              },{
                freebetOfferType: '',
                freebetOfferCategories: {
                  freebetOfferCategory: 'Bet Pack1'
                },
                tokenPossibleBet: {
                  inPlay: 'N',
                  betLevel: "ANY"
                },
                tokenPossibleBets: []
              },{
                freebetOfferType: 'SGL',
                freebetOfferCategories: {
                  freebetOfferCategory: 'Bet Pack1'
                },
                tokenPossibleBet: {
                  inPlay: 'N',
                  betLevel: "ANY"
                },
                tokenPossibleBets: []
              },{
                freebetOfferType: 'SGL',
                tokenPossibleBet: {
                  inPlay: 'N',
                  betLevel: "ANY"
                },
                tokenPossibleBets: []
              }
            ]
          }
        }));        
        service.bppLogin(testToken).subscribe();
        tick();
        expect(pubsub.publishSync).toHaveBeenCalledWith('STORE_PRIVATE_MARKETS', [[]]);
      }));
    });

    it('#mainInit', () => {
        expect(service.mainInit()).toBeFalsy();
    });

    it('logout', () => {
      expect(service.logout('')).toEqual(jasmine.any(Observable));
      expect(service.logout('', true)).toEqual(jasmine.any(Observable));
    });

    it('#handleLogoutNotification', () => {
        expect(service.handleLogoutNotification(true)).toBeFalsy();
    });

    describe('loginSequence', () => {
        it('#whith credentials, options and isUpgradedInShopUser', () => {
            const source = service.loginSequence({}, {}, true);
            source.subscribe(
                val => {
                    expect(val).toBeFalsy();
                }
            );
        });

        it('#whithout options and isUpgradedInShopUser', () => {
            const source = service.loginSequence({}, undefined, undefined);
            source.subscribe(
                val => {
                    expect(val).toBeFalsy();
                }
            );
        });
    });

    it('acceptTermsAndConditions', () => {
        const source = service.acceptTermsAndConditions();
        source.subscribe(
            val => {
                expect(val).toBeFalsy();
            });
    });

    describe('reLoginSequence', () => {
        it('with credentials & options', () => {
            const source = service.reLoginSequence({}, {});
            source.subscribe(
                val => {
                    expect(val).toBeFalsy();
                });
        });

        it('without credentials & options', () => {
            const source = service.reLoginSequence(undefined, undefined);
            source.subscribe(
                val => {
                    expect(val).toBeFalsy();
                }
            );
        });
    });

    it('handleBppLoginError', () => {
        service['handleBppLoginError']('error' as any);
        expect(userService.rejectProxyAuth).toHaveBeenCalled();
    });

  describe('reLoginBpp', () => {
    it('should return whenProxySession observable', fakeAsync(() => {
      userService.proxyPromiseResolved.and.returnValue(false);
      service.reLoginBpp().subscribe();
      tick();
      expect(sessionService.whenProxySession).toHaveBeenCalled();
    }));
    it('should trigger bppAuthSequence', fakeAsync(() => {
      spyOn(service, 'bppAuthSequence').and.returnValue(observableOf({} as any));
      userService.proxyPromiseResolved.and.returnValue(true);
      service.reLoginBpp().subscribe();
      tick();
      expect(service.bppAuthSequence).toHaveBeenCalled();
    }));
  });

  describe('reloginBppToCommand', () => {
    it('should register command for BPP_AUTH_SEQUENCE', fakeAsync(() => {
      userService.proxyPromiseResolved.and.returnValue(false);
      service['reloginBppToCommand']();
      tick();

      expect(commandService.register).toHaveBeenCalledWith('auth/bppAuthSequence', jasmine.any(Function));
      expect(sessionService.whenProxySession).toHaveBeenCalled();
    }));
  });

  describe('initOddsBoost', () => {
    it('should load odds boost module with tokens', fakeAsync(() => {
      cmsService.getOddsBoost.and.returnValue(observableOf({ enabled: true }));
      const res: any = {
        betBoosts: { data: [{}] }
      };
      service.initOddsBoost(res).subscribe();
      tick();
      expect(commandService.executeAsync).toHaveBeenCalledWith('INIT_ODDS_BOOST', [res.betBoosts.data]);
    }));

    it('should load odds boost module with empty array', fakeAsync(() => {
      cmsService.getOddsBoost.and.returnValue(observableOf({ enabled: true }));
      service.initOddsBoost({} as any).subscribe();
      tick();
      expect(commandService.executeAsync).toHaveBeenCalledWith('INIT_ODDS_BOOST', [[]]);
    }));

    it('should not load odds boost module', fakeAsync(() => {
      cmsService.getOddsBoost.and.returnValue(observableOf({ enabled: false }));
      service.initOddsBoost({} as any).subscribe();
      tick();
      expect(commandService.executeAsync).not.toHaveBeenCalled();
    }));

    it('should load odds boost module with empty array', fakeAsync(() => {
      cmsService.getOddsBoost.and.returnValue(observableOf({ enabled: true }));
      service.initOddsBoost().subscribe();
      tick();
      expect(commandService.executeAsync).toHaveBeenCalledWith('GET_ODDS_BOOST_TOKENS', [true]);
    }));
  });

  describe('handleBppLoginError', () => {
    it('awsService BPP Login=>Error with string error', () => {
      service['handleBppLoginError']('teststring' as any);
      expect(awsService.addAction).toHaveBeenCalledWith('BPP Login=>Error', { error: 'teststring' });
    });

    it('awsService BPP Login=>Error with object error', () => {
      service['handleBppLoginError']({ error: 'teststring' } as any);
      expect(awsService.addAction).toHaveBeenCalledWith('BPP Login=>Error', { error: 'teststring' });
    });
  });

  it('should call getOddspreference', () => {
    service['getOddspreference'](userService.bppToken);
    expect(service).toBeTruthy();
  });

  it('should call isTokenPossibleBet', () => {
    expect(service.isTokenPossibleBet('', '')).toBeFalse();
    expect(service.isTokenPossibleBet('ANY_POOLS', '')).toBeTrue();
    expect(service.isTokenPossibleBet('ANY', '')).toBeTrue();
    expect(service.isTokenPossibleBet('CLASS', '321')).toBeTrue();
    expect(service.isTokenPossibleBet('CATEGORY', '21')).toBeTrue();
  });

  it('should call isTokenPossibleBets', () => {
    expect(service.isTokenPossibleBets('', '')).toBeFalse();
    expect(service.isTokenPossibleBets('ANY', '')).toBeTrue();
    expect(service.isTokenPossibleBets('ANY_POOLS', '')).toBeTrue();
    expect(service.isTokenPossibleBets('CLASS', '321')).toBeTrue();
    expect(service.isTokenPossibleBets('CLASS', '223')).toBeTrue();
    expect(service.isTokenPossibleBets('CATEGORY', '21')).toBeTrue();
  });

  it('should call tokenPossibleBetCheck', () => {
    spyOn(service,'isTokenPossibleBet').and.returnValue(true);
    let freeBet = {
        freebetOfferType: 'SGL',
        freebetOfferCategories: undefined,
        tokenPossibleBet: {
          inPlay: 'N',
          betLevel: "ANY_POOLS",
          betId: ''
        }
      }
    service.tokenPossibleBetCheck(freeBet);
    expect(service.toteFreeBets.length).toEqual(1);

    freeBet = {
      freebetOfferType: 'SGL',
      freebetOfferCategories: {
        freebetOfferCategory: 'Bet Pack'
      },
      tokenPossibleBet: {
        inPlay: 'N',
        betLevel: "ANY_POOLS",
        betId: ''
      }
   }
   service.tokenPossibleBetCheck(freeBet);
   expect(service.toteBetPacks.length).toEqual(1);
  
   freeBet = {
    freebetOfferType: 'SGL',
    freebetOfferCategories: {
      freebetOfferCategory: 'Bet Pack1'
    },
    tokenPossibleBet: {
      inPlay: 'N',
      betLevel: "ANY_POOLS",
      betId: ''
    }
  }
  service.tokenPossibleBetCheck(freeBet);
  expect(service.toteFreeBets.length).toEqual(2);
  });

  it('should call tokenPossibleBetsCheck', () => {
    spyOn(service,'isTokenPossibleBets').and.returnValue(true);
    let freeBet = {
        freebetOfferType: 'SGL',
        freebetOfferCategories: undefined,
        tokenPossibleBet: {
          inPlay: 'N',
          betLevel: "ANY_POOLS",
          betId: ''
        },
        tokenPossibleBets: [
          {
            inPlay: 'N',
            betLevel: "ANY_POOLS",
            betId: ''
        }]
      }
    service.tokenPossibleBetsCheck(freeBet);
    expect(service.toteFreeBets.length).toEqual(1);

    freeBet = {
      freebetOfferType: 'SGL',
      freebetOfferCategories: undefined,
      tokenPossibleBet: {
        inPlay: 'N',
        betLevel: "ANY_POOLS",
        betId: ''
      },
      tokenPossibleBets: [
        {
          inPlay: 'N',
          betLevel: "ANY_POOLS",
          betId: ''
      },
      {
        inPlay: 'N',
        betLevel: "ANY",
        betId: ''
    }]
    }
    service.tokenPossibleBetsCheck(freeBet);
    expect(service.toteFreeBets.length).toEqual(2);

    freeBet = {
      freebetOfferType: 'SGL',
      freebetOfferCategories: {
        freebetOfferCategory: 'Bet Pack'
      },
      tokenPossibleBet: {
        inPlay: 'N',
        betLevel: "ANY_POOLS",
        betId: ''
      },
      tokenPossibleBets: [
        {
          inPlay: 'N',
          betLevel: "ANY_POOLS",
          betId: ''
      },
      {
        inPlay: 'N',
        betLevel: "ANY",
        betId: ''
    }]
    }
  service.tokenPossibleBetsCheck(freeBet);
  expect(service.toteBetPacks.length).toEqual(1);

  freeBet = {
    freebetOfferType: 'SGL',
    freebetOfferCategories: {
      freebetOfferCategory: 'Bet Pack1'
    },
    tokenPossibleBet: {
      inPlay: 'N',
      betLevel: "ANY_POOLS",
      betId: ''
    },
    tokenPossibleBets: [
      {
        inPlay: 'N',
        betLevel: "ANY_POOLS",
        betId: ''
    },
    {
      inPlay: 'N',
      betLevel: "ANY",
      betId: ''
  }]
  }
    service.tokenPossibleBetsCheck(freeBet);
    expect(service.toteFreeBets.length).toEqual(3);
  })
});
