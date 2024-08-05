export interface ILottoNumber {
  value: number | string;
  selected: boolean;
  disabled?: boolean;
}

export interface ILottoNumberMap {
  [key: number]: ILottoNumber;
}
