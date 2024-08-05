import {SvgFilename} from './svgfilename.model';

export interface ConnectMenu {
  id: string;
  updatedAt: string;
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
  updatedBy: string;
  svgFilename: SvgFilename;
}
