export interface ICountryCode {
  allowed: boolean;
  label: string;
  phoneAreaCode: string;
  val: string;
  active?: boolean;
  id?: string;
}
export interface ICountry {
  id: string;
  countriesData: ICountryCode[];
  createdAt: string;
  createdBy: string;
  updatedAt: string;
  updatedBy: string;
}
