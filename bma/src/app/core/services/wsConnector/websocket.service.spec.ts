import { Subject } from "rxjs";
import { WebSocketSubject } from "rxjs/webSocket";
import { WebSocketService } from "./websocket.service";

describe('WebSocketService', () => {
  let service: WebSocketService;
  let ngZone;
  let fakeSocket: Subject<any>;
  beforeEach(() => {

    ngZone = {
      runOutsideAngular: jasmine.createSpy().and.callFake(fn => fn())
    };
    fakeSocket = new Subject<any>();
    spyOn(fakeSocket, 'next').and.callThrough();

    service = new WebSocketService(
      ngZone,
    );

  });

  it('constructor', () => {
    spyOn(service, 'socketListener');
    spyOn(service, 'pingpong');
    service.establishConnection('wss://featured-publisher.beta.ladbrokes.com/socket.io/?EIO=3&transport=websocket');
    const connection = service['socket'];
    connection.subscribe(p => {
      console.log(p);
      connection.next('42/0,["237640958","100.0.0"]');
      connection.complete();
    });
    expect(service).toBeTruthy();
    expect(service['ioSettings']).toEqual(jasmine.any(Object));
    expect(service['connection']).toBeDefined();
    expect(service['websocketConfig']).toEqual(jasmine.any(Object));
  });

  it('establishConnection', () => {
    const endpoint = '';
    service.getSocket = jasmine.createSpy().and.callFake(() => fakeSocket);
    service.establishConnection(endpoint);
    expect(service['socket']).toBeTruthy();
    expect(ngZone.runOutsideAngular).toHaveBeenCalled();
  });

  it('pingpong when connection is closed', (done: DoneFn) => {
    spyOn(service, 'sendMessage');
    service.socket = { closed: true };
    service['ioSettings'].pingDelay = 100;
    service.pingpong();
    setTimeout(() => {
      expect(service.sendMessage).not.toHaveBeenCalled();
      done();
    }, 1010);
  });
  it('pingpong', (done: DoneFn) => {
    spyOn(service, 'sendMessage');
    service.getSocket = jasmine.createSpy().and.callFake(() => fakeSocket);
    service['ioSettings'].pingDelay = 100;
    service.socket = new WebSocketSubject('');
    service['pingSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    service.pingpong();
    setTimeout(() => {
      expect(service.sendMessage).toHaveBeenCalled();
      done();
    }, 1010);
  });
  it('sendMessage', () => {
    const mockData = '40,{"237640958":"{}"}';
    service.getSocket = jasmine.createSpy().and.callFake(() => fakeSocket);
    service.establishConnection('');
    service.sendMessage(mockData);
    expect(fakeSocket.next).toHaveBeenCalledTimes(1);
  });
  it('should addEventListener for connection', () => {
    service.getSocket = jasmine.createSpy().and.callFake(() => fakeSocket);
    service.establishConnection('');
    service.addEventListener('testMessage', () => { });
    expect(service['callbacks']['testMessage']).toBeTruthy();
  });
  it('should clear callbacks', () => {
    service.getSocket = jasmine.createSpy().and.callFake(() => fakeSocket);
    service.establishConnection('');
    service.addEventListener('testMessage', () => { });
    service.clearCallbacks();
    expect(service['callbacks']).toEqual({});
  });
  it('removeEventListener', () => {
    const event = 'ON_OK';
    const handler = () => { };
    service.addEventListener('ON_FAIL', handler);
    service.addEventListener('ON_OK', handler);
    const check = service['callbacks']['ON_OK'];
    service.removeEventListener(event, handler);
    expect(check).toBeDefined();
    expect(service['callbacks']['ON_OK']).not.toBeDefined();
    expect(service['callbacks']['ON_FAIL']).toBeDefined();
  });
  it('removeEventListener if no callback event', () => {
    const event = 'ON_OK';
    const handler = () => { };
    const callback = { 'ON_OK': [() => { }] };
    service['callbacks'] = [callback];
    service.removeEventListener(event, handler);
    expect(service['callbacks'][event]).not.toBeDefined();
  });

  it('removeAllListeners', () => {
    const events = ['ON_OK', 'ON_FAIL'];
    const handler = () => { };
    service.addEventListener('ON_FAIL', () => { });
    service.addEventListener('ON_OK', () => { });
    service['callbacks']['ON_FAIL'] = handler;
    service.removeAllListeners(events);
    expect(service['callbacks']['ON_OK']).toBeUndefined();
    expect(service['callbacks']['ON_FAIL']).toBeUndefined();
  });
  it('socket subscription able to listen', (done) => {
    spyOn(service, 'callBacks');
    const endpoint = '';
    const mockData = '40,{"237640958":"{}"}';
    service.getSocket = jasmine.createSpy().and.callFake(() => fakeSocket);
    service.establishConnection(endpoint);
    service.socketListener();
    service.socket.subscribe((item) => {
      expect(service.callBacks).toHaveBeenCalled();
      done();
    });
    service.socket.next(mockData);
  });
  it('callBacks', () => {
    const mockEvent = '237640958';
    service['callbacks'] = { mockEvent: () => { } };
    const mockData = '42/0,["237640958","100.0.0"]';
    const index = mockData.indexOf(',');
    const response = JSON.parse(mockData.substr(index + 1));
    service.callBacks(mockData);
    expect(response).toBeDefined();
  });
  it('callBacks have listener', () => {
    const mockEvent = '237640958';
    const func = () => { name: 'connected' };
    service['callbacks'] = { 237640958: [func] };
    const mockData = '42/0,["237640958","100.0.0"]';
    const cBack = service['callbacks'][mockEvent];
    service.callBacks(mockData);
    expect(service['callbacks']['237640958'][0]).toEqual(func);
    expect(cBack).toBeDefined();
  });
  it('callBacks undefined', () => {
    const mockEvent = '237640958';
    service['callbacks'] = { mockevent: () => { name: 'connected' } };
    const mockData = '42/0,["237640958","100.0.0"]';
    const cBack = service['callbacks'][mockEvent];
    service.callBacks(mockData);
    expect(cBack).not.toBeDefined();
  });
  it('#disconnect should terminate connection', () => {
    spyOn(service, 'sendMessage');
    service.getSocket = jasmine.createSpy().and.callFake(() => fakeSocket);
    service.establishConnection('');
    service['pingSubscription'] = {
      unsubscribe: jasmine.createSpy('unsubscribe')
    } as any;
    service.disconnect();
    expect(service['pingSubscription'].unsubscribe).toHaveBeenCalled();
    expect(service['socket']).toBe(undefined);
    expect(service['callbacks']).toBe(undefined);
  });

  it('onConnect', () => {
    service['socket'] = { closed: false };
    spyOn(service, 'pingpong');
    service.onConnect();
    expect(service.pingpong).toHaveBeenCalled();
  });
  it('should establish WS connection for eventhub with EH namespace', () => {
    service.getSocket = jasmine.createSpy().and.callFake(() => fakeSocket);
    service.establishConnection('');
    expect(ngZone.runOutsideAngular).toHaveBeenCalled();
  });
  it('isConnected', () => {
    service['socket'] = null;
    expect(service['isConnected']()).toBeFalsy();
    service['socket'] = { closed: true };
    expect(service['isConnected']()).toBeFalsy();
    service['socket'] = { closed: false };
    expect(service['isConnected']()).toBeTruthy();
  });
});