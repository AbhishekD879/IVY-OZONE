export interface IFeaturedAemModuleModel {
  '@type': string;
  displayOrder: string;
  isOutright: boolean;
  isWoEw: boolean;
  maxOffers: number;
  pageType: string;
  showExpanded: boolean;
  showModuleLoader: boolean;
  sportId: number;
  timePerSlide: number;
  _id: string;
  data: IFeaturedAemSlideModel[];
}

export interface IFeaturedAemSlideModel {
  '@type': string;
  appTarget: string;
  displayOrder: number;
  guid: number;
  imgUrl: string;
  imsLevel: string[];
  offerName: string;
  offerTitle: string;
  selectChannels: string[];
  userType: string[];
  webTarget: string;
  appUrl?: string;
  mobTandCLink?: string;
  webTandCLink?: string;
  webTandC?: string;
  webUrl?: string;

  clickTracked?: boolean;
  viewTracked?: boolean;
}

export interface ITermsAndConditions {
  showTC: boolean;
  text: string;
  href: string;
}
