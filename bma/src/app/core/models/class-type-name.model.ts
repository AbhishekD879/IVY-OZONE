export interface IClassTypeNameData {
  name: string;
  typeDisplayOrder: number;
  cashoutAvail: boolean;
}

export interface IClassTypeName {
  INT: IClassTypeNameData[];
  UK: IClassTypeNameData[];
  VR: IClassTypeNameData[];
  FR: IClassTypeNameData[];
  AE: IClassTypeNameData[];
  ZA: IClassTypeNameData[];
  US: IClassTypeNameData[];
  AU: IClassTypeNameData[];
  CL: IClassTypeNameData[];
}

export interface IClassItem {
  cashoutAvail?: boolean;
  liveStreamAvailable?: boolean;
  name?: string;
  typeDisplayOrder?: number;
}
