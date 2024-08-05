export interface IMatrixFormation {
  rowIndex: number;
  collIndex: number;
  position: string;
  stat: string;
  statId: number;
  roleId: string;
  defaultStat?: { stat: string; statId: number; };
}

export interface IShowView {
  view: string;
  player?: any;
  item?: IMatrixFormation;
}
