import { Injectable } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import * as LaunchDarkly from 'launchdarkly-js-client-sdk';
import { LDContext, LDOptions } from 'launchdarkly-js-client-sdk';
import { CONTEXT_KINDS, FALLBACK_FLAGS, FLAG_GA_COOKIE, GA_COOKIE } from '@core/services/flagSource/constants/flag-source.constants';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { StorageService } from '@core/services/storage/storage.service';
import { UserService } from '@core/services/user/user.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FlagSourceService } from '@app/core/services/flagSource/flag-source.service';

@Injectable()
export class FlagHelperService {
  client: LaunchDarkly.LDClient;
  
  private readonly title = 'flagSourceService';
  constructor(
    private windowRefService: WindowRefService,
    private pubsub: PubSubService,
    private userService: UserService,
    private storageService: StorageService,
    private flagSourceService: FlagSourceService) {
    this.initialiseFlagsOfServer();
    // to identify context when user logs in and logs out of the application
    this.pubsub.subscribe(this.title, [this.pubsub.API.SUCCESSFUL_LOGIN, this.pubsub.API.SUCCESSFUL_LOGOUT], () => {
      this.identifyContext();
    });
  }

  /**
   * Method to identify new context
   */
  identifyContext() {
    this.getContext().then((context) => {
      this.client.identify(context, null, function () {
        console.log("New context's flags available");
      });
    });
  }

  /**
   * Method to get context instance
   * @returns - LD context
   */
  getContext(): Promise<LDContext> {
    return this.getUserGAId().then((userGAId) => {
      let context;
      if (!this.userService.status) {
        context = {
          kind: CONTEXT_KINDS.anonymous_user,
          gaId: userGAId,
          key: userGAId
        } as LaunchDarkly.LDUser;
      } else if (this.userService.status) {
        context = {
          kind: CONTEXT_KINDS.multi,
          anonymoususer: {
            key: userGAId,
            gaId: userGAId
          },
          user: {
            key: this.userService.custId,
            customerId: this.userService.custId
          }
        } as LaunchDarkly.LDMultiKindContext;
      }
      return context;
    })
  }

  /**
   * Method to get user ga id
   * @returns - Ga id
   */
  getUserGAId(): Promise<string> {
    return new Promise((resolve) => {
      for (let i = 1; i <= 5; i++) {
        this.windowRefService.nativeWindow.setTimeout(() => {
          if (this.getCookie(GA_COOKIE).length) {
            i = 6;
            resolve(this.getCookie(GA_COOKIE));
          } else if (i === 5) {
            let randomKey = '';
            if (!this.storageService.getCookie(FLAG_GA_COOKIE)) {
              randomKey = `${window.crypto.getRandomValues(new Uint16Array(1))[0]}`;
              this.storageService.setCookie(FLAG_GA_COOKIE, randomKey, undefined, 365);
            } else {
              randomKey = this.storageService.getCookie(FLAG_GA_COOKIE);
            }
            resolve(`${randomKey}`);
          }
        }, 3000);
      }
    });
  }

  /**
   * Method to get cookie data
   * @param name - name of cookie
   * @returns - cookie value
   */
  getCookie(name): string {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop().split(';').shift();
    }
    return '';
  }

  initialiseFlagsOfServer() {
    const flags = this.flagSourceService.flagStore;
    if (flags && flags.length) {
      this.getLDFlagsFromServer(flags);
    } else {
      this.publishAllFlags(FALLBACK_FLAGS);
    }
  }

  /**
   * Method to get flags from server and initialize client
   * @param flagsData - window flags
   */
  getLDFlagsFromServer(flagsData) {
    if (flagsData) {
      flagsData = flagsData.split('singlequote').join('"');
      flagsData = flagsData.split("&quot;").join("")
      flagsData = JSON.parse(flagsData)
    }
    this.publishAllFlags(flagsData);
    this.initializeLD().then((client) => {
      this.client = client;
      this.getClientFlags();
    });
  }

  /**
   * Method to publish all flags in a project
   * @param flags - list of all flags
   */
  publishAllFlags(flags) {
    this.flagSourceService.updateFlagstore(flags);
  }

  /**
   * Method to publish a specific flag value
   * @param key - key
   * @param defaultValue - default value to be set from LD
   */
  publishFlag(key, defaultValue) {
    const updatedFlag = {};
    updatedFlag[key] = this.client.variation(key, defaultValue);
    this.flagSourceService.updateFlagstore({ ...this.flagSourceService.flagUpdate.value, ...updatedFlag });
  }

  /**
   * Method to get all client flags and to publish change in flags
   */
  getClientFlags() {
    this.client.waitUntilReady().then(() => {
      const flags = Object.keys(this.client.allFlags()).length ? this.client.allFlags() : FALLBACK_FLAGS;
      this.publishAllFlags(flags);
      Object.entries(flags).forEach(([key, value]) => {
        if (FALLBACK_FLAGS.hasOwnProperty(key)) {
          this.client.on(`change:${key}`, (val) => {
            this.publishFlag(key, FALLBACK_FLAGS[key]);
          });
        }
      });
    });
  }

  /**
   * MEthod to set and return LD options to initialize the client
   * @returns - LD Options
   */
  getLDOptions(): LDOptions {
    return {
      streaming: true
    };
  }

  /**
   * Method to initialize launch darkly
   * @returns - Launch darkly client
   */
  initializeLD(): Promise<LaunchDarkly.LDClient> {
    return this.getContext().then((context) => {
      return LaunchDarkly.initialize(environment.FLAG_CLIENT_KEY, context, this.getLDOptions());
    });
  }
}
