import {Filename} from '@app/client/public/models/filename.model';

export interface QuestionDetailsModel {
  topLeftHeader: string;
  topRightHeader: string;
  middleHeader: string;
  homeTeamName: string;
  homeTeamSvg: Filename;
  awayTeamName: string;
  awayTeamSvg: Filename;
  channelSvg: Filename;
  description: string;
  signposting: string;
}
