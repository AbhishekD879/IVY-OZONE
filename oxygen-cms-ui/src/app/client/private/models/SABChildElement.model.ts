export interface SABChildElement {
  siteServeId: number;
  name: string;
  selection: string;
  showItemFor: string;
  children: SABChildElement[];
  parentId: number;
}
