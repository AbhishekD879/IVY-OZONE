import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable()
export class RoutesDataSharingService {
  protected activeTabIdSource = new BehaviorSubject<string>('');
  protected hasSubHeaderSource = new BehaviorSubject<boolean>(false);
  activeTabId = this.activeTabIdSource.asObservable();
  hasSubHeader = this.hasSubHeaderSource.asObservable();

  availableTabs = {
    horseracing: [],
    greyhound: []
  };

  constructor() {}

  setRacingTabs(racingName, racingTabs) {
    this.availableTabs[racingName] = racingTabs;
  }

  getRacingTabs(racingName) {
    return this.availableTabs[racingName];
  }

  updatedActiveTabId(activeTabId: string) {
    this.activeTabIdSource.next(activeTabId);
  }

  updatedHasSubHeader(hasSubHeader: boolean) {
    this.hasSubHeaderSource.next(hasSubHeader);
  }

}
