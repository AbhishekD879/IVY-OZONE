import { brand } from './constant';

describe('defaultModule', () => {
  it('Coral', () => {
    const result = brand({brand: 'bma'});
    expect(result).toBe('Coral');
  });

  it('Ladbrokes', () => {
    const result = brand({brand: 'ladbrokes'});
    expect(result).toBe('Ladbrokes');
  });
});
