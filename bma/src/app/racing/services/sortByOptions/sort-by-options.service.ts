import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class SortByOptionsService {
  option: string = 'Price';
  greyHoundOption: string = 'Price'; // separate option for greyhound page
  isGreyHound: boolean = false;

  set(option: string): void {
    if (this.isGreyHound) {
      this.greyHoundOption = option;
    } else {
      this.option = option;
    }

  }

  get(): string {
    if (this.isGreyHound) {
      return this.greyHoundOption;
    } else {
      return this.option;
    }
  }
}
