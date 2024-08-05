import {Injectable} from '@angular/core';

@Injectable()
export class GlobalLoaderService {
  public isVisible: boolean = false;

  constructor() {}

  showLoader() {
    this.isVisible = true;
  }

  hideLoader() {
    this.isVisible = false;
  }
}
