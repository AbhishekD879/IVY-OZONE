import { FreeBet } from './free-bet';

describe('FreeBet', () => {
  it('should create freebet', () => {
    const params = {
      id: '1',
      name: 'FB',
      value: 10,
      expireAt: new Date(2019, 0),
      type: 'HR',
      freeBetTokenDisplayText: 'title text',
      freeBetOfferCategories: {freeBetOfferCategory: 'bet pack'}
    };

    const freeBet = new FreeBet(params);

    expect(freeBet.id).toBe(params.id);
    expect(freeBet.name).toEqual(params.name);
    expect(freeBet.value).toBe(params.value);
    expect(freeBet.expireAt).toBe(params.expireAt);
    expect(freeBet.cleanName).toBe(params.name);
    expect(freeBet.type).toBe(params.type);
    expect(freeBet.freebetTokenDisplayText).toBe(params.freeBetTokenDisplayText);
    expect(freeBet.freebetOfferCategories).toBe(params.freeBetOfferCategories);
    expect(freeBet.doc()).toEqual({
      freebet: { id: params.id }
    } as any);
  });

  it('should create freebet with possible bet', () => {
    const freeBet = new FreeBet({
      possibleBets: [{ name: 'Football' }]
    } as any);
    expect(freeBet['possibleBet']).toEqual(' (Football)');
  });

  it('should create freebet with freebetOfferCategories', () => {
    const params = {
      freeBetOfferCategories: {freeBetOfferCategory: 'bet pack'}
    } as any;
    const freeBet = new FreeBet({} as any);
    freeBet.freebetOfferCategories = params.freeBetOfferCategories;
    expect(freeBet['freeBetOfferCategories']).toEqual(params.freeBetOfferCategories);
  });

  it('should create freebet with freeBetTokenDisplayText ', () => {
    const params = {
      freeBetTokenDisplayText: 'FB'
    } as any;
    const freeBet = new FreeBet({} as any);
    freeBet.freebetTokenDisplayText = params.freeBetTokenDisplayText;
    expect(freeBet['freeBetTokenDisplayText']).toEqual(params.freeBetTokenDisplayText);
  });
  it('set cleanName and type', () => {
    const params = {
      cleanName: 'FB',
      type: 'HR',
    } as any;
    const freeBet = new FreeBet({} as any);
    freeBet.cleanName = params.cleanName;
    freeBet.type = params.type;
  });
});
