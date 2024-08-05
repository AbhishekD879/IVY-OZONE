import { Base } from './base.model';

export interface Campaign extends Base {
  name: string;
  displayFrom: string;
  displayTo: string;
  openBetCampaignId: string;
  optimoveId: string;
  eventClassInfo?: PotCreation;
  isPotsCreated?: boolean;
  questionnarie?: {
    horseSelectionMsg: string;
    questions: Array<{ chatBoxResp: string; options: any; quesDescription: string; questionId: number }> | any;
    summaryMsg: string
    welcomeMessage: string;
  };
}

export interface PotCreation {
  classId: number;
  marketPlace: PotCreationMarket[];
  categoryId: number;
}

export interface PotCreationMarket {

  typeId: string;
  typeName: string;
  events: PotCreationEvents[];

}

export class PotCreationEvents {
  id: string;
  name: string;

}
