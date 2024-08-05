import { Injectable } from '@angular/core';

import * as _ from 'underscore';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { StorageService } from '@core/services/storage/storage.service';

@Injectable()
export class LocalStorageMapperService {
  private readonly tagName: string = 'LocalStorageMapperService';

  constructor(
    private window: WindowRefService,
    private pubSubService: PubSubService,
    private storage: StorageService) {}

  init() {
    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.REMOVE_VS_STORAGE, id => {
      const mappedStorage = JSON.parse(this.storage.get('vsbr-selection-map')) || {},
        selectionKey = mappedStorage[id];
      let brStorage = this.window.nativeWindow.localStorage.getItem('vsm-betmanager-coralvirtuals-en-selections');

      if (this.window.nativeWindow.vsmobile && this.window.nativeWindow.vsmobile.instance) {
        this.window.nativeWindow.vsmobile.instance.deselectBet(selectionKey);
      }

      brStorage = brStorage ? JSON.parse(brStorage) : [];

      brStorage = _.filter(brStorage, (item: any) => {
        return item.selectionKey !== selectionKey;
      });

      if (mappedStorage[id]) {
        delete mappedStorage[id];
      }

      this.storage.set('vsbr-selection-map', JSON.stringify(mappedStorage));
      this.window.nativeWindow.localStorage.setItem('vsm-betmanager-coralvirtuals-en-selections', JSON.stringify(brStorage));
    });

    this.pubSubService.subscribe(this.tagName, this.pubSubService.API.FLUSH_VS_STORAGE, () => {
      this.storage.remove('vsbr-selection-map');
      this.window.nativeWindow.localStorage.removeItem('vsm-betmanager-coralvirtuals-en-selections');
    });
  }
}
