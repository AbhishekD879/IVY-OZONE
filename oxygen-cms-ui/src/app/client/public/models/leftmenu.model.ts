import {SvgFilename} from './svgfilename.model';

export interface LeftMenu {
  id: string;
  updatedBy: string;
  updatedAt: string;
  createdBy: string;
  createdAt: string;
  linkTitleBrand: string;
  sortOrder: number;
  linkTitle: string;
  level: string;
  lang: string;
  brand: string;
  showItemFor: string;
  svg: string;
  svgId: string;
  inApp: boolean;
  disabled: boolean;
  targetUri: string;
  svgFilename: SvgFilename;
}
