import { of, throwError } from 'rxjs';
import { delay } from 'rxjs/operators';
import { cache } from './cache';

describe('cache', () => {
  it('should not cache data', () => {
    const src = of('data');
    expect( cache('key1', 0)(src) ).toBe(src);
  });

  it('should cache data', () => {
    const src = of('data');
    cache('key2', 1)(src).subscribe(res => {
      expect(res).toBe('data');
    });
  });

  it('should remove from cache if error occured', () => {
    const src = throwError('error');
    cache('key3', 1)(src).subscribe(null, err => {
      expect(err).toBe('error');
    });
  });

  it('should return cashed value (completed = true)', () => {
    const src = of('data');
    cache('key4', 1)(src).subscribe();
    cache('key4', 1)(src).subscribe(res => {
      expect(res).toBe('data');
    });
  });

  it('should return cashed value (completed = false)', () => {
    const src = of('data').pipe(delay(0));
    cache('key5', 1)(src).subscribe();
    cache('key5', 1)(src).subscribe(res => {
      expect(res).toBe('data');
    });
  });
});
