import { pubSubApi } from '@coreModule/services/communication/pubsub/pubsub-api.constant';
import { commandApi } from '@coreModule/services/communication/command/command-api.constant';

export const MODULES_BY_PRIORITY = [
  {
    path: commandApi.BETSLIP_READY,
    pubSubChannel: pubSubApi.BETSLIP_LOADED
  },
  {
    path: commandApi.SHOW_QUICKBET,
    pubSubChannel: pubSubApi.QUICKBET_LOADED
  },
  { // desktop only
    path: commandApi.EVENT_VIDEO_STREAM,
    pubSubChannel: pubSubApi.EVENT_VIDEO_STREAM_LOADED
  }
];

export const MODULES_LOADING_DELAY = 100;
export const SCRIPTS_LOADING_DELAY = 1000;
