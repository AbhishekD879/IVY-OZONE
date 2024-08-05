import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class CarouselMenuStateService {
  carouselStick$: Subject<{ stick: boolean, forceVisibility: boolean }>;

  constructor() {
    this.carouselStick$ = new Subject();
  }
}
