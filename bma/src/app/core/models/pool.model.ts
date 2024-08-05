export interface IPool {
  pool: IPoolEntity;
}

export interface IPoolEntity {
  id: string;
  type: string;
  marketIds: number[];
}
