import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable()
export class SportEventPageProviderService {
  private sportDataSubject: BehaviorSubject<any>;

  constructor() {
    this.sportDataSubject = new BehaviorSubject<any>(null);
  }

  get sportData(): BehaviorSubject<any> {
    return this.sportDataSubject;
  }
  set sportData(value:BehaviorSubject<any>){}

}
