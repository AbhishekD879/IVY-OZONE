export interface IClassTypeName {
  name: string;
  cashoutAvail: boolean;
  typeDisplayOrder: number;
}

export interface ISportServiceClassTypeName {
  INT: IClassTypeName[];
  UK: IClassTypeName[];
  VR: IClassTypeName[];
}
