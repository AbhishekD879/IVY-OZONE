export interface IFormation {
  id: string;
  title: string;
  actualFormation: string;
  position1: string;
  stat1: IStat;
  position2: string;
  stat2: IStat;
  position3: string;
  stat3: IStat;
  position4: string;
  stat4: IStat;
  position5: string;
  stat5: IStat;
}

interface IStat {
  id: number;
  title: string;
}
