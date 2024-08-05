import { ISiteCoreTeaserFromServer } from "@app/core/models/aem-banners-section.model";

export interface IBetslipReceiptBanner {
  type?: string;
  teasers?: ISiteCoreTeaserFromServer[];
}

export interface IBsReceiptBannerImages {
  imageSrc?: string;
  imageHref?: string;
  bannerName?: string;
}

