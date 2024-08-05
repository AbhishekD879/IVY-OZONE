export interface IBetFilterParams {
  mode?: 'online' | 'inshop';
  couponName?: string;

  cancelled?: boolean;
  pathname?: string;
}
