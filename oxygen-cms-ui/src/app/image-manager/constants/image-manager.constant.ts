import { DataTableColumn } from '@app/client/private/models';

export const IMAGE_MANAGER_ROUTES = {
  base: '/image-manager',
  add: 'add',
  details: 'details/:id'
};

export const IMAGE_MANAGER_FORM_NOTES = {
  active: '(inactive images are saved but excluded from app sprites)',
  nameUpdate: 'File selection automatically updates this name',
  initial: 'The icon will be included and loaded with initial page data, this increases app load time',
  featured: 'The icon will be included and loaded with featured module',
  additional: 'The icon will be included and loaded in a deferred manner',
  timeline: 'The icon will be included and loaded for timeline module',
  module: 'The icon will be included and loaded according to this module logic - '
};

export const IMAGE_MANAGER_FORM_ERRORS = {
  required: 'This field is required',
  unique: 'Image with this id already exist',
  pattern: 'Only digits, lowercase letters and "._-" are allowed',
  size: 'File size exceeds the limit of 20Kb',
};

export const IMAGE_MANAGER_MAX_FILE_SIZE = 20480;
export const IMAGE_MANAGER_SVG_ID_PATTERN = '[a-zA-Z0-9._-]*';

export const IMAGE_MANAGER_TABLE_COLUMNS: Array<DataTableColumn> = [
  {
    name: 'SVG Image',
    property: 'preview',
    type: 'svgIcon'
  },
  {
    name: 'Image name',
    property: 'svgId',
    type: 'link',
    link: {
      hrefProperty: 'id',
      path: 'details'
    }
  },
  {
    name: 'Status',
    property: 'isIconActive',
    type: 'boolean',
    alignment: 'center',
  },
  {
    name: 'Image Size',
    alignment: 'center',
    property: 'imageSize'
  },
  {
    name: 'Sprite Name',
    property: 'sprite',
    alignment: 'center',
  }
];
