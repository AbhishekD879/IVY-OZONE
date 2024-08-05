import { of  } from 'rxjs';
import { EventProvider } from './event.provider';
import environment from '@environment/oxygenEnvConfig';

describe('EventProvider', () => {
  let provider: EventProvider;
  let http;
  let body;

  beforeEach(() => {
    body = {
      SSResponse: {
        children: [{ event: { name: '', children: [{market: {children: []}}] } }]
      }
    };

    http = {
      get: jasmine.createSpy('get').and.returnValue(of({
        body: body
      }))
    };

    provider = new EventProvider(http);
  });

  it('constructor', () => {
    expect(provider).toBeTruthy();
    expect(provider['SITESERVER_ENDPOINT']).toBe(environment.SITESERVER_ENDPOINT);
  });

  it('getEvent', () => {
    provider.getEvent('123').subscribe();
    expect(http.get).toHaveBeenCalledWith(
      `${environment.SITESERVER_ENDPOINT}/EventToOutcomeForEvent/123?racingForm=outcome&prune=market`,
      { observe: 'response' }
    );
  });

  it('getEventsGroup', () => {
    provider.getEventsGroup('123,456,789').subscribe();
    expect(http.get).toHaveBeenCalledWith(
      `${environment.SITESERVER_ENDPOINT}/EventToOutcomeForEvent/123,456,789?racingForm=outcome&prune=market`,
      { observe: 'response' }
    );
  });

  describe('@getEventForClass', () => {
    let options: any;
    beforeEach(() => {
      options = {
        classId: 'CID',
        startTime: '12.10.2018 16:00',
        endTime: '12.10.2018 19:00',
        brTypes: 'BRT'
      };
    });

    it('getEventForClass request', () => {
      const endpoint = `${environment.SITESERVER_ENDPOINT}/EventForClass/${options.classId}?simpleFilter=class.isActive:isTrue&` +
        `simpleFilter=class.siteChannels:contains:M&${options.brTypes}&` +
        `simpleFilter=event.isResulted:isFalse&` +
        `simpleFilter=event.startTime:lessThanOrEqual:${options.endTime}&` +
        `simpleFilter=event.startTime:greaterThan:${options.startTime}`;

      provider.getEventForClass(options).subscribe();
      expect(http.get).toHaveBeenCalledWith(endpoint, { observe: 'response' });
    });

    it('getEventForClass response', () => {
      provider.getEventForClass(options).subscribe((res: any) => {
        expect(res).toEqual(body);
      });
    });
  });

  it('extendEventWithRacingFormOutcome', () => {
    const racingFormOutcomes = [];
    racingFormOutcomes.push({
      racingFormOutcome: {
        refRecordId: '1', silkName: 'silk1', id: '1', draw: 1, jockey: 'jockey'
      }
    });
    racingFormOutcomes.push({
      racingFormOutcome: {
        refRecordId: '2', silkName: 'silk2', id: '2', draw: 2, trainer: 'trainer'
      }
    });

    const marketChildren = [];
    marketChildren.push({ outcome: { id: '1' } });
    marketChildren.push({ outcome: { id: '2' } });
    marketChildren.push({ outcome: { id: '3' } });

    const eventData: any = {
      event: {
        children: [{
          market: { children: marketChildren }
        }]
      }
    };

    provider['extendEventWithRacingFormOutcome'](eventData, racingFormOutcomes);

    expect(marketChildren).toEqual([
      {outcome: {id: '1', silkName: 'silk1', racerId: '1', drawNumber: 1, jockey: 'jockey'}},
      {outcome: {id: '2', silkName: 'silk2', racerId: '2', drawNumber: 2, jockey: 'trainer'}},
      {outcome: {id: '3'}}
    ]);
  });

  it('prepareEventData', () => {
    const data: any = {
      event: {
        name: '18:00 Name', startTimeUnix: '2018.01.01',
        children: [{
          market: {
            children: [{
              outcome: {}
            }, {
              outcome: {
                children: [{
                  price: { priceDec: '01.23' }
                }]
              }
            }]
          }
        }]
      }
    };
    expect(provider['prepareEventData'](data)).toBe(data);
    expect(data.event.name).toBe('Name');
    expect(data.event.startTimeUnix).toEqual(jasmine.any(Number));
    expect(data.event.children[0].market.children[1].outcome.children[0].price.priceDec).toBe(1.23);
  });

  it('buildEvent', () => {
    provider['extendEventWithRacingFormOutcome'] = jasmine.createSpy();
    provider['prepareEventData'] = jasmine.createSpy();

    const event: any = {
      SSResponse: {
        children: [
          { racingFormOutcome: true, event: true },
          { racingFormOutcome: true }
        ]
      }
    };

    provider['buildEvent'](event);
    expect(provider['extendEventWithRacingFormOutcome']).toHaveBeenCalledWith(
      event.SSResponse.children[0], event.SSResponse.children
    );
    expect(provider['prepareEventData']).toHaveBeenCalled();
  });

  it('buildEventsGroup', () => {
    provider['extendEventsWithRacingFormOutcome'] = jasmine.createSpy();
    provider['prepareEventsData'] = jasmine.createSpy();

    const event: any = {
      SSResponse: {
        children: [
          { racingFormOutcome: true, event: true },
          { racingFormOutcome: true }
        ]
      }
    };

    provider['buildEventsGroup'](event);
    expect(provider['extendEventsWithRacingFormOutcome']).toHaveBeenCalledWith(
      [event.SSResponse.children[0]], event.SSResponse.children
    );
    expect(provider['prepareEventsData']).toHaveBeenCalled();
  });
});
