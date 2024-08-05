import { NumberNormalizerPipe } from './number-normalizer.pipe';

describe('NumberNormalizerPipe', () => {
  let pipe;

  beforeEach(() => {
    pipe = new NumberNormalizerPipe();
  });

  it('should return number with two digits after comma', () => {
    const num = pipe.transform('10.0287878654');
    expect(num).toBe('10.03');
  });

  it('should return number with two digits after comma', () => {
    const num = pipe.transform('10');
    expect(num).toBe('10.00');
  });

  it('should return number with two digits after comma when float number', () => {
    const num = pipe.transform(10.0287878654);
    expect(num).toBe('10.03');
  });

  it('should return number with two digits after comma when int number', () => {
    const num = pipe.transform(10);
    expect(num).toBe('10.00');
  });
});


