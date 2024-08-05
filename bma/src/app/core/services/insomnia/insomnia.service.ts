import { Injectable } from '@angular/core';
import { PubSubService } from '../communication/pubsub/pubsub.service';
import { ReloadService } from '../reload/reload.service';
import { StorageService } from '../storage/storage.service';
import { IInsomniaEventData, IWorkerEmuData } from './insomnia.model';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { NETWORK_CONSTANTS } from '@lazy-modules/networkIndicator/components/network-indicator/network-indicator.constants';
import { NICMSConfig } from '@lazy-modules/networkIndicator/components/network-indicator/network-indicator.model';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { DeviceService } from '@core/services/device/device.service';

@Injectable()
export class InsomniaService {
  worker: Worker;
  networkWorker: Worker;
  workerSupport: boolean = false;
  cmsNetworkData: NICMSConfig;
  isOffline: boolean = false;
  private webWorkerFileUrl: string = '/assets/insomnia.js';
  private networkIndicatorFileUrl: string = '/assets/network-indicator.js';
  private visibilityEvent: string = 'visibilitychange';
  private timeTimeoutEvents: any = {};
  private timeIntervalEvents: any = {};

  private isTriggeredMap: Map<number, boolean> = new Map();

  constructor(private pubSubService: PubSubService,
              private storageService: StorageService,
              private reloadService: ReloadService,
              private cmsService: CmsService,
              private windowRef: WindowRefService,
              private nativeBridgeService: NativeBridgeService,
              private device: DeviceService
              ) {
  }

  init(): void {
    // Creates a Web Worker
    this.worker = new Worker(this.webWorkerFileUrl);

    this.addWorkerListeners();
    this.checkWorkerSync();
  }

  /**
   * Manages creation and termination of worker
   * @returns void
   */
  initNetworkIndicator(): void {
    this.cmsService.getNetworkIndicatorConfig()
      .subscribe((data: NICMSConfig) => {
        if (data) {
          this.cmsNetworkData = data;
          this.storageService.set(NETWORK_CONSTANTS.NETWORK_STORAGE_KEY, !!this.cmsNetworkData.networkIndicatorEnabled);
          this.nativeBridgeService.networkIndicatorEnabled(!!this.cmsNetworkData.networkIndicatorEnabled);
          this.initializeNetworkWebWorker();
          this.pubSubService.subscribe(NETWORK_CONSTANTS.NW_Insomina, NETWORK_CONSTANTS.NW_I_STATUS_RELOAD, (message: string) => {
            if (this.cmsNetworkData.networkIndicatorEnabled) {
              this.isOffline = message === NETWORK_CONSTANTS.OFFLINE;
              if (message === NETWORK_CONSTANTS.OFFLINE) {
                this.emitNetworkMessageInfo(message);
                this.networkWorker.terminate();
              } else {
                this.initializeNetworkWebWorker();
              }
            }
          });
        }
      },
        (error) => {
          console.warn(error);
        });
  }

  /**
   * Manage Webworker connection based on browser visibility
   * @returns void
   */
  handleVisibilityForWebworker(): void {
    if (this.windowRef.document.visibilityState === 'hidden') {
      this.networkWorker.terminate();
      console.log('Terminated Hidden', new Date().toString());
    } else {
      this.initializeNetworkWebWorker();
      console.log('Started Shown', new Date().toString());
    }
  }

  /**
   * Creates web worker for network-indicator with config
   * @returns void
   */
  initializeNetworkWebWorker(): void {
    if (this.cmsNetworkData && this.cmsNetworkData.networkIndicatorEnabled && this.device.isMobile) {
      this.networkWorker = new Worker(this.networkIndicatorFileUrl);
      this.networkWorker.postMessage(this.cmsNetworkData);
      this.networkWorker.onmessage = (event) => {
        this.emitNetworkMessageInfo(event.data);
      };
    }
  }

