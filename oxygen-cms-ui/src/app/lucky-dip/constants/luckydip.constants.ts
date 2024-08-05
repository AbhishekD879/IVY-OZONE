import { ILuckyDipMapping } from "../lucky-dip-v2.model";

export const LUCKYDIP_BREADCRUMB_DATA = {
  contestLabel: 'LuckyDip',
  luckyDip_url: '/lucky-dip/v2',
  edit_url: '/lucky-dip/v2/edit',
};

export const LUCKYDIP_ERROR_LABELS = {
  loadingLuckyDipLabel: 'Error in loading the luckyDip',
  createLuckyDipLabel: 'Error while creating the Lucky Dip. Duplicate ID detected. Please ensure that the ID is unique',
}

export const LUCKYDIP_DEFAULT_VALUS = {
  id: '',
  updatedBy: '',
  updatedAt: '',
  createdBy: '',
  createdAt: '',
  updatedByUserName: '',
  createdByUserName: '',
  description: '',
  luckyDipConfigLevel: '',
  luckyDipConfigLevelId: ''
};

export const LUCKYDIPFORM = {
  description: 'Create Lucky Dip',
  luckyDipConfigLevel: 'LuckyDip Configuration Level',
  createLuckyDipLabel: 'Create LuckyDip',
  cancelLabel: 'Cancel',
  saveLabel: 'Save',
};

export const LUCKYDIP_CONST = {
  luckyDipPage: 'LuckyDip Configuration',
  status: 'Active',
  createLuckyDip: 'Create Lucky Dip'
};

export const LUCKYDIP_MAPPING: ILuckyDipMapping = {
  active: false,
  categoryId: '',
  typeIds: '',
  id: '',
  brand: '',
  createdBy: '',
  createdAt: '',
  updatedBy: '',
  updatedAt: '',
  updatedByUserName: '',
  createdByUserName: ''
};

export const LUCKYDIP_MAPPING_CONST = {
  active: 'Active',
  categoryId: 'Category/Sport ID',
  typeIds: 'Type ID',
  luckyDipMappingPage: 'LuckyDip Mapping',
  createLuckyDipMapping: 'Create New Mapping',
};


