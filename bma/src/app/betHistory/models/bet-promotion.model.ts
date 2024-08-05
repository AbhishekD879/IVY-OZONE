export interface IBetPromotion {
  name: string;
  label: string;
  svgId: string;
  [key: string]: string
  // Note: shallow copying is used in the bet-promotions.component
}
