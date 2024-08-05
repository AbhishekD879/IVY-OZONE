import { IConstant } from '@core/services/models/constant.model';
import { Observable, of as observableOf, throwError } from 'rxjs';
import { fakeAsync, tick, discardPeriodicTasks } from '@angular/core/testing';

import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { IError } from '@app/bpp/services/bpp/bpp.model';
import { IResponseTransGetBetDetail } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { ACTIONS } from '@lazy-modules/awsFirehose/constant/aws-firehose.constant';

describe('BPP Service', () => {
  let service: BppService,
    authServiceStub,
    infoDialogServiceStub,
    bppErrorServiceStub,
    awsStub,
    bppProvidersStub,
    userStub,
    deviceStub,
    response,
    data,
    mockError,
    successResponse,
    successReadBetResponse,
    request,
    cmsService,
    pubSubService,
    maintenanceService,
    windowRefService;

  beforeEach(() => {
    infoDialogServiceStub = {
      openDialog: jasmine.createSpy(),
      openConnectionLostPopup: jasmine.createSpy(),
      openLogoutPopup: jasmine.createSpy('openLogoutPopup')
    };

    userStub = {
      status: true,
      set: jasmine.createSpy('set')
    };

    authServiceStub = {
      reLoginBpp: () => {
        return observableOf('testResponse');
      },
      logout: jasmine.createSpy('logout')
    };

    bppProvidersStub = {
      getBetDetail: jasmine.createSpy('getBetDetail').and.returnValue(observableOf(response)),
      getBetHistory: jasmine.createSpy('getBetHistory').and.returnValue(observableOf(response)),
      placeBet: () => {
        return observableOf(response);
      },
      buildBet: () => {
        return observableOf(response);
      },
      buildBetLogged: () => {
        return observableOf(response);
      }
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({ BalanceUpdate: {},isOnlineFallback:{enabled:false}}))
    };

    pubSubService = {
      publish: jasmine.createSpy(),
      API: {
        IMPLICIT_BALANCE_REFRESH: 'IMPLICIT_BALANCE_REFRESH'
      }
    };

    bppErrorServiceStub = jasmine.createSpyObj('bppErrorServiceSpy', ['showPopup', 'errorHandler']);
    awsStub = jasmine.createSpyObj('awsSpy', ['addAction']);
    awsStub.API = ACTIONS;

    deviceStub = {
      isOnline: () => true,
      parsedUA: 'test',
      isWrapper: false
    };

    windowRefService = {
      nativeWindow: {
        navigator: {
          onLine: true
        }
      }
    } as any

    maintenanceService = {
      checkForMaintenance: jasmine.createSpy('checkForMaintenance').and.returnValue(observableOf(null))
    };

    response = { betError: [{ subErrorCode: 'DUPLICATED_BET' }] };
    successResponse = {
      betslip: {},
      betError: [{
        code: 'BET_ERROR',
        subErrorCode: 'STAKE_TOO_HIGH',
        betRef: [{ documentId: '1' }]
      }, {
        code: 'CHANGE_ERROR',
        subErrorCode: 'PRICE_CHANGED',
        errorDesc: 'price has changed',
        betRef: [{ documentId: '1' }],
        outcomeRef: { id: '933775583' }
      }],
      bet: [{
        leg: [{
          sportsLeg: {
            legPart: [{
              outcomeRef: {
                id: '933775583',
                marketId: '122935752',
                eventId: '123123'
              }
            }],
          }
        }],
        betTypeRef: { id: 'SGL' }
      }],
      bets: [{
        betTypeRef: { id: '1111' }
      }]
    };
    successReadBetResponse = {
      bet: [{
        betTypeRef: { id: 'SGL' },
        leg: [{
          sportsLeg: {
            legPart: [{
              outcomeRef: {
                id: '933775583',
                marketId: '122935752',
                eventId: '123123'
              }
            }]
          }
        }],
      }],
      betError: successResponse.betError,
    };

    mockError = {
      data: { status: 'UNAUTHORIZED_ACCESS' },
      error: { status: '' }
    };

    data = { betId: ['1', '2', '3'] };
    request = {
      bet: [
        { betTypeRef: { id: 'DBL' }, },
        { betTypeRef: { id: 'TBL' }, },
      ],
      betslip: {},
      leg: [
        { sportsLeg: {
            legPart: [{ outcomeRef: {id: '938155866'} }]
          }},
        { sportsLeg: {
            legPart: [{ outcomeRef: {id: '937912127'} }]
          }},
        { sportsLeg: {
            legPart: [{ outcomeRef: {id: '938160870'} }]
          }},
      ]
    };

    spyOn(console, 'warn');

    service = new BppService(
      authServiceStub,
      infoDialogServiceStub,
      bppErrorServiceStub,
      awsStub,
      bppProvidersStub,
      userStub,
      deviceStub,
      cmsService,
      pubSubService,
      maintenanceService,
      windowRefService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('should test bpp not placeOrBuildBet request', fakeAsync(() => {
    service.send('getBetDetail', data).subscribe(() => {}, () => {});
    expect(bppProvidersStub.getBetDetail).toHaveBeenCalledWith(data, undefined);
    expect(awsStub.addAction).not.toHaveBeenCalled();
  }));

  it('should test bpp request with url', fakeAsync(() => {
    service.send('getBetHistory', data, '/count').subscribe(() => {}, () => {});
    expect(bppProvidersStub.getBetHistory).toHaveBeenCalledWith(data, '/count');
  }));

  it('should test bpp request without url', fakeAsync(() => {
    service.send('getBetHistory', data).subscribe(() => {}, () => {});
    expect(bppProvidersStub.getBetHistory).toHaveBeenCalledWith(data, undefined);
  }));

  it('should test bpp request with incorrect provider', fakeAsync(() => {
    service.send('incorrectService', data).subscribe(() => {}, () => {});
    tick();
    expect(console.warn).toHaveBeenCalledWith('BPP service with name incorrectService does not exist.');
  }));

  it('trackAction with service name - ReadBet, should send bet data without leg property,' +
    'not changing response object', () => {
    service['trackAction']('success', 'readBet', request, successReadBetResponse);
    expect(awsStub.addAction).toHaveBeenCalledWith('ReadBetSuccess', jasmine.objectContaining({
      bet: [
        {
          betTypeRef: {
            id: 'SGL'
          }
        }
      ]
    }));
    expect(successReadBetResponse.bet[0].leg).toBeDefined();
  });

  it('trackAction with service name - buildBet', () => {
    service['trackAction']('success', 'buildBet', request, successReadBetResponse);
    expect(awsStub.addAction).toHaveBeenCalledWith('BuildBetSuccess', jasmine.any(Object));
  });

  it('trackAction with service name - buildBetLogged', () => {
    service['trackAction']('success', 'buildBetLogged', request, successReadBetResponse);
    expect(awsStub.addAction).toHaveBeenCalledWith('BuildBetSuccess', jasmine.any(Object));
  });

  it('trackAction with service name - buildComplexLegs', () => {
    service['trackAction']('success', 'buildComplexLegs', request, successReadBetResponse);
    expect(awsStub.addAction).toHaveBeenCalledWith('BuildBetSuccess', jasmine.any(Object));
  });

  it('trackAction with no service name and action', () => {
    service['trackAction'](undefined, undefined, request, successReadBetResponse);
    expect(awsStub.addAction).not.toHaveBeenCalled();
  });

  it('getBetErrors', () => {
    const analyticsParams: IConstant = {};
    service['getBetErrors'](successReadBetResponse.betError, analyticsParams);
    expect(analyticsParams).toEqual(jasmine.objectContaining(
      { subErrorCode: ['STAKE_TOO_HIGH', 'PRICE_CHANGED'], errorCode: ['BET_ERROR', 'CHANGE_ERROR'] }));
  });

  it('should test bpp request sending offline', fakeAsync(() => {
    deviceStub.isOnline = () => false;
    service.send('getBetDetail', data).subscribe(() => {}, () => {});
    tick();
    expect(infoDialogServiceStub.openConnectionLostPopup).toHaveBeenCalled();
  }));

  it('should test bpp request with funds error', fakeAsync(() => {
    spyOn<any>(service, 'retryTrigger');
    spyOn<any>(service, 'implicitBalanceRefresh');

    response.betError[0].subErrorCode = 'EXTERNAL_FUNDS_UNAVAILABLE';

    service.send('placeBet', data).subscribe(() => {}, () => {});
    tick();
    expect(awsStub.addAction).toHaveBeenCalledWith('PlaceBetSuccess', jasmine.objectContaining({
      serviceName: 'placeBet',
      request: data,
      ...response
    }));
    expect(service['retryTrigger']).toHaveBeenCalled();
    expect(service['implicitBalanceRefresh']).toHaveBeenCalledWith('placeBet', false);
  }));

  it('should test bpp request with generic error', fakeAsync(() => {
    response.betError[0] = 'testError';

    service.send('placeBet', data).subscribe(() => {}, (error) => {
      console.warn(error);
    });
    tick();
    expect(console.warn).not.toHaveBeenCalledWith('testError');
  }));

  it('should test bpp success request as default promise', fakeAsync(() => {
    spyOn<any>(service, 'implicitBalanceRefresh');

    response = 'testResponse';
    service.send('placeBet', data).subscribe((resp) => {
      console.warn(resp);
    });
    tick();
    expect(console.warn).toHaveBeenCalledWith('testResponse');
    expect(service['implicitBalanceRefresh']).toHaveBeenCalledWith('placeBet', true);
  }));

  it('should test bpp success request as observable', fakeAsync(() => {
    const successHandler = jasmine.createSpy('successHandler');
    spyOn<any>(service, 'implicitBalanceRefresh');

    response = 'testResponse';
    service.send('placeBet', data).subscribe(successHandler);
    tick();

    expect(successHandler).toHaveBeenCalledWith(response);
    expect(service['implicitBalanceRefresh']).toHaveBeenCalledWith('placeBet', true);
  }));

  it('should test bpp success request as observable with bet as parameter', fakeAsync(() => {
    const successHandler = jasmine.createSpy('successHandler');
    spyOn<any>(service, 'implicitBalanceRefresh');

    response = {bet: 'testResponse'};
    service.send('placeBet', data).subscribe(successHandler);
    tick(200);

    expect(successHandler).toHaveBeenCalledWith(response);
    expect(service['implicitBalanceRefresh']).toHaveBeenCalledWith('placeBet', true);
  }));

  it('should test bpp success request with new bppToken from response header and rewrite bppToken', fakeAsync(() => {
    bppProvidersStub.getBetDetail.and.returnValue(observableOf({ token: 'testToken' }));
    const successHandler = jasmine.createSpy('successHandler');

    (service.send('getBetDetail', {}) as Observable<IResponseTransGetBetDetail>).subscribe(successHandler);
    tick();

    expect(successHandler).toHaveBeenCalledWith({ token: 'testToken' });
    expect(userStub.set).toHaveBeenCalledWith({ bppToken: 'testToken' });
  }));

  it('should test bpp success request as observable without new bppToken', fakeAsync(() => {
    bppProvidersStub.getBetDetail.and.returnValue(observableOf({}));
    const successHandler = jasmine.createSpy('successHandler');

    (service.send('getBetDetail', {}) as Observable<IResponseTransGetBetDetail>).subscribe(successHandler);
    tick();

    expect(successHandler).toHaveBeenCalledWith({});
    expect(userStub.set).not.toHaveBeenCalled();
  }));

  it('should test bpp request with bppProviders error response', fakeAsync(() => {
    spyOn<any>(service, 'retryTrigger');
    spyOn(bppProvidersStub, 'placeBet').and.callFake(() => {
      return throwError(new Error('Fake error'));
    });
    service.send('placeBet', data).subscribe((resp) => {
      console.warn(resp);
    });
    tick(service.BPP_RETRY_TIMEOUT);

    expect(awsStub.addAction).toHaveBeenCalledWith('PlaceBetError',
      jasmine.objectContaining({
        serviceName: 'placeBet',
        request: data
      }));
    expect(service['retryTrigger']).toHaveBeenCalled();
  }));

  it('should return observable', fakeAsync(() => {
    const successHandler = jasmine.createSpy('successHandler');
    const errorHandler = jasmine.createSpy('errorHandler');
    deviceStub.isOnline = () => false;
    service.send('placeBet', data).subscribe(successHandler, errorHandler);
    tick(service.BPP_RETRY_TIMEOUT);

    expect(successHandler).not.toHaveBeenCalled();
    expect(errorHandler).toHaveBeenCalled();
  }));

  it('should handle 4016 status code', fakeAsync(() => {
    const resp = { ...response },
      observerSpy = jasmine.createSpyObj('observer', ['next', 'error', 'complete']);

    response = { betError: [{ code: '4016' }] };

    spyOn(bppProvidersStub, 'placeBet').and.callFake(() => {
      return observableOf(response);
    });
    spyOn<any>(service, 'implicitBalanceRefresh');

    (service.send('placeBet', data) as Observable<IResponseTransGetBetDetail>).subscribe(
      (res: any) => {
        expect(observerSpy.error).toHaveBeenCalledWith(res.betError[0]);
        expect(observerSpy.complete).toHaveBeenCalled();
        expect(service['implicitBalanceRefresh']).toHaveBeenCalledWith('placeBet', false);
      },
      () => {}
    );
    tick();

    response = { ...resp };
  }));

  it('should test bpp error popup show flow', () => {
    service.showErrorPopup('testError');
    expect(bppErrorServiceStub.showPopup).toHaveBeenCalledWith('testError');
  });

  it('should test bpp error popup fail flow', () => {
    userStub.status = false;
    service.showErrorPopup('testError');
    expect(bppErrorServiceStub.showPopup).not.toHaveBeenCalled();

    userStub.status = true;
    deviceStub.isOnline = () => false;
    service.showErrorPopup('testError');
    expect(bppErrorServiceStub.showPopup).not.toHaveBeenCalled();
  });

  it('should bpp service retry method error', fakeAsync(() => {
    const errorSpy = jasmine.createSpy();
    spyOn(authServiceStub, 'reLoginBpp').and.returnValue(throwError('Fake error'));
    service['retry']('placeBet', data).subscribe(() => { }, errorSpy);
    expect(errorSpy).toHaveBeenCalledWith('Fake error');
  }));
  describe('#retry', () => {
    let observerSpy;

    beforeEach(() => {
      observerSpy = jasmine.createSpyObj('observer', ['next', 'error', 'complete']);
      spyOn(bppProvidersStub, 'buildBetLogged').and.callThrough();
      spyOn(bppProvidersStub, 'placeBet').and.callThrough();
      spyOn(authServiceStub, 'reLoginBpp').and.callThrough();
    });

    it('should pass successfully buildBetLogged ', fakeAsync(() => {
      service['retry']('buildBetLogged', data).subscribe(() => {
        expect(authServiceStub.reLoginBpp).toHaveBeenCalled();
        expect(bppProvidersStub.buildBetLogged).toHaveBeenCalledWith(data);
        expect(observerSpy.next).toHaveBeenCalledWith(response);
      });

      discardPeriodicTasks();
    }));

    it('should pass successfully placeBet ', fakeAsync(() => {
      service['retry']('placeBet', data).subscribe(() => {
        expect(authServiceStub.reLoginBpp).toHaveBeenCalled();
        expect(bppProvidersStub.placeBet).toHaveBeenCalledWith(data);
        expect(observerSpy.next).toHaveBeenCalledWith(response);
      });

      discardPeriodicTasks();
    }));
    it('should pass successfully placeBet for wrapper', fakeAsync(() => {
      deviceStub.isWrapper = true;

      service['retry']('placeBet', data).subscribe(() => {
        expect(authServiceStub.reLoginBpp).toHaveBeenCalled();
        expect(bppProvidersStub.placeBet).toHaveBeenCalledWith(data);
        expect(observerSpy.next).toHaveBeenCalledWith(response);
      });

      discardPeriodicTasks();
    }));

    it('should pass successfully buildBetLogged for wrapper', fakeAsync(() => {
      deviceStub.isWrapper = true;

      service['retry']('buildBetLogged', data).subscribe(() => {
        expect(authServiceStub.reLoginBpp).toHaveBeenCalled();
        expect(bppProvidersStub.buildBetLogged).toHaveBeenCalledWith(data);
        expect(observerSpy.next).toHaveBeenCalledWith(response);
      });

      discardPeriodicTasks();
    }));

    it('should handle failure of bpp service', fakeAsync(() => {
      const errorResponse = {
        code: 401
      };
      const successHandler = jasmine.createSpy('success');
      const errorHandler = jasmine.createSpy('error');

      authServiceStub.reLoginBpp.and.returnValue(observableOf(null));
      bppProvidersStub.getBetDetail.and.returnValue(throwError(errorResponse));

      service['retry']('getBetDetail').subscribe(successHandler, errorHandler);
      tick();

      expect(errorHandler).toHaveBeenCalledWith(errorResponse);
      expect(awsStub.addAction).toHaveBeenCalledWith('getBetDetailError', jasmine.any(Object));
    }));
  });

  describe('retryTrigger', () => {
    let observerSpy;

    beforeEach(() => {
      observerSpy = jasmine.createSpyObj('observer', ['next', 'error', 'complete']);
      spyOn(bppProvidersStub, 'placeBet').and.callThrough();
      spyOn(authServiceStub, 'reLoginBpp').and.callThrough();
    });

    it('should call awsService.addAction', () => {
      service['retryTrigger']('placeBet', data, mockError, observerSpy);
      expect(awsStub.addAction).toHaveBeenCalledWith('bppService=>retryTrigger()', {
        serviceName: 'placeBet',
        data: data,
        error: mockError
      });
    });

    it('should not perform retry if error is null', () => {
      service['retryTrigger']('placeBet', data, null, observerSpy);

      expect(observerSpy.error).toHaveBeenCalledWith(null);
      expect(bppProvidersStub.placeBet).not.toHaveBeenCalled();
    });

    it('should not perform retry if error does not have valid status', () => {
      const errorData = {
        error: {
          status: null
        },
        data: {
          status: ''
        }
      };

      service['retryTrigger']('placeBet', data, errorData, observerSpy);

      expect(observerSpy.error).toHaveBeenCalledWith(errorData);
      expect(bppProvidersStub.placeBet).not.toHaveBeenCalled();
    });

    describe('should fail', () => {

      it('should fail (called "error/complete" of provided observer', fakeAsync(() => {
        service['retryTrigger']('placeBet', data, 'testError' as any, observerSpy);

        expect(authServiceStub.reLoginBpp).not.toHaveBeenCalled();
        expect(bppProvidersStub.placeBet).not.toHaveBeenCalled();
        expect(maintenanceService.checkForMaintenance).not.toHaveBeenCalled();
        expect(observerSpy.error).toHaveBeenCalledWith('testError');
      }));

      it('should handle maintenance', () => {
        spyOn(service as any, 'isMaintenanceError').and.returnValue(true);

        service['retryTrigger']('placeBet', data, 'testError' as any, observerSpy);

        expect(maintenanceService.checkForMaintenance).toHaveBeenCalled();
      });

      it('should handle failure of bpp service retry', fakeAsync(() => {
        const errorData = {
          error: {
            status: 'EXTERNAL_FUNDS_UNAVAILABLE'
          },
          data: {
            status: ''
          }
        };
        const errorResponse = {
          code: 401
        };
        spyOn<any>(service, 'implicitBalanceRefresh');

        authServiceStub.reLoginBpp.and.returnValue(observableOf(null));
        bppProvidersStub.getBetDetail.and.returnValue(throwError(errorResponse));

        service['retryTrigger']('getBetDetail', null, errorData as IError, observerSpy);
        tick();

        expect(observerSpy.error).toHaveBeenCalledWith(errorData);
        expect(bppErrorServiceStub.errorHandler).toHaveBeenCalledWith(errorResponse);
        expect(service['implicitBalanceRefresh']).toHaveBeenCalledWith('getBetDetail', false);
      }));

      afterEach(() => {
        expect(observerSpy.next).not.toHaveBeenCalled();
        expect(observerSpy.complete).toHaveBeenCalled();
      });
    });
  });

  describe('buildBetTrack', () => {
    const analyticsParams = {
      response: {},
      request: {},
      errorCode: [],
      selectionIDs: [],
      subErrorCode: [],
      serviceName: 'buildBet'
    };
    it('should test buildBet success', fakeAsync(() => {
      analyticsParams.request = request;
      service['buildBetTrack'](true, successResponse, analyticsParams, 'buildBet');
      expect(awsStub.addAction).toHaveBeenCalledWith('buildBet', analyticsParams);
    }));

    it('should test buildBetLogged success', fakeAsync(() => {
      analyticsParams.serviceName = 'buildBetLogged';
      analyticsParams.request = request;
      service['buildBetTrack'](true, successResponse, analyticsParams, 'buildBetLogged');
      expect(awsStub.addAction).toHaveBeenCalledWith('buildBetLogged', analyticsParams);
    }));

    it('should test buildComplexLegs success', fakeAsync(() => {
      analyticsParams.serviceName = 'buildComplexLegs';
      analyticsParams.request = request;
      service['buildBetTrack'](true, successResponse, analyticsParams, 'buildComplexLegs');
      expect(awsStub.addAction).toHaveBeenCalledWith('buildComplexLegs', analyticsParams);
    }));

    it('should test buildComplexLegs on error', fakeAsync(() => {
      analyticsParams.serviceName = 'buildComplexLegs';
      analyticsParams.request = request;
      successResponse.complexLeg = undefined;
      service['buildBetTrack'](true, successResponse, analyticsParams, 'buildComplexLegs');
      expect(awsStub.addAction).toHaveBeenCalledWith('buildComplexLegs', analyticsParams);
    }));

    it('should test buildBet/buildBetLogged success with betError', fakeAsync(() => {
      const params = { response: {}, request: {}, errorCode: [], selectionIDs: [], subErrorCode: [], serviceName: 'buildBet' };
      params.response = successResponse;
      params.request = request;
      service['buildBetTrack'](true, successResponse, params, 'buildBet');
      expect(params.errorCode).toEqual(['BET_ERROR', 'CHANGE_ERROR']);
      expect(params.subErrorCode).toEqual(['STAKE_TOO_HIGH', 'PRICE_CHANGED']);
      expect(params.selectionIDs).toEqual(['938155866', '937912127', '938160870']);
      expect(awsStub.addAction).toHaveBeenCalledWith('buildBet', params);
    }));

    it('should test buildBet/buildBetLogged success with no betError & bet in response', fakeAsync(() => {
      successResponse.betError = undefined;
      successResponse.bet = undefined;
      analyticsParams.response = successResponse;
      analyticsParams.request = request;
      service['buildBetTrack'](false, successResponse, analyticsParams, 'buildBet');
      expect(awsStub.addAction).toHaveBeenCalledWith('buildBet', analyticsParams);
    }));

    it('should test buildBet/buildBetLogged success with betError without errorCode and subErrorCode', fakeAsync(() => {
      successResponse.betError = [{}];
      successResponse.bet = [{
        leg: [{
          sportsLeg: {
            legPart: [{
              outcomeRef: {
                marketId: undefined,
                eventId: undefined
              }
            }]
          }
        }]
      }];
      analyticsParams.response = successResponse;
      analyticsParams.request = request;
      service['buildBetTrack'](false, successResponse, analyticsParams, 'buildBet');
      expect(awsStub.addAction).toHaveBeenCalledWith('buildBet', analyticsParams);
    }));

    it('should test buildComplexLegs success response', fakeAsync(() => {
      analyticsParams.serviceName = 'buildComplexLegs';
      successResponse = { complexLeg: [{ outcomeCombiRef: { id: '111' } }] };
      analyticsParams.response = successResponse;
      analyticsParams.request = request;
      service['buildBetTrack'](false, successResponse, analyticsParams, 'buildComplexLegs');
      expect(awsStub.addAction).toHaveBeenCalledWith('buildComplexLegs', analyticsParams);
    }));

    it('should test buildBet success response without marketId/eventId', fakeAsync(() => {
      successResponse.bet[0].leg[0].sportsLeg.legPart[0].outcomeRef = [];
      analyticsParams.response = successResponse;
      analyticsParams.request = request;
      service['buildBetTrack'](true, successResponse, analyticsParams, 'buildBet');
      expect(awsStub.addAction).toHaveBeenCalledWith('buildBet', analyticsParams);
    }));

    it('should test buildBetTrack when there is no service name', fakeAsync(() => {
      analyticsParams.serviceName = 'doSmth';
      analyticsParams.request = request;
      service['buildBetTrack'](true, successResponse, analyticsParams, 'doSmth');
      expect(awsStub.addAction).toHaveBeenCalledWith('doSmth', analyticsParams);
    }));

    it('should test buildBetTrack &  when betErrors is an object', fakeAsync(() => {
      analyticsParams.serviceName = 'buildBet';
      analyticsParams.request = request;
      successResponse.betError = {
        code: 'BET_ERROR',
        subErrorCode: 'STAKE_TOO_HIGH'
      };
      service['buildBetTrack'](true, successResponse, analyticsParams, 'buildBet');
      expect(awsStub.addAction).toHaveBeenCalledWith('buildBet', analyticsParams);

      analyticsParams.serviceName = 'ReadBetSuccess';
      service['readBetTracked'](true, successResponse, analyticsParams, 'ReadBetSuccess');
      expect(awsStub.addAction).toHaveBeenCalledWith('ReadBetSuccess', analyticsParams);
    }));
  });

  describe('trackAction', () => {
    it('should handle defaul params', () => {
      service['trackAction'](undefined, undefined, {} as any, {} as any);
      expect(awsStub.addAction).not.toHaveBeenCalled();
    });

    it('should check for service name', () => {
      service['trackAction']('success', 'cashout', {} as any, {} as any);
      expect(awsStub.addAction).not.toHaveBeenCalled();
    });

    it('should check for service name', () => {
      // eslint-disable-next-line @typescript-eslint/no-shadow
      const request = {
        id: '123'
      } as any;
      const placeBetResponse = {
        name: 'test'
      } as any;
      const serviceName = 'placeBet';

      service['trackAction']('success', serviceName, request, placeBetResponse);
      expect(awsStub.addAction).toHaveBeenCalledWith('PlaceBetSuccess', jasmine.objectContaining({
        serviceName,
        request,
        name: placeBetResponse.name
      }));
    });
  });

  it('should send "betPlacementTimeoutError" on DUPLICATED_BET error', fakeAsync(() => {
    service.send('placeBet', {} as any).subscribe({
      error: error => {
        expect(error).toEqual('betPlacementTimeoutError');
      }
    });
    tick();
  }));

  describe('implicitBalanceRefresh', () => {
    it('should not call balance refresh if no system config BalanceUpdate', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ test: 'No balance' }));
      service['implicitBalanceRefresh']('placeBet', true);

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should not call balance refresh if success and no system config BalanceUpdate BppSuccess', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ BalanceUpdate: {} }));
      service['implicitBalanceRefresh']('placeBet', true);

      expect(pubSubService.publish).not.toHaveBeenCalled();

    });

    it('should not call balance refresh if success and provider name not matched', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ BalanceUpdate: { BppSuccess: ['readBet'] } }));
      service['implicitBalanceRefresh']('placeBet', true);

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should call balance refresh if success and provider name matched', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ BalanceUpdate: { BppSuccess: ['placeBet'] } }));
      service['implicitBalanceRefresh']('placeBet', true);

      expect(pubSubService.publish).toHaveBeenCalledWith('IMPLICIT_BALANCE_REFRESH');
    });

    it('should not call balance refresh if error and no system config BalanceUpdate BppError', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ BalanceUpdate: {} }));
      service['implicitBalanceRefresh']('placeBet', false);

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should not call balance refresh if error and provider name not matched', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ BalanceUpdate: { BppError: ['readBet'] } }));
      service['implicitBalanceRefresh']('placeBet', false);

      expect(pubSubService.publish).not.toHaveBeenCalled();
    });

    it('should call balance refresh if error and provider matched', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ BalanceUpdate: { BppError: ['placeBet'] } }));
      service['implicitBalanceRefresh']('placeBet', false);

      expect(pubSubService.publish).toHaveBeenCalledWith('IMPLICIT_BALANCE_REFRESH');
    });
  });

  describe('isMaintenanceError', () => {

    it('err with maintenance message should return true', () => {
      expect(service['isMaintenanceError']({error: {message: 'maintenance!'}} as any)).toBe(true);
      expect(service['isMaintenanceError']({error: {message: 'is Maintenance'}} as any)).toBe(true);
    });

    it('other errs should return false', () => {
      expect(service['isMaintenanceError']({error: {message: 'unknown error'}} as any)).toBeFalsy();
      expect(service['isMaintenanceError']({error: {}} as any)).toBeFalsy();
      expect(service['isMaintenanceError']({} as any)).toBeFalsy();
      expect(service['isMaintenanceError'](undefined as any)).toBeFalsy();
    });
  });

  describe('placeBetTracked', () => {
    let analyticsParams;

    beforeEach(() => {
      analyticsParams = {
        request: {
          bet: [{
            betTypeRef: { id: 'type1' }
          }],
          leg: [{
            sportsLeg: {
              legPart: [{
                outcomeRef: { id: 'outcome1' }
              }]
            }
          }, {}]
        }
      };
      response.betError = null;
      response.bet = [{
        leg: [{
          sportsLeg: {
            legPart: [{
              outcomeRef: { marketId: 'market1' }
            }, {
              outcomeRef: { eventId: 'event1' }
            }]
          }
        }, {}]
      }];
    });

    it('should set ids for types, selections, events and markets', () => {
      service['placeBetTracked'](true, response, analyticsParams, 'action');
      expect(analyticsParams.betTypeIDs).toEqual(['type1']);
      expect(analyticsParams.selectionIDs).toEqual(['outcome1']);
      expect(analyticsParams.eventIDs).toEqual(['event1']);
      expect(analyticsParams.marketIDs).toEqual(['market1']);
      expect(awsStub.addAction).toHaveBeenCalledWith('action', analyticsParams);
    });

    it('should set error code', () => {
      response.betError = [{ code: 'ERR1', subErrorCode: 'ERR2' }];
      service['placeBetTracked'](true, response, analyticsParams, 'action');
      expect(analyticsParams.errorCode).toEqual(['ERR1']);
      expect(analyticsParams.subErrorCode).toEqual(['ERR2']);
    });

    it('should not set ids for events and markets', () => {
      service['placeBetTracked'](false, response, analyticsParams, 'action');
      expect(analyticsParams.betTypeIDs).toEqual(['type1']);
      expect(analyticsParams.selectionIDs).toEqual(['outcome1']);
      expect(analyticsParams.eventIDs).toBeUndefined();
      expect(analyticsParams.marketIDs).toBeUndefined();
    });
  });

  describe('readBetTracked', () => {
    let analyticsParams;

    beforeEach(() => {
      analyticsParams = {};
      response.betError = null;
      response.bet = [{
        betTypeRef: { id: 'type1' },
        leg: [{
          sportsLeg: {
            legPart: [{
              outcomeRef: { id: 'outcome1', marketId: 'market1' }
            }, {
              outcomeRef: { id: 'outcome2', eventId: 'event1' }
            }]
          }
        }]
      }];
    });

    it('should not set ids', () => {
      service['readBetTracked'](false, response, analyticsParams, 'action');
      expect(analyticsParams.betTypeIDs).toBeUndefined();
      expect(analyticsParams.selectionIDs).toBeUndefined();
      expect(analyticsParams.eventIDs).toBeUndefined();
      expect(analyticsParams.marketIDs).toBeUndefined();
      expect(awsStub.addAction).toHaveBeenCalledWith('action', analyticsParams);
    });

    it('should set ids for types, selections, events and markets', () => {
      service['readBetTracked'](true, response, analyticsParams, 'action');
      expect(analyticsParams.betTypeIDs).toEqual(['type1']);
      expect(analyticsParams.selectionIDs).toEqual(['outcome1', 'outcome2']);
      expect(analyticsParams.eventIDs).toEqual(['event1']);
      expect(analyticsParams.marketIDs).toEqual(['market1']);
    });

    it('should set error code (betError as array)', () => {
      response.betError = [{ code: 'ERR1', subErrorCode: 'ERR2' }];
      service['readBetTracked'](true, response, analyticsParams, 'action');
      expect(analyticsParams.errorCode).toEqual(['ERR1']);
      expect(analyticsParams.subErrorCode).toEqual(['ERR2']);
    });

    it('should set error code (betError as object)', () => {
      response.betError = { code: 'ERR1', subErrorCode: 'ERR2' };
      service['readBetTracked'](true, response, analyticsParams, 'action');
      expect(analyticsParams.errorCode).toEqual(['ERR1']);
      expect(analyticsParams.subErrorCode).toEqual(['ERR2']);
    });
  });

  describe('isOnlineOrNot', () => {
    it('should take value from case 1', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ 'isOnlineFallback': { 'enabled': true } })),
      service['windowRef'] = {
        nativeWindow: {
          navigator: {
            onLine: true
          }
        }
      } as any
     
      expect(service.isOnlineOrNot()).toBe(true);
    });
    it('should take value from case 2', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({ 'isOnlineFallback': {} })),
      service['windowRef'] = {
        nativeWindow: {
          navigator: {
            onLine: true
          }
        }
      } as any
      service['isDeviceOnline'] = undefined;
      expect(service.isOnlineOrNot()).toBe(true);
    });
    it('should take value from case 3', () => {
      cmsService.getSystemConfig.and.returnValue(observableOf({})),
      service['windowRef'] = {
        nativeWindow: {
          navigator: {
            onLine: true
          }
        }
      } as any
      service['isDeviceOnline'] = undefined;
      expect(service.isOnlineOrNot()).toBe(true);
    });
  });

  describe('getErrorDebug', () => {
    it('error object exist', () => {
      const error = {
        code: '1',
        status: '2',
        message: '3',
        error: '4'
      };
      const httpResponse = {
        error
      };
      expect(service['getErrorDebug'](httpResponse)).toEqual({
        debugCode: error.code,
        debugStatus: error.status,
        debugMessage: error.message,
        debugDescription: error.error
      });
    });

    it('error object is undefined or no data', () => {
      expect(service['getErrorDebug'](null)).toEqual({});
      expect(service['getErrorDebug']({})).toEqual({});
    });
  });

  afterEach(() => {
    service = null;
  });
});
