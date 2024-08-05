import { pubSubApi } from '@coreModule/services/communication/pubsub/pubsub-api.constant';
import { commandApi } from '@coreModule/services/communication/command/command-api.constant';

/**
 * List of lazy modules (desktop platform has its own!)
 * path - aliased path to module (commandApi style, with ':' symbol)
 * channel - channel name to be emitted when module's loaded
 */
export const MODULES_BY_PRIORITY = [
  {
    path: commandApi.BETSLIP_READY,
    pubSubChannel: pubSubApi.BETSLIP_LOADED
  },
  {
    path: commandApi.SHOW_QUICKBET,
    pubSubChannel: pubSubApi.QUICKBET_LOADED
  }
];

export const MODULES_LOADING_DELAY = 100;
export const SCRIPTS_LOADING_DELAY = 1000;
