/**
 * timeline config
 */
export const timelineConfig = {
  moduleName: 'timeline',
  gtmModuleLadbrokesTitle: 'ladbrokes lounge',
  gtmModuleCoralTitle: 'coral pulse',
};

export const TIMELINE_TUTORIAL = 'timelineTutorialOverlay';

export enum TIMELINE_EVENTS {
  LOAD_POST_PAGE = 'LOAD_POST_PAGE',
  CAMPAIGN_CLOSED = 'CAMPAIGN_CLOSED',
  POST_CHANGED = 'POST_CHANGED',
  POST_REMOVED = 'POST_REMOVED',
  POST_PAGE = 'POST_PAGE',
  POST = 'POST',
  TIMELINE_CONFIG = 'TIMELINE_CONFIG'
}
