import { Observable, OperatorFunction, of, throwError } from 'rxjs';
import { map, share, catchError } from 'rxjs/operators';

const cacheMap = new Map();

// Cache data for specific period of time
export function cache(key: string, timeMs: number): OperatorFunction<any, any> {
  return function(source: Observable<any>): Observable<any> {
    if (!timeMs) {
      return source;
    }

    // use cached data if available
    let cacheVal = cacheMap.get(key);
    if (cacheVal) {
      return cacheVal.completed ? of(cacheVal.data) : cacheVal.source;
    }

    // create cache
    cacheVal = {
      source: source.pipe(
        map(data => {
          cacheVal.data = data;
          cacheVal.completed = true;
          return data;
        }),
        catchError(err => {
          // remove cache if error occured
          cacheMap.delete(key);
          return throwError(err);
        }),
        share()
      ),
      data: null,
      completed: false
    };

    // store cache
    cacheMap.set(key, cacheVal);

    // remove cache when time is up
    setTimeout(() => cacheMap.delete(key), timeMs);

    return cacheVal.source;
  };
}
