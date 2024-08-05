export interface IRibbonData {
  items: IRibbonItem[];
}

export interface IRibbonCache {
  data: IRibbonItem[];
  lastUpdated: number;
}

export interface IRibbonItem {
  categoryId: number;
  categoryName?: string;
  liveEventCount: number;
  liveStreamEventCount: number;
  showInPlay: boolean;
  svgId: string;
  targetUri: string;
  targetUriCopy: string;
  upcomingEventCount: number;
  imageTitle: string;
  upcommingLiveStreamEventCount?: number; // allsports typo in property on backend
}

export interface IVirtualRibbonItem {
  sportName?: string;
  liveEventCount?: number;
}