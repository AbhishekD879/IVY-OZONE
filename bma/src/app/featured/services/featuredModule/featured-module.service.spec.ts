import { FeaturedModuleService } from './featured-module.service';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { ACTIONS } from '@lazy-modules/awsFirehose/constant/aws-firehose.constant';
import { featuredModuleMock } from '../../components/featured-module/featured-module.component.mock';
import * as _ from 'underscore';
import { of, Subject } from 'rxjs';


describe('FeaturedModuleService', () => {
  let service: FeaturedModuleService;
  let cacheEventsService;
  let commentsService;
  let timeSyncService;
  let liveEventClockProviderService;
  let awsService;
  let pubsubService;
  let segmentEventManagerService;
  let userService;
  let device;
  let webSocketService;
  let pubSubTrigger: Function;
  let fakeSocket: Subject<any>;
  beforeEach(() => {
    pubsubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake(
        (subscriberName, channel, channelFunction) => {
          pubSubTrigger = channelFunction;
        }
      ),
      publish: jasmine.createSpy('publish'),
      publishSync: jasmine.createSpy('publishSync'),
      API: pubSubApi
    };
    segmentEventManagerService = {
      getSegmentDetails: jasmine.createSpy('getSegmentDetails').and.returnValue('segment'),
      chkModuleForSegmentation: jasmine.createSpy('chkModuleForSegmentation').and.returnValue(true),
    };
    userService = {
      username: 'test'
    };
    device = {
      requestPlatform: 'mobile'
    };
    cacheEventsService = {
      store: jasmine.createSpy()
    };


    commentsService = {
      getCLockData: jasmine.createSpy()
    };

    timeSyncService = {
      getTimeDelta: jasmine.createSpy()
    };

    liveEventClockProviderService = {
      create: jasmine.createSpy()
    };

    awsService = {
      API: ACTIONS,
      addAction: jasmine.createSpy('addAction')
    };

    webSocketService = {
      connection: new Subject<any>(),
      socket: new Subject<any>(),
      connect: jasmine.createSpy().and.returnValue(of(null)),
      disconnect: jasmine.createSpy('disconnect'),
      addEventListener: jasmine.createSpy('addEventListener'),
      removeEventListener: jasmine.createSpy('removeEventListener'),
      sendMessage: jasmine.createSpy('sendMessage'),
      establishConnection: jasmine.createSpy('establishConnection'),
      isConnected: jasmine.createSpy('isConnected'),
      removeAllListeners: jasmine.createSpy('removeAllListeners'),
      getSocket: jasmine.createSpy().and.callFake(()=> fakeSocket),
      callBackMessagesHandler: jasmine.createSpy('callBackMessagesHandler')
    }
    fakeSocket = new Subject<any>();
    spyOn(fakeSocket, 'next').and.callThrough();
    spyOn(webSocketService.connection, 'next').and.callThrough();
    service = new FeaturedModuleService(
      cacheEventsService,
      commentsService,
      timeSyncService,
      liveEventClockProviderService,
      pubsubService,
      awsService,
      segmentEventManagerService,
      userService,
      device,
      webSocketService
    );
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service['moduleStates']).toEqual(jasmine.any(Map));
    expect(service['subscribedFeaturedTabModules']).toEqual(jasmine.any(Array));
    spyOn(service, 'reconnect');
    service['currentSport'] = 0;
    webSocketService.isConnected.and.returnValue(true);
    pubSubTrigger();
    expect(service.reconnect).not.toHaveBeenCalled();
  });
  it('constructor calls reconnect if not connected', () => {
    expect(service).toBeTruthy();
    spyOn(service, 'reconnect');
    webSocketService.isConnected.and.returnValue(false);
    pubSubTrigger();
    expect(service.reconnect).toHaveBeenCalled();
  });

  it('get tabModuleStates', () => {
    expect(service.tabModuleStates).toBe(service['moduleStates']);
  });
  it('segmentedSubscription', () => {
    pubsubService.subscribe.and.callFake((a, method, cb) => {
      if (method === 'SEGMENT_RECEIVED') {
        cb();
      }
    });
    spyOn(service, 'segmentReceivedListner');
    service.segmentedSubscription();
    expect(service.segmentReceivedListner).toHaveBeenCalled();
  });
  it('segmentReceivedListner emit get called', () => {
    spyOn(service, 'emit');
    webSocketService.isConnected.and.returnValue(true);
    service.segmentReceivedListner();
    expect(service.emit).toHaveBeenCalled();
  });
  it('segmentReceivedListner emit get called', () => {
    spyOn(service, 'emit');
    service.segmentReceivedListner();
    expect(service.emit).not.toHaveBeenCalled();
  });
  it('segmentReceivedListner emit did n ot called', () => {
    spyOn(service, 'emit');
    device.requestPlatform = 'desktop';
    service.segmentReceivedListner();
    expect(service.emit).not.toHaveBeenCalled();
  });
  it('segmentReceivedListner emit did n ot called', () => {
    spyOn(service, 'emit');
    device.requestPlatform = 'desktop';
    service.segmentReceivedListner();
    expect(service.emit).not.toHaveBeenCalled();
  });
  it('segmentReceivedListner emit did n ot called', () => {
    spyOn(service, 'emit');
    device.requestPlatform = 'desktop';
    service.segmentReceivedListner();
    expect(service.emit).not.toHaveBeenCalled();
  });
  it('checkForValidEmit emit did not called all false case', () => {
    spyOn(service, 'emit');
    device.requestPlatform = 'desktop';
    userService.username = '';
    segmentEventManagerService.chkModuleForSegmentation.and.returnValue(false)
    service.checkForValidEmit('');
    expect(service.emit).not.toHaveBeenCalled();
  });
  it('checkForValidEmit emit did not called false case 1', () => {
    spyOn(service, 'emit');
    device.requestPlatform = 'mobile';
    userService.username = '';
    segmentEventManagerService.chkModuleForSegmentation.and.returnValue(false)
    service.checkForValidEmit('');
    expect(service.emit).not.toHaveBeenCalled();
  });
  it('checkForValidEmit emit did not called false case 2', () => {
    spyOn(service, 'emit');
    device.requestPlatform = 'mobile';
    userService.username = 'test';
    segmentEventManagerService.chkModuleForSegmentation.and.returnValue(false)
    service.checkForValidEmit('');
    expect(service.emit).not.toHaveBeenCalled();
  });
  it('checkForValidEmit emit did not called false case 3', () => {
    spyOn(service, 'emit');
    device.requestPlatform = 'mobile';
    userService.username = 'test';
    segmentEventManagerService.chkModuleForSegmentation.and.returnValue(true)
    service.checkForValidEmit('');
    expect(service.emit).not.toHaveBeenCalled();
  });
  it('checkForValidEmit emit did not called false case 4', () => {
    spyOn(service, 'emit');
    device.requestPlatform = 'desktop';
    userService.username = '';
    segmentEventManagerService.chkModuleForSegmentation.and.returnValue(false)
    service.checkForValidEmit('test');
    expect(service.emit).not.toHaveBeenCalled();
  });
  it('checkForValidEmit emit did not called false case 5', () => {
    spyOn(service, 'emit');
    device.requestPlatform = 'desktop';
    userService.username = '';
    segmentEventManagerService.chkModuleForSegmentation.and.returnValue(true)
    service.checkForValidEmit('test');
    expect(service.emit).not.toHaveBeenCalled();
  });
  it('checkForValidEmit emit did not called false case 6', () => {
    spyOn(service, 'emit');
    device.requestPlatform = 'desktop';
    userService.username = 'test';
    segmentEventManagerService.chkModuleForSegmentation.and.returnValue(true)
    service.checkForValidEmit('test');
    expect(service.emit).not.toHaveBeenCalled();
  });

  it('checkEventModule and return value with segmentName', () => {
    device.isMobile = true;
    userService.username = 'test';
    const featuredModuleMockClone: any = _.clone(featuredModuleMock);
    const value = service.checkEventModuleAndReturnValue(featuredModuleMockClone);
    expect(value).toEqual(featuredModuleMock._id + '#segment');
  });

  it('checkEventModule And ReturnValue without segmentName', () => {
    device.isMobile = true;
    userService.username = '';
    const featuredModuleMockClone: any = _.clone(featuredModuleMock);
    const value = service.checkEventModuleAndReturnValue(featuredModuleMockClone);
    expect(value).toEqual(featuredModuleMock._id);
  });

  it('getSubscribedFeaturedTabModules', () => {
    expect(service.getSubscribedFeaturedTabModules()).toBe(service['subscribedFeaturedTabModules']);
  });

  it('addModuleToSubscribedFeaturedTabModules', () => {
    service.addModuleToSubscribedFeaturedTabModules('1');
    service.addModuleToSubscribedFeaturedTabModules('2');
    expect(service['subscribedFeaturedTabModules'].length).toBe(2);

    service.addModuleToSubscribedFeaturedTabModules('2');
    expect(service['subscribedFeaturedTabModules'].length).toBe(2);
  });

  it('clearSubscribedFeaturedTabModules', () => {
    service['subscribedFeaturedTabModules'] = ['1', '2'];
    service.clearSubscribedFeaturedTabModules();
    expect(service['subscribedFeaturedTabModules'].length).toBe(0);
  });

  it('reconnect', () => {
    spyOn(service, 'startConnection');
    service['currentSport'] = 1;
    service['currentPageType'] = 'sport';
    webSocketService.isConnected.and.returnValue(true);
    service.reconnect();
    expect(webSocketService.disconnect).toHaveBeenCalled();
    expect(service.startConnection).toHaveBeenCalledWith(service['currentSport'], service['currentPageType']);
  });
  it('reconnect connection is closed', () => {
    spyOn(service, 'disconnect');
    spyOn(service, 'startConnection');
    service['currentSport'] = 1;
    service['currentPageType'] = 'sport';
    service.reconnect();
    expect(webSocketService.disconnect).not.toHaveBeenCalled();
    expect(service.startConnection).toHaveBeenCalledWith(service['currentSport'], service['currentPageType']);
  });

  it('emit', () => {
    const event = 'ON_ERROR';
    const data = ['l', 'c'];
    service['currentSport'] = 1;
    service.emit(event, data);
    expect(webSocketService.sendMessage).toHaveBeenCalledWith(`42/${service['currentSport']},` + JSON.stringify([event, data]));
  });
  it('emit eventhub', () => {
    const event = 'ON_ERROR';
    const data = ['l', 'c'];
    service['currentSport'] = 1;
    service['currentPageType'] = 'eventhub';
    service.emit(event, data);
    expect(webSocketService.sendMessage).toHaveBeenCalledWith(`42/h${service['currentSport']},` + JSON.stringify([event, data]));
  });

  it('removeEventListener', () => {
    const event = 'ON_OK';
    const handler = () => { };
    service.removeEventListener(event, handler);
    expect(webSocketService.removeEventListener).toHaveBeenCalled();
  });

  it('removeAllListeners', () => {
    const events = ['ON_OK', 'ON_FAIL'];
    service.removeAllListeners(events);
    expect(webSocketService.removeAllListeners).toHaveBeenCalled();
  });

  it('#disconnect should terminate connection', () => {
    service.disconnect();
    expect(webSocketService.disconnect).toHaveBeenCalled();
  });

  it('onConnect', (done) => {
    service['currentPageType'] = 'sport';
    service.onConnect();
    webSocketService.connection.subscribe((item) => {
      if (item) {
        expect(pubsubService.publishSync).toHaveBeenCalledWith(pubsubService.API.FEATURED_CONNECT_STATUS, true);
        expect(awsService.addAction).toHaveBeenCalled();
      }
      done();
    });
    webSocketService.connection.next(true);
  });
  it('onConnect should send message for eventhub', (done) => {
    service['currentPageType'] = 'eventhub';
    service.onConnect();
    webSocketService.connection.subscribe((item) => {
      if (item) {
        expect(pubsubService.publishSync).toHaveBeenCalledWith(pubsubService.API.FEATURED_CONNECT_STATUS, true);
        expect(awsService.addAction).toHaveBeenCalled();
      }
      done();
    });
    webSocketService.connection.next(true);
  });

  it('errorsMessagesHandler', () => {
    const item = 'Invalid namespace';
    service.errorsMessagesHandler(item);
    expect(pubsubService.publish).toHaveBeenCalledWith(pubsubService.API.NAMESPACE_ERROR);
  });
  it('errorsMessagesHandler random error', () => {
    const item = 'RANDOM_ERROR';
    service.errorsMessagesHandler(item);
    expect(pubsubService.publish).not.toHaveBeenCalledWith(pubsubService.API.NAMESPACE_ERROR);
  });

  it('socketListener with invalid namespace', (done) => {
    const error = 'Invalid namespace';
    spyOn(service, 'errorsMessagesHandler');
    webSocketService.establishConnection();
    service.socketListener();
    webSocketService.socket.subscribe((item) => {
      expect(service.errorsMessagesHandler).toHaveBeenCalled();
      done();
    });
    webSocketService.socket.next(error);
  });
  it('socketListener with valid namespace', (done) => {
    const mockObj = { '237640958': [r => { }] };
    spyOn(service, 'errorsMessagesHandler');
    webSocketService.establishConnection();
    service.socketListener();
    webSocketService.socket.subscribe((item) => {
      expect(service.errorsMessagesHandler).not.toHaveBeenCalled();
      done();
    });
    webSocketService.socket.next(mockObj);
  });
  it('should call connection failed on socket  error', (done) => {
    spyOn(service, 'onReconnectionFailed');
    spyOn(service, 'errorsMessagesHandler');
    const settings = { reconnectionAttempts: 0, timeout: 0 };
    Object.defineProperty(service, 'ioSettings', { get: () => settings });
    webSocketService.establishConnection();
    service.socketListener();
    webSocketService.socket.subscribe((item) => {
    }
      , err => {
        expect(service.errorsMessagesHandler).not.toHaveBeenCalled();
        expect(service.onReconnectionFailed).toHaveBeenCalled();
        done();
      });
      webSocketService.socket.error({ err: 'error' });
  });

  
  it('onReconnectionFailed', () => {
    service.onReconnectionFailed();
    expect(pubsubService.publishSync).toHaveBeenCalledWith(pubsubService.API.FEATURED_CONNECT_STATUS, false);
    expect(awsService.addAction).toHaveBeenCalled();
  });
  it('startConnection', () => {
    const sportIdMock = 0;
    spyOn(service, 'socketListener').and.returnValue(of({}));
    webSocketService.addEventListener = jasmine.createSpy('addEventListener').and.callFake((event, cb) => {
      if (event === 'connect_error') {
        cb();
        expect(awsService.addAction).toHaveBeenCalled();
      }
    });
    service.startConnection(sportIdMock, 'sport');
    expect(service['currentSport']).toEqual(sportIdMock);
    expect(service['currentPageType']).toEqual('sport');
    expect(webSocketService.establishConnection).toHaveBeenCalled();
  });

  it('should handle Namespace MS error message', () => {
    service.errorsMessagesHandler('randomError');

    expect(pubsubService.publish).not.toHaveBeenCalled();

    service.errorsMessagesHandler('Invalid namespace');

    expect(pubsubService.publish).toHaveBeenCalled();
  });

  describe('#onError', () => {
    const onErrorCallback = jasmine.createSpy('onErrorCallback');
    const createMockData = (isBoosted) => {
      const ioOnHandler = (event, cb) => {
        cb(isBoosted);
      };
      webSocketService.addEventListener = jasmine.createSpy('addEventListener').and.callFake(ioOnHandler);
    };
    
    it('should not call callback function', () => {
      spyOn(service, 'reconnect');
      createMockData(true);
      service.onError(onErrorCallback);
      expect(service.reconnect).not.toHaveBeenCalled();
      expect(onErrorCallback).not.toHaveBeenCalled();
    });

    it('should reconnect', () => {
      createMockData(false);
      spyOn(service, 'reconnect');
      service.onError(onErrorCallback);
      expect(onErrorCallback).toHaveBeenCalled();
      expect(service.reconnect).toHaveBeenCalled();
    });
  });

  it('#cacheEvents should cache data', () => {
    const data: any = {};
    service.cacheEvents(data);
    expect(cacheEventsService.store).toHaveBeenCalledWith('ribbonEvents', data);
  });

  it('#cacheEvents should NOT cache data', () => {
    const data: any = {};
    service.cacheEvents(undefined);
    expect(cacheEventsService.store).not.toHaveBeenCalledWith('ribbonEvents', data);
  });

  it('addClock', () => {
    const events: any = [
      {},
      { comments: { latestPeriod: {} }, categoryCode: '' },
      { comments: { latestPeriod: {} }, categoryCode: '' }
    ];

    expect(service.addClock(events)).toBe(events);
    expect(commentsService.getCLockData).toHaveBeenCalledTimes(2);
    expect(liveEventClockProviderService.create).toHaveBeenCalledTimes(2);
    expect(timeSyncService.getTimeDelta).toHaveBeenCalled();
  });

  describe('#trackDataReceived', () => {
    it('should track featured structure changed', () => {
      service.trackDataReceived({
        events: ['12213', '12312312'],
        someData: 'someData'
      }, 'FEATURED_STRUCTURE_CHANGED');

      expect(awsService.addAction).toHaveBeenCalledWith('FEATURED_WS_STRUCTURE_RECEIVED', {
        message: 'FEATURED_STRUCTURE_CHANGED',
        payloadSize: 53
      });
    });
  });
});
