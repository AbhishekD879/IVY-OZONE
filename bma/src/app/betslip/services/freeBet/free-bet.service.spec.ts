import { FreeBetService } from './free-bet.service';
import { IFreeBet } from '@betslip/services/freeBet/free-bet.model';

describe('FreeBetService', () => {

  let service: FreeBetService;
  const element = {
    id: '16',
    name: 'bet',
    offerName: 'offerName',
    value: 25,
    type: 'someType',
    expiry: '2050-12-11T22:00:00.000Z',
    expireAt: new Date('2048-12-11T22:00:00.000Z'),
    possibleBets: [
      {
        name: 'Football',
        betLevel: "Any",
        betType: "any",
        betId: "1234",
      }],
    freeBetOfferCategories: {freeBetOfferCategory: 'bet pack'},
    freeBetTokenDisplayText: "Football"
  };

  beforeEach(() => {
    service = new FreeBetService();
  });

  it('should return correct result of parseOne method', () => {
    const result = service.parseOne(element);
    expect(result.name).toBe('offerName');
    expect(result.id).toBe('16');
    expect(result.value).toBe(25);
    expect(result.type).toBe('someType');
    expect(result.expireAt.getFullYear()).toBe(2050);
  });

  it('should return correct result of construct method', () => {
    const result = service.construct(element);
    expect(result.name).toBe('bet');
    expect(result.id).toBe('16');
    expect(result.value).toBe(25);
    expect(result.type).toBe('someType');
    expect(result.expireAt.getFullYear()).toBe(2048);
  });

  it('should return correct result of parse method', () => {
    const elements: IFreeBet[] = [
      element,
      {
        id: '18',
        name: 'bet2',
        offerName: 'offerName2',
        value: 80,
        type: 'someType2',
        expiry: '2075-12-11T22:00:00.000Z'
      }
    ];
    const result = service.parse(elements);
    expect(result.length).toBe(2);
    expect(result[0].name).toBe('offerName');
    expect(result[0].id).toBe('16');
    expect(result[0].value).toBe(25);
    expect(result[0].type).toBe('someType');
    expect(result[0].expireAt.getFullYear()).toBe(2050);
    expect(result[1].name).toBe('offerName2');
    expect(result[1].id).toBe('18');
    expect(result[1].value).toBe(80);
    expect(result[1].type).toBe('someType2');
    expect(result[1].expireAt.getFullYear()).toBe(2075);
  });

  it('should construct freebet with empty params', () => {
    expect(service.construct({} as any)).toEqual(jasmine.any(Object));
  });
});
