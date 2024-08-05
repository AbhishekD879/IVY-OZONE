

import { Base } from '@app/client/private/models/base.model';

export interface PopularAccasWidget extends Base {
  "title": string;
  "cardCta": string;
  "cardCtaAfterAdd": string;
  "data": [PopularAccasCard];
  "displayOn": { string : boolean }[]
}

export interface PopularAccasCard extends Base {
  "title": string;
  "subTitle": string;
  "svgId": string;
  "displayFrom": string;
  "displayTo": string;
  "sortOrder": number;
  "locations": string[];
  "numberOfTimeBackedLabel": string;
  "numberOfTimeBackedThreshold": number;
  "accaIdsType": string;
  "listOfIds": string;
  "marketTemplateIds": string;
  "accaRangeMin": number;
  "accaRangeMax": number
}

export const ArrayIdsTypeList = [
  {label:'Event ID', id: 'EVENT'},
  {label:'League ID',id: 'LEAGUE'},
  {label:'Selection ID', id: 'SELECTION'},
  {label:'All', id: 'ALL'}
];

export const SportCategories = [{ imageTitle: "Sportbook Homepage" },
{ imageTitle: 'Football Homepage' }]