import { NgZone } from '@angular/core';
import { MonoTypeOperatorFunction, Observable, Subscriber, Subscription } from 'rxjs';

/**
 * runOutsideZone()
 * @param {NgZone} zone
 * @returns {MonoTypeOperatorFunction<T>}
 */
export function runOutsideZone<T>(zone: NgZone): MonoTypeOperatorFunction<T> {
  return (source: Observable<T>) => {
    return new Observable((observer: Subscriber<T>) => {
      let subscription$: Subscription = Subscription.EMPTY;

      zone.runOutsideAngular(() => {
        subscription$ = source.subscribe(observer);
      });

      return subscription$;
    });
  };
}
