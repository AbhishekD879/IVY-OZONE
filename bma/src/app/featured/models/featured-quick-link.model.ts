
export interface IOquickLinkDataModel {
  destination: string;
  displayOrder: number;
  id: string;
  svgId: string;
  title: string;
}

export interface IOFeaturedQuickLinksModel {
  data: IOquickLinkDataModel[];
  showExpanded: boolean;
  sportId: number;
  title: string;
  _id: string;
}
