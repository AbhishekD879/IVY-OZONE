export interface IForecastMatrixMap {
  [key: string]: {
    ['1st']: string;
    ['2nd']: string;
    any: string;
  };
}

export interface ITricastMatrixMap {
  [key: string]: {
    ['1st']: string;
    ['2nd']: string;
    ['3rd']: string;
    ['any']: any;
  };
}
