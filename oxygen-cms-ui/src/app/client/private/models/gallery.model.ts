import {Filename} from './filename.model';

export interface Gallery {
  id: string;
  key: string;
  name: string;
  publishedDate: string;
  images: Filename[];
}
