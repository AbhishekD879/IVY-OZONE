import { Base } from './base.model';

export interface AssetManagement extends Base {
  sportId: number;
  teamName: string;
  secondaryNames: string[];
  primaryColour: string;
  secondaryColour: string;
  teamsImage?:  IAssetFile,
  fiveASideToggle?: boolean,
  highlightCarouselToggle?: boolean,
  imagename ?: string; 
  size ?: number;
  svg ?: string;
  svgId ?: string;
}

/**
 *  uiModel differs from backend
 *  input field for secondNames is string, backend model requires array (see above)
 */
export interface AssetManagementExt extends AssetManagement {
  secondaryNamesStr: string;
}

export interface IAssetFile extends File {
  originalname?: string;
  svg ?: string;
}
