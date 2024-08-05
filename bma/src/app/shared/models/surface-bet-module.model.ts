import { ISurfaceBetEvent } from '@shared/models/surface-bet-event.model';

export interface ISurfaceBetModule {
  data: ISurfaceBetEvent[];
  title: string;
  displayOrder: number;
}
