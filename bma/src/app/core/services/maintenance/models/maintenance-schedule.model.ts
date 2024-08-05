import { IMaintenancePage } from '@core/services/cms/models';

export interface IMaintenanceSchedule {
  maintenancePage: IMaintenancePage;
  endTimeout: number;
}
