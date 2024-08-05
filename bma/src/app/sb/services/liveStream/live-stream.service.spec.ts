import { LiveStreamService } from '@sb/services/liveStream/live-stream.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { eventEntityMock } from '@uktote/components/betBuilder/bet-builder.component.mock';


describe('LiveStreamService', () => {
  let service: LiveStreamService;

  let windowRef: WindowRefService;


  const providerInfo = {
    listOfMediaProviders: [{
      name: 'testStr',
      children: [{
        media: {
          id: 'V46381',
          refRecordId: '1397869',
          refRecordType: 'event',
          accessProperties: `A`,
          siteChannels: 'd,e,i,o,v,'
        }
      }]
    }],
    priorityProviderName: 'Perform',
    priorityProviderCode: 'PERFORM'
  } as any;

  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        location: {
          origin: 'https://bm-tst1.coral.co.ukTEST',
          href: ''
        },
        _QLGoingDown: {
          status: true
        }
      }
    } as any;

    service = new LiveStreamService(windowRef);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });

  it('resetProviders: should set false to all providers when error received from optIn MS', () => {
    eventEntityMock.streamProviders.Perform = true;
    eventEntityMock.streamProviders.IMG = true;
    service['resetProviders'](eventEntityMock);
    expect(eventEntityMock.streamProviders.Perform).toBeFalsy();
    expect(eventEntityMock.streamProviders.IMG).toBeFalsy();
    expect(eventEntityMock.streamProviders.ATR).toBeFalsy();
    expect(eventEntityMock.streamProviders.RPGTV).toBeFalsy();
    expect(eventEntityMock.streamProviders.RacingUK).toBeFalsy();
    expect(eventEntityMock.streamProviders.iGameMedia).toBeFalsy();
  });

  it('setProp: should find object key case-insensitive and set value', () => {
    eventEntityMock.streamProviders.iGameMedia = false;
    service['setProp'](eventEntityMock.streamProviders, 'iGameMedia', true);

    expect(eventEntityMock.streamProviders.iGameMedia).toBeTruthy();
  });

  it('prioritizeStream: should reset stream provider for event entity base on optIn response', () => {
    eventEntityMock.liveStreamAvailable = true;
    eventEntityMock.streamProviders.IMG = true;

    service.prioritizeStream(eventEntityMock, providerInfo);

    expect(eventEntityMock.liveStreamAvailable).toBeTruthy();
    expect(eventEntityMock.streamProviders.Perform).toBeTruthy();
    expect(eventEntityMock.streamProviders.IMG).toBeFalsy();
  });

  it('prioritizeStream: should not reset stream provider for event entity if no optIn response available', () => {
    eventEntityMock.liveStreamAvailable = true;
    providerInfo.priorityProviderCode = undefined;
    eventEntityMock.streamProviders.IMG = false;
    eventEntityMock.streamProviders.Perform = false;

    service.prioritizeStream(eventEntityMock, providerInfo);

    expect(eventEntityMock.liveStreamAvailable).toBeTruthy();
    expect(eventEntityMock.streamProviders.Perform).toBeFalsy();
    expect(eventEntityMock.streamProviders.IMG).toBeFalsy();
    expect(eventEntityMock.streamProviders.ATR).toBeFalsy();
    expect(eventEntityMock.streamProviders.RPGTV).toBeFalsy();
    expect(eventEntityMock.streamProviders.RacingUK).toBeFalsy();
    expect(eventEntityMock.streamProviders.iGameMedia).toBeFalsy();
  });

  it('prioritizeStream: should not reset stream provider for event entity if liveStream is not available for this event', () => {
    eventEntityMock.liveStreamAvailable = false;
    providerInfo.priorityProviderCode = undefined;

    service.prioritizeStream(eventEntityMock, providerInfo);

    expect(eventEntityMock.liveStreamAvailable).toBeFalsy();
    expect(eventEntityMock.streamProviders.Perform).toBeFalsy();
    expect(eventEntityMock.streamProviders.IMG).toBeFalsy();
    expect(eventEntityMock.streamProviders.ATR).toBeFalsy();
    expect(eventEntityMock.streamProviders.RPGTV).toBeFalsy();
    expect(eventEntityMock.streamProviders.RacingUK).toBeFalsy();
    expect(eventEntityMock.streamProviders.iGameMedia).toBeFalsy();
  });

  it('prioritizeStream: should not reset stream provider if event is not available', () => {
    let event = eventEntityMock;
    event = {};
    providerInfo.priorityProviderCode = undefined;

    service.prioritizeStream(event, providerInfo);

    expect(event).toEqual({});
  });

  describe('isLiveStreamAvailable method', () => {
    let liveStreamConfig;
    let eventObj;

    beforeEach(() => {
      liveStreamConfig = [{
        type: 'testType'
      }] as any;

      eventObj = {
        test: 'test'
      } as any;
    });

    it('should return false if no liveStreamConfig object', () => {
      liveStreamConfig = undefined as any;
      const result = service.isLiveStreamAvailable(liveStreamConfig)(eventObj);

      expect(result).toEqual(false);
    });

    it('should return false if no eventObj object', () => {
      eventObj = undefined as any;
      const result = service.isLiveStreamAvailable(liveStreamConfig)(eventObj);

      expect(result).toEqual(false);
    });

    it('should return false if liveStreamConfig is empty', () => {
      liveStreamConfig = [];
      const result = service.isLiveStreamAvailable(liveStreamConfig)(eventObj);

      expect(result).toEqual(false);
    });

    it('should return false if eventObj is empty', () => {
      eventObj = {};
      const result = service.isLiveStreamAvailable(liveStreamConfig)(eventObj);

      expect(result).toEqual(false);
    });

    it('should return init object with liveStreamAvailable property into false', () => {
      const controlObject = {
        liveStreamAvailable: false,
        streamProviders: {
          testType: false
        }
      };
      const result = service.isLiveStreamAvailable(liveStreamConfig)(eventObj);

      expect(result).toEqual(controlObject);
    });

    it('should return init object with liveStreamAvailable and streamProviders.testType properties into true', () => {
      eventObj.drilldownTagNames = 'test';
      liveStreamConfig[0].drilldownTagNames = 'test';
      const controlObject = {
        liveStreamAvailable: true,
        streamProviders: {
          testType: true
        }
      };
      const result = service.isLiveStreamAvailable(liveStreamConfig)(eventObj);

      expect(result).toEqual(controlObject);
    });
  });

  describe('checkCondition method', () => {
    let liveStreamConfig;
    let eventObj;

    beforeEach(() => {
      liveStreamConfig = [{
        type: 'testType'
      }] as any;

      eventObj = {
        test: 'test'
      } as any;
    });

    it('should return false if eventObj not have the "drilldownTagNames" property', () => {
      const result = service.checkCondition(liveStreamConfig, eventObj);

      expect(result).toEqual(false);
    });

    it('should return false if liveStreamConfig not have an object with the "drilldownTagNames" property', () => {
      eventObj.drilldownTagNames = 'test';
      const result = service.checkCondition(liveStreamConfig, eventObj);

      expect(result).toEqual(false);
    });

    it('should return true if all conditions are correct', () => {
      eventObj.drilldownTagNames = 'test';
      liveStreamConfig[0].drilldownTagNames = 'test';
      const result = service.checkCondition(liveStreamConfig, eventObj);

      expect(result).toEqual(true);
    });
  });

  describe('addLiveStreamAvailability method', () => {
    let liveStreamConfig;
    let eventsArray;

    beforeEach(() => {
      liveStreamConfig = [{
        type: 'testType'
      }] as any;

      eventsArray = [{
        test: 'test'
      }] as any;
    });

    it('should return events objects as is in the case when liveStreamConfig is not passed', () => {
      eventsArray[0] = 'notObject';
      const result = service.addLiveStreamAvailability()(eventsArray);

      expect(result).toEqual(eventsArray);
    });

    it('should return events objects as is in the case when liveStreamConfig passed', () => {
      eventsArray[0] = 'notObject';
      const result = service.addLiveStreamAvailability(liveStreamConfig)(eventsArray);

      expect(result).toEqual(eventsArray);
    });

    it('should return extended events objects', () => {
      const controlObject = [{ test: 'test',
                               liveStreamAvailable: false,
                               streamProviders: { testType: false }}];
      const result = service.addLiveStreamAvailability(liveStreamConfig)(eventsArray);

      expect(result).toEqual(controlObject);
    });
  });

  describe('checkIfRacingEvent method', () => {
    let event;

    beforeEach(() => {
      event = {
        categoryId: '39'
      } as any;
    });

    it('should return false in the case when _QLGoingDown.status is "Advert"', () => {
      windowRef.nativeWindow._QLGoingDown.status = 'Advert';
      const result = service.checkIfRacingEvent(event);

      expect(result).toEqual(false);
    });

    it('should return true in the case when _QLGoingDown.status is "nothing"', () => {
      windowRef.nativeWindow._QLGoingDown.status = 'nothing';
      const result = service.checkIfRacingEvent(event);

      expect(result).toEqual(true);
    });

    it('should return false in the case when _QLGoingDown.status is default', () => {
      const result = service.checkIfRacingEvent(event);

      expect(result).toEqual(false);
    });

    it('should return false in the case when event.categoryId is incorrect', () => {
      windowRef.nativeWindow._QLGoingDown.status = 'nothing';
      event.categoryId = undefined;
      const result = service.checkIfRacingEvent(event);

      expect(result).toEqual(false);
    });

    it('should return true in the case when _QLGoingDown.status is incorrect', () => {
      windowRef.nativeWindow._QLGoingDown.status = undefined;
      const result = service.checkIfRacingEvent(event);

      expect(result).toEqual(true);
    });
  });
});
