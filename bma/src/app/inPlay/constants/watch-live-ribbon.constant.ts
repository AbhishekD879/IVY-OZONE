/**
 * Hardcoded icon should be removed when api is updated for ribbon
 */
import { IRibbonItem } from '@app/inPlay/models/ribbon.model';

export const watchLiveItem: IRibbonItem = {
  categoryId: 999999,
  liveEventCount: null,
  liveStreamEventCount: null,
  showInPlay: true,
  svgId: 'live-stream',
  targetUri: '/in-play/watchlive',
  targetUriCopy: 'watchlive',
  upcomingEventCount: null,
  imageTitle: 'Watch Live',
  upcommingLiveStreamEventCount: null
};
