import { Injectable } from '@angular/core';
import { StorageService } from '@core/services/storage/storage.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Injectable()
export class SessionStorageService extends StorageService {

    constructor (protected windowRefService: WindowRefService) {
      super(windowRefService);
    }

    protected init() {
      this.storageType = 'sessionStorage';
      this.setPrefix('OX');
      this.isSupported = this.checkSupport();
    }
}
