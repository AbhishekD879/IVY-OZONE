export class UpsellItemModel {
  marketName: string;
  price: number;
  priceDen: number;
  priceNum: number;
  selectionId: number;
  selectionName: string;
  fallbackImagePath?: string;
  imageUrl?: string;

  public static isValid(upsell: UpsellItemModel): boolean {
    return !!(
      upsell.marketName &&
      upsell.price &&
      upsell.priceDen &&
      upsell.priceNum &&
      upsell.selectionId &&
      upsell.selectionName
    );
  }

  constructor(upsell: UpsellItemModel) {
    this.marketName = upsell.marketName;
    this.price = upsell.price;
    this.priceDen = upsell.priceDen;
    this.priceNum = upsell.priceNum;
    this.selectionId = upsell.selectionId;
    this.selectionName = upsell.selectionName;
    this.fallbackImagePath = upsell.fallbackImagePath;
    this.imageUrl = upsell.imageUrl;
  }

}

export interface IUpsellOptions {
  [upsellId: string]: UpsellItemModel;
}

export interface IUpsellModel {
  dynamicUpsellOptions?: IUpsellOptions;
  defaultUpsellOption?: UpsellItemModel;
  fallbackImagePath?: string;
  imageUrl?: string;
}
