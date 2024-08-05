import { Injectable } from '@angular/core';
import { ReplaySubject } from 'rxjs';
import { ISportInstanceStorage, ISportInstance } from '@app/core/services/cms/models';

@Injectable({
  providedIn: 'root'
})
export class SportsConfigStorageService {
  private sportInstanceStore: ISportInstanceStorage = {};

  storeSport(sportName: string, sportInstance$: ReplaySubject<ISportInstance>): void {
    this.sportInstanceStore[sportName] = sportInstance$;
  }

  getSport(sportName: string): ReplaySubject<ISportInstance> {
    const sportInstance$: ReplaySubject<ISportInstance> = this.sportInstanceStore[sportName];
    if (sportInstance$) {
      return sportInstance$;
    }
  }

  getSports(sportNames?: string[]): ISportInstanceStorage {
    if (sportNames) {
      const filteredSports: ISportInstanceStorage = {};
      sportNames.forEach((sportName: string) => {
        const sportInstance$: ReplaySubject<ISportInstance> = this.sportInstanceStore[sportName];
        if (sportInstance$) {
          filteredSports[sportName] = sportInstance$;
        }
      });
      return filteredSports;
    } else {
      return Object.assign({}, this.sportInstanceStore);
    }
  }
}
