import { of as observableOf, asyncScheduler, Subject, throwError } from 'rxjs';
import { HttpHeaders, HttpParams } from '@angular/common/http';
import { fakeAsync, tick } from '@angular/core/testing';

import {
  IBetsRequest,
  IBppRequest,
  ICashoutBetRequest,
  IMatchDayRewardsParamsRequest,
  IFreeBetOfferRequest,
  IGetVideoStreamRequest,
  IOfferBet,
  IReadBetRequest,
  IRequestTransFreebetTrigger,
  IRequestTransGetBetDetail,
  IRequestTransGetBetDetails,
  IRequestTransGetBetsPlaced,
  IRequestTransPoolGetDetail,
  IRequestTransBetpackTrigger
} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { BppProvidersService } from '@app/bpp/services/bppProviders/bpp-providers.service';
import environment from '@environment/oxygenEnvConfig';
import { BETSREQUESTDATA } from './bpp-providers.mock';

describe('BppProvidersService', () => {
  let service: BppProvidersService, proxyHeadersServiceStub, httpServiceStub;
  let successHandler;
  let bppCacheService;
  let deviceService;

  const tokenHeader = '12345';
  const newBppToken = 'newBppToken';

  beforeEach(() => {
    bppCacheService = {
      cachedFreebetsResponce: {},
      processFreebetsResponce: jasmine.createSpy('processFreebetsResponce').and.callFake((response) => response.body),
      setupCacheRemoveLogic: jasmine.createSpy('setupCacheRemoveLogic')
    };
    deviceService = {
      freeBetChannel: 'M'
    };
    proxyHeadersServiceStub = {
      generateBppAuthHeaders: jasmine.createSpy('generateBppAuthHeaders').and.returnValue(tokenHeader)
    };

    httpServiceStub = {
      get: jasmine.createSpy('httpGet').and.returnValue(observableOf(null)),
      post: jasmine.createSpy('httpPost').and.returnValue(observableOf(null)),
      put: jasmine.createSpy('httpPut').and.returnValue(observableOf(null))
    };

    successHandler = jasmine.createSpy('successHandler');

    service = new BppProvidersService(bppCacheService, proxyHeadersServiceStub, httpServiceStub, deviceService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('endpoint should be initialized', () => {
    expect(service.BPP_ENDPOINT).toBe(environment.BPP_ENDPOINT);
  });

  it('should build bet', fakeAsync(() => {
    const body: IBetsRequest = {
      betslip: {
        documentId: '123',
        clientUserAgent: 'Chrome',
        stake: {
          currencyRef: {
            id: '123'
          }
        },
        slipPlacement: {
          ipAddress: '127.0.0.0',
          channelRef: {
            id: '123'
          }
        },
        betRef: [{
          documentId: '123',
        }],
      },
      bet: [
        {
          documentId: '123',
          betTypeRef: {
            id: '123'
          },
          stake: {
            currencyRef: {
              id: '123'
            },
          },
          lines: {
            number: 1
          },
          legRef: [
            {
              documentId: '123',
              ordering: 'ASC'
            }
          ]
        }
      ],
    };
    const response = {
      body: {
        betslip: [],
        bet: [],
        leg: [],
        betError: [],
        errs: []
      }
    };

    httpServiceStub.post.and.returnValue(observableOf(response));

    service.buildBet(body).subscribe(successHandler);
    tick();

    expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/v1/buildBet`, body,
      jasmine.objectContaining({
        headers: null
      })
    );
    expect(successHandler).toHaveBeenCalledWith(response.body);
  }));

  it('should build bet logged', fakeAsync(() => {
    const body: IBetsRequest = {
      betslip: {
        documentId: '123',
        clientUserAgent: 'Chrome',
        stake: {
          currencyRef: {
            id: '123'
          }
        },
        slipPlacement: {
          ipAddress: '127.0.0.0',
          channelRef: {
            id: '123'
          }
        },
        betRef: [{
          documentId: '123',
        }],
      },
      bet: [
        {
          documentId: '123',
          betTypeRef: {
            id: '123'
          },
          stake: {
            currencyRef: {
              id: '123'
            },
          },
          lines: {
            number: 1
          },
          legRef: [
            {
              documentId: '123',
              ordering: 'ASC'
            }
          ]
        }
      ],
    };
    const response = {
      body: {
        betslip: [],
        bet: [],
        leg: [],
        betError: [],
        errs: []
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.post.and.returnValue(observableOf(response));

    service.buildBetLogged(body).subscribe(successHandler);
    tick();

    expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/v1/buildBet`, body,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should place bet', fakeAsync(() => {
    const body: IBetsRequest = {
      betslip: {
        documentId: '123',
        clientUserAgent: 'Chrome',
        stake: {
          currencyRef: {
            id: '123'
          }
        },
        slipPlacement: {
          ipAddress: '127.0.0.0',
          channelRef: {
            id: '123'
          }
        },
        betRef: [{
          documentId: '123',
        }],
      },
      bet: [
        {
          documentId: '123',
          betTypeRef: {
            id: '123'
          },
          stake: {
            currencyRef: {
              id: '123'
            },
          },
          lines: {
            number: 1
          },
          legRef: [
            {
              documentId: '123',
              ordering: 'ASC'
            }
          ]
        }
      ],
    };
    const response = {
      body: {
        betslip: [],
        bet: [],
        leg: [],
        betError: [],
        errs: []
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.post.and.returnValue(observableOf(response));

    service.placeBet(body).subscribe(successHandler);
    tick();

    expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/v1/placeBet`, body,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('random fail', fakeAsync(() => {
    const body: IBetsRequest = {
      betslip: {
        documentId: '123',
        clientUserAgent: 'Chrome',
        stake: {
          currencyRef: {
            id: '123'
          }
        },
        slipPlacement: {
          ipAddress: '127.0.0.0',
          channelRef: {
            id: '123'
          }
        },
        betRef: [{
          documentId: '123',
        }],
      },
      bet: [
      ],
    };
    service.placeBet(body).subscribe(() => { }, () => { });
    tick();
    expect(httpServiceStub.post).not.toHaveBeenCalled();
  }));

  it('should place pool bet', fakeAsync(() => {
    const body: IBetsRequest = {
      betslip: {
        documentId: '123',
        clientUserAgent: 'Chrome',
        stake: {
          currencyRef: {
            id: '123'
          }
        },
        slipPlacement: {
          ipAddress: '127.0.0.0',
          channelRef: {
            id: '123'
          }
        },
        betRef: [{
          documentId: '123',
        }],
      },
      bet: [
        {
          documentId: '123',
          betTypeRef: {
            id: '123'
          },
          stake: {
            currencyRef: {
              id: '123'
            },
          },
          lines: {
            number: 1
          },
          legRef: [
            {
              documentId: '123',
              ordering: 'ASC'
            }
          ]
        }
      ],
    };
    const response = {
      body: {
        betslip: [],
        bet: [],
        leg: [],
        betError: [],
        errs: []
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.post.and.returnValue(observableOf(response));

    service.placePoolBet(body).subscribe(successHandler);
    tick();

    expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/v2/placePoolBet`, body,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should place win pool bet', fakeAsync(() => {
    const body: IBetsRequest = {
      betslip: {
        documentId: '123',
        clientUserAgent: 'Chrome',
        stake: {
          currencyRef: {
            id: '123'
          }
        },
        slipPlacement: {
          ipAddress: '127.0.0.0',
          channelRef: {
            id: '123'
          }
        },
        betRef: [{
          documentId: '123',
        }],
      },
      bet: [
        {
          documentId: '123',
          betTypeRef: {
            id: '123'
          },
          stake: {
            currencyRef: {
              id: '123'
            },
          },
          lines: {
            number: 1
          },
          legRef: [
            {
              documentId: '123',
              ordering: 'ASC'
            }
          ]
        }
      ],
    };
    const response = {
      body: {
        betslip: [],
        bet: [],
        leg: [],
        betError: [],
        errs: []
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.post.and.returnValue(observableOf(response));

    service.placeWinPoolBet(body).subscribe(successHandler);
    tick();

    expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/v1/placeWinPoolBet`, body,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should cashout bet', fakeAsync(() => {
    const body: ICashoutBetRequest = {
      betRef: {
        provider: 'qwerty',
        id: '123'
      },
      channelRef: {
        id: '123'
      },
      cashoutValue: {
        value: '123'
      }
    };
    const response = {
      body: {
        betslip: [],
        bet: [],
        leg: [],
        betError: [],
        errs: []
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.post.and.returnValue(observableOf(response));

    service.cashoutBet(body).subscribe(successHandler);
    tick();

    expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/v1/cashoutBet`, body,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should read bet', fakeAsync(() => {
    const body: IReadBetRequest = {
      betRef: [{
        provider: 'qwerty',
        id: '123'
      }]
    };
    const response = {
      body: {
        betslip: [],
        bet: [],
        leg: [],
        betError: [],
        errs: []
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.post.and.returnValue(observableOf(response));

    service.readBet(body).subscribe(successHandler);
    tick();

    expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/v1/readBet`, body,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should offer bet', fakeAsync(() => {
    const body: IOfferBet = {
      offerBetAction: [{
        betRef: {
          provider: 'qwerty',
          id: '123'
        },
        offerBetActionRef: {
          id: '123'
        }
      }]
    };
    const response = {
      body: {
        betslip: [],
        bet: [],
        leg: [],
        betError: [],
        errs: []
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.post.and.returnValue(observableOf(response));

    service.offerBet(body).subscribe(successHandler);
    tick();

    expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/v1/offerBet`, body,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  describe('#getBetHistory', () => {
    let params;
    let response;

    beforeEach(() => {
      params = {
        returnAvaliableFilters: 'qwerty'
      } as any;
      response = {
        body: {
          bet: []
        },
        headers: {
          get: jasmine.createSpy('get').and.returnValue(newBppToken)
        }
      };
    });
    it('should get bet history', fakeAsync(() => {
      httpServiceStub.get.and.returnValue(observableOf(response));

      service.getBetHistory(params).subscribe(successHandler);
      tick();

      expect(httpServiceStub.get).toHaveBeenCalledWith(
        `${environment.BPP_ENDPOINT}/accountHistory?returnAvaliableFilters=qwerty`,
        jasmine.objectContaining({
          headers: jasmine.any(HttpHeaders)
        })
      );
      expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
    }));

    it('should get betCount', fakeAsync(() => {
      response = {
        body: {
          betCounter: '10'
        },
        headers: {
          get: jasmine.createSpy('get').and.returnValue(newBppToken)
        }
      };

      httpServiceStub.get.and.returnValue(observableOf(response));

      service.getBetHistory(params, '/count').subscribe(successHandler);
      tick();

      expect(httpServiceStub.get).toHaveBeenCalledWith(
        `${environment.BPP_ENDPOINT}/accountHistory/count?returnAvaliableFilters=qwerty`,
        jasmine.objectContaining({
          headers: jasmine.any(HttpHeaders)
        })
      );
      expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
    }));
  });

  it('should get bet detail', fakeAsync(() => {
    const params: IRequestTransGetBetDetail = {
      betId: ['1', '2', '3']
    };
    const response = {
      body: {
        response: {
          respTransGetBetDetail: {
            bet: []
          }
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.getBetDetail(params).subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/getBetDetail/betslip`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders),
        params: jasmine.any(HttpParams)
      })
    );
    expect(httpServiceStub.get.calls.argsFor(0)[1].params.toString())
      .toEqual('betId=1&betId=2&betId=3');
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should get pool bet detail', fakeAsync(() => {
    const params: IRequestTransPoolGetDetail = {
      poolBetId: '12345'
    };
    const response = {
      body: {
        response: {
          poolBetDetail: {
            poolBet: []
          }
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.getPoolBetDetail(params).subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/getPoolBetDetail`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders),
        params: jasmine.any(HttpParams)
      })
    );
    expect(httpServiceStub.get.calls.argsFor(0)[1].params.toString())
      .toEqual('poolBetId=12345');
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should get bet details', fakeAsync(() => {
    const params: IRequestTransGetBetDetails = {
      cashoutBets: 'qwerty',
      status: 'qwerty',
      returnPartialCashoutDetails: 'qwerty',
      filter: 'qwerty'
    };
    const response = {
      body: {
        response: {
          respTransGetBetDetails: {
            bets: []
          }
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.getBetDetails(params).subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/getBetDetails`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders),
        params: jasmine.any(HttpParams)
      })
    );
    expect(httpServiceStub.get.calls.argsFor(0)[1].params.toString())
      .toEqual('cashoutBets=qwerty&status=qwerty&returnPartialCashoutDetails=qwerty&filter=qwerty');
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should get bets placed', fakeAsync(() => {
    const params: IRequestTransGetBetsPlaced = {
      request: {
        reqClientAuth: {
          returnToken: 'Y',
          user: 'qwerty',
          password: 'qwerty'
        },
        reqTransGetBetsPlaced: {
          token: '12345',
          eventId: '12345'
        }
      }
    };
    const response = {
      body: {
        response: {
          respTransGetBetsPlaced: {
            bets: []
          }
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.getBetsPlaced(params).subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/getBetsPlaced`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders),
        params: jasmine.any(HttpParams)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should call be made for euros', fakeAsync(() => {
    const params: IMatchDayRewardsParamsRequest = {
      returnOffers: 'Y',
      returnFreebetTokens: 'N'
    };
    const response = {
      body: {
        response: {
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.getMatchDayRewardsWithBadges(params).subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/matchDayRewardsWithBadges`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders),
        params: jasmine.any(HttpParams)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should call be made for euros default', fakeAsync(() => {
    const response = {
      body: {
        response: {
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.getMatchDayRewardsWithOutBadges().subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/matchDayRewardsWithOutBadges`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders),
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should call be made for euroHowItWorks', fakeAsync(() => {
    const response = {
      body: {
        response: {
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.getHowItWorksData().subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/howItWorks`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders),
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should free bet offer', fakeAsync(() => {
    const params: IFreeBetOfferRequest = {
      freebetOfferId: '12345'
    };
    const response = {
      body: {
        freebetOffer: []
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.freeBetOffer(params).subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/freebetOffers`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders),
        params: jasmine.any(HttpParams)
      })
    );
    expect(httpServiceStub.get.calls.argsFor(0)[1].params.toString())
      .toEqual('freebetOfferId=12345');
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should get free bet trigger', fakeAsync(() => {
    const params: IRequestTransFreebetTrigger = {
      value: 'qwerty',
      source: 'qwerty'
    };
    const response = {
      body: {
        response: {
          freebetResponseModel: {
            freebetCalledTrigger: {}
          }
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.freebetTrigger(params).subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/freebetTrigger`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders),
        params: jasmine.any(HttpParams)
      })
    );
    expect(httpServiceStub.get.calls.argsFor(0)[1].params.toString())
      .toEqual('value=qwerty&source=qwerty');
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should get bet pack', fakeAsync(() => {
    const params: IRequestTransBetpackTrigger = {
      value: 'qwerty',
      source: 'qwerty',
      extTriggerId: 'qwerty'
    };
    const response = {
      body: {
        response: {
          freebetResponseModel: {
            freebetCalledTrigger: {}
          }
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.betPackTrigger(params).subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/betPackTrigger`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders),
        params: jasmine.any(HttpParams)
      })
    );
    expect(httpServiceStub.get.calls.argsFor(0)[1].params.toString())
      .toEqual('value=qwerty&source=qwerty&extTriggerId=qwerty');
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should video stream', fakeAsync(() => {
    const params: IGetVideoStreamRequest = {
      requestModel: {
        accountVideoStreams: {
          streamDetails: {
            startTime: '12345',
            endTime: '12345',
            streamId: '12345',
            providerName: 'qwerty'
          },
          eventId: '12345',
          token: '12345',
          error: {
            accountFailureCode: 'qwerty',
            externalId: 'qwerty',
            accountFailureKey: 'qwerty',
            accountFailureReason: 'qwerty',
            accountFailureDebug: 'qwerty',
            accountFailureElement: [{
              value: 'qwerty'
            }],
            accountFailureInfo: [{
              name: 'qwerty',
              value: 'qwerty'
            }],
            accountFailureSpecifics: {
              content: ['a', 'b', 'c']
            }
          }
        },
        clientAuthModel: {
          returnToken: 'Y',
          user: 'qwerty',
          password: 'qwerty'
        }
      }
    };
    const response = {
      body: {
        result: {
          successModel: {
            eventId: '12345'
          }
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.videoStream(params).subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/videoStream`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders),
        params: jasmine.any(HttpParams)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should call all freebets', () => {
    const response = {
      body: {
        response: {
          model: {}
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response, asyncScheduler));

    service.allAccountFreebets('SPORTS').subscribe(successHandler);

    expect(httpServiceStub.get).toHaveBeenCalledWith(

      `${environment.BPP_ENDPOINT}/accountFreebets?channel=${deviceService.freeBetChannel}`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(service.getFreebetsRequest).toBeDefined();
  });

  it('should not be called twice', () => {
    (service.getFreebetsRequest as any) = new Subject();

    // secondCall
    service.allAccountFreebets('SPORTS');

    // expect to get present cached observable from previous call
    expect(httpServiceStub.get).not.toHaveBeenCalled();
  });


  it('should call all freebets and get cached response data', fakeAsync(() => {
    const cachedResponse: any = {
      body: {
        response: {
          model: {}
        }
      }
    };

    (service.getFreebetsRequest as any) = {};
    service['bppCacheService'].cachedFreebetsResponce = {
      SPORTS: cachedResponse.body
    };

    service.allAccountFreebets('SPORTS').subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).not.toHaveBeenCalled();

    expect(successHandler).toHaveBeenCalledWith(cachedResponse.body);
  }));

  it('should call error callback on getData call', () => {
    const errorResponse = {
      code: 401
    };
    const errorSpy = jasmine.createSpy();
    (service['getData'] as any) = jasmine.createSpy().and.returnValue(throwError(errorResponse))
      (service['getData'] as any).subscribe(successHandler, errorSpy);
    expect(errorSpy).toHaveBeenCalledWith(errorResponse);
  });

  it('should account freebets', fakeAsync(() => {
    const response = {
      body: {
        response: {
          model: {}
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    deviceService.freeBetChannel = 'M';

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.accountFreebets().subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(
      `${environment.BPP_ENDPOINT}/accountFreebets?freebetTokenType=SPORTS&channel=M`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should account freebetOffers', fakeAsync(() => {
    const response = {
      body: {
        response: {
          model: {}
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    deviceService.freeBetChannel = 'M';

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.accountFreebetsWithLimits().subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(
      `${environment.BPP_ENDPOINT}/accountFreebetsWithLimits?freebetTokenType=SPORTS&channel=M&returnOffers=Y&returnFreebetTokens=Y&returnQualifiedOffers=Y`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should call accountGetLimits', fakeAsync(() => {
    const response = {
      body: {
        response: {
          model: {}
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.accountGetLimits().subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(
      `${environment.BPP_ENDPOINT}/accountGetLimits?freebetTokenType=SPORTS&limitSort=BETPACK_DAILY_CUST_LIMIT`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should get betpacks offer data', fakeAsync(() => {
    const body = {
      freebetOfferIds: ['1','2'], 
      returnLimits: 'Y', 
      freeBetTriggerType: 'PURCHASE', 
      ignoreStartDate: 'Y'
    };
    const response = {
      body: {
        response: {
          respFreebetGetOffers: {
            freebetOffer: [
              {
                freebetOfferId: '37505'
              }
            ]
          }
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    deviceService.freeBetChannel = 'M';

    httpServiceStub.put.and.returnValue(observableOf(response));
    service.initialWSGetLimits(body).subscribe(successHandler);
    tick();

    expect(httpServiceStub.put).toHaveBeenCalledWith(
      `${environment.BPP_ENDPOINT}/freebetOffers`, body, { 
        observe: 'response', 
        withCredentials: true, 
        headers: null 
      });
    expect(successHandler).toHaveBeenCalledWith(response.body);
  }));

  it('should account offers', fakeAsync(() => {
    const response = {
      body: {
        response: {
          model: {}
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.accountOffers().subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(
      `${environment.BPP_ENDPOINT}/accountFreebets?freebetTokenType=SPORTS&channel=M&returnOffers=Y`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('should get private markets and setup cache remove', fakeAsync(() => {
    const response = {
      body: {
        response: {
          model: {}
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.privateMarkets().subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(
      `${environment.BPP_ENDPOINT}/accountFreebets?freebetTokenType=ACCESS`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
    expect(bppCacheService.setupCacheRemoveLogic).toHaveBeenCalled();
  }));

  it('should return allAccountFreebets observable is present for private markets', fakeAsync(() => {
    (service.getFreebetsRequest as any) = new Subject();

    service.privateMarkets();

    expect(httpServiceStub.get).not.toHaveBeenCalled();
  }));

  it('should return allAccountFreebets cached response if present for private markets', fakeAsync(() => {
    const cachedMarketsResponseMock = {};

    bppCacheService.cachedFreebetsResponce['ACCESS'] = cachedMarketsResponseMock;

    service.privateMarkets()
      .subscribe((data: any) => {
        expect(data).toEqual(cachedMarketsResponseMock);
      });

    expect(httpServiceStub.get).not.toHaveBeenCalled();
  }));

  it('should return allAccountFreebets observable is present for private markets', fakeAsync(() => {
    (service.getFreebetsRequest as any) = new Subject();

    service.privateMarkets();
    expect(httpServiceStub.get).not.toHaveBeenCalled();
  }));

  it('should get currency rates', fakeAsync(() => {
    const response = {
      body: {
        betslip: [],
        bet: [],
        leg: [],
        betError: [],
        errs: []
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.getCurrencyRates().subscribe(successHandler);

    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/currencies`,
      jasmine.objectContaining({
        headers: null
      })
    );
    expect(successHandler).toHaveBeenCalledWith(response.body);
  }));

  it('should get data', () => {
    const url = 'path/to/api',
      headers = null,
      params = null;

    service['getData'](url, headers, params);

    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/${url}`, {
      observe: 'response',
      withCredentials: true,
      headers: null,
      params: null
    });
  });

  it('should get response data', () => {
    const url = 'path/to/api', params = `a&b&c`;

    service['createHeaders'] = jasmine.createSpy().and.returnValue(`12345`);
    service['getResponseData'](url, params);

    expect(service['createHeaders']).toHaveBeenCalled();
    expect(httpServiceStub.get).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/${url}?${params}`, {
      observe: 'response',
      withCredentials: true,
      headers: `12345`
    });
  });

  it('should create headers', () => {
    const result = service['createHeaders']();

    expect(proxyHeadersServiceStub.generateBppAuthHeaders).toHaveBeenCalled();
    expect(result.get('token')).toEqual(tokenHeader);
  });

  it('should create get params', () => {
    const params1: IRequestTransGetBetDetails = {
      cashoutBets: 'qwerty',
      status: 'qwerty',
      returnPartialCashoutDetails: 'qwerty',
      filter: 'qwerty'
    },
      params2: IRequestTransPoolGetDetail = {
        poolBetId: '12345'
      };

    const result1 = service['createGetParams'](params1);
    const result2 = service['createGetParams'](params2);

    expect(result1.keys().length).toBe(4);
    expect(result2.keys().length).toBe(1);

    expect(result1.get('cashoutBets')).toBe(params1.cashoutBets);
    expect(result2.get('poolBetId')).toBe(params2.poolBetId);
  });

  it('should get encode params', () => {
    const params: IRequestTransGetBetDetails = {
      cashoutBets: 'qwerty',
      status: 'qwerty',
      returnPartialCashoutDetails: 'qwerty',
      filter: 'qwerty'
    };

    const result = service['getEncodeParams'](params);

    expect(result).toEqual(jasmine.any(String));
    expect((result.match(/&/g) || []).length).toBe(Object.keys(params).length - 1);
    expect(result.includes(Object.keys(params)[0])).toBeTruthy();
  });

  it('should post data', () => {
    const url = 'path/to/api',
      body: IBppRequest = {
        poolBetId: '12345'
      },
      headers = null;

    service['postData'](url, body, headers);

    expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/${url}`, body, {
      observe: 'response',
      withCredentials: true,
      headers: null
    });
  });

  it('should get accountOddsBoost', fakeAsync(() => {
    const response = {
      body: {
        response: {
          model: {}
        }
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.get.and.returnValue(observableOf(response));
    service.accountOddsBoost().subscribe(successHandler);
    tick();

    expect(httpServiceStub.get).toHaveBeenCalledWith(
      `${environment.BPP_ENDPOINT}/accountFreebets?freebetTokenType=BETBOOST`,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders),
        params: null
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  it('postData method should default headers', () => {
    service['postData']('', { poolBetId: '' });

    expect(httpServiceStub.post.calls.argsFor(0)[2]).toEqual({
      observe: 'response',
      withCredentials: true,
      headers: null
    });
  });

  it('should validateBet', fakeAsync(() => {
    const body: any = {};
    const response = {
      body: {
        bet: []
      },
      headers: {
        get: jasmine.createSpy('get').and.returnValue(newBppToken)
      }
    };

    httpServiceStub.post.and.returnValue(observableOf(response));

    service.validateBet(body).subscribe(successHandler);
    tick();

    expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/validateBet`, body,
      jasmine.objectContaining({
        headers: jasmine.any(HttpHeaders)
      })
    );
    expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
  }));

  afterEach(() => {
    service = null;
  });

  describe('buildbet or buildbetlogged on QuickBet', () => {
    it('should build bet', fakeAsync(() => {
      const body: IBetsRequest = BETSREQUESTDATA;
      const response = {
        body: {
          betslip: [],
          bet: [],
          leg: [],
          betError: [],
          errs: []
        },
        headers: {
          get: jasmine.createSpy('get').and.returnValue(newBppToken)
        }
      };

      httpServiceStub.post.and.returnValue(observableOf(response));

      service.quickBet(body, false).subscribe(successHandler);
      tick();

      expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/v1/buildBet`, body,
        jasmine.objectContaining({
          headers: null
        })
      );
      expect(successHandler).toHaveBeenCalledWith(response.body);
    }));

    it('should build bet when logged ', fakeAsync(() => {
      const body: IBetsRequest = {
        betslip: {
          documentId: '123',
          clientUserAgent: 'Chrome',
          stake: {
            currencyRef: {
              id: '123'
            }
          },
          slipPlacement: {
            ipAddress: '127.0.0.0',
            channelRef: {
              id: '123'
            }
          },
          betRef: [{
            documentId: '123',
          }],
        },
        bet: [
          {
            documentId: '123',
            betTypeRef: {
              id: '123'
            },
            stake: {
              currencyRef: {
                id: '123'
              },
            },
            lines: {
              number: 1
            },
            legRef: [
              {
                documentId: '123',
                ordering: 'ASC'
              }
            ]
          }
        ],
      };
      const response = {
        body: {
          betslip: [],
          bet: [],
          leg: [],
          betError: [],
          errs: []
        },
        headers: {
          get: jasmine.createSpy('get').and.returnValue(newBppToken)
        }
      };

      httpServiceStub.post.and.returnValue(observableOf(response));

      service.quickBet(body, true).subscribe(successHandler);
      tick();

      expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/v1/buildBet`, body,
        jasmine.objectContaining({
          headers: jasmine.any(HttpHeaders)
        })
      );
      expect(successHandler).toHaveBeenCalledWith({ ...response.body, token: newBppToken });
    }));
  });

  describe('lottoBuildBet or lottoBuildBetLogged', () => {
    it('should lotto build bet', fakeAsync(() => {
      const body: IBetsRequest = BETSREQUESTDATA;
      const response = {
        body: {
          betslip: [],
          bet: [],
          leg: [],
          betError: [],
          errs: []
        },
        headers: {
          get: jasmine.createSpy('get').and.returnValue(newBppToken)
        }
      };

      httpServiceStub.post.and.returnValue(observableOf(response));

      service.lottoBuildBet(body).subscribe(successHandler);
      tick();

      expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/v1/lotto/buildBet`, body,
        jasmine.objectContaining({
          headers: null
        })
      );
      expect(successHandler).toHaveBeenCalledWith(response.body);
    }));

    it('should lotto build bet when logged ', fakeAsync(() => {
      const body: IBetsRequest = {
        betslip: {
          documentId: '123',
          clientUserAgent: 'Chrome',
          stake: {
            currencyRef: {
              id: '123'
            }
          },
          slipPlacement: {
            ipAddress: '127.0.0.0',
            channelRef: {
              id: '123'
            }
          },
          betRef: [{
            documentId: '123',
          }],
        },
        bet: [
          {
            documentId: '123',
            betTypeRef: {
              id: '123'
            },
            stake: {
              currencyRef: {
                id: '123'
              },
            },
            lines: {
              number: 1
            },
            legRef: [
              {
                documentId: '123',
                ordering: 'ASC'
              }
            ]
          }
        ],
      };
      const response = {
        body: {
          betslip: [],
          bet: [],
          leg: [],
          betError: [],
          errs: []
        },
        headers: {
          get: jasmine.createSpy('get').and.returnValue(newBppToken)
        }
      };

      httpServiceStub.post.and.returnValue(observableOf(response));

      service.lottoBuildBetLogged(body).subscribe(successHandler);
      tick();

      expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/v1/lotto/buildBet`, body,
        jasmine.objectContaining({
          headers: jasmine.any(HttpHeaders)
        })
      );
      expect(successHandler).toHaveBeenCalledWith({ ...response.body });
    }));
  });
});
