export interface Base {
  id: string;
  brand: string;

  createdBy: string;
  createdAt: string;

  updatedBy: string;
  updatedAt: string;

  updatedByUserName: string;
  createdByUserName: string;

  universalSegment?: boolean;
  exclusionList?: string[];
  inclusionList?: string[];
}
