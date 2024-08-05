import {Base} from '@app/client/private/models/base.model';
import {Filename} from '@app/client/public/models/filename.model';

export interface VirtualSportParent extends Base {
  title: string;
  active: boolean;
  svgFilename: Filename;
  svgId: string;
  ctaButtonUrl: string;
  ctaButtonText: string;
  desktopImageId: string;
  mobileImageId: string;
  redirectionURL: string;
  signposting: string;
  topSports: boolean;
  topSportsIndex: number;
  tracksRefs?: any[];
  isTopSportIndexValid?:boolean;
}
