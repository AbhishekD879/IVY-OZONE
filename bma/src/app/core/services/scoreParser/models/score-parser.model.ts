import { ITypedScoreData, IScoreType } from '@core/services/scoreParser/models/score-data.model';

export interface IScoreParser {
  getType: () => IScoreType | null;
  parse: (name: string) => ITypedScoreData | null;
}
