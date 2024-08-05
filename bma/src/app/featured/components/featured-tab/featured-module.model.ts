export interface IFeaturedModule {
  devices: string[];
  directiveName: string;
  id: string;
  showTabOn: string;
  title: string;
  url: string;
  visible: boolean;
  // eventhub tabs scheduling
  displayFrom?: string;
  displayTo?: string;
}
