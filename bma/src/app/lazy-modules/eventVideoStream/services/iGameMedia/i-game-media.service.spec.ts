import { IGameMediaService } from './i-game-media.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { eventEntityMock } from '@uktote/components/betBuilder/bet-builder.component.mock';
import { IIGameMediaModel } from './i-gameMedia.model';
import { Observable, of as observableOf, throwError } from 'rxjs';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';
import { HttpParams } from '@angular/common/http';

describe('IGameMediaService', () => {
  let service: IGameMediaService;

  let http,
    user,
    device,
    asyncScriptLoaderService,
    windowRef,
    watchRulesService,
    cms,
    awsService,
    commandService;

  const iGameMediaStreamQualities = {
    mobile: ['HLS-LOW'],
    wrapper: ['HLS-LOW-RAW'],
    tablet: ['HLS-HIGH', 'HLS-LOW'],
    desktop: ['HLS-WEB', 'DASH', 'RTMP-HIGH']
  };

  const iGameMediaStreams = [
    {
      streamWidth: 640,
      streamHeight: 360,
      uniqueStreamName: 'RTMP-HIGH',
      streamType: 'RTMP',
      streamLink: 'https://player-test.igamemedia.com/BNW/0',
      eventStatusCode: 'O'
    },
    {
      streamWidth: 640,
      streamHeight: 360,
      uniqueStreamName: 'HLS-HIGH',
      streamType: 'HLS',
      streamLink: 'https://player-test.igamemedia.com/BNW/a',
      eventStatusCode: 'O'
    },
    {
      streamWidth: 640,
      streamHeight: 360,
      uniqueStreamName: 'HLS-LOW',
      streamType: 'HLS',
      streamLink: 'https://player-test.igamemedia.com/BNW/b',
      eventStatusCode: 'O'
    },
    {
      streamWidth: 640,
      streamHeight: 360,
      uniqueStreamName: 'HLS-WEB',
      streamType: 'HLS',
      streamLink: 'https://player-test.igamemedia.com/BNW/0',
      eventStatusCode: 'O'
    },
    {
      streamWidth: 640,
      streamHeight: 360,
      uniqueStreamName: 'HLS-LOW-RAW',
      streamType: 'HLS',
      streamLink: 'https://player-test.igamemedia.com/BNW/b',
      eventStatusCode: 'O'
    }
  ];

  beforeEach(() => {
    http = {
      get: jasmine.createSpy(),
      post: jasmine.createSpy().and.returnValue(observableOf(null))
    };
    user = {
      bppToken: 'qwerty123',
      sportBalance: '34',
      username:'ukmigct',
    };
    device = {
      performProviderIsMobile: jasmine.createSpy('performProviderIsMobile').and.returnValue(true)
    };
    asyncScriptLoaderService = {};
    windowRef = {
      nativeWindow: {
        igm: {}
      }
    };
    cms = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf({
        FeatureToggle: {
          IGMOneLink: 'IGMOneLink'
        }
      }))
    };
    watchRulesService = {
      getFailureReason: jasmine.createSpy('getFailureReason'),
      sendAwsData: jasmine.createSpy('sendAwsData'),
      canWatchEvent: jasmine.createSpy('canWatchEvent')
  };
  awsService = {
      addAction: jasmine.createSpy('addAction')
    };
    const reloginBPPObservable = observableOf(true);
    commandService = {
      executeAsync: jasmine.createSpy('reLoginBpp').and.returnValue(reloginBPPObservable),
      API: {
        BPP_AUTH_SEQUENCE: ''
      }
    };

    service = new IGameMediaService(
      http,
      user,
      device,
      cms,
      asyncScriptLoaderService,
      windowRef,
      watchRulesService,
      awsService,
      commandService
    );
  });

  describe('getStreamsForEvent', () => {
    let body;
    beforeEach(() => {
      body = {
        listOfMediaProviders: [{ id: 'VST10', name: 'IMG Video Streaming', mediaTypeCode: 'VST' }],
        priorityProviderCode: 'IMG',
        priorityProviderName: 'IMG Video Streaming'
      };
      http.get = jasmine.createSpy('get').and.returnValue(observableOf({ body }));
      service['sendAwsData'] = jasmine.createSpy('sendAwsData');
    });

    it('should call with success response (URL with IG_MEDIA_ENDPOINT)', () => {
      const url = environment.IG_MEDIA_ENDPOINT;

      service.getStreamsForEvent(eventEntityMock).subscribe((result: IIGameMediaModel) => {
        expect(http.get).toHaveBeenCalledWith(`${url}/${eventEntityMock.id}`, {
          observe: 'response',
          params: jasmine.any(HttpParams),
          headers: jasmine.any(Object)
        });
        expect(service['sendAwsData'])
          .toHaveBeenCalledWith('getVideoStreamingSuccess', eventEntityMock, {
            providerName: body.priorityProviderName,
            response: body
          });
        expect(result).toEqual(body);
      });
    });

    it('should call with success response (URL with IG_MEDIA_TOTE_ENDPOINT)', () => {
      const eventEntity = Object.assign({}, eventEntityMock, {categoryName: 'INTERNATIONAL_TOTE'});
      eventEntity.streamProviders = Object.assign({}, eventEntityMock.streamProviders, {iGameMedia: true});
      const url = environment.IG_MEDIA_TOTE_ENDPOINT;

      service.getStreamsForEvent(eventEntity).subscribe((result: Object) => {
        expect(http.get).toHaveBeenCalledWith(`${url}/${eventEntity.id}`, {
          observe: 'response',
          params: jasmine.any(HttpParams),
          headers: jasmine.any(Object)
        });
        expect(service['sendAwsData'])
          .toHaveBeenCalledWith('getVideoStreamingSuccess', eventEntity, {
            providerName: body.priorityProviderName,
            response: body
          });
        expect(result).toEqual(body);
      });
    });

    it('should test Error response', () => {
      const url = environment.IG_MEDIA_ENDPOINT,
        error = { error: 'errorString' };
      http.get = jasmine.createSpy('get').and.returnValue(throwError(error));

      service.getStreamsForEvent(eventEntityMock).subscribe(null, (err: Object) => {
        expect(service['sendAwsData']).toHaveBeenCalledTimes(1);
        expect(service['sendAwsData']).toHaveBeenCalledWith('getVideoStreamingError', eventEntityMock, {
          errorPayload: error
        });
        expect(http.get).toHaveBeenCalledWith(`${url}/${eventEntityMock.id}`, {
          observe: 'response',
          params: jasmine.any(HttpParams),
          headers: jasmine.any(Object)
        });
        expect(err).toEqual(error);
      });
    });

    it('should relogin to BPP if authentication error is received', (done) => {
      const AUTH_ERROR_CODE = 1403;

      const invalidTokenResponse = observableOf({ body: { code: AUTH_ERROR_CODE } });
      const validTokenResponse = observableOf({ body: { code: ':)' } });

      http.get = jasmine.createSpy('get').and.returnValues(invalidTokenResponse, validTokenResponse);

      service.getStreamsForEvent(eventEntityMock).subscribe(() => {
        expect(commandService.executeAsync).toHaveBeenCalled();
        done();
      });

    });
  });

  it('getStream, should return stream data', () => {
    service['device'] = { isWrapper: true } as any;
    service['isLoggedIn'] = jasmine.createSpy('isLoggedIn').and.returnValue(observableOf(true));
    service['isEventFinished'] = jasmine.createSpy('isEventFinished').and.returnValue(observableOf(true));
    service['getStreamsList'] = jasmine.createSpy('getStreamsList').and.returnValue(observableOf(1));

    service['filterStartedStreams'] = jasmine.createSpy('filterStartedStreams').and.returnValue(observableOf([]));
    service['chooseStreamQuality'] = jasmine.createSpy('chooseStreamQuality').and.returnValue(observableOf({}));
    service['isStreamAvailable'] = jasmine.createSpy('isStreamAvailable').and.returnValue(observableOf({}));
    service['checkCanWatch'] = jasmine.createSpy('checkCanWatch').and.returnValue(observableOf({}));


    service.getStream(eventEntityMock, {} as any).subscribe((result) => {
      expect(cms.getSystemConfig).toHaveBeenCalled();
      expect(service['isLoggedIn']).toHaveBeenCalled();
      expect(service['isEventFinished']).toHaveBeenCalledWith(eventEntityMock);
      expect(service['getStreamsList']).toHaveBeenCalledWith(eventEntityMock, 'IGMOneLink' as any, {} as any);
      expect(service['filterStartedStreams']).toHaveBeenCalledWith(1 as any);
      expect(service['chooseStreamQuality']).toHaveBeenCalledWith([], 'IGMOneLink' as any);
      expect(service['isStreamAvailable']).toHaveBeenCalledWith(eventEntityMock, {});
      expect(service['checkCanWatch']).toHaveBeenCalledWith(eventEntityMock, {} as any);
      expect(result).toEqual({});
    });
  });

  it('getStream, should return stream data: StreamnBet', () => {
    service['device'] = { isWrapper: false } as any;
    service['isLoggedIn'] = jasmine.createSpy('isLoggedIn').and.returnValue(observableOf(true));
    service['isEventFinished'] = jasmine.createSpy('isEventFinished').and.returnValue(observableOf(true));
    service['getStreamsList'] = jasmine.createSpy('getStreamsList').and.returnValue(observableOf(1));

    service['filterStartedStreams'] = jasmine.createSpy('filterStartedStreams').and.returnValue(observableOf([]));
    service['chooseStreamQuality'] = jasmine.createSpy('chooseStreamQuality').and.returnValue(observableOf({}));
    service['isStreamAvailable'] = jasmine.createSpy('isStreamAvailable').and.returnValue(observableOf({}));
    service['checkCanWatch'] = jasmine.createSpy('checkCanWatch').and.returnValue(observableOf({}));


    service.getStream(eventEntityMock, {} as any, true).subscribe((result) => {
      expect(cms.getSystemConfig).toHaveBeenCalled();
      expect(service['isLoggedIn']).toHaveBeenCalled();
      expect(service['isEventFinished']).toHaveBeenCalledWith(eventEntityMock);
      expect(service['getStreamsList']).toHaveBeenCalledWith(eventEntityMock, true, {} as any);
      expect(service['filterStartedStreams']).toHaveBeenCalledWith(1 as any);
      expect(service['chooseStreamQuality']).toHaveBeenCalledWith([], true);
      expect(service['isStreamAvailable']).toHaveBeenCalledWith(eventEntityMock, {});
      expect(service['checkCanWatch']).toHaveBeenCalledWith(eventEntityMock, {} as any);
      expect(result).toEqual({});
    });
  });

  it('replaceAmps, should replace "&amp;" to "&"', () => {
    const result = service.replaceAmps('test&amp;url&amp;');
    expect(result).toEqual('test&url&');
  });

  describe('getIFrameDimensions', () => {
    it('should return desktop video dimensions', () => {
      const desktop = {
        isDesktop: true,
        videoDimensions: {
          height: '768px',
          width: '1024px'
        }
      };

      expect(service.getIFrameDimensions(desktop, 1024, {})).toEqual(desktop.videoDimensions);
    });

    it('should return mobile video dimensions', () => {
      const desktop = {
          isDesktop: false,
          videoDimensions: {
            height: '768px',
            width: '1024px'
          }
        },
        streamData = {
          streamHeight: '1024',
          streamWidth: '768'
        };
      service['mobileDimensions'] = jasmine.createSpy('mobileDimensions').and.returnValue(desktop.videoDimensions);
      const result = service.getIFrameDimensions(desktop, 1024, streamData);

      expect(service['mobileDimensions']).toHaveBeenCalledWith(1024, streamData);
      expect(result).toEqual(desktop.videoDimensions);
    });
  });

  it('sendAwsData, should test AWS Firehose', () => {
    const actionName = 'getVideoStreams';
    const dataToSend = {
      bppToken: user.bppToken.substr(0, 7),
      userBalance: user.sportBalance,
      eventId: eventEntityMock.id
    };
    const trackingData = { errorPayload: 'testError' };
    service['sendAwsData'](actionName, eventEntityMock as ISportEvent, trackingData);
    expect(awsService.addAction).toHaveBeenCalledWith(actionName, Object.assign(dataToSend, trackingData));
  });

  it('mobileDimensions', () => {
    const streamData = {
      streamHeight: '1024',
      streamWidth: '768'
    };

    expect(service['mobileDimensions'](768, streamData)).toEqual({ width: '100%', height: 1021.4 });
  });

  describe('isLoggedIn', () => {
    it('should return true', () => {
      service['user'] = { status: 'status' } as any;
      service['isLoggedIn']().subscribe((result: boolean) => {
        expect(result).toBeTruthy();
      });
    });

    it('should throw error', () => {
      service['isLoggedIn']().subscribe(null, (error: string) => {
        expect(error).toEqual('onlyLoginRequired');
      });
    });
  });

  describe('isEventFinished', () => {
    it('should return false', () => {
      service['isEventFinished']({} as any).subscribe((result: boolean) => {
        expect(result).toBeFalsy();
      });
    });

    it('should throw error', () => {
      const eventEntity = { isFinished: true };
      service['isEventFinished'](eventEntity as any).subscribe(null, (error: string) => {
        expect(error).toEqual('eventFinished');
      });
    });
  });

  describe('isStreamAvailable', () => {
    it('should return stream', () => {
      const eventEntity = {
          categoryName: 'football'
        } as ISportEvent,
        stream = {},
        successHandler = jasmine.createSpy('successHandler'),
        errorHandler = jasmine.createSpy('errorHandler');

      service['isStreamAvailable'](eventEntity, stream).subscribe(successHandler, errorHandler);
      expect(successHandler).toHaveBeenCalledWith({});
    });

    it('should return error "stream is not available" when stream is already started', () => {
      const eventEntity = {
          startTime: '2018-06-30T16:57:00Z'
        } as ISportEvent,
        successHandler = jasmine.createSpy('successHandler'),
        errorHandler = jasmine.createSpy('errorHandler');

      service['isStreamAvailable'](eventEntity, undefined).subscribe(successHandler, errorHandler);
      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalledWith('streamIsNotAvailable');
    });

    it('should return error "event is not started" when stream is not started', () => {
      const eventEntity = {
          startTime: '2100-06-30T16:57:00Z'
        } as ISportEvent,
        successHandler = jasmine.createSpy('successHandler'),
        errorHandler = jasmine.createSpy('errorHandler');

      service['isStreamAvailable'](eventEntity, undefined).subscribe(successHandler, errorHandler);
      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalledWith('eventNotStarted');
    });
  });

  describe('getStreamsList', () => {
    it('should use getStreamsForEvent', () => {
      service.getStreamsForEvent = jasmine.createSpy('getStreamsForEvent').and.returnValue(observableOf(1));
      service['getStreamsList'](eventEntityMock, false)
        .subscribe((result: number) => {
          expect(service.getStreamsForEvent).toHaveBeenCalledWith(eventEntityMock);
          expect(result).toEqual(1);
        });
    });

    it('should use providerInfo', () => {
      const providerInfo = { stream: 'stream' } as any;
      service['getStreamsList'](eventEntityMock, false, providerInfo)
        .subscribe((result: number) => {
          expect(result).toEqual(providerInfo);
        });
    });

    it('should use getNativeStreams', () => {
      service['getNativeStreams'] = jasmine.createSpy('getNativeStreams').and.returnValue(observableOf(1));
      service['getStreamsList'](eventEntityMock, true, {} as any)
        .subscribe((result: number) => {
          expect(service['getNativeStreams']).toHaveBeenCalledWith(eventEntityMock);
          expect(result).toEqual(1);
        });
    });

    it('should throw error', () => {
      service['getNativeStreams'] = jasmine.createSpy('getNativeStreams').and.returnValue(throwError(''));
      service['getStreamsList'](eventEntityMock, true, {} as any)
        .subscribe(null, (error: string) => {
          expect(service['getNativeStreams']).toHaveBeenCalledWith(eventEntityMock);
          expect(error).toEqual('serverError');
        });
    });
  });

  describe('getNativeStreams', () => {
    it('should return stream data or number', () => {
      service['getNativeIGMStreamForEvent'] = jasmine.createSpy('getNativeIGMStreamForEvent')
        .and.returnValue(observableOf(1));
      service['decodeStreamLink'] = jasmine.createSpy('decodeStreamLink').and.returnValue(observableOf(2));

      service['getNativeStreams'](eventEntityMock).subscribe((result: number) => {
        expect(service['getNativeIGMStreamForEvent']).toHaveBeenCalledWith(eventEntityMock);
        expect(service['decodeStreamLink']).toHaveBeenCalledWith(1 as any);
        expect(result).toEqual(2);
      });
    });

    it('should throw error', () => {
      service['getNativeIGMStreamForEvent'] = jasmine.createSpy('getNativeIGMStreamForEvent')
        .and.returnValue(observableOf(1));
      service['decodeStreamLink'] = jasmine.createSpy('decodeStreamLink').and.returnValue(observableOf(-1));

      service['getNativeStreams'](eventEntityMock).subscribe(null, (error: string) => {
        expect(service['getNativeIGMStreamForEvent']).toHaveBeenCalledWith(eventEntityMock);
        expect(service['decodeStreamLink']).toHaveBeenCalledWith(1 as any);
        expect(error).toEqual('streamIsNotAvailable');
      });
    });
  });

  it('getNativeIGMStreamForEvent, should return media model', () => {
    service['loadIGMStreamService'] = jasmine.createSpy('loadIGMStreamService').and.returnValue(observableOf(''));
    service.getStreamsForEvent = jasmine.createSpy('getStreamsForEvent').and.returnValue(observableOf({}));

    service['getNativeIGMStreamForEvent']({} as any).subscribe((result: Object) => {
      expect(service['loadIGMStreamService']).toHaveBeenCalled();
      expect(service.getStreamsForEvent).toHaveBeenCalledWith({} as any, { ViewType: 'RAW' });
      expect(result).toEqual({});
    });
  });

  describe('loadIGMStreamService', () => {
    it('should prepared file streamservice.js', () => {
      service['asyncScriptLoaderService'] = {
        loadJsFile: jasmine.createSpy('loadJsFile').and.returnValue(observableOf('test'))
      } as any;

      service['loadIGMStreamService']().subscribe((result: string) => {
        expect(service['asyncScriptLoaderService'].loadJsFile).toHaveBeenCalledWith(environment.IGM_STREAM_SERVICE_ENDPOINT);
        expect(result).toEqual('test');
      });
    });

    it('should throw error', () => {
      service['asyncScriptLoaderService'] = {
        loadJsFile: jasmine.createSpy('loadJsFile').and.returnValue(throwError('error'))
      } as any;

      service['loadIGMStreamService']().subscribe(null, (error: string) => {
        expect(service['asyncScriptLoaderService'].loadJsFile).toHaveBeenCalledWith(environment.IGM_STREAM_SERVICE_ENDPOINT);
        expect(error).toEqual('IGM streamservice.js not available');
      });
    });
  });

  describe('decodeStreamLink', () => {
    let streamData: IIGameMediaModel;

    beforeEach(() => {
      streamData = {
        streams: [{ uniqueStreamName: '', streamLink: '', eventStatusCode: '' }]
      };
      service['windowRef'] = {
        nativeWindow: {
          igm: {}
        }
      } as any;
    });

    it('should return stream', () => {
      expect(service['decodeStreamLink'](streamData)).toEqual(jasmine.any(Observable));
    });

    it('should return nothing', () => {
      streamData = {};
      const actualResult = service['decodeStreamLink'](streamData);

      actualResult.subscribe(data => {
        expect(data).toEqual(-1);
      });
    });

    it('should return stream error', () => {
      streamData = { details: { failureCode: '', failureDebug: '', failureKey: '' } };

      service['decodeStreamLink'](streamData).subscribe(data => {
        expect(data).toEqual(streamData);
      });
    });

    it('should NOT modify streamData', () => {
      streamData = {
        streams: [{ streamLink: '' }],
        details: {}
      } as any;
      service['windowRef'] = {
        nativeWindow: {
          igm: {
            getStreamUrl: jasmine.createSpy('getStreamUrl')
          }
        }
      } as any;

      service['decodeStreamLink'](streamData).subscribe((result: Object) => {
        expect(service['windowRef'].nativeWindow.igm.getStreamUrl).not.toHaveBeenCalled();
        expect(result).toEqual(streamData);
      });
    });

    it('should modify streamData', () => {
      streamData = {
        streams: [{ streamLink: 'streamLink' }],
        details: {}
      } as any;
      service['windowRef'] = {
        nativeWindow: {
          igm: {
            getStreamUrl: jasmine.createSpy('getStreamUrl').and.returnValue(Promise.resolve(['respStreamLink']))
          }
        }
      } as any;

      service['decodeStreamLink'](streamData).subscribe((result: Object) => {
        expect(service['windowRef'].nativeWindow.igm.getStreamUrl).toHaveBeenCalledWith('streamLink');
        expect(result).toEqual(streamData);
      });
    });

    it('should throw error', () => {
      streamData = {
        streams: [{ streamLink: 'streamLink' }],
        details: {}
      } as any;
      service['windowRef'] = {
        nativeWindow: {
          igm: {
            getStreamUrl: jasmine.createSpy('getStreamUrl').and.returnValue(Promise.reject())
          }
        }
      } as any;

      service['decodeStreamLink'](streamData).subscribe(null, (error: Object) => {
        expect(service['windowRef'].nativeWindow.igm.getStreamUrl).toHaveBeenCalledWith('streamLink');
        expect(error).toEqual(streamData);
      });
    });
  });

  describe('filterStartedStreams, ', () => {
    it('should return streams', () => {
      const response = {
        streams: [
          { eventStatusCode: 'NOT o' } as any,
          { eventStatusCode: 'O'} as any,
          { eventStatusCode: 'O'} as any
        ]
      } as any;

      service['filterStartedStreams'](response).subscribe((result: Object[] | Object) => {
        expect(result).toEqual([response.streams[1], response.streams[2]]);
      });
    });

    it('should return response', () => {
      const response = { code: 1 } as any;

      service['filterStartedStreams'](response).subscribe((result: Object[] | Object) => {
        expect(result).toEqual(response);
      });
    });

    it('should return []', () => {
      const response = {
        streams: [
          { eventStatusCode: 'NOT o' } as any,
          { eventStatusCode: 'O'} as any,
          { eventStatusCode: 'O'} as any
        ]
      } as any;

      spyOn(_, 'where').and.returnValue(undefined);
      service['filterStartedStreams'](response).subscribe((result: Object[] | Object) => {
        expect(_.where).toHaveBeenCalledWith(response.streams, {eventStatusCode: 'O'});
        expect(result).toEqual([]);
      });
    });

  });

  describe('chooseStreamQuality',  () => {
    let streamsList,
      streamQualities;
    beforeEach(() => {
      streamsList = { streamLink: 'streamLink' } as any;
      streamQualities = ['1'];
      service['deviceQualities'] = jasmine.createSpy('deviceQualities').and.returnValue(streamQualities);
      service['preferredQuality'] = jasmine.createSpy('preferredQuality').and.returnValue(streamsList);
    });

    it('should return streamsList', () => {
      streamsList = { details: {} } as any;

      service['chooseStreamQuality'](streamsList, true).subscribe((result: Object) => {
        expect(result).toEqual(streamsList);
      });
    });

    it('should return streamQualities', () => {
      service['chooseStreamQuality'](streamsList, true).subscribe((result: Object) => {
        expect(service['deviceQualities']).toHaveBeenCalledWith(true);
        expect(service['preferredQuality']).toHaveBeenCalledWith(streamQualities, streamsList);
        expect(result).toEqual(streamsList);
      });
    });

    it('should throw error', () => {
      streamQualities = [];
      service['deviceQualities'] = jasmine.createSpy('deviceQualities').and.returnValue(streamQualities);

      service['chooseStreamQuality'](streamsList, true).subscribe(null, (error: string) => {
        expect(service['deviceQualities']).toHaveBeenCalledWith(true);
        expect(service['preferredQuality']).toHaveBeenCalledWith(streamQualities, streamsList);
        expect(error).toEqual('streamIsNotAvailable');
      });
    });
  });

  describe('deviceQualities', () => {
    it('should return stream qualities for wrapper', () => {
      expect(service['deviceQualities'](true)).toEqual(service['STREAM_QUALITIES'].wrapper);
    });

    it('should return stream qualities for tablet', () => {
      service['device'] = { strictViewType: 'tablet'} as any;

      expect(service['deviceQualities'](false)).toEqual(service['STREAM_QUALITIES'].tablet);
    });

    it('should return []', () => {
      service['device'] = { strictViewType: 'TV'} as any;

      expect(service['deviceQualities'](false)).toEqual([]);
    });
  });

  describe('preferredQuality', () => {
    it('should return preferred quality for desktop', () => {
      expect(service['preferredQuality'](iGameMediaStreamQualities.desktop, iGameMediaStreams)).toEqual(iGameMediaStreams[3]);
    });

    it('should return preferred quality for tablet', () => {
      expect(service['preferredQuality'](iGameMediaStreamQualities.tablet, iGameMediaStreams)).toEqual(iGameMediaStreams[1]);
    });

    it('should return preferred quality for mobile', () => {
      expect(service['preferredQuality'](iGameMediaStreamQualities.mobile, iGameMediaStreams)).toEqual(iGameMediaStreams[2]);
    });

    it('should return preferred quality for wrapper', () => {
      expect(service['preferredQuality'](iGameMediaStreamQualities.wrapper, iGameMediaStreams)).toEqual(iGameMediaStreams[4]);
    });

    it('should return preferred quality for unknown device', () => {
      expect(service['preferredQuality']([], iGameMediaStreams)).toEqual(undefined);
    });

    it('should return alternative quality for tablet', () => {
      const streamsWithoutPreferable = iGameMediaStreams.filter(stream => stream.uniqueStreamName !== 'HLS-HIGH');
      expect(service['preferredQuality'](iGameMediaStreamQualities.tablet, streamsWithoutPreferable))
        .toEqual(streamsWithoutPreferable[1]);
    });

    it('should return alternative quality for desktop', () => {
      const streamsWithoutPreferable = iGameMediaStreams.filter(stream => stream.uniqueStreamName !== 'HLS-WEB');
      expect(service['preferredQuality'](iGameMediaStreamQualities.desktop, streamsWithoutPreferable))
        .toEqual(streamsWithoutPreferable[0]);
    });

    it('should return alternative quality for mobile', () => {
      const streamsWithoutPreferable = iGameMediaStreams.filter(stream => stream.uniqueStreamName !== 'HLS-LOW');
      expect(service['preferredQuality'](iGameMediaStreamQualities.mobile, streamsWithoutPreferable)).toEqual(undefined);
    });

    it('should return alternative quality for wrapper', () => {
      const streamsWithoutPreferable = iGameMediaStreams.filter(stream => stream.uniqueStreamName !== 'HLS-LOW-RAW');
      expect(service['preferredQuality'](iGameMediaStreamQualities.wrapper, streamsWithoutPreferable)).toEqual(undefined);
    });
  });

  describe('quality', () => {
    it('quality, should return quality based on uniqueStreamName', () => {
      expect(service['quality']('HLS-HIGH', iGameMediaStreams)).toEqual(iGameMediaStreams[1]);
    });

    it('quality, should return undefined if uniqueStreamName was not found in iGameMediaStreams', () => {
      expect(service['quality']('HLS-UNKNOWN', iGameMediaStreams)).toEqual(undefined);
    });
  });

  describe('checkCanWatch', () => {
    let eventEntity,
      streamsList;

    beforeEach(() => {
      eventEntity = {
        categoryName: 'football'
      } as ISportEvent;
      streamsList = {
        details: {
          failureCode: '4068'
        }
      } as IIGameMediaModel;
      watchRulesService.getFailureReason.and.returnValue('streamIsNotAvailable');
    });

    it('should return error when response from OPT IN MS returns error', () => {
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      const actualResult = service['checkCanWatch'](eventEntity, streamsList as any);
      (actualResult as Observable<IIGameMediaModel>).subscribe(successHandler, errorHandler);

      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalledWith('streamIsNotAvailable');
    });

    it('should return streamsList when response from OPT IN MS not containing error and contain streams', () => {
      streamsList = { streams: [] } as IIGameMediaModel;

      service['checkCanWatch'](eventEntity, streamsList).subscribe((result: Object) => {
        expect(result).toEqual(streamsList);
      });
    });

    it('should return streamsList when response from OPT IN MS not containing error', () => {
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');
      streamsList = {} as IIGameMediaModel;

      const actualResult = service['checkCanWatch'](eventEntity, streamsList as any);
      (actualResult as Observable<IIGameMediaModel>).subscribe(successHandler, errorHandler);

      expect(successHandler).toHaveBeenCalledWith(streamsList);
      expect(errorHandler).not.toHaveBeenCalled();
    });

    it('should return deniedByWatchRules error when response from OPT IN MS returns' +
      '"Error on passing qualification"(Ladbrokes/Coral - 4104/8502 - failureCode)', () => {
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');
      eventEntity.id = 123;
      streamsList.details.failureCode = '4104';
      watchRulesService.getFailureReason.and.returnValue('deniedByWatchRules');

      streamsList.details.failureCode = '4104';

      const actualResult = service['checkCanWatch'](eventEntity, streamsList as any);
      (actualResult as Observable<IIGameMediaModel>).subscribe(successHandler, errorHandler);

      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalledWith('deniedByWatchRules');
      expect(watchRulesService.getFailureReason).toHaveBeenCalledWith('4104');
      expect(watchRulesService.sendAwsData).toHaveBeenCalledWith(123, '4104', 'deniedByWatchRules');
    });

    it('should return deniedByWatchRules error when response from OPT IN MS returns for INTERANTIONAL TOTE' +
      '"Error on passing qualification"(Ladbriokes/Coral - 4104/8502 - failureCode)', () => {
      eventEntity.categoryName = 'INTERNATIONAL_TOTE';
      eventEntity.id = 123123;
      streamsList.details.failureCode = '4104';

      service['checkCanWatch'](eventEntity, streamsList as any);
      expect(watchRulesService.canWatchEvent).toHaveBeenCalledWith(streamsList, eventEntity.categoryId, eventEntity.id);

    });

    it('should return streamlist', () => {
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');
      streamsList.streams = [{streamLink: 'someLink'}];


      const actualResult = service['checkCanWatch'](eventEntity, streamsList as any);
      (actualResult as Observable<IIGameMediaModel>).subscribe(successHandler, errorHandler);

      expect(successHandler).toHaveBeenCalledWith(streamsList as any);
      expect(errorHandler).not.toHaveBeenCalled();
    });
  });

  describe('isEventStarted', () => {
    it('should check if event is started by event"s startTime', () => {
      const eventEntity = {
        startTime: '2018-06-30T16:57:00Z'
      } as ISportEvent;

      expect(service['isEventStarted'](eventEntity)).toBeTruthy();
    });

    it('should check if event is started by event"s startTime(negative case)', () => {
      const eventEntity = {
        startTime: '2100-06-30T16:57:00Z'
      } as ISportEvent;

      expect(service['isEventStarted'](eventEntity)).toBeFalsy();
    });
  });

  describe('processProviderConfig', () => {
    it('should process config', () => {
      const data: any = {
        priorityProviderName: 'Perform',
        meta: { csbIframeEnabled: true, csbIframeSportIds: '1' }
      };
      service['processProviderConfig'](data);
      expect(data.meta.CSBIframeEnabled).toBeDefined();
      expect(data.meta.CSBIframeSportIds).toBeDefined();
    });

    it('should not process config', () => {
      const data: any = { priorityProviderName: 'At The Races', meta: {} };
      service['processProviderConfig'](data);
      expect(data.meta.CSBIframeEnabled).not.toBeDefined();
      expect(data.meta.CSBIframeSportIds).not.toBeDefined();
    });
  });
  describe('getHRReplayStreamUrls', () => {
    it('should post data', () => {
      const body = {
        "token": "qwerty123",
        "eventId": 89798698,
        "user": "ukmigct",
        "device": "mobile"
      },
      url=`${environment.OPT_IN_ENDPOINT}/api/video/vod`,
      result = service['getHRReplayStreamUrls'](89798698);
      expect(http.post).toHaveBeenCalledWith(url, body);
      expect(result).toEqual(jasmine.any(Observable));
    });
    it('should post data', () => {
      device.performProviderIsMobile.and.returnValue(false);
      const body = {
        "token": "qwerty123",
        "eventId": 89798698,
        "user": "ukmigct",
        "device": "desktop"
      },
      url=`${environment.OPT_IN_ENDPOINT}/api/video/vod`,
      result = service['getHRReplayStreamUrls'](89798698);
      expect(http.post).toHaveBeenCalledWith(url, body);
      expect(result).toEqual(jasmine.any(Observable));
    });
  });
});




