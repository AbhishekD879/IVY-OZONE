export interface IRoutingHelperEvent {
  categoryId: string|number;
  categoryName: string;
  className: string;
  typeName: string;
  name: string;
  id: string|number;
  originalName?: string;
  isResulted?: boolean;
  localTime?: string;
}

export interface IRoutingHelperCompetition {
  sport: string;
  className: string;
  typeName: string;
}
