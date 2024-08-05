import { WindowRefService } from './window-ref.service';

describe('WindowRefService', () => {
  let service: WindowRefService;
  let pubsub;
  let command;

  beforeEach(() => {
    pubsub = {
      subscribe: jasmine.createSpy(),
      unsubscribe: jasmine.createSpy(),
      publish: jasmine.createSpy(),
    };
    command = {
      execute: jasmine.createSpy(),
      executeAsync: jasmine.createSpy(),
    };
    service = new WindowRefService(pubsub, command);
  });

  it('constructor', () => {
    expect(service.nativeWindow.io).toBeDefined();
    expect(service.nativeWindow.ps).toBeDefined();
    expect(service.nativeWindow.command).toBeDefined();
  });

  it('should get document reference', () => {
    expect(service.document instanceof Document).toBe(true);
  });

  it('should get window reference', () => {
    expect(service.nativeWindow instanceof Window).toBe(true);
  });
});
