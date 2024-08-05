export interface IGamingCategoryData {
  path: string;
  id: string;
  specialsTypeIds?: Array<number>;
  dispSortName?: string | Array<string>;
  primaryMarkets?: string;
  viewByFilters: Array<string>;
  oddsCardHeaderType: string;
  isMultiTemplateSport: boolean;
}

export interface IRacingCategoryData {
  path: string;
  id: string;
  specialsClassIds: string;
}

export interface IVirtualsCategoryData {
  id: string;
  specialsClassIds: string;
}

export interface ICurrentMatchesCategoryData {
  name: string;
  id: string;
}

export interface ICategoriesData {
  [key: string]: any;
}