  /**
   * Publishes network config object based on network state
   * @param  {string} networkState
   * @returns void
   */
  emitNetworkMessageInfo(networkState: string): void {
    if (this.isOffline) {
      networkState = NETWORK_CONSTANTS.OFFLINE;
    }
    const networkStatus = this.cmsNetworkData.networkSpeed[networkState];
    if (networkStatus) {
      this.pubSubService.publish(NETWORK_CONSTANTS.NW_I_STATUS, { displayText: networkStatus.displayText, networkSpeed: networkState, infoMsg: networkStatus.infoMsg });
    }
  }

  setTimeoutAction(eventData: IInsomniaEventData, interval): void {
    // Posts a message to the Web Worker
    if (this.workerSupport) {
      // Posts a message to the Web Worker
      this.worker.postMessage({ eventData, interval, type: 'timeout' });
    } else {
      this.workerEmu({ eventData, interval, type: 'timeout' });
    }
  }

  private findTimeEvent(eventName: string): boolean {
    return this.timeTimeoutEvents[eventName] !== undefined || this.timeIntervalEvents[eventName] !== undefined;
  }

  private workerEmu(data: IWorkerEmuData): void {
    const evt = { data };

    if (evt.data.clearTimeouts === true) {
      this.timeTimeoutEvents = {};
    }

    if (evt.data.clearIntervals === true) {
      this.timeIntervalEvents = {};
    }

    if (evt.data.type === 'interval' || evt.data.type === 'timeout') {
      if (this.findTimeEvent(evt.data.eventData.eventName)) {
        // Clear timeouts and intervals if repeated.
        if (evt.data.type === 'timeout') {
          clearTimeout(this.timeTimeoutEvents[evt.data.eventData.eventName].timeout);
          delete this.timeTimeoutEvents[evt.data.eventData.eventName];
        } else {
          clearInterval(this.timeIntervalEvents[evt.data.eventData.eventName].interval);
          delete this.timeIntervalEvents[evt.data.eventData.eventName];
        }
      }

      // Set timeouts and intervals.
      if (evt.data.type === 'timeout') {
        this.timeTimeoutEvents[evt.data.eventData.eventName] = { timeout: setTimeout(() => {
          this.pubSubService.publish('INSOMNIA', [evt.data.eventData]);
          }, evt.data.interval),
          eventData: evt.data.eventData };
      } else {
        this.timeIntervalEvents[evt.data.eventData.eventName] = { interval: setInterval(() => {
            this.pubSubService.publish('INSOMNIA', [evt.data.eventData]);
          }, evt.data.interval),
          eventData: evt.data.eventData };
      }
    }
  }

  /**
   * Stores value in storage to show alternative loading screen in next app reload and reloads app.
   */
  private reloadApp(): void {
    const storageKey = 'show-alternative-screen';
    // Check if sessionStorage is supported because private mode in Safari will raise
    // "QuotaExceededError". In this case store in cookies.
    if (this.storageService.isSupported) {
      sessionStorage.setItem(storageKey, 'true');
    } else {
      this.storageService.setCookie(storageKey, 'true', null, 1);
    }

    this.reloadService.reload();
  }

  private addWorkerListeners(): void {
    // Triggered by postMessage in the Web Worker
    this.worker.onmessage = (evt) => {
      // evt.data is the values from the Web Worker
      if (this.isTriggeredMap.get(evt.data.classId)) { return; }

      this.isTriggeredMap.set(evt.data.classId, true);

      if (evt.data.checkWorkerAvailability) {
        this.workerSupport = evt.data.checkWorkerAvailability;
      } else if (evt.data.checkWorkerSync) {
        // Reload app.
        this.reloadApp();
      } else {
        this.pubSubService.publish('INSOMNIA', [evt.data]);
      }

      setTimeout(() => {
        this.isTriggeredMap.set(evt.data.classId, false);
      }, 10000);
    };

    // If the Web Worker throws an error
    this.worker.onerror = () => {
      // evt.data is the values from the Web Worker
      // ToDo: handle worker error.
    };
  }

  private checkWorkerSync(): void {
    this.worker.postMessage({ checkWorkerAvailability: true });
    // ToDo: time interval for worker sync should be set within the time factory.
    this.worker.postMessage({ checkWorkerSync: true, interval: 5000, type: 'interval' });
  }
}
