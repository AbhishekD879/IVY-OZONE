import { TimelineService } from '@lazy-modules/timeline/services/timeline.service';
import { Observable, of as observableOf, throwError } from 'rxjs';
import { ACTIONS } from '@lazy-modules/awsFirehose/constant/aws-firehose.constant';

describe('TimelineService', () => {
  let timelineService;
  let wsConnectorService;
  let awsService;
  let gtmService;

  beforeEach(() => {
    wsConnectorService = {
      create: jasmine.createSpy().and.returnValue({
        state$: observableOf(null),
        addAnyMessagesHandler: jasmine.createSpy('addAnyMessagesHandler'),
        connection: {
          on: jasmine.createSpy('on')
        },
        emit: jasmine.createSpy('emit'),
        isConnected: jasmine.createSpy('isConnected').and.returnValue(true),
        connect: jasmine.createSpy().and.returnValue(observableOf(null)),
        disconnect: jasmine.createSpy('disconnect'),
        addEventListener: jasmine.createSpy('addEventListener'),
        removeEventListener: jasmine.createSpy('removeEventListener')
      })
    };

    awsService = {
      addAction: jasmine.createSpy(),
      API: ACTIONS
    };

    gtmService = {
      push: jasmine.createSpy('gtm')
    };

    timelineService = new TimelineService(wsConnectorService, awsService, gtmService);
  });

  describe('connect()', () => {
    it('should open web socket connection', () => {
      spyOn(timelineService, 'createSocket');

      timelineService.createSocket();
      expect(timelineService['wsConnectorService'].create).not.toHaveBeenCalled();
    });

    it('should start connection if socket is opened', () => {
      spyOn(timelineService, 'connect');
      timelineService.socket = {};
      timelineService.connect();

      expect(timelineService.connect).toHaveBeenCalled();
    });
  });

  describe('disconnect()', () => {
    beforeEach(() => {
      timelineService.createSocket();
    });
    it('should close socket connection if disconnect', () => {
      const disconnect = jasmine.createSpy('disconnect');
      timelineService.socket = {disconnect};

      timelineService.disconnect();

      expect(disconnect).toHaveBeenCalled();
      expect(timelineService.socket).toBeNull();
    });

    it('should do nothing if socket connection already disconnect', () => {
      timelineService.socket = null;

      timelineService.disconnect();

      expect(timelineService.socket).toBeNull();
    });
  });

  describe('reconnect()', () => {
    it('should disconnect old and connect new web socket', () => {
      spyOn(timelineService, 'connect');
      spyOn(timelineService, 'disconnect');

      timelineService.reconnect();

      expect(timelineService.disconnect).toHaveBeenCalled();
      expect(timelineService.connect).toHaveBeenCalled();
    });
  });

  describe('events handlers ', () => {
    beforeEach(() => {
      timelineService.createSocket();
    });

    it('should  add new event listener', () => {
      const args = ['eventName', () => {}];
      timelineService.addListener(...args);

      expect(timelineService.socket.addEventListener).toHaveBeenCalled();
      expect(timelineService.socket.addEventListener).toHaveBeenCalledWith(...args);
    });

    it('should remove listener for event', () => {
      const args = ['eventName', () => {}];
      timelineService.removeListener(...args);

      expect(timelineService.socket.removeEventListener).toHaveBeenCalled();
      expect(timelineService.socket.removeEventListener).toHaveBeenCalledWith(...args);
    });

    it('should emit event to socket', () => {
      const args = ['eventName', []];
      timelineService.emit(...args);

      expect(timelineService.socket.emit).toHaveBeenCalled();
      expect(timelineService.socket.emit).toHaveBeenCalledWith(...args);
    });
  });

  describe('addAwsEventListeners()', () => {
    beforeEach(() => {
      timelineService.createSocket();
    });

    it('shouldn\'t add listeners if no socket connection', () => {
      timelineService.socket = {} as any;
      timelineService.addAwsEventListeners();
      expect(timelineService.awsService.addAction).not.toHaveBeenCalled();
    });

    it('should add listeners if is active socket connection', () => {
      timelineService.addAwsEventListeners();
      expect(timelineService.socket.connection.on).toHaveBeenCalledTimes(5);
    });

    it('on connect_error', () => {
      const error = 'someError';

      timelineService.socket.connection.on.and.callFake((action, cb) => {
        action === 'connect_error' && cb(error);
      });

      timelineService.addAwsEventListeners();

      expect(awsService.addAction).toHaveBeenCalledWith(
        awsService.API.TIMELINE_WS_CONNECTION_FAILED, {error}
      );
    });

    it('on connect', () => {
      timelineService.socket.connection.on.and.callFake((action, cb) => {
        action === 'connect' && cb();
      });

      timelineService.addAwsEventListeners();

      expect(awsService.addAction).toHaveBeenCalledWith(
        awsService.API.TIMELINE_WS_CONNECTION_SUCCESS
      );
    });

    it('on reconnect', () => {
      const attemp = 1;
      timelineService.socket.connection.on.and.callFake((action, cb) => {
        action === 'reconnect' && cb(attemp);
      });

      timelineService.addAwsEventListeners();

      expect(awsService.addAction).toHaveBeenCalledWith(
        awsService.API.TIMELINE_WS_RECONNECTION_SUCCESS, {attemp}
      );
    });

    it('on reconnect_failed', () => {
      timelineService.socket.connection.on.and.callFake((action, cb) => {
        action === 'reconnect_failed' && cb();
      });

      timelineService.addAwsEventListeners();

      expect(awsService.addAction).toHaveBeenCalledWith(
        awsService.API.TIMELINE_WS_RECONNECTION_FAILED
      );
    });

    it('on reconnect_attempt', () => {
      const attemp = 5;
      timelineService.socket.connection.on.and.callFake((action, cb) => {
        if (action === 'reconnect_attempt') {
          cb(attemp);
        }
      });
      timelineService.addAwsEventListeners();
      expect(awsService.addAction).toHaveBeenCalledWith(
        awsService.API.TIMELINE_WS_RECONNECTION_ATTEMP, {attemp}
      );
    });
  });

  describe('start connection', () => {
    beforeEach(() => {
      timelineService.createSocket();
    });

    it('should start connection', () => {
      spyOn(timelineService, 'addAwsEventListeners');

      const connection = timelineService.connect();

      expect(connection).toEqual(jasmine.any(Observable));
      expect(timelineService.wsConnectorService.create).toHaveBeenCalled();

      connection.subscribe();

      expect(timelineService.addAwsEventListeners).toHaveBeenCalled();
    });

    it('should throw error if not start connection', () => {
      spyOn(timelineService, 'addAwsEventListeners');

      const error = 'someError';
      const errorHandler = jasmine.createSpy('errorHandler');
      const successHandler = jasmine.createSpy('successHandler');
      const connection = timelineService.connect();

      expect(connection).toEqual(jasmine.any(Observable));
      expect(timelineService.wsConnectorService.create).toHaveBeenCalled();

      timelineService.socket.connect = jasmine.createSpy().and.returnValue(throwError(error));

      timelineService.connect().subscribe(successHandler, errorHandler);

      expect(errorHandler).toHaveBeenCalled();
      expect(successHandler).not.toHaveBeenCalled();
      expect(timelineService.addAwsEventListeners).not.toHaveBeenCalled();
      expect(timelineService.awsService.addAction).toHaveBeenCalled();
      expect(timelineService.awsService.addAction).toHaveBeenCalledWith(
        awsService.API.TIMELINE_WS_CONNECTION_FAILED, {error}
      );
    });
  });

  it('push gtm for ladbrokes', () => {
    timelineService.gtm('testAction', { test: 'test' }, 'ladbrokes lounge');
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      eventAction: 'testAction',
      eventCategory: 'ladbrokes lounge',
      test: 'test'
    });
  });

  it('push gtm for coral', () => {
    timelineService.gtm('testAction', { test: 'test' }, 'coral pulse');
    expect(gtmService.push).toHaveBeenCalledWith('trackEvent', {
      eventAction: 'testAction',
      eventCategory: 'coral pulse',
      test: 'test'
    });
  });
});