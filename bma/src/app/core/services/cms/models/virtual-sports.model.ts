export interface IVirtualChild {
  id: string;
  title: string;
  classId: string;
  streamUrl: string;
  numberOfEvents: number;
  showRunnerNumber: boolean;
  showRunnerImages: boolean;
  eventAliases?: { [event: string]: string };
}

export interface IVirtualSports {
  id: string;
  title: string;
  svg: string;
  svgId: string;
  ctaButtonUrl: string;
  ctaButtonText: string;
  desktopImageId: string;
  mobileImageId: string;
  signposting:string;
  redirectionURL: string;
  topSports: boolean;
  topSportsIndex: string;
  tracks?: IVirtualChild[];
}

export interface IVirtualSportAliasesDto {
  classId: string;
  parent: string;
  child: string;
  events?: { [event: string]: string };
}

export interface IVirtualSportsHomePage extends IVirtualSports{
  imgURL: string;
  altText: string;
}

export interface IVirtualSportNavigationInfo {
  id: string;
  sportInfo: any;
}