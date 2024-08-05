import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { ACTIONS } from '@lazy-modules/awsFirehose/constant/aws-firehose.constant';
import { FanzoneFeaturedService } from './fanzone-featured-ms.service';
import { of, Subject } from 'rxjs';

describe('FanzoneFeaturedService', () => {
  let service: FanzoneFeaturedService;

  let cacheEventsService;
  let commentsService;
  let timeSyncService;
  let liveEventClockProviderService;
  let windowRefService;
  let awsService;
  let pubsubService;
  let ngZone;
  let segmentEventManagerService;
  let userService;
  let device;
  let webSocketService;
  let fakeSocket: Subject<any>;
  let pubSubTrigger: Function;

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

    ngZone = {
      runOutsideAngular: jasmine.createSpy().and.callFake(fn => fn())
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
      isConnected: jasmine.createSpy('isConnected').and.callFake(fn => fn()),
      removeAllListeners: jasmine.createSpy('removeAllListeners'),
    }
    fakeSocket = new Subject<any>();
    spyOn(fakeSocket, 'next').and.callThrough();
    service = new FanzoneFeaturedService(
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
    spyOn(service, 'reconnect').and.callThrough();
    expect(service).toBeTruthy();
    expect(service['moduleStates']).toEqual(jasmine.any(Map));
    expect(service['subscribedFeaturedTabModules']).toEqual(jasmine.any(Array));
    service['currentSport'] = 0;
    webSocketService.isConnected.and.returnValue(true);
    pubSubTrigger();
    expect(service.reconnect).not.toHaveBeenCalled();
  });

  it('get tabModuleStates', () => {
    expect(service.tabModuleStates).toBe(service['moduleStates']);
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

  it('reconnect connection is open', () => {
    spyOn(service, 'disconnect');
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
    webSocketService.isConnected.and.returnValue(false);
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
  it('callBacks', () => {
    const mockEvent = '237640958';
    service['callbacks'] = { mockEvent: [] };
    const mockData = '40,{"237640958":"{}"}';
    expect(service['callbacks'][mockEvent]).toBeUndefined();
  });
  
  it('onReconnectionFailed', () => {
    service.onReconnectionFailed();
    expect(pubsubService.publishSync).toHaveBeenCalledWith(pubsubService.API.FEATURED_CONNECT_STATUS, false);
    expect(awsService.addAction).toHaveBeenCalled();
  });
  it('startConnection', () => {
    const sportIdMock = 0;
    spyOn(service, 'socketListener').and.returnValue(of({}));
    service.addEventListener = jasmine.createSpy('addEventListener').and.callFake((event, cb) => {
      if (event === 'connect_error') {
        cb();
        expect(awsService.addAction).toHaveBeenCalled();
      } else {
        cb();
      }
    });
    service.startConnection(sportIdMock, 'sport');
    expect(service['currentSport']).toEqual(sportIdMock);
    expect(service['currentPageType']).toEqual('sport');
    expect(webSocketService.establishConnection).toHaveBeenCalled();
  });

  it('startConnection eventhub', () => {
    const hubIndexdMock = 0;

    spyOn(service, 'addEventListener');
    spyOn(service, 'socketListener').and.returnValue(of({}));

    service.startConnection(hubIndexdMock, 'eventhub');

    expect(service['currentSport']).toEqual(hubIndexdMock);
    expect(service['currentPageType']).toEqual('eventhub');
  });

  it('should handle Namespace MS error message', () => {
    service.errorsMessagesHandler('randomError');

    expect(pubsubService.publish).not.toHaveBeenCalled();

    service.errorsMessagesHandler('Invalid namespace');

    expect(pubsubService.publish).toHaveBeenCalled();
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

});