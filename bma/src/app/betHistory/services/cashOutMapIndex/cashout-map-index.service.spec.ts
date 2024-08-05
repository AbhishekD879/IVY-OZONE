import { CashoutMapIndexService } from '@app/betHistory/services/cashOutMapIndex/cashout-map-index.service';
import { ICashoutMapItem } from '../../models/cashout-map-item.model';

describe('test CashoutMapIndexService', () => {
  let service: CashoutMapIndexService;

  beforeEach(() => {
    service = new CashoutMapIndexService();
  });

  it('#initCreate should create initial value', () => {
    const type: string = 'event';
    const id: string = '1';
    const index: Object = service;
    service.initCreate(index, type, id);
    expect(index[type][id]).toEqual([]);
  });

  it('#create should create new cashout bet and avoid duplication', () => {
    const type: string = 'event';
    const id: string = '3';
    const cashOutBetId: string = '1';
    const isSettled: boolean = false;
    const bet: ICashoutMapItem = {
      id: cashOutBetId,
      isSettled: isSettled
    };

    service.create(type, id, cashOutBetId, isSettled);
    expect(service[type][id]).toEqual([bet]);

    service.create(type, id, cashOutBetId, isSettled);
    expect(service[type][id]).toEqual([bet]);
  });

  it('#reset should reset outcome, market, event', () => {
    const cashOutBetId: string = '1';
    const isSettled: boolean = false;

    service.create('outcome', '1', cashOutBetId, isSettled);
    service.create('market', '1', cashOutBetId, isSettled);
    service.create('event', '1', cashOutBetId, isSettled);
    service.reset();

    expect(service.outcome).toEqual({});
    expect(service.market).toEqual({});
    expect(service.event).toEqual({});
  });

  it('#getItems should return ids by settled status', () => {
    const type: string = 'event';

    service.create(type, '1', '1', false);
    service.create(type, '1', '2', true);
    service.create(type, '2', '3', false);

    expect(service.getItems(type)).toEqual(['1', '2']);
    expect(service.getItems(type, false)).toEqual(['1', '2']);
    expect(service.getItems(type, true)).toEqual(['2']);
  });

  it('#deleteItem should delete outcomes, markets, events', () => {
    service.create('outcome', '1', '1', false);
    service.create('market', '2', '1', false);
    service.create('event', '3', '1', false);
    service.create('event', '3', '2', false);

    const outcomeIds = ['1'];
    const marketIds = ['2'];
    const eventIds = ['3'];
    service.deleteItem(outcomeIds, marketIds, eventIds, '1');

    expect(service['outcome']).toEqual({});
    expect(service['market']).toEqual({});

    const  eventsAfterDelete: { [key: string]: ICashoutMapItem[]} = {
      '3': [
        {
          id: '2',
          isSettled: false
        }
      ]
    };
    expect(service['event']).toEqual(eventsAfterDelete);
  });

  it('#deleteItemByType should delete cashout by type', () => {
    const type: string = 'event';
    service.create(type, '1', '1', false);
    service.create(type, '1', '2', false);
    service.create(type, '2', '1', false);

    const  resultAfterFirstDelete: { [key: string]: ICashoutMapItem[]} = {
      '1': [
        {
          id: '2',
          isSettled: false
        }
      ]
    };

    service.deleteItemByType(service, type, '1', ['1', '2']);
    expect(service[type]).toEqual(resultAfterFirstDelete);

    service.deleteItemByType(service, type, '2', ['1']);
    expect(service[type]).toEqual({});
  });
});
