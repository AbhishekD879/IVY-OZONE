
export interface CountryCode {
  allowed: boolean;
  label: string;
  phoneAreaCode: string;
  val: string;
  active?: boolean;
}
export interface Country {
  id: string;
  countriesData: CountryCode[];
  createdAt: string;
  createdBy: string;
  updatedAt: string;
  updatedBy: string;
}
