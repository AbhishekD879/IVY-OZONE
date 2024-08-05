import { Base } from './base.model';

export interface FiveASideFormation extends Base {
  title: string;
  actualFormation: string;
  position1: string;
  stat1: Stat | null;
  position2: string;
  stat2: Stat | null;
  position3: string;
  stat3: Stat | null;
  position4: string;
  stat4: Stat | null;
  position5: string;
  stat5: Stat | null;
  sortOrder: number;
}

interface Stat {
  id: number;
  title: string;
}
