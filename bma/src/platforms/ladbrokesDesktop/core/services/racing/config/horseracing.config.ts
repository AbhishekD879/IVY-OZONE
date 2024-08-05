import { ladbrokesHorseracingConfig as horseracingConfig } from '@ladbrokesMobile/core/services/racing/config/horseracing.config';

horseracingConfig.config.tabs.specials = {
  hidden: true,
  isNotStarted: true,
  typeFlagCodes: 'SP',
  isNotResulted: true,
  externalKeysEvent: false,
  excludeEventsClassIds: ''
};

export const ladbrokesHorseracingConfig = horseracingConfig;
